import base64


from layerx.datalake.annotation import Annotation
from layerx.datalake.query import Query

from .ground_truth import GroundTruth
from .constants import BOX_ANNOTATION, POLYGON_ANNOTATION, LINE_ANNOTATION, MediaType
from .datalakeinterface import DatalakeInterface
from .file_upload import FileUpload
from .logger import get_debug_logger
from .model_run import ModelRun

datalake_logger = get_debug_logger('DatalakeClient')


class DatalakeClient:
    """
    Python SDK of Datalake
    """

    def __init__(self, encoded_key_secret: str, layerx_url: str) -> None:
        _datalake_url = f'{layerx_url}/datalake' #/datalake :3000
        self.datalake_interface = DatalakeInterface(encoded_key_secret, _datalake_url)

    def upload_annotation_from_cocojson(self, file_path: str):
        """
        available soon
        """
        datalake_logger.debug(f'file_name={file_path}')
        _annotation = GroundTruth(client=self)
        _annotation.upload_coco(file_path)

    def upload_modelrun_from_json(
            self,
            storage_base_path: str,
            model_id: str,
            file_path: str,
            annotation_geometry: str,
            is_normalized: bool
    ):
        datalake_logger.debug(f'upload_modelrun_from_json file_path={file_path}, '
                              f'annotation_geometry={annotation_geometry}')
        _model = ModelRun(client=self)
        if annotation_geometry == BOX_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, BOX_ANNOTATION, is_normalized)
        elif annotation_geometry == POLYGON_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, POLYGON_ANNOTATION, is_normalized)
        elif annotation_geometry == LINE_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, LINE_ANNOTATION, is_normalized)
        else:
            datalake_logger.debug(f'unsupported annotation_geometry={annotation_geometry}')

    def upload_groundtruth_from_json(
            self,
            storage_base_path: str,
            operation_id: str,
            file_path: str,
            annotation_geometry: str,
            is_normalized: bool
    ):
        datalake_logger.debug(f'upload_groundtruth_from_json file_path={file_path}, '
                              f'annotation_geometry={annotation_geometry}')
        _groundTruth = GroundTruth(client=self)
        if annotation_geometry == BOX_ANNOTATION:
            _groundTruth.upload_groundtruth_json(storage_base_path, operation_id, file_path, BOX_ANNOTATION, is_normalized)
        elif annotation_geometry == POLYGON_ANNOTATION:
            _groundTruth.upload_groundtruth_json(storage_base_path, operation_id, file_path, POLYGON_ANNOTATION, is_normalized)
        elif annotation_geometry == LINE_ANNOTATION:
            _groundTruth.upload_groundtruth_json(storage_base_path, operation_id, file_path, LINE_ANNOTATION, is_normalized)
        else:
            datalake_logger.debug(f'unsupported annotation_geometry={annotation_geometry}')

    def file_upload(self, path: str, collection_type, collection_name, meta_data_object, override):
        _upload = FileUpload(client=self)
        _upload.file_upload_initiate(path, collection_type, collection_name, meta_data_object, override)

    def get_upload_status(self, collection_name):
        _upload = FileUpload(client=self)
        return _upload.get_upload_status(collection_name)

    def remove_collection_annotations(self, collection_id: str, model_run_id: str):
        print(f'annotation delete of collection ={collection_id}', f'model id={model_run_id}')
        _model = Annotation(client=self)
        _model.remove_collection_annotations(collection_id, model_run_id)


    """
    get selection id for query, collection id, filter data
    """
    def get_selection_id(self, collection_id, query, filter, object_type, object_list):
        _query = Query(client=self)
        response = _query.get_selection_id(collection_id, query, filter, object_type, object_list)
        return response


    def get_object_type_by_id(self, object_id):
        response = self.datalake_interface.get_object_type_by_id(object_id)
        return response

    def get_all_system_labels(self):
        response = self.datalake_interface.get_all_label_list()
        return response

    def get_all_label_groups(self):
        response = self.datalake_interface.get_all_group_list()
        return response

    def create_label_group(self, group_name, label_keys):
        if group_name == '' or len(label_keys) == 0:
            print('Label group name or label list is empty')
            return None
        response = self.datalake_interface.create_label_group(group_name, label_keys)
        return response



