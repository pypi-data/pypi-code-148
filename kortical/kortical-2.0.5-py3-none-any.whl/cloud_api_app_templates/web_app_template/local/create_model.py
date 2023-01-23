import os
import pandas as pd
from kortical import api
from kortical.api.project import Project
from kortical.api.environment import Environment
from kortical.app import get_config
from module_placeholder.helpers.root_dir import from_root_dir


app_config = get_config(format='yaml')
data_file_name = app_config['data_file_name']
model_name = app_config['model_name']
target = app_config['target']

if __name__ == '__main__':
    api.init()

    project = Project.get_selected_project()
    environment = Environment.get_selected_environment(project)

    # Load dataset
    df = pd.read_csv(from_root_dir(os.path.join("data", data_file_name)))

    # Do custom pre-processing (data cleaning / feature creation)

    # Create model
    instance = api.instance.Instance.create_or_select(model_name, delete_unpublished_models=True, stop_train=True)
    data = api.data.Data.upload_df(df, name=model_name)
    data.set_targets(target)

    model = instance.train_model(
        data,
        number_of_train_workers=3,
        target_score=0.945
    )

    print(f"Model score [{model.score} {model.evaluation_metric}]")

    environment.create_component_instance(model.id)

    print(f"Published model [{model.id} {model_name}] to environment [{environment}]")
