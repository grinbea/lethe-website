import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np

import sys
sys.path.append('/bigd/code/ncspardo/proyecto-lethe/Lethe')
from main import predict
from model.frequency_modeling import apply_fft

columns = []
for c in range(1,1024):
    columns.append("f"+str(c))
columns.append('Sleep_stages')

files_dict = {
    "healthy" : 0,
    "narco"   : 1,
    "ins"     : 2,
    "sdb"     : 3,
    "rbd"     : 4,
    "plm"     : 5
}

descrip_dict = {
    0: "You are healthy",
    1: "Narcolepsy",
    2: "Insomny",
    3: "SDB",
    4: "RBD",
    5: "PLM"
}

#api_url = 'https://github.com/ncspardo/proyecto-lethe/tree/master/Lethe/predict'
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
    test_data = pd.read_csv(uploaded_file, names=columns)
    #response = requests.get(api_url, params=test_data)
    #diagnosis = response.json()
    diagnosis = predict(test_data)
    max_index = np.argmax(diagnosis)
    
    dg = descrip_dict[max_index]
    st.header(f'Your diagnosis is:  {dg}')
