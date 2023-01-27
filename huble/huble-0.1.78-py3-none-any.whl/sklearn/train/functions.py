from re import sub
import sklearn
import lightgbm as lgb
import xgboost as xgb
import catboost as cb

#Classification

def logistic_regression():
    model = sklearn.linear_model.LogisticRegression()
    return model

def svm_svc(**params):
    model = sklearn.svm.SVC(**params["parameters"])
    return model

def gaussian_naive_bayes(**params):
    model = sklearn.sklearn.naive_bayes.GaussianNB(**params["parameters"])
    return model

def multinomial_naive_bayes(**params):
    model = sklearn.naive_bayes.MultinomialNB(**params["parameters"])
    return model

def st_gradient_descent(**params):
    model = sklearn.linear_model.SGDClassifier(**params["parameters"])
    return model

def knn(**params):
    model = sklearn.neighbors.KNeighborsClassifier(**params["parameters"])
    return model

def decision_tree(**params):
    model = sklearn.tree.DecisionTreeClassifier(**params["parameters"])
    return model

def random_forest(**params):
    model = sklearn.ensemble.RandomForestClassifier(**params["parameters"])
    return model

def gradient_boosting(**params):
    model = sklearn.ensemble.GradientBoostingClassifier(**params["parameters"])
    return model

# def lgbm(**params):
#     model = lgb.LGBMClassifier(**params["parameters"])
#     return model

def xgboost(**params):
    model = xgb.XGBClassifier(**params["parameters"])
    return model

#Regression

def linear_regression(**params):
    model = sklearn.linear_model.LinearRegression(**params["parameters"])
    return model

def lgbm_reg(**params):
    model = lgb.LGBMRegressor(**params["parameters"])
    return model

def xgboost_reg(**params):
    model = xgb.XGBRegressor(**params["parameters"])
    return model

def catboost_reg(**params):
    model = cb.CatBoostRegressor(**params["parameters"])
    return model

def st_gradient_descent_reg(**params):
    model = sklearn.linear_model.SGDRegressor(**params["parameters"])
    return model

def kernel_ridge_reg(**params):
    model = sklearn.kernel_ridge.KernelRidge(**params["parameters"])
    return model

def elastic_net_reg(**params):
    model = sklearn.linear_model.ElasticNet(**params["parameters"])
    return model

def bayesian_ridge_reg(**params):
    model = sklearn.linear_model.BayesianRidge(**params["parameters"])
    return model

def gradient_boosting_reg(**params):
    model = sklearn.ensemble.GradientBoostingRegressor(**params["parameters"])
    return model

def svm_svr(**params):
    model = sklearn.svm.SVR(**params["parameters"])
    return model

#Clustering

def mean_shift(**params):
    model = sklearn.cluster.MeanShift(**params["parameters"])
    return model

def kmeans(**params):
    model = sklearn.cluster.KMeans(**params["parameters"])
    return model

def agglomerative(**params):
    model = sklearn.cluster.AgglomerativeClustering(**params["parameters"])
    return model

def birch(**params):
    model = sklearn.cluster.birch(**params["parameters"])
    return model

def spectral(**params):
    model = sklearn.cluster.SpectralClustering(**params["parameters"])
    return model

def affinity_propogation(**params):
    model = sklearn.cluster.AffinityPropagation(**params["parameters"])
    return model

def optics(**params):
    model = sklearn.cluster.OPTICS(**params["parameters"])
    return model

def dbscan(**params):
    model = sklearn.cluster.DBSCAN(**params["parameters"])
    return model

