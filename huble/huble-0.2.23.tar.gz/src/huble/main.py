from .functions import fetch_experiment
from .sklearn import generate_file

# {
#   "id": "ad40ca00-4a45-4690-babb-4e6b15348302",
#   "title": "able-air",
#   "pipelineJSON": {
    
#   },
#   "project": {
#     "targetColumn": "Survived",
#     "taskType": "classification"
#   }
# }
def run_experiment(experiment_id,auth_key=''):
  #TODO: Implement auth keys
  experiment = fetch_experiment(experiment_id)
  print(experiment)
  pipeline = experiment['pipelineJSON']
  project = experiment['project']
  target_column = project['targetColumn']
  task_type = project['taskType']
  generate_file(pipeline,task_type=task_type,target_column=target_column)