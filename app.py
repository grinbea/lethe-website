import streamlit as st
import requests
import os
import sys
FRONT_ROOT_DIRECTORY = os.environ.get('FRONT_ROOT_DIRECTORY')
sys.path.append('FRONT_ROOT_DIRECTORY')
from params import *
sys.path.append(BACK_ROOT_DIRECTORY)
from Lethe.main import predict

# Title and description
st.title('EGC Diagnosis - Predict sleep disorders')

#api_url = /bigd/code/ncspardo/proyecto-lethe/Lethe/main.py

# Input section
col1, col2 = st.columns(2)

with col1:
    st.input("Name: ")

with col2:
    st.input("Age: ")

uploaded_file = st.file_uploader("Choose a file", type=["png"])

if st.button('Get diagnosis'):

    if uploaded_file is not None:
        try:
            with st.spinner('Predicting...'):
                test_data = pd.read_csv(uploaded_file)
                #diagnosis = predict(test_data)
                st.markdown("Your diagnosis is " + diagnosis)
        except:
            st.markdown("No results found.")
    else:
            st.markdown("Upload your file first")

