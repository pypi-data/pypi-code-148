import copy
import os
import json


class ModelJanitor:
    def __init__(self, model_path, model_meta_template, params, updatable_keys=[]):
        self.model_path = model_path
        if os.path.exists(model_path) is False:
            os.makedirs(model_path)
        self.metadata_filename = os.path.join()
        self.params = params
        self.updatable_keys = updatable_keys
        self.model_meta_template = model_meta_template
        suffix = self.expand_name_template(self.model_meta_template, params)
        self.model_meta_filename = os.path.join(
            self.model_path, f"model_meta_{suffix}.json"
        )

    @staticmethod
    def expand_name_template(template, params):
        exp = copy.copy(template)
        for key in params:
            src = "{" + key + "}"
            dst = f"{params[key]}"
            exp = exp.replace(src, dst).replace("[", "(").replace("]", ")")
        return exp

    def save_model_metadata(self, params, current_epoch):
        params["current_epoch"] = current_epoch
        try:
            with open(self.model_meta_filename, "w") as f:
                f.write(json.dumps(params))
        except Exception as e:
            print(f"Failed to store model metadata to {self.model_meta_filename}: {e}")
            return False
        return True

    def read_model_metadata(self):
        try:
            with open(self.model_meta_filename, "r") as f:
                params = json.load(f)
        except Exception as e:
            print(
                f"Cannot access project meta-data at {self.model_meta_filename}: {e}, starting anew."
            )
            return None
        return params

    def is_metadata_compatible(self, current_params, saved_params):
        is_valid = True
        keys = set(list(current_params.keys()) + list(saved_params.keys()))
        for key in keys:
            if key in self.updatable_keys:
                continue
            if key not in saved_params:
                print(
                    f"Key {key} not available in last checkpoint model_meta, current_params[{key}]: {current_params[key]},"
                )
                print(
                    "cannot import incompatible model. Put key in `updatable_keys` list, if irrelevant."
                )
                is_valid = False
            elif key not in current_params:
                print(
                    f"Key {key} not available in params, last checkpoint saved_params[{key}]: {saved_params[key]},"
                )
                print(
                    "cannot import incompatible model. Put key in `updatable_keys` list, if irrelevant."
                )
                is_valid = False
            elif saved_params[key] != current_params[key]:
                print(
                    f"Last checkpoint saved_params[{key}]: {saved_params[key]} != current_params[{key}]: {current_params[key]},"
                )
                print(
                    "cannot import incompatible model. Put key in `updatable_keys` list, if irrelevant."
                )
                is_valid = False
        if is_valid is False:
            print("Aborting import.")
            return False
        return True
