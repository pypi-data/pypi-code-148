from common.np import *
from common.util_gpu import create_contexts_target, to_cpu, to_gpu
from sklearn.metrics import confusion_matrix, precision_score, recall_score, matthews_corrcoef, accuracy_score
import matplotlib.pyplot as plt
import math
import time
import os

class metrics_cal:
    def __init__(self):
        self.accuracy_arr=np.empty((0,1))
        self.confusion_arr=np.empty((2,2))
        self.precision_arr=np.empty((0,1))
        self.recall_arr=np.empty((0,1))
        self.mcc_arr=np.empty((0,1))
        self.sensitivity_arr=np.empty((0,1))
        self.specificity_arr=np.empty((0,1))        
        
        self.accuracy_avg=0.0
        self.confusion_avg=0.0
        self.precision_avg=0.0
        self.recall_avg=0.0
        self.mcc_avg=0.0
        self.sensitivity_avg=0.0
        self.specificity_avg=0.0
    
    def metrics_num(self, pre, ta, num_classes):
        for i in range(num_classes):
            predic = to_cpu(np.array((pre ==i )))
            tag = to_cpu(np.array((ta ==i)))
            tn, fp, fn, tp = confusion_matrix(tag, predic).ravel()
            specificity = tn/(tn+fp)
            sensitivity = tp / (tp+fn)
            accuracy = accuracy_score(tag, predic)
            confusion = confusion_matrix(tag, predic)
            precision = precision_score(tag, predic)
            recall = recall_score(tag, predic)
            mcc = matthews_corrcoef(tag, predic)
            self.accuracy_arr= np.vstack([self.accuracy_arr,accuracy])
            self.confusion_arr= np.vstack((self.confusion_arr, confusion))
            self.precision_arr = np.vstack((self.precision_arr, precision))
            self.recall_arr = np.vstack((self.recall_arr, recall))
            self.mcc_arr = np.vstack((self.mcc_arr, mcc))
            self.sensitivity_arr = np.vstack((self.sensitivity_arr, sensitivity))
            self.specificity_arr = np.vstack((self.specificity_arr, specificity))
            self.accuracy_avg=self.accuracy_arr.sum() / len(self.accuracy_arr)
            self.confusion_avg=self.confusion_arr.sum() / len(self.confusion_arr)
            self.precision_avg=self.precision_arr.sum() / len(self.precision_arr)
            self.recall_avg=self.recall_arr.sum() / len(self.recall_arr)
            self.mcc_avg=self.mcc_arr.sum() / len(self.mcc_arr)      
            self.sensitivity_avg = self.sensitivity_arr.sum() / len(self.sensitivity_arr)
            self.specificity_avg = self.specificity_arr.sum() / len(self.specificity_arr)            
#        return accuracy_arr, confusion_arr,precision_arr, recall_arr, mmc_arr
           
    def metrics_plot(self, pre, ta, title, epoch, mkdir_):
        pre = to_cpu(pre)
        ta = to_cpu(ta)
        confusion = confusion_matrix(ta, pre)
        rows = confusion.sum(axis=1, keepdims=True)
        norm = confusion / rows
        np.fill_diagonal(norm, 0)
        plt.matshow(norm, cmap='Reds')
        plt.ylabel('Actual Data')
        plt.xlabel('Prediction')
        title = title+' epoch '+ str(epoch)
        plt.title(title)
        now = time.localtime()
        s = mkdir_#'%04d-%02d-%02d %02d:%02d' %(now.tm_year, now.tm_mon, now.tm_mday,now.tm_hour,now.tm_min)
        if not os.path.isdir(s):
            os.mkdir(s)
        plt.savefig(s+'/'+title+'.png',format='png')