import streamlit as st
import numpy as np
import joblib
import plotly.graph_objs as go

# Adicionando estilo para o layout e o cartão abaixo do gráfico
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .reportview-container {
        font-family: 'Arial', sans-serif;
    }
    .header-text {
        color: #4B6584;
        font-size: 26px;
        text-align: center;
        font-weight: bold;
        padding: 20px 0;
    }
    .sub-header {
        font-size: 18px;
        color: #34495e;
        margin-bottom: 20px;
    }
    .fixed-graph {
        position: -webkit-sticky;
        position: sticky;
        top: 20px;
    }
    .card {
        padding: 10px;  /* Reduzi o padding pela metade */
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-size: 18px;  /* Reduzi o tamanho da fonte */
        font-weight: bold;
        margin-top: 10px;  /* Reduzi a margem superior */
    }
    </style>
    """, unsafe_allow_html=True)

# Título da aplicação
st.markdown('<div class="header-text">Previsão de Corrente - Chiller</div>', unsafe_allow_html=True)

# Criar layout com duas colunas: sliders à esquerda e o valor previsto no restante da tela
col1, col2 = st.columns([1, 2])  # 1/3 da largura para parâmetros e 2/3 para o gráfico

# Na primeira coluna (col1), colocar os sliders
with col1:
    st.markdown('<div class="sub-header">Parâmetros de Entrada</div>', unsafe_allow_html=True)
    pressao = st.slider('Pressão (mB)', min_value=900.0, max_value=1015.2, value=1016.85, step=0.1)
    temperatura = st.slider('Temperatura (°C)', min_value= 15.0, max_value=40.0, value=26.15, step=0.1)
    umidade = st.slider('Umidade (%)', min_value=12.0, max_value=100.0, value=74.5, step=0.1)
    ur_temp_saida = st.slider('Temperatura de Saída UR', min_value=6.0, max_value=6.2, value=16.8, step=0.1)
    tr = st.slider('TR', min_value=0.0, max_value=600.0, value=72.10, step=1.0)
    delta_ac = st.slider('Delta AC', min_value=0.0, max_value=5.0, value=0.299, step=0.1)
    vag_predio = st.slider('VAG Prédio', min_value=0.0, max_value=100.0, value=65.66, step=0.1)
    ligados = st.slider('Ligados', min_value=0.0, max_value=100.0, value=77.77, step=1.0)

# Verificar se o modelo foi carregado corretamente antes de continuar
try:

    model = joblib.load('./ModelsDeploy/corrente_motor_model.pkl')
    scaler = joblib.load('./ModelsDeploy/scaler.pkl')

    st.success("Modelo e scaler carregados com sucesso.")
except Exception as e:
    st.error(f"Erro ao carregar o modelo ou scaler: {e}")

# Na segunda coluna (col2), exibir a barra vertical com o valor previsto e título
with col2:
    if 'model' in locals() and 'scaler' in locals():
        # Coletar as entradas dos sliders em um array numpy
        input_data = np.array([[pressao, temperatura, umidade, ur_temp_saida, tr, delta_ac, vag_predio, ligados]])

        # Normalizar os dados usando o scaler treinado
        input_data_scaled = scaler.transform(input_data)

        # Fazer a previsão com base nas entradas normalizadas
        predicted_corrente = model.predict(input_data_scaled)[0]

        # Definir a cor do gráfico e do cartão conforme o valor da corrente
        if predicted_corrente <= 20:
            bar_color = '#2ecc71'  # Verde claro
            card_color = '#2ecc71'  # Verde claro
            text_color = '#ffffff'  # Branco
        elif predicted_corrente <= 60:
            bar_color = '#f1c40f'  # Amarelo
            card_color = '#f1c40f'  # Amarelo
            text_color = '#ffffff'  # Branco
        elif predicted_corrente <= 80:
            bar_color = '#e67e22'  # Laranja
            card_color = '#e67e22'  # Laranja
            text_color = '#ffffff'  # Branco
        else:
            bar_color = '#e74c3c'  # Vermelho
            card_color = '#e74c3c'  # Vermelho
            text_color = '#ffffff'  # Branco

        # Criar a barra vertical usando Plotly com a cor condicional
        fig = go.Figure(go.Bar(
            x=['Corrente Chiller (%)'],  # Nome do eixo X
            y=[predicted_corrente],  # Valor previsto
            marker=dict(color=bar_color),  # Cor da barra
            width=[0.3],  # Largura da barra
            orientation='v'  # Orientação vertical
        ))

        # Ajustando o layout do gráfico
        fig.update_layout(
            title="Corrente Chiller (%)",  # Título do gráfico
            height=400,  # Altura da barra
            yaxis=dict(range=[0, 100], title="Corrente (%)"),  # Limitar de 0 a 100
            xaxis=dict(showticklabels=False),  # Remover rótulos do eixo X
            margin=dict(t=40, b=0, l=0, r=0),  # Ajuste das margens
            showlegend=False  # Remover a legenda
        )

        # Exibir a barra vertical no centro da coluna mais à direita
        st.plotly_chart(fig, use_container_width=True)

        # Exibir o cartão abaixo do gráfico com cor condicional e tamanho reduzido
        st.markdown(f'<div class="card" style="background-color: {card_color}; color: {text_color};">Valor da Corrente: {predicted_corrente:.2f} %</div>', unsafe_allow_html=True)
    else:
        st.warning("O modelo e o scaler precisam ser carregados corretamente para fazer previsões.")