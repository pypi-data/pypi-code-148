from eolymp.typewriter import typewriter_pb2, fragment_pb2
from eolymp.typewriter.typewriter_http import TypewriterClient

from peolymp.abstract import AbstractAPI


class TypeWriterAPI(AbstractAPI):

    def __init__(self, **kwargs):
        super(TypeWriterAPI, self).__init__(**kwargs)
        self.client = TypewriterClient(self.http_client, url=self.get_url())

    def upload_asset(self, filename, data):
        return self.client.UploadAsset(typewriter_pb2.UploadAssetInput(filename=filename, data=data)).link

    def get_fragment(self, fragment_id):
        return self.client.DescribeFragment(typewriter_pb2.DescribeFragmentInput(fragment_id=fragment_id)).fragment

    def add_fragment(self, path, locale, title, content):
        fragment = fragment_pb2.Fragment(path=path, locale=locale, title=title, content=content)
        print(fragment)
        return self.client.CreateFragment(typewriter_pb2.CreateFragmentInput(fragment=fragment))

    def update_fragment(self, fragment_id, path, locale, title, content):
        fragment = fragment_pb2.Fragment(path=path, locale=locale, title=title, content=content)
        return self.client.UpdateFragment(typewriter_pb2.UpdateFragmentInput(fragment_id=fragment_id, fragment=fragment))

    def get_fragments(self):
        return self.client.ListFragments(typewriter_pb2.ListFragmentsInput(size=100)).items
