# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 11:00:35 2022

@author: chinn
"""
import numpy as np
from sklearn.model_selection import train_test_split, KFold

from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, recall_score, f1_score, confusion_matrix

from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist

from sklearn.cross_decomposition import PLSRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import LinearSVC, SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import GridSearchCV, cross_val_predict

import matplotlib.pyplot as plt


class nirData():
    def __init__(self, X, y, trainIdx=None, testIdx=None):
        self.X = X
        self.y = y
        self.trainIdx = trainIdx
        self.testIdx = testIdx

    def get_train_test_Data(self):
        if self.trainIdx == None or self.testIdx == None:
            sampleSplit_random()
        return (self.X[self.trainIdx,:],self.y[self.trainIdx,:],
                self.X[self.testIdx,:],self.y[self.testIdx,:])



class classification():
    def __init__(self, X, y, method = None, **kwargs):
        self.X = X
        self.y = y
        self.method = method


    def train(self):
        pass

    def predict():
        pass

class regression():
    def __init__(self, X, y, method = None, **kwargs):
        self.X = X
        self.y = y
        self.method = method


    def train(self):
        pass

    def predict():
        pass


class pls:
    def __init__(self, nComp = 2):
        self.nComp = nComp

    def fit(self, X, y):
        self.X = X
        self.y = y
        meanX = np.mean(X,axis = 0)
        meany = np.mean(y)
        Xcentered = X - meanX
        ycentered = y - meany
        model = simpls(Xcentered, ycentered, self.nComp)
        meanX_hat = -1 * np.dot(meanX, model['B']) + meany
        model['B'] = np.append(meanX_hat[np.newaxis,:], model['B'],axis=0)
        self.model = model
        return self

    def predict(self, Xnew, nComp = None):
        if nComp is None:
            B = self.model['B'][:,-1]
        else:
            B = self.model['B'][:, nComp-1]
        if Xnew.shape[1] != B.shape[0]-1:
            raise ValueError('The feature number of predictor is isconsistent with that of indepnentent.')
        Xnew = np.append(np.ones([Xnew.shape[0],1]), Xnew, axis=1)
        ynew_hat = np.dot(Xnew,B)
        return ynew_hat

    def crossValidation_predict(self, nfold = 10):
        X = self.X
        y = self.y
        yhat = np.zeros((y.shape[0],self.nComp))
        model = pls(nComp = self.nComp)
        for train, test in KFold(n_splits=nfold).split(X):
            model.fit(X[train,:], y[train])
            yhat[test,:] = model.predict(X[test,:],np.arange(self.nComp)+1)
        return yhat

    def get_optLV(self, nfold = 10):
        yhat_cv = self.crossValidation_predict(nfold)
        rmsecv = []
        r2cv = []
        for i in range(yhat_cv.shape[1]):
            reportcv = regresssionReport(self.y, yhat_cv[:,i])
            rmsecv.append(reportcv["rmse"])
            r2cv.append(reportcv["r2"])
        optLV = int(np.argmin(rmsecv)+1)
        self.optLV = optLV
        return optLV

    def transform(self, Xnew):
        meanX = np.mean(self.X, axis = 0)
        Xnew_c = Xnew - meanX
        Tnew = np.dot(Xnew_c,self.model['x_weights'])
        return Tnew

    def calc_VIP(self, nComp = None):
        if nComp==None:
            nComp=self.model['B'].shape[1]
        b = self.model['B'][1:,nComp-1]
        T = self.model['x_scores']
        W = self.model['x_weights']
        up=0
        low=0
        for i in range(T.shape[1]):
            up += b**2 * np.dot(T[:,i],T[:,i]) * ((W[:,i])/np.linalg.norm(W[:,i]))**2
            low += b**2 * np.dot(T[:,i],T[:,i])
        VIP = np.sqrt(len(b)*up/low)
        return VIP

    def plot_prediction(self, y, yhat, xlabel = "Reference", ylabel = "Prediction", title = "", ax = None):
        report = regresssionReport(y,yhat)
        if ax == None:
            fig, ax = plt.subplots()
        ax.plot([np.min(y)*0.95,np.max(y)*1.05],[np.min(y)*0.95,np.max(y)*1.05],
                color = 'black',label = "y=x")
        ax.scatter(y, yhat,color = 'tab:green', marker='*', label ='Prediction')
        ax.text(0.7, 0.03,
                "RMSEP = {:.4f}\nR$^2$ = {:.2}".format(report["rmse"],report["r2"]),
                transform = ax.transAxes)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0))
        ax.set_title(title)


class plsda(PLSRegression):
    def __init__(self, n_components=2, scale=True, **kwargs):
        super().__init__(n_components=n_components, scale=scale, **kwargs)
        self.lda = LinearDiscriminantAnalysis()

    def fit(self, X, y):
        self.X = X
        self.y = y
        super().fit(X, y)
        self.lda.fit(self.x_scores_, y)
        return self

    def predict(self, X):
        return self.lda.predict(self.transform(X))

    def predict_log_proba(self, X):
        return self.lda.predict_log_proba(self.predict(X))

    def predict_proba(self, X):
        return self.lda.predict_proba(self.predict(X))

    def crossValidation_predict(self, nfold = 10):
        X = self.X
        y = self.y
        yhat = np.zeros((y.shape[0],self.n_components))
        for i in range(self.n_components):
            model = plsda(n_components = i+1)
            for train, test in KFold(n_splits=nfold).split(X):
                model.fit(X[train,:], y[train])
                yhat[test,i] = model.predict(X[test,:])
        return yhat

    def get_optLV(self, nfold = 10):
        yhat_cv = self.crossValidation_predict(nfold)
        accuracy_cv = []
        for i in range(yhat_cv.shape[1]):
            if len(self.lda.classes_) == 2 :
                report_cv = binaryClassificationReport(self.y, yhat_cv[:,i])
                accuracy_cv.append(report_cv["accuracy"])
            elif len(self.lda.classes_) > 2:
                report_cv = multiClassificationReport(self.y, yhat_cv[:,i])
                accuracy_tmp = [rep["accuracy"] for rep in report_cv.values()]
                accuracy_cv.append(sum(accuracy_tmp))

        optLV = int(np.argmax(accuracy_cv)+1)
        self.optLV = optLV
        return optLV

    def get_confusion_matrix(self, X, y):
        yhat = self.predict(X)
        cm = confusion_matrix(y, yhat)
        return cm

    def get_vip(self):
        t = self.x_scores_ / self.x_scores_.std(axis=0)
        s = np.sum(t**2, axis=1)
        s /= np.sum(t**2)
        vip = s * np.sum(t**2, axis=1)
        return vip

    def permutation_test(self, X, y, n_repeats=100,n_jobs = None):
        # Initialize arrays to store Q2 and R2 values
        q2 = np.zeros(n_repeats)
        r2 = np.zeros(n_repeats)
        permutation_ratio = np.zeros(n_repeats)
        # Perform the permutation test
        for i in range(n_repeats):
            # Shuffle the target variable
            y_shuffled = np.random.permutation(y)

            # Fit the model to the shuffled target variable
            self.fit(X, y_shuffled)

            # Calculate the cross-validated Q2 and R2 values
            y_pred = cross_val_predict(self, X, y_shuffled, cv=10, n_jobs = n_jobs)
            q2[i] = self.score(X, y_shuffled)
            r2[i] = r2_score(y_shuffled, y_pred)
            permutation_ratio[i] = np.sum(y_shuffled != y) / len(y)
        return q2, r2, permutation_ratio

class lsvc(LinearSVC):# linear svc
    def get_optParams(self, X, y, Params = None, nfold = 10, n_jobs = None):
        if Params is None:
            Params = {'C': np.logspace(-4, 5, 10),
                      'penalty': ('l1', 'l2')}
        self.gsh = GridSearchCV(estimator=self,  param_grid=Params,
                           cv = nfold, n_jobs = n_jobs)
        self.gsh.fit(X, y)
        return self.gsh.best_params_

    def get_confusion_matrix(self, X, y):
        yhat = self.predict(X)
        cm = confusion_matrix(y, yhat)
        return cm

class svc(SVC):# linear svc
    def get_optParams(self, X, y, Params = None, nfold = 10, n_jobs = None):
        if Params is None:
            Params = {'C': np.logspace(-4, 5, 10),
                      'gamma':np.logspace(-4, 5, 10),
                      'kernel': ('poly', 'rbf', 'sigmoid')}
        self.gsh = GridSearchCV(estimator=self,  param_grid=Params,
                           cv = nfold, n_jobs = n_jobs)
        self.gsh.fit(X, y)
        return self.gsh.best_params_

    def get_confusion_matrix(self, X, y):
        yhat = self.predict(X)
        cm = confusion_matrix(y, yhat)
        return cm

class rf(RandomForestClassifier):
    def get_optParams(self, X, y, Params = None, nfold = 10, n_jobs = None):
        if Params is None:
            Params = {'n_estimators': np.arange(100)+1,
                      'max_depth': np.arange(3)+1}
        self.gsh = GridSearchCV(estimator=self,  param_grid=Params,
                           cv = nfold, n_jobs = n_jobs)
        self.gsh.fit(X, y)
        return self.gsh.best_params_

    def get_confusion_matrix(self, X, y):
        yhat = self.predict(X)
        cm = confusion_matrix(y, yhat)
        return cm


class multiClass_to_binaryMatrix():
    def __init__(self):
        pass

    def fit(self, x):
        self.classes = np.unique(x)
        return self

    def transform(self, x):
        Xnew = np.zeros((len(x),len(self.classes)), dtype=int)
        if len(self.classes) > 2 :
            for i, classi in enumerate(self.classes):
                Xnew[:,i] = x==classi
        return Xnew

    def reTransform(self, xnew):
        x = [np.classes(np.where(xnew[i,:])) for i in range(xnew.shape[0])]
        return x

def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """

    accuracy = np.trace(cm) / np.sum(cm).astype('float')
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            if normalize:
                plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                         horizontalalignment="center",
                         color="white" if cm[i, j] > thresh else "black")
            else:
                plt.text(j, i, "{:,}".format(cm[i, j]),
                         horizontalalignment="center",
                         color="white" if cm[i, j] > thresh else "black")


    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()

