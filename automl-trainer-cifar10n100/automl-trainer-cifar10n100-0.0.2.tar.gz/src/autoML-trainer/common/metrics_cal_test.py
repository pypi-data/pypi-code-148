from common.np import *
from util_gpu import create_contexts_target, to_cpu, to_gpu
from sklearn.metrics import confusion_matrix, precision_score, recall_score, matthews_corrcoef, accuracy_score
import matplotlib.pyplot as plt

class metrics_cal:
    def __init__(self):
        self.accuracy_arr=np.empty((0,1))
        self.confusion_arr=np.empty((2,2))
        self.precision_arr=np.empty((0,1))
        self.recall_arr=np.empty((0,1))
        self.mmc_arr=np.empty((0,1))
        self.accuracy_avg=0.0
        self.confusion_avg=0.0
        self.precision_avg=0.0
        self.recall_avg=0.0
        self.mmc_avg=0.0       
        
    
    def metrics_num(self, pre, ta):
        
        for i in range(10):
            predic = to_cpu(np.array((pre ==i )))
            tag = to_cpu(np.array((ta ==i)))
            tn, fp, fn, tp = confusion_matrix(tag, predic)
            specificity = tn/(tn+fp)
            preci_ = tp /(tp+fp)
            accuracy = accuracy_score(tag, predic)
            confusion = confusion_matrix(tag, predic)
            precision = precision_score(tag, predic)
            recall = recall_score(tag, predic)
            mmc = matthews_corrcoef(tag, predic)
            self.accuracy_arr= np.vstack([accuracy_arr,accuracy])
            self.confusion_arr= np.vstack((confusion_arr, confusion))
            self.precision_arr = np.vstack((precision_arr, precision))
            self.recall_arr = np.vstack((recall_arr, recall))
            self.mmc_arr = np.vstack((mmc_arr, mmc))
            self.accuracy_avg=self.accuracy_arr.sum() / len(accuracy_arr)
            self.confusion_avg=0.0
            self.precision_avg=0.0
            self.recall_avg=0.0
            self.mmc_avg=0.0             
#        return accuracy_arr, confusion_arr,precision_arr, recall_arr, mmc_arr
           
    def metrics_plot(self, pre, ta):
        pre = to_cpu(pre)
        ta = to_cpu(ta)
        confusion = confusion_matrix(ta, pre)
        rows = confusion.sum(axis=1, keepdims=True)
        norm = confusion / rows
        np.fill_diagonal(norm, 0)
        plt.matshow(norm, cmap='Reds')
        plt.show()