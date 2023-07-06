from fastapi import status
import requests
import json

API_URL = "http://127.0.0.1:8000/"


def test_welcome():
    response = requests.get(API_URL)
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == 'Welcome to the API'


def test_check_client_id():
    url = API_URL + str(192535)
    response = requests.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == True


def test_check_client_id_2():
    url = API_URL + str(100000)
    response = requests.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == False


def test_get_prediction():
    url = API_URL + "prediction/" + str(192535)
    response = requests.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == 0.4805479971101088