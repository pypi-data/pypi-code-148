from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, matthews_corrcoef, cohen_kappa_score
from sklearn.model_selection import train_test_split
import sys
import preprocess
import rankTransform
import dropout
import getDEgenes
import xgboost as xgb
from datetime import datetime
import argparse
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run XGBoost on the given dataset')
    parser.add_argument('--train', type=str, default=os.path.join('data', 'train.csv'), help='Path to the training data (in csv format)')
    parser.add_argument('--test', type=str, default=os.path.join('data', 'test.csv'), help='Path to the testing data (in csv format)')
    parser.add_argument('--out', type=str, default=os.path.join('log'), help='Path to the output directory')
    
    parser.add_argument('--experiment', type=str, default='pbmc', help='Experiment name')
    parser.add_argument('--f', type=float, default=0.85, help='Dropout rate to select')
    parser.add_argument('--n_iter', type=int, default=2, help='Number of dropout iterations')
    parser.add_argument('--use_exp_rank', type=bool, default=False, help='Use exponential rank transformation')
    parser.add_argument('--use_de', type=bool, default=True, help='Use DE gene selection')
    parser.add_argument('--de_gene_path', type=str, default=os.path.join('log', 'DEgenes'), help='Path to pickle dump of DE gene selection')
    parser.add_argument('--find_de_after', type=bool, default=False, help='Find DE genes after dropout')
    parser.add_argument('--class_balance', type=int, default=0, help='Use SMOTE for handling class imbalance (1 for yes, 0 for no; defaults to 0)')
    
    ## For reproducability of results
    np.random.seed(0)

    ## Parse the arguments
    args = parser.parse_args()
    experiment = args.experiment
    out = args.out
    train = args.train
    test = args.test
    f = args.f
    n_iter = args.n_iter
    use_exp_rank = args.use_exp_rank
    use_de = args.use_de
    de_gene_path = args.de_gene_path
    de_gene_path = de_gene_path + "_" + experiment +".pkl"
    find_de_after = args.find_de_after
    class_balance = args.class_balance
    
    file_out = open(f'{out}_{experiment}.txt', 'w')
    sys.stdout = file_out
    result_history = {}
    result_history[(f, n_iter)] = {'with_rank': {'val_accuracy':0, 'test_accuracy':0}}

    try:
        train_df = pd.read_csv(train, index_col = 0)
        test_df =  pd.read_csv(test, index_col = 0)
    except:
        print("Error reading the files")
        sys.exit(1)
    print("Starting script on Experiment: {}".format(experiment))
    print("Using dropout rate: {}".format(f))
    print("Using {} iterations of dropout".format(n_iter))
    new_cols = [col for col in test_df.columns if col != 'celltype'] + ['celltype']
    train_df = train_df[new_cols]
    test_df = test_df[new_cols]  
    
    print(train_df.shape, test_df.shape)

    if not find_de_after:
        getDEgenes.save_gene_list(train_df, de_gene_path)

    ## Dropout
    print("starting dropout...")
    non_zero_cols = [col for col in train_df.columns if (train_df[col] == 0).sum() != len(train_df)]
    train_df = train_df[non_zero_cols]
    if n_iter != 0:
        try:
            train_df = pd.read_csv('dropped_out_train_' + str(experiment) + '_f=' + str(f) + '_n_iter=' + str(n_iter) + '.csv', index_col = 'index')
        except:
            train_df = dropout.apply_dropout(train_df.iloc[:,:-1], train_df.celltype, n_iter, f)
            # train_df.to_csv('dropped_out_train_' + str(experiment) + '_f=' + str(f) + '_n_iter=' + str(n_iter) + '.csv')

    if find_de_after:
        getDEgenes.save_gene_list(train_df, de_gene_path)
    
    ## taking common genes
    print("Taking common genes...")
    final_columns = list(set(train_df.columns).intersection(set(test_df.columns)))
    print('Common columns', len(final_columns))
    final_columns = [i for i in final_columns if i != 'celltype'] + ['celltype']
    train_df = train_df[final_columns]
    test_df = test_df[final_columns]

    print("Starting preprocessing...")
    train_dic = preprocess.preprocess(train_df.iloc[:,:-1], train_df.iloc[:,-1:], min_cells=20,min_genes=50)
    test_dic = preprocess.preprocess(test_df.iloc[:,:-1],test_df.iloc[:,-1:], get_hvgs=False, min_cells=0, min_genes=0)

    train_adata = train_dic['data']
    test_data = test_dic['data']
    hvgs = train_dic['hvg']

    print("taking hvgs...")
    test_data = test_data[:, hvgs.index]
    train_df = train_adata.to_df()
    test_df = test_data.to_df()
    train_df['celltype'] = train_adata.obs.celltype.to_list()
    test_df['celltype'] = test_data.obs.celltype.to_list()

    ## Training and testing
    print("starting training...")
    train, val = train_test_split(train_df.sample(frac=1), test_size=0.2)
    train_feats = train.iloc[:,:-1]
    if use_exp_rank:
        train_ranks = rankTransform.rank_transform_exp(train_feats)
    else:
        train_ranks = rankTransform.rank_transform(train_feats)
    if use_de and use_exp_rank:
        train_ranks = rankTransform.rank_transform_de_exp(train_ranks, path = de_gene_path)
    if use_de:
        train_ranks = rankTransform.rank_transform_de(train_ranks, path = de_gene_path)

    val_feats = val.iloc[:,:-1]
    if use_exp_rank:
        val_ranks = rankTransform.rank_transform_exp(val_feats)
    else:
        val_ranks = rankTransform.rank_transform(val_feats)

    if use_de and use_exp_rank:
        val_ranks = rankTransform.rank_transform_de_exp(val_ranks, path = de_gene_path)
    if use_de:
        val_ranks = rankTransform.rank_transform_de(val_ranks, path = de_gene_path)
    X_train, Y_train = train_ranks.to_numpy(), train.celltype.to_list()
    X_val, Y_val = val_ranks.to_numpy(), val.celltype.to_list()

    X_combined = np.vstack((X_train, X_val))
    y_combined = Y_train + Y_val
    
