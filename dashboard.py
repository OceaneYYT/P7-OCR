# Dash URL : http://localhost:8501

import streamlit as st
from PIL import Image
import shap
import requests
import json
import pandas as pd
import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# local
API_URL = "http://127.0.0.1:8000/"
# deployment cloud
# API_URL =

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
    id_client = st.text_input("Sélectionnez un numéro de client:", value="192535")
    st.caption("Exemple de client prédit négatif (non defaut) : 192535")
    st.caption("Exemple de client prédit positif (en defaut) : 162820")


    st.markdown("""---""")
    st.write("Created by Océane Youyoutte")