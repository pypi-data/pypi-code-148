from urllib.parse import urlparse
import cv2
import numpy as np

from hikvision_isapi_cli.client import Client


class RtspClient:
    def __init__(self, client: Client, rtsp_port: int, path: str) -> None:
        """
        Initialize the RtspClient class.

        :param client: A `Client` object containing the credentials for the RTSP stream.
        :param rtsp_port: The RTSP port of the stream.
        :param path: The path of the stream.
        """

        self.client = client
        self.rtsp_port = rtsp_port
        self.path = path
        self.host = urlparse(client.base_url).hostname
        self.stream_url = (
            f"rtsp://{client.username}:{client.password}@{self.host}:{rtsp_port}/{path}"
        )
        self.cap = cv2.VideoCapture(self.stream_url)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 60)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"H264"))

    async def get_snapshot(self) -> bytes:
        """
        Capture a snapshot from the RTSP stream and return the binary data of the image.

        :return: The binary data of the image, or None if the frame cannot be read.
        """
        ret, frame = self.cap.read()
        if ret:
            # Encode the image as JPEG
            _, img_encoded = cv2.imencode(".jpg", frame)
            # Return the binary data
            return img_encoded.tobytes()
        else:
            # Return None if the frame cannot be read
            return None

    async def release(self):
        """
        Release the RTSP stream.
        """

        self.cap.release()

    async def open(self):
        """
        Open the RTSP stream.
        """
        self.cap.open(self.stream_url)
    
    async def stream_source(self) -> str:
        """
        The RTSP stream string.
        """

        return self.stream_url
    
