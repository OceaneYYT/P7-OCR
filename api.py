# Library imports
from fastapi import FastAPI
import pandas as pd
import pickle
import shap

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
def test_client_id(client_id: int):
    """
    Customer search in the database
    :param: client_id (int)
    :return: message (string).
    """
    if client_id in list(data['SK_ID_CURR']):
        return {'error': 'Client ID not found'}
    else:
        return {'valid': 'Client ID is valid'}

