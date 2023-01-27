def return_function(node):
    if node["data"]["value"] == "Train-Test Split":
        return temp_train_test_split(node['data']['parameters'])
    elif node["data"]["value"] == "Train Model":
        return temp_train_model(node['data']['parameters'])

def temp_train_test_split(params):
    parameters = {
        "test_size": params["test_size"],
    }
    return f"training_dataset, test_dataset = huble.sklearn.train_test_split(data=data,parameters={parameters})"


def temp_train_model(params):
    return f"Model = huble.sklearn.train_model(data=data, model=model, column={params['target_column']})"
    