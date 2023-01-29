"""
This module defines custom typings which will be used throughout the package. "Custom typings" thereby
does NOT refer to custom data classes, but instead this means more descriptive names for special cases of
native datatypes.

This package has made the choice to represent certain core data instances as native datatypes such as
dictonaries and lists instead of creating custom classes. This choice was mainly made because the
corresponding data has to be (1) easily serializable and de-serializable and (2) have dynamic properties.
As such it has been decided that using native data types is simpler. Of course, these datatypes still
follow a certain internal structure which will be described in this module.

This module defines alternative names for these native datatypes, which are more descriptive and are used
as typing annotations throughout the package to identify whenever such a special format is used as a
parameter or return of a function.
"""
import typing as t

import numpy as np


GraphDict = t.Dict[str, t.Union[t.List[float], np.ndarray]]

MetadataDict = t.Dict[str, t.Union[int, float, str, dict, list, GraphDict]]

VisGraphIndexDict = t.Dict[int, t.Union[str, MetadataDict]]

VisGraphNameDict = t.Dict[str, t.Union[str, MetadataDict]]

"""
Visual Graph Dataset Metadata Dict

This is a special kind of dictionary which is used to store the metadata information for an ENTIRE visual 
graph dataset in contrast to just one element. These metadata annotations can optionally be added to a 
dataset folder in the format of a YAML file. These metadata annotations will have some base fields which are 
usually present and some fields which are generated automatically. However, custom metadata may also be 
added to those files in the future to facilitate more advanced features for custom datasets.
"""
VisGraphMetaDict = t.Dict[str, t.Union[str, float, int]]


# == DATA TYPE CHECKS ==

def assert_graph_dict(obj: t.Any) -> None:
    """
    Implements assertions to make sure that the given ``value`` is a valid GraphDict.

    :param obj: The obj to be checked
    :return: None
    """
    # Most importantly the value has to be a dict
    assert isinstance(obj, dict), ('The given object is not a dict and thus cannot be a GraphDict')

    # Then there are certain keys it must implement
    required_keys = [
        'node_indices',
        'node_attributes',
        'edge_indices',
        'edge_attributes',
    ]
    for key in required_keys:
        assert key in obj.keys(), (f'The given object is missing the key {key} to be a GraphDict')
        value = obj[key]
        assert isinstance(value, (list, np.ndarray)), (f'The value corresponding to the key {key} is not '
                                                       f'of the required type list or numpy array')

    # TODO: We can also check the shapes
