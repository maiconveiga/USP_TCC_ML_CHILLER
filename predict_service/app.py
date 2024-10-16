import streamlit as st
import numpy as np
import joblib
import pandas as pd

# Carregar o modelo e o scaler
model_corrente = joblib.load('ModelsDeploy/corrente/model.pkl')
scaler_corrente = joblib.load('ModelsDeploy/corrente/scaler.pkl')

model_deltaAC = joblib.load('ModelsDeploy/deltaAC/model.pkl')
scaler_deltaAC = joblib.load('ModelsDeploy/deltaAC/scaler.pkl')

model_Ligados = joblib.load('ModelsDeploy/Ligados/model.pkl')
scaler_Ligados = joblib.load('ModelsDeploy/Ligados/scaler.pkl')

model_TR = joblib.load('ModelsDeploy/TR/model.pkl')
scaler_TR = joblib.load('ModelsDeploy/TR/scaler.pkl')

model_VAG = joblib.load('ModelsDeploy/VAG/model.pkl')
scaler_VAG = joblib.load('ModelsDeploy/VAG/scaler.pkl')

# Ajustar o layout: sliders na lateral
st.sidebar.title("Parâmetros de Entrada")

# Sliders para os parâmetros de entrada
pressao = st.sidebar.slider('Pressão (mB)', min_value=900.0, max_value=1030.0, value=1014.8)
temperatura = st.sidebar.slider('Temperatura (°C)', min_value=15.0, max_value=40.0, value=21.0)
umidade = st.sidebar.slider('Umidade (%)', min_value=0.0, max_value=100.0, value=69.0)
ur_temp_saida = st.sidebar.slider('Temperatura de Saída (°C)', min_value=4.5, max_value=20.0, value=7.2)
FimDeSemana = st.sidebar.selectbox('Fim de Semana', [0, 1], index=0)
HorarioComercial = st.sidebar.selectbox('Horário Comercial', [0, 1], index=0)

#Previsão VAG
input_data_VAG = np.array([[pressao, temperatura, umidade, FimDeSemana, HorarioComercial]])
input_data_scaled_VAG = scaler_VAG.transform(input_data_VAG)
previsaoVAG = model_VAG.predict(input_data_scaled_VAG)

#Previsão Ligados
input_data_Ligados = np.array([[pressao, temperatura, umidade, ur_temp_saida, FimDeSemana, HorarioComercial, previsaoVAG[0]]])
input_data_scaled_Ligados = scaler_Ligados.transform(input_data_Ligados)
previsaoLigados = model_Ligados.predict(input_data_scaled_Ligados)

# Previsão de Delta AC
input_data_deltaAC = np.array([[pressao, temperatura, umidade, ur_temp_saida, previsaoVAG[0], previsaoLigados[0]]])
input_data_scaled_deltaAC = scaler_deltaAC.transform(input_data_deltaAC)
previsaodeltaAC = model_deltaAC.predict(input_data_scaled_deltaAC)

# Previsão de TR
input_data_TR = np.array([[pressao, temperatura, umidade, previsaodeltaAC[0], previsaoVAG[0], FimDeSemana, HorarioComercial, previsaoLigados[0]]])
input_data_scaled_TR = scaler_TR.transform(input_data_TR)
previsaoTR = model_TR.predict(input_data_scaled_TR)

# Previsão de corrente
input_data_corrente = np.array([[pressao, temperatura, umidade, ur_temp_saida, previsaoTR[0], previsaodeltaAC[0], previsaoVAG[0], previsaoLigados[0]]])
input_data_scaled_corrente = scaler_corrente.transform(input_data_corrente)
previsaoCorrente = model_corrente.predict(input_data_scaled_corrente)

# Exibir os resultados em uma tabela centralizada
st.title('Previsões de Desempenho')

# Criar um DataFrame para os resultados
resultados = pd.DataFrame({
    'Parâmetro': ['Corrente (%)', 'VAG (%)', 'Fancoils Ligados (%)', 'Delta AC (°C)', 'TR'],
    'Previsão': [
        f'{previsaoCorrente[0]:.2f}', 
        f'{previsaoVAG[0]:.2f}', 
        f'{previsaoLigados[0]:.2f}', 
        f'{previsaodeltaAC[0]:.2f}', 
        f'{previsaoTR[0]:.2f}'
    ]
})

# Exibir a tabela com os resultados no centro
st.markdown(
    """
    <style>
    .center-table {
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True
)

st.table(resultados.style.set_properties(**{'text-align': 'center'}))