def multiClassificationReport(ytrue,ypred):
    labels = np.unique(ytrue)
    report = dict()
    for labeli in labels:
        report[labeli] = binaryClassificationReport(ytrue = ytrue == labeli, ypred = ypred == labeli)
    return report

def binaryClassificationReport(ytrue,ypred):
    if len(np.unique(ytrue))>2:
        raise("Use the multiClassificationReport function for multiple classification.")
    else:
        tn, fp, fn, tp = confusion_matrix(ytrue,ypred).ravel()
        report = dict()
        report["accuracy"] = accuracy_score(ytrue, ypred)
        report["sensitivity"] = recall_score(ytrue, ypred)#recall
        report["specificity"] = tn/(tn+fp)
        report["f1"] = f1_score(ytrue, ypred)
        return report

def regresssionReport(ytrue,ypred):
    report = dict()
    report["rmse"] = mean_squared_error(ytrue, ypred, squared=False)
    report["r2"] =  r2_score(ytrue, ypred)
    return report

def simpls(X, y, nComp):
    '''
    Partial Least Squares, SIMPLS
    Ref https://github.com/freesiemens/SpectralMultivariateCalibration/blob/master/pypls.py
    :param X:
    :param y:
    :param nComp:
    :return:
    '''
    n_samples, n_variables = X.shape
    if np.ndim(y) == 1:
        y = y[:, np.newaxis]
    if n_samples != y.shape[0]:
        raise ValueError('The number of independent and dependent variable are inconsistent')

    nComp = np.min((nComp, n_samples, n_variables))
    V = np.zeros((n_variables, nComp))
    x_scores = np.zeros((n_samples, nComp))  # X scores (standardized)
    x_weights = np.zeros((n_variables, nComp))  # X weights
    x_loadings = np.zeros((n_variables, nComp))  # X loadings
    y_loadings = np.zeros((1, nComp))  # Y loadings
    y_scores = np.zeros((n_samples, nComp))  # Y scores
    s = np.dot(X.T, y).ravel()  # cross-product matrix between the X and y_data
    for i in range(nComp):
        r = s
        t = np.dot(X, r)
        tt = np.linalg.norm(t)
        t = t / tt
        r = r / tt
        p = np.dot(X.T, t)
        q = np.dot(y.T, t)
        u = np.dot(y, q)
        v = p  # P的正交基
        if i > 0:
            v = v - np.dot(V, np.dot(V.T, p))  # Gram-Schimidt orthogonal
            u = u - np.dot(x_scores, np.dot(x_scores.T, u))
        v = v / np.linalg.norm(v)
        s = s - np.dot(v, np.dot(v.T, s))
        x_weights[:, i] = r
        x_scores[:, i] = t
        x_loadings[:, i] = p
        y_loadings[:, i] = q
        y_scores[:, i] = u
        V[:, i] = v
    B = np.cumsum(np.dot(x_weights, np.diag(y_loadings.ravel())), axis=1)
    return {'B': B, 'x_scores': x_scores, 'x_loadings': x_loadings, 'y_loadings': y_loadings, \
            'x_scores_weights': x_weights, 'x_weights': x_weights, 'y_scores':y_scores}



