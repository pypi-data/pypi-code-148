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
  pipeline = experiment['pipelineJSON']
  project = experiment['project']
  target_column = project['targetColumn']
  task_type = project['taskType']
  try:
    generate_file(pipeline,target_column,task_type)
  except:
    print("Error generating file")
    return
