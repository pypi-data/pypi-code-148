import os
import sys
import io
import numpy as np
import pandas as pd
import tarfile
from .logger import Logger
from .script_generator import ScriptGenerator
import yaml
import subprocess  # for deploy_to_kyma
import re  # for deploy_to_kyma
import stat
import shutil
import requests
import json
from google.cloud import storage
from google.cloud import aiplatform

class DwcGCP:
    def __init__(self, configs={}):
        
        if type(configs) != dict:
            raise TypeError('configs must be a dictionary.')

        self.logger = Logger.get_instance()
        
        if 'project' not in configs:
            raise ValueError('Error: Please initialize class with GCP project in configs parameter')
        
        if 'staging_bucket' not in configs:
            raise ValueError('Error: Please initialize class with the staging_bucket parameter in configs parameter. This is a GCP Cloud Storage bucket path. Ex: "gs://"')
        
        if 'location' not in configs:
            raise ValueError('Error: Please initialize class with location / region')
        
        self.location = configs['location']
        self.project_name = configs['project']
        split_staging_bucket = configs['staging_bucket'].split('/')
        self.bucket_name = split_staging_bucket[2]
        
        aiplatform.init(**configs)

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        self.logger.info(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )

    def download_blob(self, bucket_name, source_blob_name, destination_file_name):

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)

        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        self.logger.info(
            "Downloaded storage object {} from bucket {} to local file {}.".format(
                source_blob_name, bucket_name, destination_file_name
            )
        )

    def make_tarfile(self, output_filename, source_dir):
        if type(output_filename) != str:
            raise TypeError('output_filename must be a string.')
        if type(source_dir) != str:
            raise TypeError('source_dir must be a string.')

        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

    def make_tar_bundle(self, output_filename='training.tar.gz', source_dir='training', destination='train/training.tar.gz'):
        if type(output_filename) != str:
            raise TypeError('output_filename must be a string.')
        if type(source_dir) != str:
            raise TypeError('source_dir must be a string.')
        if type(destination) != str:
            raise TypeError('destination must be a string.')

        self.make_tarfile(output_filename, source_dir)
        self.upload_blob(self.bucket_name, output_filename, destination)

    def _custom_python_package_training_job(self, training_inputs):
        self.logger.info('creating custom python package training job')
        return aiplatform.CustomPythonPackageTrainingJob(**training_inputs)
        
    def _custom_training_job(self, training_inputs):
        self.logger.info('creating custom training job')
        return aiplatform.CustomTrainingJob(**training_inputs)
    
    def train_model(self, training_inputs, training_type='custom', params={}):
        if type(training_inputs) != dict:
            raise TypeError('training_inputs must be a dictionary.')
        if type(params) != dict:
            raise TypeError('params must be a dictionary.')
        if type(training_type) != str:
            raise TypeError('training_type must be a string.')
        
        if training_type == 'customPythonPackage':
            #required for customPythonPackage - display_name, python_package_gcs_uri, python_module_name, container_uri
            if 'display_name' not in training_inputs or 'python_package_gcs_uri' not in training_inputs or 'python_module_name' not in training_inputs or 'container_uri' not in training_inputs:
                raise ValueError('display_name, python_package_gcs_uri, python_module_name and container_uri are required parameters when creating a custom python package training job')
            try:
                job = self._custom_python_package_training_job(training_inputs)
            except Exception as e:
                self.logger.error('Error creating training job', e)
                raise
        elif training_type == 'custom':
            #required for custom - display_name, script_path, container_uri
            if 'display_name' not in training_inputs or 'script_path' not in training_inputs or 'container_uri' not in training_inputs:
                raise ValueError('display_name, script_path, and container_uri are required parameters when creating a custom training job ')
            try:
                job = self._custom_training_job(training_inputs)
            except Exception as e:
                self.logger.error('Error creating training job', e)
                raise
        else:
            raise ValueError('training_type must be custom or customPythonPackage. Any other values are not accepted.') 
                    
        self.logger.info('running training job')
        return job.run(**params)
                                 
        
    def create_or_get_endpoint(self, endpoint_config={}, create_endpoint=True):
        if type(endpoint_config) != dict:
            raise TypeError('endpoint_config must be a dictionary.')
        if type(create_endpoint) != bool:
            raise TypeError('create_endpoint must be a bool value.')

        if create_endpoint == True:
            if not endpoint_config:
                self.logger.info('no endpoint_config passed...using project and location as specified in DwcGCP constructor, alongside other Vertex AI default values for endpoint creation.')
            return aiplatform.Endpoint.create(**endpoint_config)
        else:
            if 'endpoint_name' in endpoint_config:
                raise ValueError("When create_endpoint is false, endpoint_config must be a dictionary with a required key of endpoint_name, with other optional key and values passed. Please refer to this libraries read me for more information on the possible key-value pairs.")
            return aiplatform.Endpoint(**endpoint_config)
              
    def upload_custom_predictor(self, cpr_model_config, upload_config={}):
        if type(cpr_model_config) != dict:
            raise TypeError('cpr_model_config must be a dictionary.')
        if type(upload_config) != dict:
            raise TypeError('upload_config must be a dictionary.')

        if 'local_model' in upload_config:
            raise ValueError('You cannot pass local_model here. You are building a new cpr model and uploading that with this function.')
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", '-U', '--user', '-r', cpr_model_config['requirements_path'], '--no-cache-dir'])
        self.logger.info('building custom predictor routine')
        local_model = aiplatform.prediction.LocalModel.build_cpr_model(**cpr_model_config)
        local_model.push_image()
        self.logger.info('local model pushed to ' + cpr_model_config['output_image_uri'])
        
        upload_config['local_model'] = local_model
        self.logger.info('uploading model.')
        
        return aiplatform.Model.upload(**upload_config)
    
    def deploy(self, model, model_config={}):
        if type(model_config) != dict:
            raise TypeError('model_config must be a dictionary.')

        if type(model) == aiplatform.Model or type(model) == str:
            if type(model) == str:
                model = aiplatform.Model(model_name=model)
                
            return model.deploy(**model_config)
        else:
            raise TypeError('model_name must either be a string representing a fully-qualified model resource name or model ID or an aiplatform.Model object.')
            
    def predict(self, endpoint, predict_params):
        if type(predict_params) != dict:
            raise TypeError('predict_params must be a dictionary.')

        if type(endpoint) == str or type(endpoint) == aiplatform.Endpoint:
            if type(endpoint) == str:
                endpoint = aiplatform.Endpoint(endpoint_name=endpoint)
            if 'instances' not in predict_params:
                raise ValueError('instances must be a key in the predict_params list')
            result = endpoint.predict(**predict_params)
            return result.predictions
        else:
            raise TypeError('endpoint should be a string representing a fully-qualified endpoint resource name or endpoint ID or an aiplatform.Endpoint object.')
            
            