#     oversample = SMOTE()
#     X_train_, Y_train_ = oversample.fit_resample(X_train, Y_train)
    
#     clf = xgb.XGBClassifier(max_depth=3, learning_rate=0.2, n_estimators = 500)
#     clf.fit(X_train_, Y_train_, sample_weight=None)
#     predicted_labels = clf.predict(X_val)

#     print("Results on Validation set")
#     print("MCC:", matthews_corrcoef(Y_val, predicted_labels))
#     print()
#     print("Kappa:", cohen_kappa_score(Y_val, predicted_labels))
#     print()
#     print("Classification Report")
#     print(classification_report(Y_val, predicted_labels))
#     a = classification_report(Y_val, predicted_labels, output_dict = True)
#     result_history[(f, n_iter)]['with_rank']['val_accuracy'] = a['accuracy']

#     print()
    print("Results on Test set")
    
    ## Train final model on the entire data (train + val)
    if class_balance == 1:
        oversample = SMOTE()
        X_combined, y_combined = oversample.fit_resample(X_combined, y_combined)
    print(X_combined[0],y_combined[0],type(X_combined),type(y_combined))
    clf = xgb.XGBClassifier(max_depth=3, learning_rate=0.2, n_estimators = 500)
    clf.fit(X_combined, y_combined, sample_weight=None)

    # parameters = {'n_estimators': [100, 200, 300, 400, 500], 'max_depth': [1, 2, 3, 4],  'grow_policy': ['depthwise', 'lossguide'], 'learning_rate': [0.1, 0.5, 1.0], 'subsample': [0.6, 0.8, 1.0]}
    # xgb_classifier = xgb.XGBClassifier(random_state = 0)
    # clf = GridSearchCV(xgb_classifier, parameters)
    # clf.fit(X_combined, y_combined)
    # print("Grid search parameters:")
    # print(clf)
    # print()
    
    test_feats = test_df.iloc[:,:-1]
    if use_exp_rank:
        test_ranks = rankTransform.rank_transform_exp(test_feats)
    else:
        test_ranks = rankTransform.rank_transform(test_feats)
    if use_de and use_exp_rank:
        test_ranks = rankTransform.rank_transform_de_exp(test_ranks, path = de_gene_path)
    if use_de:
        test_ranks = rankTransform.rank_transform_de(test_ranks, path = de_gene_path)
        
    test_ranks['celltype'] = test_df['celltype'].to_list()
    X_test, Y_test = test_ranks.iloc[:,:-1].to_numpy(), test_ranks.celltype.to_list()
    predicted_labels_test = clf.predict(X_test)
    unique_labels = list(set(list(set(Y_test)) + list(set(predicted_labels_test))))
    unique_labels.sort()
    array = confusion_matrix(Y_test, predicted_labels_test, normalize='true')
    array = array.round(2)
    print("Confusion matrix:")
    print(array)
    print()
    print("MCC:", matthews_corrcoef(Y_test, predicted_labels_test))
    print()
    print("Kappa:", cohen_kappa_score(Y_test, predicted_labels_test))
    print()
    print("Classification Report")
    print(classification_report(Y_test, predicted_labels_test))
    a = classification_report(Y_test, predicted_labels_test, output_dict = True)
    result_history[(f, n_iter)]['with_rank']['test_accuracy'] = a['accuracy']
    
    df_cm = pd.DataFrame(array, index = unique_labels, columns = unique_labels)
    plt.figure(figsize = (10,7))
    sns.heatmap(df_cm, annot=True, cmap="YlGnBu")
    plt.savefig(f'{out}_{datetime.now()}_{experiment}_confusion_matrix.png')
    