from eolymp.typewriter import typewriter_pb2
from eolymp.typewriter.typewriter_http import TypewriterClient

from peolymp.abstract import AbstractAPI


class TypeWriterAPI(AbstractAPI):

    def __init__(self, **kwargs):
        super(TypeWriterAPI, self).__init__(**kwargs)
        self.client = TypewriterClient(self.http_client)

    def upload_asset(self, filename, data):
        return self.client.UploadAsset(typewriter_pb2.UploadAssetInput(filename=filename, data=data)).link
