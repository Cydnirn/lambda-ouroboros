# inference.py
import joblib
import os
import json
import pandas as pd
from io import StringIO

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def input_fn(request_body, request_content_type):
    print("RequestBody", request_body)
    try:
        data = pd.read_json(StringIO(request_body), typ="dictionary")
        if isinstance(data, pd.Series):
            data = data.to_frame().T
            data = pd.get_dummies(data, columns=["location"])
            data.head()
            return data
    except ValueError as e:
        print("Error in parsing JSON:", e)
        raise ValueError("Error in parsing JSON: {}".format(e))


def predict_fn(input_data, model):
    predictions = model.predict(input_data)
    return predictions

def output_fn(prediction, content_type):
    return str(prediction)