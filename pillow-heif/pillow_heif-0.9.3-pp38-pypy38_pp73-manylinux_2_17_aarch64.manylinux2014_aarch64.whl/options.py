"""
Options to change pillow_heif's runtime behaviour.
"""


DECODE_THREADS = 4
"""Maximum number of threads to use for decoding images(when it is possible)

When use pillow_heif as a plugin you can set it with: `register_*_opener(decode_threads=8)`"""


THUMBNAILS = True
"""Option to enable/disable thumbnail support

When use pillow_heif as a plugin you can set it with: `register_*_opener(thumbnails=False)`"""


QUALITY = None
"""Default encoding quality

.. note:: Quality specified during calling ``save`` has higher priority then this.

Possible values: None, -1, range(0-100).
Set -1 for lossless quality or from 0 to 100, where 0 is lowest and 100 is highest.

.. note:: Also for lossless encoding you should specify ``chroma=444`` during save.

When use pillow_heif as a plugin you can set it with: `register_*_opener(quality=-1)`"""


SAVE_HDR_TO_12_BIT = False
"""Should 16 bit images be saved to 12 bit instead of 10 bit``

When use pillow_heif as a plugin you can set it with: `register_*_opener(save_to_12bit=True)`"""
