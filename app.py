import streamlit as st
import requests
import os
import sys
import pandas as pd
FRONT_ROOT_DIRECTORY = os.environ.get('FRONT_ROOT_DIRECTORY')
sys.path.append('FRONT_ROOT_DIRECTORY')
from params import *
sys.path.append(BACK_ROOT_DIRECTORY)
from Lethe.main import predict

columns = []
for c in range(1,1025):
    columns.append("f"+str(c))
columns.append('phase')

files_dict = {
    "healthy" : 0,
    "narco"   : 1,
    "plm"     : 2,
    "sdb"     : 3,
    "nfle"    : 4,
    "rbd"     : 5
}


# Title and description
st.title('     EGC Diagnosis     ')
st.title('Predict sleep disorders')

#api_url = /bigd/code/ncspardo/proyecto-lethe/Lethe/main.py

# Input section
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name: ")

with col2:
    age = st.text_input("Age: ")

uploaded_file = st.file_uploader("Choose a file", type=["csv"])

uploaded_file = '/bigd/code/grinbea/lethe-website/test_data/test_bal_healthy.csv'
if st.button('Get diagnosis'):
    test_data = pd.read_csv(uploaded_file, names=columns)
    diagnosis = predict(test_data)
    diag = 0
    for key,value in files_dict.items():
        if diagnosis[0] == value:
            diag = key
    st.header(f'{name} diagnosis is  {diag}')

