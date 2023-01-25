import itertools
import matplotlib.pyplot as plt
import numpy as np
import sklearn.metrics as metrics

def roc(preds, ground, metric):
    fpr, tpr, threshold = metrics.roc_curve(ground, preds)
    roc_auc = metrics.auc(fpr, tpr)
    plt.title('Receiver Operating Characteristic ({})'.format(metric));
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc);
    plt.legend(loc = 'lower right');
    plt.plot([0, 1], [0, 1],'r--');
    plt.xlim([0, 1]);
    plt.ylim([0, 1]);
    plt.ylabel('True Positive Rate');
    plt.xlabel('False Positive Rate');
    plt.show();
    return fpr, tpr, threshold


def pr(preds, ground, metric):
    precision, recall, threshold = metrics.precision_recall_curve(ground, preds)
    average_precision = metrics.average_precision_score(ground, preds)
    plt.step(recall, precision, color='b', alpha=0.2, where='post')
    plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall ({}) AP: {:.3f}'.format(metric, average_precision))
    plt.show();
    return precision, recall, threshold


def best_threshold(precisions, recalls, thresholds):
    thresh = 0.0
    best_f1 = 0.0
    thresh_prec = 0.0
    thresh_rec = 0.0
    for p, r, t in zip(precisions, recalls, thresholds):       
        f1 = 2*(p*r)/(p+r)
        if f1 > best_f1:
            best_f1 = f1
            thresh_prec = p
            thresh_rec = r
            thresh = t

    print ("F1: ", best_f1)
    print ("Precision: ", thresh_prec)
    print ("Recall: ", thresh_rec)
    return thresh


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