def sampleSplit_random(X,test_size=0.25, random_state=1, shuffle=False):
    sampleIdx = np.arange(X.shape[0])
    trainIdx, testIdx = train_test_split(sampleIdx,test_size=test_size,
                                         random_state=random_state,
                                         shuffle=shuffle)
    return trainIdx, testIdx

def sampleSplit_KS(X, test_size=0.25, metric='euclidean', *args, **kwargs):
    """Kennard Stone Sample Split method
    Parameters
    ----------
    spectra: ndarray, shape of i x j
        i spectrums and j variables (wavelength/wavenumber/ramam shift and so on)
    test_size : float, int
        if float, then round(i x (1-test_size)) spectrums are selected as test data, by default 0.25
        if int, then test_size is directly used as test data size
    metric : str, optional
        The distance metric to use, by default 'euclidean'
        See scipy.spatial.distance.cdist for more infomation
    Returns
    -------
    select_pts: list
        index of selected spetrums as train data, index is zero based
    remaining_pts: list
        index of remaining spectrums as test data, index is zero based
    References
    --------
    Kennard, R. W., & Stone, L. A. (1969). Computer aided design of experiments.
    Technometrics, 11(1), 137-148. (https://www.jstor.org/stable/1266770)
    """
    Xscore = PCA(n_components=2).fit_transform(X)
    distance = cdist(Xscore, Xscore, metric=metric, *args, **kwargs)
    select_pts = []
    remaining_pts = [x for x in range(distance.shape[0])]

    # first select 2 farthest points
    first_2pts = np.unravel_index(np.argmax(distance), distance.shape)
    select_pts.append(first_2pts[0])
    select_pts.append(first_2pts[1])

    # remove the first 2 points from the remaining list
    remaining_pts.remove(first_2pts[0])
    remaining_pts.remove(first_2pts[1])

    for i in range(round(X.shape[0]*(1-test_size)) - 2):
        # find the maximum minimum distance
        select_distance = distance[select_pts, :]
        min_distance = select_distance[:, remaining_pts]
        min_distance = np.min(min_distance, axis=0)
        max_min_distance = np.max(min_distance)

        # select the first point (in case that several distances are the same, choose the first one)
        points = np.argwhere(select_distance == max_min_distance)[:, 1].tolist()
        for point in points:
            if point in select_pts:
                pass
            else:
                select_pts.append(point)
                remaining_pts.remove(point)
                break
    return select_pts, remaining_pts
