import streamlit as st
import numpy as np
import joblib
import pandas as pd
import plotly.graph_objects as go
from tensorflow.keras.models import load_model

def set_css():
    st.markdown(
        """
        <style>
        .custom-title {
            font-size: 40px !important;  /* Reduzindo cerca de 1/3 do tamanho */
        }
        .custom-subtitle {
            font-size: 22px !important;  /* Reduzindo cerca de 1/3 do tamanho */
        }
        </style>
        """, unsafe_allow_html=True
    )

# Adicionar o CSS personalizado para o tamanho da fonte
set_css()

#pathProd = ''
pathProd = 'predict_service/'

# Carregar o modelo e o scaler
model_corrente = load_model(f'{pathProd}ModelsDeploy/corrente/model.h5')
scaler_corrente = joblib.load(f'{pathProd}ModelsDeploy/corrente/scaler.pkl')

model_deltaAC = joblib.load(f'{pathProd}ModelsDeploy/deltaAC/model.pkl')
scaler_deltaAC = joblib.load(f'{pathProd}ModelsDeploy/deltaAC/scaler.pkl')

model_Ligados = joblib.load(f'{pathProd}ModelsDeploy/Ligados/model.pkl')
scaler_Ligados = joblib.load(f'{pathProd}ModelsDeploy/Ligados/scaler.pkl')

model_TR = joblib.load(f'{pathProd}ModelsDeploy/TR/model.pkl')
scaler_TR = joblib.load(f'{pathProd}ModelsDeploy/TR/scaler.pkl')

model_VAG = joblib.load(f'{pathProd}ModelsDeploy/VAG/model.pkl')
scaler_VAG = joblib.load(f'{pathProd}ModelsDeploy/VAG/scaler.pkl')

model_KWH = joblib.load(f'{pathProd}ModelsDeploy/KWH/model.pkl')
scaler_KWH = joblib.load(f'{pathProd}ModelsDeploy/KWH/scaler.pkl')

# Ajustar o layout: sliders na lateral
st.sidebar.title("Parâmetros de Entrada")

# Sliders para os parâmetros de entrada
pressao = st.sidebar.number_input('Pressão (mB)', min_value=900.0, max_value=1030.0, value=1008.6)
temperatura = st.sidebar.number_input('Temperatura (°C)', min_value=15.0, max_value=40.0, value=31.9)
umidade = st.sidebar.number_input('Umidade (%)', min_value=0.0, max_value=100.0, value=76.0)
ur_temp_saida = st.sidebar.number_input('Temperatura de Saída (°C)', min_value=4.5, max_value=20.0, value=9.5)

# Fim de Semana e Horário Comercial podem continuar como selectbox
FimDeSemana = st.sidebar.selectbox('Fim de Semana', [0, 1], index=0)
HorarioComercial = st.sidebar.selectbox('Horário Comercial', [0, 1], index=1)

# Adicionar abas para Chiller 1, Chiller 2 e Comparativo
tab1, tab2, tab3 = st.tabs(["Chiller 1", "Chiller 2", "Comparativo"])

# Função para prever valores
def calcular_previsoes():
    # Previsão Ligados Chiller 1
    input_data_Ligados = np.array([[pressao, temperatura, umidade, ur_temp_saida, FimDeSemana, HorarioComercial]])
    input_data_scaled_Ligados = scaler_Ligados.transform(input_data_Ligados)
    previsaoLigados = model_Ligados.predict(input_data_scaled_Ligados)

    # Previsão VAG Chiller 1
    input_data_VAG = np.array([[pressao, temperatura, umidade, FimDeSemana, HorarioComercial, previsaoLigados[0]]])
    input_data_scaled_VAG = scaler_VAG.transform(input_data_VAG)
    previsaoVAG = model_VAG.predict(input_data_scaled_VAG)

    # Previsão de Delta AC Chiller 1
    input_data_deltaAC = np.array([[pressao, temperatura, umidade, ur_temp_saida, previsaoVAG[0], previsaoLigados[0]]])
    input_data_scaled_deltaAC = scaler_deltaAC.transform(input_data_deltaAC)
    previsaodeltaAC = model_deltaAC.predict(input_data_scaled_deltaAC)
 
    # Previsão de TR Chiller 1
    input_data_TR = np.array([[pressao, temperatura, umidade, previsaodeltaAC[0], previsaoVAG[0], ur_temp_saida, FimDeSemana, HorarioComercial, previsaoLigados[0]]])
    input_data_scaled_TR = scaler_TR.transform(input_data_TR)
    previsaoTR = model_TR.predict(input_data_scaled_TR)

    # Previsão de KWH Chiller 1
    input_data_KWH = np.array([[pressao, temperatura, umidade, previsaodeltaAC[0], previsaoTR[0], ur_temp_saida, previsaoVAG[0], previsaoLigados[0]]])
    input_data_scaled_KWH = scaler_KWH.transform(input_data_KWH)
    previsaoKWH = model_KWH.predict(input_data_scaled_KWH)

    # Previsão de corrente Chiller 1
    input_data_corrente = np.array([[pressao, temperatura, umidade, ur_temp_saida, previsaoTR[0], previsaodeltaAC[0], previsaoVAG[0], previsaoLigados[0], previsaoKWH[0]]])
    input_data_scaled_corrente = scaler_corrente.transform(input_data_corrente)
    previsaoCorrente = model_corrente.predict(input_data_scaled_corrente)

    # Retornar todas as previsões
    return previsaoCorrente, previsaoVAG, previsaoLigados, previsaodeltaAC, previsaoTR, previsaoKWH

