from .Project import _Project
from .Datasource import global_methods

# original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

def train_and_test_callback(model_path, hyper_param_values, project_info, datasource_key, trainer_key_exists, prev_round, yes_stats, yes_submission, token, host):
    # signal.signal(signal.SIGINT, original_sigint_handler)
    project = _Project(token, host, project_info['key'])

    if not trainer_key_exists:
        return

    train = global_methods[datasource_key]['train']
    test = global_methods[datasource_key]['test']

    project_key = project_info['key']
    ext = project_info['modelType']
    current_round = project_info['currentRound']
    federated_model_path = get_federated_path(project_key, model_path, ext, datasource_key, prev_round)

    if not yes_submission or not yes_stats:
        # Pull
        print(f'>>> ({project_key}-{datasource_key}) Waiting to download round ({prev_round}) federated model...')
        project.pull_model(federated_model_path, round=prev_round, datasource_key=datasource_key, federated_model=True)

    # Test
    if not yes_stats:
        print(f'>>> ({project_key}-{datasource_key}) Running validation on round ({prev_round}) federated model...')
        test_res = test(datasource_key, federated_model_path, project_info)
        if test_res is not None:
            scores, num_samples = test_res
            print(scores)
            print(f'>>> ({project_key}-{datasource_key}) Uploading scores...')
            project.report_stats(scores, num_samples, prev_round, datasource_key)
            print('Done.')
        print()

    # Train and push
    if not yes_submission:
        new_model_path = get_trained_path(project_key, model_path, ext, datasource_key, current_round)

        print(f'>>> ({project_key}-{datasource_key}) Training weights on local model...')
        train_res = train(datasource_key, federated_model_path, new_model_path, project_info, hyper_param_values)

        print(f'>>> ({project_key}-{datasource_key}) Uploading round ({current_round}) trained model...')
        if train_res:
            project.push_model(new_model_path, datasource_key, params=train_res)
        else:
            project.push_model(new_model_path, datasource_key)
        print('Done.')
        print()

def get_trained_path(project_key, base, ext, ds, round):
    return f'{base}/trained_model_{project_key}_{ds}_{round}.{ext}'
def get_federated_path(project_key, base, ext, ds, round):
    return f'{base}/federated_model_{project_key}_{ds}_{round}.{ext}'