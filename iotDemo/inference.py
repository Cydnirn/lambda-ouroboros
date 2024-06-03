# inference.py
import joblib
import os
import pandas as pd

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        print("RequestBody", request_body)
        try:
            data = pd.read_json(request_body)
            if isinstance(data, pd.Series):
                data = data.to_frame().T
            print("Input data", data)
            return data
        except ValueError as e:
            print("Error in parsing JSON:", e)
            raise ValueError("Error in parsing JSON: {}".format(e))
    else:
        raise ValueError("Unsupported content type: {}".format(request_content_type))

def predict_fn(input_data, model):
    predictions = model.predict(input_data)
    return predictions

def output_fn(prediction, content_type):
    return str(prediction)
