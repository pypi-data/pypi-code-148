import base64

from layerx import datalake, dataset, studio
from layerx.datalake.constants import MediaType, ObjectType



class LayerxClient:
    """
    Python SDK of LayerX
    """

    def __init__(self, api_key: str, secret: str, layerx_url: str) -> None:
        _string_key_secret = f'{api_key}:{secret}'
        _key_secret_bytes = _string_key_secret.encode("ascii")
        _encoded_key_secret_bytes = base64.b64encode(_key_secret_bytes)
        self.encoded_key_secret = _encoded_key_secret_bytes.decode("ascii")
        self.layerx_url = layerx_url

    def upload_annoations_for_folder(
            self,
            collection_base_path: str,
            operation_unique_id: str,
            json_data_file_path: str,
            shape_type: str,
            is_normalized: bool,
            is_model_run: bool
    ):
        """
        Upload annotation data from a json file
        """
        # init datalake client
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)

        if is_model_run:
            _datalake_client.upload_modelrun_from_json(
                collection_base_path,
                operation_unique_id,
                json_data_file_path,
                shape_type,
                is_normalized
            )
        else:
            _datalake_client.upload_groundtruth_from_json(
                collection_base_path,
                operation_unique_id,
                json_data_file_path,
                shape_type,
                is_normalized)

    """
    Download dataset """

    def download_dataset(self, version_id: str, export_type: str):
        # init dataset client
        _dataset_client = dataset.DatasetClient(self.encoded_key_secret, self.layerx_url)

        # start download
        _dataset_client.download_dataset(version_id, export_type)

    """"
    Images/vidoe upload
    """

    def file_upload(self, path: str, collection_type, collection_name, meta_data_object="", override=False):
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)
        _datalake_client.file_upload(path, collection_type, collection_name, meta_data_object, override)

    """
    Download collection annotations
    From datalake
    @param collection_id - id of dataset version
    @param model_id - Optional: id of the model (same operation_id given in upload annotations) 
    if we need annotations for that specific model """

    def download_annotations(self, collection_id: str, model_id: str):
        # init dataset client
        _dataset_client = dataset.DatasetClient(self.encoded_key_secret, self.layerx_url)

        # start download
        _dataset_client.download_annotations(collection_id, model_id)
    

    """"
    Images and annotation upload
    """
    def upload_data(self, collection_name, file_path, meta_data_object, operation_unique_id, json_data_file_path, shape_type, is_normalized, is_model_run):

        if (file_path == None):
            print('file upload cannot be done')
        else:
            self.file_upload(file_path, MediaType.IMAGE.value, collection_name, meta_data_object, False)

        if (json_data_file_path == None):
            print('annotation upload cannot be done')
        else:
            self.upload_annoations_for_folder(collection_name, operation_unique_id, json_data_file_path, shape_type, is_normalized, is_model_run)
    


    """"
    get upload progress
    """

    def get_upload_status(self, collection_name):
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)
        return _datalake_client.get_upload_status(collection_name)

    """
    remove annotations of collection model run
    """
    def remove_annotations(self, collection_id: str, model_run_id: str):
        print(f'remove annotations of collection: {collection_id}, operation id: {model_run_id}')

        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)

        _datalake_client.remove_collection_annotations(collection_id, model_run_id)
    

    """
    create annotation studio project using query, filter and collections
    """
    def __create_studio_project(self, project_name: str, collection_id: str, query: str, filter, object_type: int, object_list, fps):
        print(f'create project using query, filter and collections - project name: {project_name}, ')

        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)
        _studio_client = studio.StudioClient(self.encoded_key_secret, self.layerx_url)

        response = _datalake_client.get_selection_id(collection_id, query, filter, object_type, object_list)
        print('selection id: ',response)
        get_selection_id_success = True
        if("isSuccess" in response):
            if(response["isSuccess"] == False):
                get_selection_id_success = False
        if get_selection_id_success == True:
            project_response = _studio_client.create_project(project_name, response['selectionTag'], fps)
            print('project_response: ',project_response)
            return project_response
        else:
            print('project_response: ',{
                "isSuccess": False
            })
            return {
                "isSuccess": False
            }
    
    def __get_object_type_by_id(self, object_id: str):
        print(f'get object type by id: {object_id}')

        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)
        response =  _datalake_client.get_object_type_by_id(object_id)
        return response
    

    """
    create annotation studio project using query, filter and collections
    """
    def create_annotation_project_from_collection(self, project_name: str, collection_id: str, query: str = "", filter = {}, fps: int = 0):
        print(f'create project using query, filter and collections - project name: {project_name}, ')

        if(collection_id == None or collection_id == ''):
            print('collection id must be provided')
            return {
                "isSuccess": False,
                "error": 'collection id must be provided'
            }
        object_type_object = self.__get_object_type_by_id(collection_id)
        object_type = None
        if "objectType" in object_type_object:
            object_type = object_type_object["objectType"]
        
        if object_type == None:
            print('object type cannot find for collection id')
            return {
                "isSuccess": False,
                "error": 'object type cannot find for collection id'
            }

        #if((fps == None) and (object_type == ObjectType.VIDEO.value or object_type == ObjectType.VIDEO_COLLECTION.value)):
        #    print('fps must be provided')
        #    return {
        #        "isSuccess": False,
        #        "error": 'fps must be provided'
        #    }

        try:
            response = self.__create_studio_project(project_name, collection_id, query, filter, ObjectType.IMAGE, [], fps)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "isSuccess": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    create annotation studio project using query, filter and collections
    """
    def create_annotation_project_from_datalake(self, project_name: str, datalake_query: str, datalake_filter = {}, object_type: int = ObjectType.IMAGE, fps: int = 0):
        print(f'create project using query, filter and collections - project name: {project_name}, ')
        
        #Prevent all objects case
        if datalake_query == "" and datalake_filter == {}:
            print('At least either valid filter or query should be given')
            return {
                "is_success": False,
                "error": "Not enough selection parameters"
            }

        #if(object_type == ObjectType.VIDEO or object_type == ObjectType.VIDEO_COLLECTION):
        #    return {
        #        "isSuccess": False,
        #        "error": 'fps must be provided'
        #    }

        try:
            response = self.__create_studio_project(project_name, "", datalake_query, datalake_filter,  object_type, [], fps)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }
    

    """
    update annotation project using query, filter and collections
    """
    def __update_objects_to_studio_project(self, project_id: str, collection_id: str, query: str, filter, object_type: int, object_list, fps):
        print(f'create project using query, filter and collections - project id: {project_id}, ')

        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)
        _studio_client = studio.StudioClient(self.encoded_key_secret, self.layerx_url)

        response = _datalake_client.get_selection_id(collection_id, query, filter, object_type, object_list)
        print('selection id: ',response)
        get_selection_id_success = True
        if("isSuccess" in response):
            if(response["isSuccess"] == False):
                get_selection_id_success = False
        if get_selection_id_success == True:
            project_response = _studio_client.update_project(project_id, response['selectionTag'], fps)
            print('project_response: ',project_response)
            return project_response
        else:
            print('project_response: ',{
                "is_success": False
            })
            return {
                "is_success": False
            }

    """
    update annotation studio project using query, filter and collections
    """
    def add_files_to_annotation_project_from_collection(self, project_id: str, collection_id: str, query: str, filter, fps: int = 0):
        print(f'create project using query, filter and collections - project name: {project_id}, ')

        if collection_id == None or collection_id == '':
            return {
                "is_success": False,
                "error": 'collection id must be provided'
            }

        object_type_object = self.__get_object_type_by_id(collection_id)
        object_type = None
        if "objectType" in object_type_object:
            object_type = object_type_object["objectType"]
        
        if object_type == None:
            print('object type cannot find for collection id')
            return {
                "is_success": False,
                "error": 'object type cannot find for collection id'
            }
        #if(fps == None and (object_type == ObjectType.VIDEO.value or object_type == ObjectType.VIDEO_COLLECTION.value)):
        #    return {
        #        "isSuccess": False,
        #        "error": 'fps must be provided'
        #    }

        try:
            response = self.__update_objects_to_studio_project(project_id, collection_id, query, filter, 0, [], fps)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    update annotation studio project using query, filter and collections
    """
    def add_files_to_annotation_project_from_datalake(self, project_id: str, query: str, filter, object_type: int, fps: int = 0):
        print(f'create project using query, filter and collections - project name: {project_id}, ')

        #if(object_type == ObjectType.VIDEO or object_type == ObjectType.VIDEO_COLLECTION):
        #    return {
        #        "isSuccess": False,
        #        "error": 'fps must be provided'
        #    }

        try:
            response = self.__update_objects_to_studio_project(project_id, "", query, filter, object_type, [], fps)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }
    """
    delete a annotation studio project by project id
    """
    def delete_studio_project(self, project_id: str):
        if(project_id == None or project_id == ""):
            print("Project id not available")
            print({
                "is_success": False,
                "error": f'Project id not available'
            })
            return {
                "is_success": False,
                "error": f'Project id not available'
            }
        print(f'delete project - project id: {project_id}')
        _studio_client = studio.StudioClient(self.encoded_key_secret, self.layerx_url)
        try:
            response = _studio_client.delete_project(project_id)
            print('project delete', response)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    update the labels of studio project
    """
    def __update_labels_to_studio_project(self, project_id: str, add_list, remove_list):
        print(f'add labels to project - project id: {project_id}, add label list: {add_list}, remove label list: {remove_list}')

        _studio_client = studio.StudioClient(self.encoded_key_secret, self.layerx_url)

        response = _studio_client.update_labels_to_project(project_id, add_list, remove_list)

        return response
    
    """
    add the labels of studio project
    """
    def add_labels_to_studio_project(self, project_id: str, add_list):
        print(f'add labels to project - project id: {project_id}, label list: {add_list}')
        try:
            response =  self.__update_labels_to_studio_project(project_id, add_list, [])
            print('response: ', response)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    remove the labels of studio project
    """
    def remove_labels_to_studio_project(self, project_id: str, remove_list):
        print(f'remove labels to project - project id: {project_id}, label list: {remove_list}')

        try:
            response =  self.__update_labels_to_studio_project(project_id, [], remove_list)
            print('response: ', response)
            return response
        except Exception as e:
            print("An exception occurred", format(e))
            return {
                "is_success": False,
                "error": f'An exception occurred: {format(e)}'
            }

    """
    Get list of studio project
    """
    def get_studio_project_list(self):
        _studio_client = studio.StudioClient(self.encoded_key_secret, self.layerx_url)
        return _studio_client.studio_project_list()

    """
    Get list of all system labels
    """
    def get_all_labels(self):
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)
        return _datalake_client.get_all_system_labels()

    """
    Create a group from labels (label keys)
    """
    def create_label_group(self, group_name, label_ids):
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)
        return _datalake_client.create_label_group(group_name, label_ids)

    """
    List All label groups
    """
    def get_all_label_groups(self):
        _datalake_client = datalake.DatalakeClient(self.encoded_key_secret, self.layerx_url)
        return _datalake_client.get_all_label_groups()

    """
    Attach label group to annotation project
    """
    def attach_label_group_to_annotation_project(self, project_id, group_id):
        _studio_client = studio.StudioClient(self.encoded_key_secret, self.layerx_url)
        return _studio_client.project_set_label_group(project_id, group_id)

    """
    Download project annotations
    @param project_id - id of annotation project
    """

    def download_project_annotations(self, project_id: str):
        # init dataset client
        _dataset_client = dataset.DatasetClient(self.encoded_key_secret, self.layerx_url)

        # start download
        _dataset_client.download_annotations_for_project(project_id)
    