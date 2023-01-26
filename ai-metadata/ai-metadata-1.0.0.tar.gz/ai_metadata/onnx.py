#
# Copyright (c) 2023 AutoDeployAI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import numpy as np
from .base import MetadataModel, MiningFunction, ModelSerialization
from .utils import test_data_to_ndarray, is_compatible_shape


class ONNXModel(MetadataModel):
    """A wrapper of an ONNX model
    """

    def __init__(self,
                 model,
                 mining_function: 'MiningFunction' = None,
                 x_test=None,
                 y_test=None,
                 data_test=None,
                 source_object=None,
                 **kwargs):
        super().__init__(model, mining_function, x_test, y_test, data_test, source_object, **kwargs)
        self.onnx_model = self.load_model(self.model)
        self.sess = None
        self._algorithm = None

    @staticmethod
    def is_support(model) -> bool:
        return ONNXModel.load_model(model)

    def model_type(self) -> str:
        return 'onnx'

    def framework(self) -> str:
        return 'ONNX'

    def framework_version(self) -> str:
        return str(self.onnx_model.ir_version)

    def serialization(self) -> 'ModelSerialization':
        return ModelSerialization.ONNX

    def function_name(self) -> 'MiningFunction':
        algorithm = self.algorithm()
        if algorithm is not None:
            if algorithm in ('LinearClassifier', 'SVMClassifier', 'TreeEnsembleClassifier'):
                return MiningFunction.CLASSIFICATION
            if algorithm in ('LinearRegressor', 'SVMRegressor', 'TreeEnsembleRegressor'):
                return MiningFunction.REGRESSION
        return super().function_name()

    def runtime(self) -> str:
        return 'ONNXRuntime'

    def algorithm(self) -> str:
        if self._algorithm is None:
            use_onnx_ml = False
            if self.onnx_model is not None:
                graph = self.onnx_model.graph
                for node in graph.node:
                    if node.domain == 'ai.onnx.ml':
                        use_onnx_ml = True
                        if node.op_type in ('LinearClassifier', 'LinearRegressor', 'SVMClassifier', 'SVMRegressor',
                                            'TreeEnsembleClassifier', 'TreeEnsembleRegressor'):
                            self._algorithm = node.op_type
                            break
                if self._algorithm is None and not use_onnx_ml:
                    self._algorithm = 'NeuralNetwork'
        return self._algorithm

    def predict(self, data):
        # Suppose the first field is the prediction
        outputs = self.outputs()
        output_name = outputs[0]['name']
        y_pred = np.asarray(self.predict_raw(data, output_name=output_name))
        shape = y_pred.shape
        if len(shape) > 1 and shape[1] > 1:
            y_pred = np.argmax(y_pred, axis=1)
        return y_pred

    def predict_proba(self, data):
        output_name = None
        outputs = self.outputs()
        for x in outputs:
            if output_name is None:
                output_name = x['name']
            if 'probability' in x['name']:
                output_name = x['name']
        y_pred = self.predict_raw(data, output_name=output_name)
        return y_pred

    def predict_raw(self, data, **kwargs):
        output_name = kwargs['output_name'] if 'output_name' in kwargs else None
        sess = self._get_inference_session()

        # The data is already a dict with proper types
        if isinstance(data, dict):
            prediction = sess.run([output_name], data)
        else:
            x = sess.get_inputs()[0]
            if x.type == "tensor(float)":
                data = np.asarray(data, np.float32)
            prediction = sess.run([output_name], {x.name: data})

        if len(prediction) == 1:
            prediction = prediction[0]
        return prediction

    def inputs(self) -> list:
        result = []

        sess = self._get_inference_session()
        for x in sess.get_inputs():
            result.append({
                'name': x.name,
                'type': x.type,
                'shape': x.shape
            })

        # suppose there is only 1 tensor input
        data = test_data_to_ndarray(self.x_test, self.data_test)
        if data is not None and len(result) == 1:
            if is_compatible_shape(data.shape, result[0]['shape']):
                result[0]['sample'] = [data[0].tolist()]
        return result

    def targets(self) -> list:
        return []

    def outputs(self) -> list:
        result = []

        sess = self._get_inference_session()
        for x in sess.get_outputs():
            result.append({
                'name': x.name,
                'type': x.type,
                'shape': x.shape
            })
        return result

    def save_model(self, model_path) -> 'ModelSerialization':
        import onnx
        if isinstance(self.model, onnx.ModelProto):
            onnx_model = self.model
        elif isinstance(self.model, (bytes, bytearray)):
            onnx_model = onnx.load_model_from_string(self.model)
        else:
            onnx_model = onnx.load_model(self.model)
        onnx.save(onnx_model, model_path)
        return self.serialization()

    def _get_inference_session(self):
        if self.sess is None:
            import onnxruntime as rt
            self.sess = rt.InferenceSession(self.onnx_model.SerializeToString())
        return self.sess

    @staticmethod
    def load_model(model):
        try:
            import onnx

            if isinstance(model, onnx.ModelProto):
                return model

            if isinstance(model, (bytes, bytearray)):
                onnx_model = onnx.load_model_from_string(model)
            else:
                # could be either readable or a file path
                onnx_model = onnx.load_model(model)

            onnx.checker.check_model(onnx_model)
            return onnx_model
        except Exception:
            return None

