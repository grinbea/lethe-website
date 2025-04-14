import streamlit as st
import pandas as pd
import requests
from fpdf import FPDF
import base64
from datetime import datetime
import time

api_url = 'http://127.0.0.1:8000/predict'
#api_url = 'http://proyecto-lethe-1029998951756.europe-west1.run.app'

# Configuración de página
st.set_page_config(
    page_title="NEUROSLEEP PRO",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS estilo CyberPunk
with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
st.markdown("""
    <style>
    </style>
""", unsafe_allow_html=True)

with open("Sleep Neuro PRO (3).png", "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()
st.markdown(
    f"""
    <div style="text-align: right; padding-top: 10px;">
        <img src="data:image/png;base64,{encoded}" width="250">
    </div>
    """,
    unsafe_allow_html=True

# Información detallada para cada diagnóstico
DIAGNOSIS_INFO = {
    "0": {
        "name": "The analysis could not find any irregaularity based on the frequency patterns",
        "description": "The analysis indicates normal sleep architecture without evidence of significant sleep disorders.",
        "key_parameters": {
            "AHI": "<5 events/hour",
            "SpO2 Nadir": ">90%",
            "Arousal Index": "<10/hour"
        },
        "symptoms": [
            "Normal sleep duration",
            "Good sleep quality",
            "Daytime alertness"
        ],
        "recommendations": [
            "Maintain good sleep hygiene",
            "Annual sleep evaluation",
            "Monitor for symptoms"
        ],
        "model_accuracy": 87,
        "confidence": 80
    },
    "1": {
        "name": "Narcolepsy",
        "description": "The analysis suggests characteristics consistent with narcolepsy, a chronic neurological disorder.",
        "key_parameters": {
            "Sleep Latency": "<8 minutes",
            "REM Latency": "<15 minutes",
            "SOREMPs": ">=2 in MSLT"
        },
        "symptoms": [
            "Excessive daytime sleepiness",
            "Sleep attacks",
            "Cataplexy"
        ],
        "recommendations": [
            "Clinical evaluation",
            "Multiple Sleep Latency Test",
            "HLA-DQB1 testing"
        ],
        "model_accuracy": 87,
        "confidence": 80
    },
    "2": {
        "name": "Insomnia",
        "description": "The analysis indicates patterns consistent with chronic insomnia disorder.",
        "key_parameters": {
            "Sleep Efficiency": "<85%",
            "Sleep Latency": ">30 minutes",
            "WASO": ">30 minutes"
        },
        "symptoms": [
            "Difficulty falling asleep",
            "Frequent awakenings",
            "Daytime fatigue"
        ],
        "recommendations": [
            "Cognitive Behavioral Therapy",
            "Sleep diary",
            "Sleep hygiene optimization"
        ],
        "model_accuracy": 87,
        "confidence": 80
    },
    "3": {
        "name": "Sleep Disordered Breathing",
        "description": "The analysis reveals significant respiratory disturbances during sleep.",
        "key_parameters": {
            "AHI": ">=15 events/hour",
            "SpO2 Nadir": "<90%",
            "Arousal Index": ">15/hour"
        },
        "symptoms": [
            "Loud snoring",
            "Witnessed apneas",
            "Morning headaches"
        ],
        "recommendations": [
            "Polysomnography",
            "ENT evaluation",
            "Weight management"
        ],
        "model_accuracy": 87,
        "confidence": 80
    }
}

# Generador de PDF
def generate_medical_report(patient_info, diagnosis_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_margins(left=15, top=15, right=15)
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    pdf.set_text_color(10, 15, 40)
    pdf.cell(0, 10, "NEUROSLEEP PRO DIAGNOSTIC REPORT", ln=1, align='C', fill=False)

    # Información del paciente
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Patient: {patient_info['name']}", ln=1)
    pdf.cell(0, 10, f"Age: {patient_info['age']}", ln=1)
    pdf.cell(0, 10, f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)

    # Sección de diagnóstico
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(10, 15, 40)
    pdf.cell(0, 10, f"Primary Diagnosis: {diagnosis_data['name']}", ln=1, align='C', center=True)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, diagnosis_data["description"], align='C')


    # Parámetros clave
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(10, 15, 40)
    pdf.cell(0, 10, "Key Metrics", align='C', center=True, ln=2)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0,0,0)
    for param, value in diagnosis_data["key_parameters"].items():
        pdf.cell(0, 10, f" {param}: {value}", ln=1, align='L')

    # Model Information
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(10, 15, 40)
    pdf.cell(0, 10, "Diagnostic Confidence:", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"- Model Accuracy: {diagnosis_data['model_accuracy']}% ", ln=1)
    pdf.cell(0, 10, f"- Analysis Confidence: {diagnosis_data['confidence']}%", ln=1)
    pdf.set_text_color(0,0,0)

    # Recomendaciones
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Clinical Recommendations:", ln=1)
    pdf.set_font("Arial", size=12)
    for rec in diagnosis['recommendations']:
        pdf.cell(0, 10, f"- {rec}", ln=1)

    # Security Footer
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "Secured by Proyecto Lethe, supported by Le Wagon", ln=1)


    return bytes(pdf.output(dest='S'))  #.encode('latin1')

# Interfaz de usuario

st.header("NEUROSLEEP PRO")
st.subheader("Advanced Sleep Diagnostics Platform")


# Layout principal -
main_col, side_col = st.columns([3, 1])

# Sección principal (la de la izquierda)
with main_col:
    # Sección de entrada de datos
    st.markdown("""
        <div class="cyber-card">
            <h2>Patient Data</h2>
    """, unsafe_allow_html=True)

    patient_name = st.text_input("Full Name")
    patient_age = st.number_input("Age", 10, 110)

    st.markdown("<h2>Upload Study Data</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv"])

