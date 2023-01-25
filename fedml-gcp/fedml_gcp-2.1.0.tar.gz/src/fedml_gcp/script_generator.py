import sys
import string
import json
import inspect
import ast
import os
from importlib import import_module
import random
import ctypes


class ScriptGeneratorHelper:

    def begin(self, tab="\t"):
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self):
        return ''.join(self.code)

    def write(self, string):
        self.code.append(self.tab * self.level + string)

    def indent(self):
        self.level = self.level + 1

    def dedent(self):
        if self.level == 0:
            raise SyntaxError("internal error in code generator")
        self.level = self.level - 1


class ScriptGenerator():

    def write_flaskapp(self, filename, predictor=None):
        code = ScriptGeneratorHelper()
        code.begin(tab='    ')

        code.write('from __future__ import print_function\n')
        code.write('import io\n')
        code.write('import os\n')
        code.write('import joblib\n')
        code.write('import signal\n')
        code.write('import sys\n')
        code.write('import traceback\n')
        code.write('\n')
        code.write('from flask import Flask, request, jsonify\n')
        code.write('from flask_restful import Resource, Api\n')
        # changed for packaging
        if predictor:
            code.write('from predictor import MyPredictor\n')
        else:
            code.write('from fedml_gcp import Model\n')
        code.write('\n')
        code.write('app = Flask(__name__)\n')
        code.write('api = Api(app)\n')
        # file, extension = entrypoint.rsplit('.', 1)
        # code.write("user_module = '" + file + "'\n")
        # code.write('model_path = os.path.join(prefix, "model")\n')

        code.write('class HomePage (Resource):\n')
        code.indent()
        code.write("def get(self):\n")
        code.indent()
        code.write("return 'FedML Kyma Deploy with GCP'\n")
        code.dedent()
        code.write('\n')
        code.dedent()
        code.write('\n')

        code.write('class RunModel (Resource):\n')
        code.indent()
        code.write('def post(self):\n')
        code.indent()
        code.write('try:\n')
        code.indent()
        if predictor:
            code.write('json_data = request.get_json(force=True)\n')
            code.write('loaded_model = joblib.load("model.pkl")\n')
            code.write('model = MyPredictor(loaded_model)\n')
            code.write('results = model.predict(json_data)\n')
            code.dedent()
            code.write('except Exception as e:\n')
            code.indent()
            code.write('print((str(e)), file=sys.stderr)\n')
            code.dedent()
            code.write('result = {"predictions": results}\n')
            code.write('return result\n')
            code.dedent()
            code.write('\n')
            code.dedent()
            code.write('\n')
        else:
            code.write('data = None\n')
            code.write('data = request.get_json(force=True)\n')
            code.write('loaded_model = joblib.load("model.pkl")\n')
            code.write('model = Model(loaded_model)\n')
            code.write('results = model.predict(data)\n')
            code.dedent()
            code.write('except Exception as e:\n')
            code.indent()
            code.write('print((str(e)), file=sys.stderr)\n')
            code.dedent()
            code.write('result = {"predictions": results.tolist()}\n')
            code.write('return result\n')
            code.dedent()
            code.write('\n')
            code.dedent()
            code.write('\n')

        code.write("api.add_resource(HomePage, '/')\n")
        code.write("api.add_resource(RunModel, '/predict')\n")
        code.write('\n')

        code.write("if __name__ == '__main__':\n")
        code.indent()
        code.write("app.run('0.0.0.0', '8080', debug=True)\n")

        f = open(filename, 'w')
        f.write(code.end())
        f.close()

    def write_dockerfile(self, filename, has_requirements, predictor=None):
        code = ScriptGeneratorHelper()
        code.begin(tab='    ')

        code.write('# Build an image that can do inference on Kyma\n')
        code.write(
            '# This is a Python 3 image that uses the gunicorn, flask stack\n')
        code.write('# for serving inferences in a stable way.\n')

        code.write('\n')
        code.write('FROM python:3.7-slim-buster\n')
        code.write('\n')
        code.write('MAINTAINER FedML SAP <ci_sce@sap.com>\n')
        code.write('\n')
        code.write('\n')

        code.write('\n')
        code.write('ADD api.py /\n')
        if predictor:
            code.write('ADD predictor.py /\n')
        code.write('ADD model.pkl /\n')
        # code.write('ADD fedml_gcp-2.0.0-py3-none-any.whl /\n')
        if has_requirements == True:
            code.write('ADD requirements.txt /\n')

        code.write('\n')
        code.write('RUN pip install flask\n')
        code.write('RUN pip install flask_restful\n')
        code.write('RUN pip install pandas\n')
        code.write('RUN pip install sklearn\n')
        code.write('RUN pip install numpy\n')
        code.write('RUN pip install joblib\n')
        code.write('\n')

        if has_requirements == True:
            code.write(
                'RUN pip --no-cache-dir install -r requirements.txt\n')
            code.write('\n')
        code.write('\n')

        # TODO : Change for PIP INSTALL
        code.write(
            'RUN pip install fedml_gcp\n')

        code.write('EXPOSE 8080\n')
        code.write('CMD [ "python", "./api.py"]')

        f = open(filename, 'w')
        f.write(code.end())
        f.close()

    def write_deployment(self, filename, num_instances, container_image, project_name):
        full_image_name = 'gcr.io/'+project_name+'/'+container_image
        code = ScriptGeneratorHelper()
        code.begin(tab='    ')

        code.write('apiVersion: v1\n')
        code.write('kind: Service\n')
        code.write('metadata:\n')
        code.write('  name: '+container_image+'\n')
        code.write('  labels:\n')
        code.write('    app: '+container_image+'\n')
        code.write('spec:\n')
        code.write('  ports:\n')
        code.write('  - name: http\n')
        code.write('    port: 8080\n')
        code.write('  selector:\n')
        code.write('    app: '+container_image+'\n')
        code.write('\n')
        code.write('---\n')
        code.write('\n')
        code.write('apiVersion: apps/v1\n')
        code.write('kind: Deployment\n')
        code.write('metadata:\n')
        code.write('  name: '+container_image+'\n')
