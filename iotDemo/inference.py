# inference.py
import joblib
import os
import pandas as pd

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        input_data = pd.read_json(request_body)
        return input_data
    raise ValueError("Unsupported content type: {}".format(request_content_type))

def predict_fn(input_data, model):
    predictions = model.predict(input_data)
    return predictions

def output_fn(prediction, content_type):
    return str(prediction)
