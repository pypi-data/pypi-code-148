# -*- coding: utf-8 -*-

import pandas as pd

import load_model as singleton_model
from training_data_creation import create_training_data as createData
from custom_t5_model import CustomT5
from sklearn.model_selection import train_test_split
import os
import time
import config


def trainModel(df):
    custom_model = CustomT5()
    start = time.time()
    df.dropna()
    df = df.rename(columns={"UseCase": "target_text", "Sentences": "source_text"})
    df, unseen_df = train_test_split(df, test_size=0.1)
    df = df[['source_text', 'target_text']]
    train_df, test_df = train_test_split(df, test_size=0.20)
    unseen_df = pd.DataFrame(data=unseen_df)
    try:
        os.mkdir("datasets")
    except OSError as error:
        pass
    unseen_df.to_csv(config.un_seen_data, mode='w', index=False)
    custom_model.from_pretrained(model_type="t5", model_name=config.model_name)
    custom_model.train(train_df=train_df,
                       eval_df=test_df,
                       source_max_token_len=128,
                       target_max_token_len=50,
                       outputdir="outputs/%s" % config.model_name,
                       save_only_last_epoch=True,
                       dataloader_num_workers=4,
                       batch_size=8, max_epochs=5, use_gpu=config.gpu)
    end = time.time()
    execution_time = (end - start) * 10 ** 3 / 1000
    print("Model training completed with %d minutes" % execution_time)


def predict(sentences):
    sentences = sentences.replace(".", "")
    # let's load the trained model for inferencing:
    return singleton_model.model.predict(sentences)[0]


def testAccuracy():
    try:
        os.mkdir("report")
    except OSError as error:
        pass
    unseen_df = pd.read_csv(config.un_seen_data)
    report = pd.DataFrame(
        data={"classifications": [None], "sentence": [None], "Predicted": [None], "Expected": [None], "Result": [None]})
    for ind in unseen_df.index:
        start = time.time()
        sentence = unseen_df['source_text'][ind]
        target = unseen_df['target_text'][ind]
        use_case = predict(sentence)
        end = time.time()
        execution_time = (end - start) * 10 ** 3
        print("The time of execution of above program is :%d ms" % execution_time)
        if use_case.casefold().replace("{", "").replace("}", "") != target.casefold():
            df1 = pd.DataFrame(
                data={"classifications": unseen_df['classifications'][ind], "sentence": [sentence],
                      "Predicted": [use_case], "Expected": [target], "Result": ["Fail"],
                      "execution_time(in ms)": execution_time})
        else:
            df1 = pd.DataFrame(
                data={"classifications": unseen_df['classifications'][ind], "sentence": [sentence],
                      "Predicted": [use_case], "Expected": [target], "Result": ["Pass"],
                      "execution_time(in ms)": execution_time})
        if len(report.dropna()) == 0:
            report = df1
        report = pd.concat([report, df1])
        print(ind, "out of", len(unseen_df), ": ", sentence, target, df1["Result"][0])
    report.to_csv(config.report, mode='w', index=False)


def controller(val=0, sentence=""):
    if val == 0:
        use_case = {"UseCase": predict(sentence)}
        print(use_case)
    elif val == 1:
        createData()
    elif val == 2:
        df = pd.read_csv(config.training_csv_path).dropna()
        list_data = pd.read_csv(config.path_list_data).dropna()
        df.update(list_data)
        trainModel(df)
    elif val == 3:
        testAccuracy()


if __name__ == '__main__':
    """
    controller(sentence="x is null") It means it will run usecase.
    controller(val=1) It means it will create training dataset.
    controller(val=2) It means it will start training with created dataset.
    controller(val=3) It means it will start Testing accuracy with unseen data.   
    Note: Before running 
    controller(sentence="x is null")
    controller(val=3) 
    Have to change trained model path.
    """
    try:
        singleton_model.load_model()
    except:
        print("Model not found")
    sentence = "Input must be from {10;30}."
    # controller(sentence=sentence)
    # controller(1)
    controller(2)
    controller(3)