if st.button("Initiate Analysis"):
    if uploaded_file is not None:
        with st.spinner("Processing neural patterns..."):
            try:
                # Procesar archivo
                columns = [f"f{i}" for i in range(1,1024)] + ['Sleep_stages']
                df = pd.read_csv(uploaded_file, names=columns)
                data = df.to_dict(orient='records')

                # Llamar a la API
                response = requests.post(api_url, json={'data': data})
                diagnosis_code = response.json()['diagnosis']
                diagnosis = DIAGNOSIS_INFO.get(diagnosis_code, DIAGNOSIS_INFO["0"])

                st.success("Analysis Complete")

                # Mostrar resultados - fuera del contexto de columnas principales
                st.markdown("""
                    <div class="cyber-card">
                        <h2>Diagnostic Results</h2>
                        <h3>Primary Diagnosis</h3>
                        <p class="metric-value">{diagnosis_name}</p>
                        <p class="diagnosis-text">{diagnosis_description}</p>
                    </div>
                """.format(
                    diagnosis_name=diagnosis['name'],
                    diagnosis_description=diagnosis['description']
                ), unsafe_allow_html=True)

#api_url = 'http://127.0.0.1:8000/predict'
api_url = 'http://proyecto-lethe-1029998951756.europe-west1.run.app'

                # Ahora las métricas fuera del contexto de columnas anidadas
                st.markdown("<h3>Key Parameters</h3>", unsafe_allow_html=True)

                # Crear columnas en el nivel superior del flujo
                metric_cols = st.columns(3)
                for i, (param, value) in enumerate(diagnosis["key_parameters"].items()):
                    with metric_cols[i]:
                        st.markdown(f"""
                            <div class="cyber-card">
                            <h3>{param}</h3>
                            <p class="metric-value">{value}</p>
                            </div>
                        """, unsafe_allow_html=True)

                # Síntomas y recomendaciones
                st.markdown("""
                    <div class="cyber-card">
                    <h3>Common Symptoms</h3>
                    <ul>
                """, unsafe_allow_html=True)
                for symptom in diagnosis["symptoms"]:
                    st.markdown(f"<li>{symptom}</li>", unsafe_allow_html=True)
                st.markdown("</ul></div>", unsafe_allow_html=True)

                st.markdown("""
                    <div class="cyber-card">
                        <h3>Clinical Recommendations</h3>
                        <ul>
                """, unsafe_allow_html=True)
                for rec in diagnosis["recommendations"]:
                    st.markdown(f"<li>{rec}</li>", unsafe_allow_html=True)
                st.markdown("</ul></div>", unsafe_allow_html=True)

                # Generación del super PDF
                pdf_report = generate_medical_report(
                    {"name": patient_name, "age": patient_age},
                    diagnosis
                )
                b64 = base64.b64encode(pdf_report).decode()
                st.download_button(
                    label="Download Full Report (PDF)",
                    data=pdf_report,
                    file_name="sleep_diagnosis_report.pdf",
                    mime="application/octet-stream"
                )

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
    else:
        st.warning("Please upload a valid CSV file first")

# Barra lateral (derecha)
with side_col:
    st.markdown("""
        <div class="sidebar-section">
            <h2>Clinic Details</h2>
    """, unsafe_allow_html=True)

    st.selectbox("Department", ["Neurophysiology", "Sleep Medicine", "Pulmonology"])
    st.date_input("Study Date")
