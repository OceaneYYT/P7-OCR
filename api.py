# Library imports
from fastapi import FastAPI
import pandas as pd
import pickle
import uvicorn
import shap
import json

# Create a FastAPI instance
app = FastAPI()

# Loading the model and data
model = pickle.load(open('model.pkl', 'rb'))
data = pd.read_csv('test_df_sample.csv')


# Functions
@app.get('/')
def welcome():
    """
    Welcome message.
    :param: None
    :return: Message (string).
    """
    return 'Welcome to the API'


@app.get('/{client_id}')
def check_client_id(client_id: int):
    """
    Customer search in the database
    :param: client_id (int)
    :return: message (string).
    """
    if client_id in list(data['SK_ID_CURR']):
        return 'Client ID is valid'
    else:
        return 'Client ID not found'


@app.get('/prediction/{client_id}')
def get_prediction(client_id: int):
    """
    Calculates the probability of default for a client.
    :param: client_id (int)
    :return: probability of default (dict).
    """
    client_data = data[data['SK_ID_CURR'] == client_id]
    features = client_data.drop('SK_ID_CURR', axis=1)
    prediction = model.predict_proba(features)
    return {'prediction': prediction.tolist()}


@app.get('/shap/')
def shap_values():
    """
    Calculates shap values
    :param: client_id (int)
    :return: explainer et shap values
    """
    explainer = shap.TreeExplainer(model['classifier'])
    shap_val = explainer.shap_values(data.drop('SK_ID_CURR', axis=1))
    print(shap_val)
    return {'explainer': explainer, 'shap_values': shap_val}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
