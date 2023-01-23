from functools import partial
from multiprocessing import Pool
from pathlib import Path

from six.moves.urllib.parse import urlparse

from rebotics_sdk.advanced import remote_loaders
from rebotics_sdk.constants import RCDB


class FileUploadError(Exception):
    def __init__(self, msg, response):
        super(FileUploadError, self).__init__(msg)
        self.response = response


class RCDBImportFlow(object):
    def __init__(self, rcdb_interface, retailer, retailer_model, extension):
        """
        Process wrapper with automatic API hooks

        :param ReboticsClassificationDatabase rcdb_interface:
        :param str retailer:
        :param str retailer_model:
        :param str extension:
        """
        self.rcdb = rcdb_interface
        self.import_request = self.rcdb.data_import(retailer, retailer_model, extension)
        self.rcdb_id = self.import_request['id']

    def __enter__(self):
        self.rcdb.update(self.rcdb_id, status=RCDB.EXPORT_IN_PROGRESS)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val:
            self.rcdb.update(self.rcdb_id, status=RCDB.EXPORT_ERROR)
        else:
            self.rcdb.update(self.rcdb_id, status=RCDB.EXPORT_DONE)

    def upload_file(self, packed, progress_bar=False):
        destination = self.import_request['destination']
        response = remote_loaders.upload(destination, packed, progress_bar=progress_bar)
        if response.status_code > 300:
            raise FileUploadError(
                'Failed to upload destination. Response: {}. {}'.format(response.status_code, response.content),
                response)


class ReboticsClassificationDatabase(object):
    def __init__(self, *args, **kwargs):
        self.provider = kwargs.get('provider', None)

    def create(self, retailer, model, backup_type='feature_vectors', extension='rcdb'):
        return self.provider.rcdb_create({
            'retailer': retailer,
            'facenet_model': model,
            'extension': extension,
            'backup_type': backup_type,
        })

    def data_import(self, retailer, model, extension='zip', **kwargs):
        return self.provider.create_classification_database_import(retailer, model, extension, **kwargs)

    def update(self, id_, status=RCDB.EXPORT_DONE, entries_count=0):
        assert status in (c[0] for c in RCDB.EXPORT_STATUS_CHOICES)
        return self.provider.rcdb_update(id_, {
            'status': status,
            'entries_count': entries_count
        })

    def get(self, id_):
        return self.provider.rcdb_get(id_)

    def import_flow(self, retailer, retailer_model, extension):
        return RCDBImportFlow(
            self, retailer, retailer_model, extension
        )


class FeatureVectorFlow(object):
    def __init__(self, provider, session):
        self.provider = provider
        self.session = session

    def get(self):
        return self.session.get()

    def export(self, triggered_by='sdk', source_model='', result_model='previews_backup', batch_size=50000):
        d = dict(
            triggered_by=triggered_by,
            source_model=source_model,
            result_model=result_model,
            batch_size=batch_size
        )
        return self.session.post(json=d)
