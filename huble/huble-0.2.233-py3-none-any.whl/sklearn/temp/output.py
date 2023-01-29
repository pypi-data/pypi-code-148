import huble

def run_file():
  model = huble.sklearn.st_gradient_descent(parameters={'loss': 'hinge', 'penalty': 'l2', 'fit_intercept': True, 'alpha': 0.0001, 'max_iter': 1000, 'tol': 0.001, 'random_state': 'None', 'shuffle': True, 'learning_rate': 'optimal', 'initial_learning_rate': 0, 'early_stopping': False, 'validation_fraction': 1})
  data=huble.util.load_dataset('https://ipfs.filebase.io/ipfs/QmRspeqXi9J2PVTmXYwMaBif9dYWVkNhM8EFomUAfajnT1')
  data = huble.sklearn.drop_duplicates(data=data,parameters={'subset': [], 'keep': 'first', 'inplace': False, 'ignore_index': False})
  data = huble.sklearn.remove_mismatch_data(data=data, parameters={'exceptions': []})
  data = huble.sklearn.remove_outliers(data=data,columns=['Ticket'])
  data = huble.sklearn.drop_rows_columns(data=data,parameters={'labels': ['PassengerId', 'Pclass', 'Name'], 'axis': 0, 'inplace': False, 'errors': 'raise'})
  data = huble.sklearn.clean_data(data=data)
  training_dataset, test_dataset = huble.sklearn.train_test_split(data=data,parameters={'test_size': '0.25'})
  Model = huble.sklearn.train_model(data=training_dataset, model=model, column='Survived')
  metrics = huble.util.evaluate_model(model=Model, test_dataset=test_dataset, target_column= 'Survived', task_type='classification' )
