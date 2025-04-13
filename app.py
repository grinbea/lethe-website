import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np
#
#import sys
#sys.path.append('/bigd/code/ncspardo/proyecto-lethe/Lethe')
#from main import predict
#from model.frequency_modeling import apply_fft

files_dict = {
    "healthy" : 0,
    "narco"   : 1,
    "ins"     : 2,
    "sdb"     : 3,
    "plm"     : 4,
    "rbd"     : 5
}

descrip_dict = {
    0: "You are healthy",
    1: "Narcolepsy",
    2: "Insomny",
    3: "SDB",
    4: "PLM",
    5: "RBD"
}

api_url = 'http://127.0.0.1:8000/predict'

# Title and description
st.header('     ECG Diagnosis     ')
st.title('Predict sleep disorders')

# Input section
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name: ")

with col2:
    age = st.text_input("Age: ")

uploaded_file = st.file_uploader("Choose a file", type=["csv"])

if st.button('Get diagnosis'):
    columns = []
    for c in range(1,1024):
        columns.append("f"+str(c))
    columns.append('Sleep_stages')

    df = pd.read_csv(uploaded_file,names=columns)
    ddf = df.to_dict(orient='records')

    response = requests.post(api_url, json={'data':ddf})
    diagnosis = response.json()
    dg = int(diagnosis['diagnosis'])
    
    st.header(f'Your diagnosis is:  {descrip_dict[dg]}')