# Aba Chiller 1
with tab1:
    #st.title('Previsões de Desempenho - Chiller 1')
    st.markdown('<h1 class="custom-title">Previsões de Desempenho - Chiller 1</h1>', unsafe_allow_html=True)

    previsaoCorrente, previsaoVAG, previsaoLigados, previsaodeltaAC, previsaoTR, previsaoKWH = calcular_previsoes()

    # Criar um DataFrame para os resultados
    resultados_1 = pd.DataFrame({
        'Parâmetro': ['Corrente (%)', 'VAG (%)', 'Fancoils Ligados (%)', 'Delta AC (°C)', 'TR', 'KWH'],
        'Previsão': [
            f'{previsaoCorrente[0][0]:.2f}',
            f'{previsaoVAG[0]:.2f}', 
            f'{previsaoLigados[0]:.2f}', 
            f'{previsaodeltaAC[0]:.2f}', 
            f'{previsaoTR[0]:.2f}',
            f'{previsaoKWH[0]:.2f}'
        ]
    })

    st.table(resultados_1.style.set_properties(**{'text-align': 'center'}))

# Aba Chiller 2
with tab2:
   #st.title('Previsões de Desempenho - Chiller 2')
    st.markdown('<h1 class="custom-title">Previsões de Desempenho - Chiller 2</h1>', unsafe_allow_html=True)

    previsaoCorrente_2, previsaoVAG_2, previsaoLigados_2, previsaodeltaAC_2, previsaoTR_2, previsaoKWH_2 = calcular_previsoes()

    # Criar um DataFrame para os resultados
    resultados_2 = pd.DataFrame({
        'Parâmetro': ['Corrente (%)', 'VAG (%)', 'Fancoils Ligados (%)', 'Delta AC (°C)', 'TR', 'KWH'],
        'Previsão': [
            f'{previsaoCorrente_2[0][0]:.2f}',
            f'{previsaoVAG_2[0]:.2f}', 
            f'{previsaoLigados_2[0]:.2f}', 
            f'{previsaodeltaAC_2[0]:.2f}', 
            f'{previsaoTR_2[0]:.2f}',
            f'{previsaoKWH_2[0]:.2f}'
        ]
    })

    st.table(resultados_2.style.set_properties(**{'text-align': 'center'}))

# Aba Comparativo
with tab3:
    #st.title('Comparativo de Desempenho entre Chiller 1 e Chiller 2')
    st.markdown('<h1 class="custom-title">Comparativo</h1>', unsafe_allow_html=True)

    # Valores de previsão para o gráfico
    parametros = ['Corrente (%)', 'VAG (%)', 'Fancoils Ligados (%)', 'Delta AC (°C)', 'TR', 'KWH']
    
    chiller_1_valores = [float(previsaoCorrente[0][0]), float(previsaoVAG[0]), float(previsaoLigados[0]), float(previsaodeltaAC[0]), float(previsaoTR[0]), float(previsaoKWH[0])]
    chiller_2_valores = [float(previsaoCorrente_2[0][0]), float(previsaoVAG_2[0]), float(previsaoLigados_2[0]), float(previsaodeltaAC_2[0]), float(previsaoTR_2[0]), float(previsaoKWH_2[0])]

    # Criar gráficos interativos para cada parâmetro
    for i, parametro in enumerate(parametros):
        fig = go.Figure()

        # Adicionar barras de Chiller 1 e Chiller 2
        fig.add_trace(go.Bar(x=['Chiller 1'], y=[chiller_1_valores[i]], name='Chiller 1'))
        fig.add_trace(go.Bar(x=['Chiller 2'], y=[chiller_2_valores[i]], name='Chiller 2'))

        # Configurações do gráfico
        fig.update_layout(
            title=f'Comparação de {parametro} entre Chiller 1 e Chiller 2',
            xaxis_title='Chiller',
            yaxis_title=parametro,
            barmode='group'
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
