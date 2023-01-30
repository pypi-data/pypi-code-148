from flask import Flask
import load_model
import main
import pandas as pd
import time
import config

app = Flask(__name__)
flag = False


@app.route('/loadModel/')
def loadModel():
    load_model.load_model()
    main.predict("x could be null")
    return "Model Loaded"


@app.route('/getPrediction/<string:sentences>/')
def getSentences(sentences):
    start_time = time.time()
    try:
        result = main.predict(sentences)
    except:
        load_model.load_model()
        result = main.predict(sentences)
    running_time = "%s seconds :" % (time.time() - start_time)
    return {"sentences:": sentences, "Usecase:": result, "execution_time": running_time}



@app.route('/train/')
def train():
    main.controller(1)
    df = pd.read_csv(config.training_csv_path)
    main.trainModel(df)


@app.route('/test/')
def createData():
    main.controller(1)
    return "test completed"


app.debug = False
app.run()
