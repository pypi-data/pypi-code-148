import logging
import math
import random
import warnings
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

import torch

from vtorch.common.checks import ConfigurationError
from vtorch.common.utils import ensure_list, is_lazy
from vtorch.data.entity import InstanceFeatureVectors
from vtorch.data.iterators.batch import Batch
from vtorch.data.iterators.bucket_iterator import BucketIterator, argsort_by_fields
from vtorch.data.iterators.interruptable import InterruptableDataIterator

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


# TODO refactor this and original BucketIterator to minimise code duplication


class BucketIteratorInterruptable(BucketIterator, InterruptableDataIterator):
    """
    An iterators which by default, pads batches with respect to the maximum input lengths `per
    batch`. Additionally, you can provide a list of field names and padding keys which the dataset
    will be sorted by before doing this batching, causing inputs with similar length to be batched
    together, making computation more efficient (as less time is wasted on padded elements of the
    batch).
    Parameters
    ----------
    sorting_keys : List[Tuple[str, str]]
        To bucket inputs into batches, we want to group the instances by padding length, so that we
        minimize the amount of padding necessary per batch. In order to do this, we need to know
        which fields need what type of padding, and in what order.
        For example, ``[("sentence1", "num_tokens"), ("sentence2", "num_tokens"), ("sentence1",
        "num_token_characters")]`` would sort a dataset first by the "num_tokens" of the
        "sentence1" field, then by the "num_tokens" of the "sentence2" field, and finally by the
        "num_token_characters" of the "sentence1" field.
        documentation somewhere that gives the standard padding keys used by different fields.
    batch_size : int, optional, (default = 32)
        The size of each batch of instances yielded when calling the iterators.
    biggest_batch_first : bool, optional (default=False)
        This is largely for testing, to see how large of a batch you can safely use with your GPU.
        This will let you try out the largest batch that you have in the instances `first`, so that if
        you're going to run out of memory, you know it early, instead of waiting through the whole
        epoch to find out at the end that you're going to crash.
        Note that if you specify ``max_instances_in_memory``, the first batch will only be the
        biggest from among the first "max instances in memory" instances.
    instances_per_epoch : int, optional, (default = None)
        See :class:`BaseDataIterator`.
    cache_instances : bool, optional, (default = False)
        See :class:`BaseDataIterator`.
    maximum_samples_per_batch : ``Tuple[str, int]``, (default = None)
        See :class:`BasicIterator`.
    num_epochs_per_instances : ``Union[int, None]``, (default = 1)
    batch_reverse_sort: bool, optional  (default = False)
        If True, bigger batches by lengths will go first
    sampling_rate_namespace: str, optional (default = None)
        To use sampling you need to provide `sampling_rate_namespace` and `sampling_rate_field` to retrieve
         sampling rate form Instance
    sampling_rate_field: str, optional (default = None)
        See `sampling_rate_namespace`
    """

    def __init__(
        self,
        sorting_keys: List[str],
        batch_size: int,
        biggest_batch_first: bool = False,
        instances_per_epoch: Optional[int] = None,
        cache_instances: bool = False,
        maximum_samples_per_batch: Optional[Tuple[Tuple[str, str], int]] = None,
        shuffle_random: Optional[random.Random] = None,
        batch_reverse_sort: bool = False,
        sampling_rate_namespace: Optional[str] = None,
        sampling_rate_field: Optional[str] = None,
        sampling_random: Optional[random.Random] = None,
    ) -> None:
        if not sorting_keys:
            raise ConfigurationError("BucketIterator requires field_keys to be specified")

        super().__init__(
            cache_instances=cache_instances,
            batch_size=batch_size,
            instances_per_epoch=instances_per_epoch,
            maximum_samples_per_batch=maximum_samples_per_batch,
            num_epochs_per_instances=1,
            shuffle_random=shuffle_random,
            sorting_keys=sorting_keys,
            biggest_batch_first=biggest_batch_first,
            batch_reverse_sort=batch_reverse_sort,
            sampling_rate_namespace=sampling_rate_namespace,
            sampling_rate_field=sampling_rate_field,
            sampling_random=sampling_random,
        )
        self._current_batch_ids: Optional[List[List[int]]] = None
        self._current_batch_n: Optional[int] = None

    def _get_instance_copy_without_sampling(self, instance: InstanceFeatureVectors) -> InstanceFeatureVectors:
        return {
            namespace: feature_vectors
            for namespace, feature_vectors in instance.items()
            if namespace != self._sampling_rate_namespace
        }

    def _create_batches(
        self, instances: Iterable[InstanceFeatureVectors], shuffle: bool
    ) -> Iterable[Tuple[Batch, List[int]]]:

        if self._current_batch_ids is not None:
            # For the purposes of simplicity we assume that an iterator loaded from a checkpoint
            #  will be used with the same data that it was used previously.
            #  If this is not the case, this might raise an error due to IndexOutOfBounds error or behave unexpectedly
            batches: List[Batch] = [
                Batch(
                    [
                        self._get_instance_copy_without_sampling(instances[indx])  # type: ignore
                        for indx in batch_instance_indxs
                    ]
                )
                for batch_instance_indxs in self._current_batch_ids
            ]

        else:
            sampled_instances = []
            sampled_instances_indices = []
            if self._sampling_rate_namespace is not None and self._sampling_rate_field is not None:
                for instance_index, instance in enumerate(instances):
                    sampling_rate = instance.get(self._sampling_rate_namespace, {}).get(
                        self._sampling_rate_field, [1.0]
                    )[0]
                    if self.sampling_random.random() < sampling_rate:
                        instance_copy = self._get_instance_copy_without_sampling(instance)
                        sampled_instances.append(instance_copy)
                        sampled_instances_indices.append(instance_index)
            else:
                sampled_instances = [self._get_instance_copy_without_sampling(instance) for instance in instances]
                sampled_instances_indices = list(range(len(sampled_instances)))
            sort_indices = argsort_by_fields(sampled_instances, self._sorting_keys, reverse=self._batch_reverse_sort)
            sampled_instances = [sampled_instances[i] for i in sort_indices]
            sampled_instances_indices = [sampled_instances_indices[i] for i in sort_indices]
            batches = self._form_batches(sampled_instances)  # after this step batches can differ in size
            batched_ids = self._batchify_ids(instance_ids=sampled_instances_indices, batched_instances=batches)
            batches, batched_ids = self._biggest_batch_first_and_shuffle(batches, shuffle, batched_ids)
            self._current_batch_ids = batched_ids

        yield from zip(batches, self._current_batch_ids)

    def __call__(
        self, instances: Iterable[InstanceFeatureVectors], shuffle: bool = True
    ) -> Iterator[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]:
        """
        Returns a generator that yields batches over the given dataset
        for the given number of epochs. If ``num_epochs`` is not specified,
        it will yield batches forever.
        Parameters
        ----------
        instances : ``Iterable[InstanceFeatureVectors]``
            The instances in the dataset. IMPORTANT: this must be able to be
            iterated over *multiple times*. That is, it must be either a List
            or some other object whose ``__iter__`` method returns a fresh iterators
            each time it's called.
        num_epochs : ``int``, optional (default=``None``)
            How times should we iterate over this dataset?  If ``None``, we will iterate over it
            forever.
        shuffle : ``bool``, optional (default=``True``)
            If ``True``, we will shuffle the instances in ``dataset`` before constructing batches
            and iterating over the instances.
        """
        batches, batch_instance_ids = list(zip(*list(self._create_batches(instances, shuffle))))
        if self._current_batch_n is None:
            self._current_batch_n = 0

        for batch, instance_ids in zip(batches[self._current_batch_n :], batch_instance_ids[self._current_batch_n :]):
            tensor_dict: Dict[str, Dict[str, torch.Tensor]] = batch.as_tensor_dict()  # type: ignore
            self._current_batch_n += 1
            yield tensor_dict, instance_ids

        self._reset_state()

    def _reset_state(self) -> None:
        self._current_batch_ids = None
        self._current_batch_n = None

    def state_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def get_num_batches(self, instances: Iterable[InstanceFeatureVectors]) -> int:
        """
        Returns the number of batches that ``dataset`` will be split into; if you want to track
        progress through the batch with the generator produced by ``__call__``, this could be
        useful.
        """
        if is_lazy(instances) and self._instances_per_epoch is None:
            # Unable to compute num batches, so just return 1.
            return 1
        elif self._instances_per_epoch is not None:
            return math.ceil(self._instances_per_epoch / self._batch_size)
        elif self._current_batch_ids is not None:
            return len(self._current_batch_ids)
        else:
            # Not lazy, so can compute the list length.
            return math.ceil(len(ensure_list(instances)) / self._batch_size)

    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        # TODO we could also make some checks that the loaded field values are compatible with what we currently have.
        #  i.e. the batch sizes, sorting keys mathc, etc...
        for key, val in state_dict.items():
            if key in self.__dict__:
                self.__setattr__(key, val)
            else:
                warnings.warn(
                    f"Version/Object mismatch. Trying to set value for field {key},"
                    f" that does not exist for an object {self}"
                )
