import oss2


class AliOssStore(object):
    def __init__(self, host_base, access_key_id, access_key_secret, bucket_name):
        """
        auto define the store object
        for more detail please refer
        https://github.com/scrapy/scrapy/blob/0ede017d2ac057b1c3f9fb77a875e4d083e65401/scrapy/pipelines/files.py
        :param host_base:
        :param access_key_id:
        :param access_key_secret:
        :param bucket_name:
        """
        self._auth = oss2.Auth(access_key_id, access_key_secret)
        self._bucket = oss2.Bucket(self._auth, host_base, bucket_name)

    def stat_file(self, path, info):
        # always return the empty result ,force the media request to download the file
        return {}

    def _check_file(self, path):
        return self._bucket.object_exists(path)

    def persist_file(self, path, buf, info, meta=None, headers=None):
        """Upload file to Ali oss storage"""
        self._upload_file(path, buf)

    def _upload_file(self, path, buf):
        self._bucket.put_object(key=path, data=buf.getvalue())