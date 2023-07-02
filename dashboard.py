# Dash URL : http://localhost:8501

import streamlit as st
from PIL import Image
import shap
import requests
import time
# from urllib.parse import urljoin
import json
import pandas as pd
import numpy as np
# import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# local
API_URL = "http://127.0.0.1:8000/"
# deployment cloud
# API_URL =

# Chargement des dataset
data_train = pd.read_csv('train_df_sample.csv')
data_test = pd.read_csv('test_df_sample.csv')

# Fonctions


def get_prediction(id: int):
    """Récupère la probabilité de défaut du client via l'API.
    :param: id_client (int).
    :return: probabilité de défaut (float) et la décision (str)
    """
    url_get_pred = API_URL + "prediction/" + str(id_client_dash)
    response = requests.get(url_get_pred)
    proba_default = round(float(response.content), 3)
    best_threshold = 0.54
    if proba_default >= best_threshold:
        decision = "Refusé "
    else:
        decision = "Accordé"

    return proba_default, decision


def jauge_score(proba):
    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=proba * 100,
        mode="gauge+number+delta",
        title={'text': "Jauge de score"},
        delta={'reference': 54},
        gauge={'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "black"},
               'bar': {'color': "MidnightBlue"},
               'steps': [
                   {'range': [0, 20], 'color': "Green"},
                   {'range': [20, 45], 'color': "LimeGreen"},
                   {'range': [45, 54], 'color': "Orange"},
                   {'range': [54, 100], 'color': "Red"}],
               'threshold': {'line': {'color': "brown", 'width': 4}, 'thickness': 1, 'value': 54}}))

    st.plotly_chart(fig)


# Titre de la page
st.set_page_config(page_title="Dashboard Prêt à dépenser", layout="wide")

# Sidebar
with st.sidebar:
    logo = Image.open('img/logo pret à dépenser.png')
    st.image(logo, width=200)
    # Page selection
    page = st.selectbox('Navigation', ["Home", "Information du client", "Interprétation locale",
                                               "Interprétation globale"])

    # ID Selection
    st.markdown("""---""")
    # id_client_dash = int(st.text_input("Sélectionnez un numéro de client:", value="192535"))
    # st.caption("Exemple de client prédit négatif (non defaut) : 192535")
    # st.caption("Exemple de client prédit positif (en defaut) : 420554")

    # if st.button("Entrer"):
        # Vérifie si l'ID client est valide
        # url_check_id = urljoin(API_URL, "id_client={id_client_dash}")
        # Requesting l'API et enregistre la reponse
        # response = requests.get(url_check_id)
                                #, data=id_client_dash)
        # st.write(response.content)
        # if response.content == True:
            # st.success("ID client valide")
            # id_correct = True
        # else:
            # st.error("ID client incorrect")
            # id_correct = False

    list_id_client = list(data_test['SK_ID_CURR'])
    list_id_client.insert(0, '<Select>')
    id_client_dash = st.selectbox("ID Client", list_id_client)

    st.markdown("""---""")
    st.write("Created by Océane Youyoutte")

if page == "Home":
    st.title("Dashboard Prêt à dépenser - Home Page")
    st.markdown("Ce site contient un dashboard interactif permettant d'expliquer aux clients les raisons\n"
                "d'approbation ou refus de leur demande de crédit.\n"
                
                "\nLes prédictions sont calculées à partir d'un algorithme d'apprentissage automatique, "
                "préalablement entraîné. Il s'agit d'un modèle *Light GBM* (Light Gradient Boosting Machine). "
                "Les données utilisées sont disponibles [ici](https://www.kaggle.com/c/home-credit-default-risk/data). "
                "Lors du déploiement, un sample de ces données a été utilisé.\n"
                
                "\nLe dashboard est composé de plusieurs pages :\n"
                "- **Information du client**: Vous pouvez y retrouver toutes les informations relatives au client"
                "selectionné dans la colonne de gauche, ainsi que le résultat de sa demande de crédit."
                "Je vous invite à accéder à cette page afin de commencer.\n"
                "- **Interprétation locale**: Vous pouvez y retrouver quelles caractéritiques du client ont le plus"
                "influençé le choix d'approbation ou refus de la demande de crédit.\n"
                "- **Intérprétation globale**: Vous pouvez y retrouver notamment des comparaisons du client avec"
                "les autres clients de la base de données.")


if page == "Information du client":
    st.write("Cliquez sur le bouton ci-dessous pour commencer l'analyse de la demande :")
    button_start = st.button("Statut de la demande")
    if button_start:
        if id_client_dash != '<Select>':
            # Calcul des prédictions et affichage des résultats
            st.markdown("RÉSULTAT DE LA DEMANDE")
            probability, decision = get_prediction(id_client_dash)

            if decision == 'Accordé':
                st.success("Crédit accordé")
            else:
                st.error("Crédit refusé")

            # Affichage de la jauge
            jauge_score(probability)

    # Affichage des informations client
    infos_client = st.checkbox("Afficher les informations du client")
    if infos_client:
        st.info("Voici les informations du client:")
        st.write(pd.DataFrame(data_test.loc[data_test['SK_ID_CURR'] == id_client_dash]))


