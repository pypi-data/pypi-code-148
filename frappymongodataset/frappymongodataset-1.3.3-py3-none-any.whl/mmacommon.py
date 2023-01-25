import io
import base64
import numpy as np
from PIL import Image as PilImage

# source: https://github.com/maet3608/mma-common


# Map first two bytes of image to image format.
PREFIX2FMT = {(255, 216): 'jpg', (71, 73): 'gif', (137, 80): 'png',
              (66, 77): 'bmp', (73, 73): 'tif', (77, 77): 'tif'}


def base64decode(data):
    """
    Return decoded data where data is base64 encoded binary data.
    :param str data: Base64 encoded binary data.
    :return: Decoded data
    :rtype: bytes
    """
    return base64.b64decode(data)


def base64encode(data):
    """
    Return bytes encoded as base64.
    :param bytes data: Binary data to encode.
    :return: Base64 encoded bytes
    :rtype: str
    """
    return base64.b64encode(data).decode('utf-8')


def load_raw_image(path):
    """
    Load raw image in binary format from specified path.
    Also see :py:func:`.save_raw_image`.
    :param str path: File path.
    :return: Raw image
    :rtype: str
    """
    with open(path, 'rb') as f:
        return f.read()


def parse_data_url(data_url):
    """
    Parses a data URL and returns its components.
    Data URLs are defined as follows::
       dataurl    := "data:" [ mediatype ] [ ";base64" ] "," data
       mediatype  := [ type "/" subtype ] *( ";" parameter )
       data       := *urlchar
       parameter  := attribute "=" value
    This specific implementation is limited to data urls of the following
    format::
        dataurl := "data:" type "/" subtype ";base64" "," data
    Here an example::
      'data:image/jpg;base64,/9j/4SXNRXhpZg...AUAFFABRQB//Z'
    References:
    - http://tools.ietf.org/html/rfc2397
    - http://www.askapache.com/online-tools/base64-image-converter/
    :param str data_url: A data URL.
    :return: Components of the data URL,
             e.g. ('image', 'png', 'base64', '/9j/4S')
    :rtype: tuple (datatype, subtype, encoding, data)
    :raises: ValueError if data URL doesn't follow spec.
    """
    if not data_url.startswith('data:'):
        raise ValueError("Not a data URL: " + data_url[:40])
    try:
        header, data = data_url.split(',')
        header = header.replace('data:', '')
        mediatype, encoding = header.rsplit(';', 1)
        datatype, subtype = mediatype.split('/')
    except BaseException:
        raise ValueError("Data URL not in correct format: " + data_url[:40])
    return datatype, subtype, encoding, data


def extract_data_and_type(data_url):
    """
    Returns raw data and type for a base64 encoded ndarray or image.
    Data URLs for base64 encoded images are of the form:
      'data:image/jpg;base64,/9j/4SXNRXhpZg...AUAFFABRQB//Z'
    While data URLs for numpy arrays are:
      'data:ndarray/npz;base64,eNqb7BfqGx...BHEYdzA=='
    :param str data_url: Data URL for an image or ndarray.
    :return: raw data and type, e.g. 'jpg' or 'gz'
    :rtype: tuple (raw_data, datatype, subtype)
    :raises: ValueError if url doesn't contain base64 encoded image or ndarray.
    """
    datatype, subtype, encoding, data = parse_data_url(data_url)
    if not (encoding == 'base64' and
            (datatype == 'image' or datatype == 'ndarray')):
        raise ValueError("Invalid data : " + data_url[:50])
    return base64decode(data), datatype, subtype


def ndarray_from_bytes(bdata):
    """
    Return an ndarray deserialized from byte data.
    Retrieve an ndarray from a byte representation created via
    ndarray_to_bytes(). Byte representation can be compressed or not.
    >>> arr_in = np.ones((3, 4))
    >>> bdata = ndarray_to_bytes(arr_in)
    >>> arr_out = ndarray_from_bytes(bdata)
    :param bytes bdata: Binary data created via ndarray_to_bytes()
    :return: Numpy array
    :rtype: numpy.ndarray
    """

    buf = io.BytesIO(bdata)
    ret = np.load(buf, allow_pickle=False)
    if isinstance(ret, np.ndarray):
        data = ret
    else:
        assert len(ret.files) == 1, 'Expect one ndarray in npz file!'
        arr_name = ret.files[0]
        data = ret[arr_name]
        ret.close()
    return data


def ndarray_from_data_url(data_url, dtype=None):
    """
    Return numpy ndarray for data in data_url.
    Data in data_url can be image data or numpy arrays, e.g.
    'data:image/gif;base64,/9j/4SXNR...'
    'data:ndarray/npy;base64,/9j/HYUDN...
    'data:ndarray/npz;base64,/9j/KL5DNS...
    :param data_url: Data URL for image, e.g.:
             'data:image/gif;base64,/9j/4SXNRXhpZgAUAFFABRQB//Z'
    :param dtype:  Data type of returned numpy array, inferred if None
    :return: Image as numpy array
    :rtype: numpy.ndarray
    """
    bdata, datatype, _ = extract_data_and_type(data_url)
    if datatype == 'image':
        buf = io.BytesIO(bdata)
        return np.asarray(PilImage.open(buf), dtype)
    elif datatype == 'ndarray':
        return ndarray_from_bytes(bdata)
    else:
        raise ValueError('Unknown data type: ' + data_url[:30])


def image_to_data_url(image_bytes, fmt):
    """
    Return data URL for given raw image.
    :param image_bytes: Raw binary image in some image format.
    :param str fmt: Image format, e.g. jpg, tif, png, gif, bmp
    :return: Data URL for image, e.g.:
             'data:image/gif;base64,/9j/4SXNRXhpZgAUAFFABRQB//Z'
    :rtype: str
    """
    data = base64encode(image_bytes)
    return 'data:image/{0};base64,{1}'.format(fmt, data)


def imagefile_to_data_url(path):
    """
    Read image in binary format and return data URL with base64 encoded image.
    Implementation based on:
    https://github.com/sindresorhus/file-type/blob/master/index.js
    http://www.fileformat.info/format/tiff/corion.htm
    :param str path: Path to image in binary format.
    :return: data URL, e.g. 'data:image/gif;base64,/9j/4SXNRXhpZg...AABRQB//Z'
    :rtype: str
    :raises: ValueError if file extension is missing.
    """

    def _extension(img):
        prefix = tuple(c if isinstance(c, int) else ord(c) for c in img[:2])
        try:
            return PREFIX2FMT[prefix]
        except KeyError:
            raise ValueError('Unknown image type: %s: %s' % (str(prefix), path))

    img = load_raw_image(path)
    return image_to_data_url(img, _extension(img))


def imagefile_to_ndarray(path):
    """
    Gets the image from the given path as a numpy data array.
    :param str path: Path to image in binary format
    :return: the image as a numpy data array
    """
    data_url = imagefile_to_data_url(path)
    return ndarray_from_data_url(data_url)