#         code.write('  labels:\n')
#         code.write('    app: '+container_image+'\n')
        code.write('spec:\n')
        code.write('  selector:\n')
        code.write('    matchLabels:\n')
        code.write('      app: '+container_image+'\n')
        code.write('  replicas: '+str(num_instances)+'\n')
        code.write('  template:\n')
        code.write('    metadata:\n')
        code.write('      labels:\n')
        code.write('        app: '+container_image+'\n')
        code.write('    spec:\n')
        # code.write('      imagePullSecrets:\n')
        # code.write('        - name: '+profile_name+'-aws-ecr\n')
        code.write('      containers:\n')
        code.write('        - image: '+full_image_name)
        code.write('\n')
        code.write('          name: '+container_image+'\n')
        code.write('          ports:\n')
        code.write('          - containerPort: 8080\n')
        code.write('\n')
        code.write('---\n')
        code.write('\n')
        code.write('apiVersion: gateway.kyma-project.io/v1alpha1\n')
        code.write('kind: APIRule\n')
        code.write('metadata:\n')
        code.write('  name: '+container_image+'\n')
        code.write('spec:\n')
        code.write('  gateway: kyma-gateway.kyma-system.svc.cluster.local\n')
        code.write('  service:\n')
        code.write('    name: '+container_image+'\n')
        code.write('    port: 8080\n')
        code.write('    host: '+container_image+'\n')
        code.write('  rules:\n')
        code.write('    - path: /.*\n')
        code.write('      methods: ["GET", "POST"]\n')
        code.write('      mutators: []\n')
        code.write('      accessStrategies:\n')
        code.write('        - handler: noop\n')
        code.write('          config: {}\n')

        f = open(filename, 'w')
        f.write(code.end())
        f.close()
