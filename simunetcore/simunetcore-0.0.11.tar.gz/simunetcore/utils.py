import gzip
import base64
import io
from datetime import datetime

def compress(content):
    """
    Compresses the content using gzip and base64 encode.
    Raises a TypeError if argument is None.

    Parameters
    ----------
    content : str
        The content to be compressed.

    Returns
    -------
    compressed_text : str
        A string containing the base64 encoded and compressed content.

    Raises
    ------
    `ValueError` if argument `content` is None.
    
    """

    if content is None:
        raise ValueError("Argument is None")

    # Convert content to string
    text = str(content)

    # Compress text using gzip
    stream_out = io.BytesIO()
    with gzip.GzipFile(fileobj = stream_out, mode = "w") as zip_file:
        zip_file.write(text.encode())

    # Encode text using base64
    compressed_text = base64.b64encode(stream_out.getvalue())

    # Return the result
    return compressed_text.decode()
    
def decompress(content):
    """
    Decompresses the base64 encoded content using gzip and base64.
    Raises `TypeError` if argument is not of type str.

    Parameters
    ----------
    content : str
        The base64 encoded and gzipped content to be decompressed.

    Returns
    -------
    decompressed_text : str
        A string containing the decoded and decompressed text.

    Raises
    ------
    `TypeError` if argument `content` is not a str.

    """

    if not isinstance(content, str):
        raise TypeError("String argument expected")
        
    # Convert to string
    text = str(content)  
    # Decode the text from base64
    text = base64.b64decode(text.encode())

    # Compressde text using gzip
    stream_in = io.BytesIO()
    stream_in.write(text)
    stream_in.seek(0)
    with gzip.GzipFile(fileobj = stream_in, mode = "rb") as zip_file:
        decompressed_text = zip_file.read()

    # Return the result
    return decompressed_text.decode()
 
def current_time():
    """
    Returns the current utc time in isoformat.

    Returns
    -------
    utc_now : str
        A string containing the utc time in isoformat.

    """
    utc_now = datetime.utcnow().isoformat()[:-3]
    return utc_now