import torch
from lightly.loss.memory_bank import MemoryBankModule
from lightly.models.modules import SwaVProjectionHead, SwaVPrototypes
from torch import nn


class SwaV(nn.Module):
    def __init__(
        self,
        backbone,
        num_ftrs,
        out_dim,
        n_prototypes,
        n_queues,
        queue_length=0,
        start_queue_at_epoch=0,
        n_steps_frozen_prototypes=0,
    ):
        super().__init__()
        self.backbone = backbone
        self.projection_head = SwaVProjectionHead(num_ftrs, num_ftrs, out_dim)
        self.prototypes = SwaVPrototypes(out_dim, n_prototypes, n_steps_frozen_prototypes)

        self.queues = None
        if n_queues > 0:
            self.queues = [MemoryBankModule(size=queue_length) for _ in range(n_queues)]
            self.queues = nn.ModuleList(self.queues)
            self.queue_length = queue_length
            self.num_features_queued = 0
            self.start_queue_at_epoch = start_queue_at_epoch

    def forward(self, high_resolution, low_resolution, epoch=None, step=None):
        self.prototypes.normalize()

        high_resolution_features = [self._subforward(x) for x in high_resolution]
        low_resolution_features = [self._subforward(x) for x in low_resolution]

        high_resolution_prototypes = [self.prototypes(x, step) for x in high_resolution_features]
        low_resolution_prototypes = [self.prototypes(x, step) for x in low_resolution_features]
        queue_prototypes = self._get_queue_prototypes(high_resolution_features, epoch)

        return high_resolution_prototypes, low_resolution_prototypes, queue_prototypes

    def _subforward(self, input):
        features = self.backbone(input).flatten(start_dim=1)
        features = self.projection_head(features)
        features = nn.functional.normalize(features, dim=1, p=2)
        return features

    @torch.no_grad()
    def _get_queue_prototypes(self, high_resolution_features, epoch=None):
        if self.queues is None:
            return None

        if len(high_resolution_features) != len(self.queues):
            raise ValueError(
                f"The number of queues ({len(self.queues)}) should be equal to the number of high "
                f"resolution inputs ({len(high_resolution_features)}). Set `n_queues` accordingly."
            )

        # Get the queue features
        queue_features = []
        for i in range(len(self.queues)):
            _, features = self.queues[i](high_resolution_features[i], update=True)
            # Queue features are in (num_ftrs X queue_length) shape, while the high res
            # features are in (batch_size X num_ftrs). Swap the axes for interoperability.
            features = torch.permute(features, (1, 0))
            queue_features.append(features)

        # Do not return queue prototypes if not enough features have been queued
        self.num_features_queued += high_resolution_features[0].shape[0]
        if self.num_features_queued < self.queue_length:
            return None

        # If loss calculation with queue prototypes starts at a later epoch,
        # just queue the features and return None instead of queue prototypes.
        if self.start_queue_at_epoch > 0:
            if epoch is None:
                raise ValueError(
                    "The epoch number must be passed to the `forward()` " "method if `start_queue_at_epoch` is greater than 0."
                )
            if epoch < self.start_queue_at_epoch:
                return None

        # Assign prototypes
        queue_prototypes = [self.prototypes(x) for x in queue_features]
        return queue_prototypes
