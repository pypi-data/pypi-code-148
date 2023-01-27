def return_function(node):
    if node["data"]["value"] == "Logistic Regression":
        return temp_logistic_regression(node['data']['parameters'])
    elif node["data"]["value"] == "SVM (SVC)":
        return temp_svm_svc(node['data']['parameters'])
    elif node["data"]["value"] == "Gaussian Naive Bayes":
        return temp_gaussian_naive_bayes(node['data']['parameters'])
    elif node["data"]["value"] == "Multinomial Naive Bayes":
        return temp_multinomial_naive_bayes(node['data']['parameters'])
    elif node["data"]["value"] == "Stochastic Gradient Descent Classifier":
        return temp_st_gradient_descent_classifier(node['data']['parameters'])
    elif node["data"]["value"] == "KNN":
        return temp_knn(node['data']['parameters'])
    elif node["data"]["value"] == "Decision Tree Classifier":
        return temp_decision_tree(node['data']['parameters'])
    elif node["data"]["value"] == "Random Forest Classifier":
        return temp_random_forest(node['data']['parameters'])
    elif node["data"]["value"] == "Gradient Boosting Classifier":
        return temp_gradient_boosting(node['data']['parameters'])
    elif node["data"]["value"] == "LGBM Classifier":
        return temp_lgbm(node['data']['parameters'])
    elif node["data"]["value"] == "XGBoost Classifier":
        return temp_xgboost(node['data']['parameters'])

    elif node["data"]["value"] == "Linear Regression":
        return temp_linear_regression(node['data']['parameters'])
    elif node["data"]["value"] == "LGBM Regressor":
        return temp_lgbm_regressor(node['data']['parameters'])
    elif node["data"]["value"] == "XGBoost Regressor":
        return temp_xgboost_regressor(node['data']['parameters'])
    elif node["data"]["value"] == "CatBoost Regressor":
        return temp_catboost_regressor(node['data']['parameters'])
    elif node["data"]["value"] == "Stochastic Gradient Descent Regression":
        return temp_st_gradient_descent_regressor(node['data']['parameters'])
    elif node["data"]["value"] == "Kernel Ridge Regression":
        return temp_kernel_ridge(node['data']['parameters'])
    elif node["data"]["value"] == "Elastic Net Regression":
        return temp_elastic_net(node['data']['parameters'])
    elif node["data"]["value"] == "Bayesian Ridge Regression":
        return temp_bayesian_ridge(node['data']['parameters'])
    elif node["data"]["value"] == "Gradient Boosting Regression":
        return temp_gradient_boosting_reg(node['data']['parameters'])
    elif node["data"]["value"] == "SVM (SVR)":
        return temp_svm_svr(node['data']['parameters'])

    elif node["data"]["value"] == "Mean Shift":
        return temp_mean_shift(node['data']['parameters'])
    elif node["data"]["value"] == "KMeans":
        return temp_kmeans(node['data']['parameters'])
    elif node["data"]["value"] == "Agglomerative Clustering":
        return temp_agglomerative(node['data']['parameters'])
    elif node["data"]["value"] == "BIRCH":
        return temp_birch(node['data']['parameters'])
    elif node["data"]["value"] == "Spectral Clustering":
        return temp_spectral(node['data']['parameters'])
    elif node["data"]["value"] == "Affinity Propagation":
        return temp_affinity_propogation(node['data']['parameters'])
    elif node["data"]["value"] == "OPTICS":
        return temp_optics(node['data']['parameters'])
    elif node["data"]["value"] == "DBSCAN":
        return temp_dbscan(node['data']['parameters'])
   
def temp_logistic_regression():
#     parameters = {
#         "penalty": params["penalty"],
#         "fit_intercept": params["fit_intercept"],
#         "random_state": params["random_state"],
#         "solver": params["solver"],
#         "max_iter": params["max_iter"],
#         "multi_class": params["multi_class"],
#         "tol": params["tol"],
#     }
    return f"model = huble.sklearn.logistic_regression()"


def temp_svm_svc(params):
    parameters = {
        "C" : params['C'], 
        "kernel" : params['kernel'],
        "probability" : params['probability'],
        "random_state": params["random_state"],
        "max_iter": params["max_iter"],
        "decision_function_shape": params["decision_function_shape"],
        "tol": params["tol"],
    }
    return f"model = huble.sklearn.svm_svc(parameters={parameters})"

def temp_gaussian_naive_bayes(params):
    parameters = {
        "priors" : params['priors'],
        "var_smoothing" : params['var_smoothing'],
    }
    return f"model = huble.sklearn.gaussian_naive_bayes(parameters={parameters})"

def temp_multinomial_naive_bayes(params):
    parameters = {
        "class_prior" : params['class_prior'],
        "alpha" : params['alpha'],
        "fit_prior" : params['fit_prior'],
    }
    return f"model = huble.sklearn.multinomial_naive_bayes(parameters={parameters})"

def temp_st_gradient_descent_classifier(params):
    parameters = {
        "loss" : params['loss'], 
        "penalty": params["penalty"],
        "fit_intercept": params["fit_intercept"],
        "alpha" : params['alpha'],
        "max_iter": params["max_iter"],
        "tol": params["tol"],
        "random_state": params["random_state"],
        "shuffle" : params['shuffle'],
        "learning_rate" : params['learning_rate'],
        "initial_learning_rate" : params['initial_learning_rate'],
        "early_stopping" : params['early_stopping'],
        "validation_fraction" : params['validation_fraction'],
    }
    return f"model = huble.sklearn.st_gradient_descent(parameters={parameters})"


def temp_knn(params):
    parameters = {
        "n_neighbors" : params['n_neighbors'], 
        "weights" : params['weights'], 
        "algorithm" : params['algorithm'],
        "metric" : params['metric'],
    }
    return f"model = huble.sklearn.knn(parameters={parameters})"


def temp_decision_tree(params):
    parameters = {
        "criterion" : params['criterion'],
        "splitter" : params['splitter'],
        "max_depth" : params['max_depth'],
        "max_leaf_nodes" : params['max_leaf_nodes'],
        "random_state" : params['random_state'],
    }
    return f"model = huble.sklearn.decision_tree(parameters={parameters})"


def temp_random_forest(params):
    parameters = {
        "criterion" : params['criterion'],
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "max_leaf_nodes" : params['max_leaf_nodes'],
        "random_state" : params['random_state'],
    }
    return f"model = huble.sklearn.random_forest(parameters={parameters})"


def temp_gradient_boosting(params):
    parameters = {
        "criterion" : params['criterion'],
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "max_leaf_nodes" : params['max_leaf_nodes'],
        "random_state" : params['random_state'],
        "loss" : params['loss'],
        "learning_rate" : params['learning_rate'],
        "subsample" : params['subsample'],
        "tol" : params['tol'],
    }
    return f"model = huble.sklearn.gradient_boosting(parameters={parameters})"


def temp_lgbm(params):
    parameters = {
        "boosting_type" : params['boosting_type'],
        "num_leaves" : params['num_leaves'],
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "random_state" : params['random_state'],     
        "learning_rate" : params['learning_rate'],
    }
    return f"model = huble.sklearn.lgbm(parameters={parameters})"


def temp_xgboost(params):
    parameters = {
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "random_state" : params['random_state'],     
        "learning_rate" : params['learning_rate'],
    }
    return f"model = huble.sklearn.xgboost(parameters={parameters})"


#Regression

def temp_linear_regression(params):
    parameters = {
        "fit_intercept" : params['fit_intercept'],
        "normalize" : params['normalize'],
        "copy_X" : params['copy_X'],
        "positive" : params['positive'],
    }
    return f"model = huble.sklearn.linear_regression(parameters={parameters})"


def temp_lgbm_regressor(params):
    parameters = {
        "boosting_type" : params['boosting_type'],
        "num_leaves" : params['num_leaves'],
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "random_state" : params['random_state'],     
        "learning_rate" : params['learning_rate'],
    }
    return f"model = huble.sklearn.lgbm_reg(parameters={parameters})"

def temp_xgboost_regressor(params):
    parameters = {
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "random_state" : params['random_state'],     
        "learning_rate" : params['learning_rate'],
    }
    return f"model = huble.sklearn.xgboost_reg(parameters={parameters})"

def temp_catboost_regressor(params):
    parameters = {
        "iterations" : params['iterations'],    
        "learning_rate" : params['learning_rate'],
    }
    return f"model = huble.sklearn.catboost_reg(parameters={parameters})"

def temp_st_gradient_descent_regressor(params):
    parameters = {
        "loss" : params['loss'], 
        "penalty": params["penalty"],
        "fit_intercept": params["fit_intercept"],
        "alpha" : params['alpha'],
        "max_iter": params["max_iter"],
        "tol": params["tol"],
        "random_state": params["random_state"],
        "shuffle" : params['shuffle'],
        "learning_rate" : params['learning_rate'],
        "early_stopping" : params['early_stopping'],
    }
    return f"model = huble.sklearn.st_gradient_descent_reg(parameters={parameters})"

def temp_kernel_ridge(params):
    parameters = {
        "alpha" : params['alpha'],  
    }
    return f"model = huble.sklearn.kernel_ridge_reg(parameters={parameters})"

def temp_elastic_net(params):
    parameters = {
        "fit_intercept" : params['fit_intercept'],
        "normalize" : params['normalize'],
        "copy_X" : params['copy_X'],
        "positive" : params['positive'],
        "alpha" : params['alpha'],
        "l1_ratio" : params['l1_ratio'],
        "selection" : params['selection'],
    }
    return f"model = huble.sklearn.elastic_net_reg(parameters={parameters})"

def temp_bayesian_ridge(params):
    parameters = {
        "n_iter" : params['n_iter'], 
    }
    return f"model = huble.sklearn.bayesian_ridge_reg(parameters={parameters})"

def temp_gradient_boosting_reg(params):
    parameters = {
        "criterion" : params['criterion'],
        "n_estimators" : params['n_estimators'],
        "max_depth" : params['max_depth'],
        "max_leaf_nodes" : params['max_leaf_nodes'],
        "random_state" : params['random_state'],
        "loss" : params['loss'],
        "learning_rate" : params['learning_rate'],
        "subsample" : params['subsample'],
        "tol" : params['tol'],
    }
    return f"model = huble.sklearn.gradient_boosting_reg(parameters={parameters})"

def temp_svm_svr(params):
    parameters = {
        "C" : params['C'], 
        "kernel" : params['kernel'],
        "max_iter": params["max_iter"],
        "tol": params["tol"],
    }
    return f"model = huble.sklearn.svm_svr(parameters={parameters})"

#Clustering

def temp_mean_shift(params):
    parameters = {
        "bandwidth" : params['bandwidth'],
        "bin_seeding" : params['bin_seeding'],
        "min_bin_freq" : params['min_bin_freq'],
        "cluster_all" : params['cluster_all'],
        "max_iter" : params['max_iter'],
    }
    return f"model = huble.sklearn.mean_shift(parameters={parameters})"


def temp_kmeans(params):
    parameters = {
        "n_clusters" : params['n_clusters'],
        "init" : params['init'],
        "copy_X" : params['copy_X'],
        "tol" : params['tol'],
        "max_iter" : params['max_iter'],     
        "algorithm" : params['algorithm'],
        "random_state" : params['random_state'],
    }
    return f"model = huble.sklearn.kmeans(parameters={parameters})"

def temp_agglomerative(params):
    parameters = {
        "n_clusters" : params['n_clusters'],
        "linkage" : params['linkage'],
    }
    return f"model = huble.sklearn.agglomerative(parameters={parameters})"

def temp_birch(params):
    parameters = {
        "threshold" : params['threshold'],    
        "branching_factor" : params['branching_factor'],
        "n_clusters" : params['n_clusters'],
    }
    return f"model = huble.sklearn.birch(parameters={parameters})"

def temp_spectral(params):
    parameters = {
        "n_clusters" : params['n_clusters'], 
        "eigen_solver": params["eigen_solver"],
        "n_init": params["n_init"],
        "assign_labels" : params['assign_labels'],
    }
    return f"model = huble.sklearn.spectral(parameters={parameters})"

def temp_affinity_propogation(params):
    parameters = {
        "damping" : params['damping'],  
        "max_iter" : params['max_iter'],  
        "convergence_iter" : params['convergence_iter'],  
        "affinity" : params['affinity'],  
    }
    return f"model = huble.sklearn.affinity_propogation(parameters={parameters})"

def temp_optics(params):
    parameters = {
        "min_samples" : params['min_samples'],
        "algorithm" : params['algorithm'],
    }
    return f"model = huble.sklearn.optics(parameters={parameters})"

def temp_dbscan(params):
    parameters = {
        "eps" : params['eps'],
        "min_samples" : params['min_samples'],
        "algorithm" : params['algorithm'],
    }
    return f"model = huble.sklearn.dbscan(parameters={parameters})"



