#%% Instalações
#!pip install pyodbc
#!pip install sqlalchemy 
#!pip install holidays

#%% Importações

#from AED_UR_5MIN import go_UR_5MIN
from AED_UR import getUR
from AED_AHU_VAG import getVAG
#from UTILS import go_LISTAR_PONTOS
from AED_UR_GRAFICOS import boxplot
from AED_UR_GRAFICOS import dispercao
from AED_UR_GRAFICOS import histograma
from AED_UR_GRAFICOS import infos
from AED_UR_GRAFICOS import mapacalor
from EAD_Meteorologico import DadosMeteorologicos
import pandas as pd

#%% Gerar lista de pontos do sistema que tem trend
#go_LISTAR_PONTOS()

#%% Executa análise com 5 minutos de intervalo (Com acréscimo)
#go_UR_5MIN()

#%% Executa análise com 30 minutos de internalo (Sem acréscimo)
getUR()

#%% Executa análise de VAG
getVAG()

#%% Gerar dataframe

df_UR = pd.read_csv('Dados BMS\df_UR.csv', delimiter=',')
df_VAG = pd.read_csv('Dados BMS\df_VAG.csv', delimiter=',')

#%% Juntar os dataframes

colunas_para_juntar = ['VAG Predio', 'Ligados']

df_UR = pd.merge(df_UR, df_VAG[['UTCDateTime'] + colunas_para_juntar], on='UTCDateTime', how='left')

df_UR.info() 

del colunas_para_juntar

#%% Executa tratamento de dados mateorológicos
df_UR = DadosMeteorologicos(df_UR)

df_UR.info() 

#%% Análise UR 

infos(df_UR)
dispercao(df_UR)
histograma(df_UR)
mapacalor(df_UR)
boxplot(df_UR)


#%% Deduções

# Foi notado que:
# ur_correnteMotor 
#   0.99 UR_KWH - Medida de potência, faz sentido.
#   -0.6 UR_TEMP_SAIDA - Menor temperatura do chiller, menos corrente?
#   0.84 ur_temp_entrada_condensacao - Quanto menor condensação, melhor
#   0.92 ur_temp_saida_condensacao - Quanto menor condensação, melhor
#   0.56 temp_externa
#   0.88 TR
#   0.95 delta_AC - Quanto menor condensação, melhor
#   0.67 VAG Predio
# UR_KWH
#   -0.54 UR_TEMP_SAIDA
#   0.82 ur_temp_entrada_condensacao
#   0.9 ur_temp_saida_condensacao
#   0.59 temp_externa
#   0.86 TR
#   0.96 delta_AC
#   0,7 vag Predio
# UR_TEMP_ENTRADA
#   0.74 delta_AG
# UR_TEMP_SAIDA
#   -0.62 ur_temp_entrada_condensacao
#   -0.62 ur_temp_saida_condensacao
#   -0.63 TR
#   -0.5 delta_AC
# ur_temp_entrada_condensacao
#   0.98 ur_temp_saida_condensacao
#   0.74 TR
#   0.79 delta_AC
#   0.5 VAG Predio
# ur_temp_saida_condensacao
#   0.56 temp_externa
#   0.81 TR
#   0.89 delta_AC
#   0.59 VAG Predio
# temp_externa
#   0.62 delta_AC
#   0.6 VAG Predio
# TR
#   0.84 delta_AC
#   0.57 VAG Predio
# delta_AC
#   0.73 VAG Preio
#   0.52 Ligados
# VAG Predio
#   0.83 Ligados
# AHUs correlacionados
# AHU-02-01 0.66 AHU-SS1-05
# AHU-02-02 0.6 AHU-01-07
# AHU-03-01 0.71 AHU-02-02
# AHU-03-02 0.65 AHU-02-02
# AHU-03-02 0.73 AHU-03-01
# AHU-03-01 0.62 AHU-03-03
# AHU-05-01 0.6 AHU-04-01
# AHU-05-03 0.61 AHU-03-03
# AHU-06-06 0.73 AHU-06-07
# AHU-06-09 0.75 AHU-06-10
# AHU-06-06 0.66 AHU-06-09
# AHU-06-06 0.67 AHU-06-10
# AHU-06-07 0.68 AHU-06-10
# AHU-06-10 0.6 AHU-SS1-02
# AHU-03-01 0.61 AHU-06-01
# AHU-06-03 0.62 AHU-06-01
# VAG Predio 0.64 AHU-01-07
# VAG Predio 0.7 AHU-02-02
# VAG Predio 0.57 AHU-02-05
# VAG Predio 0.68 AHU-03-01
# VAG Predio 0.7 AHU-03-02
# VAG Predio 0.66 AHU-03-03
# VAG Predio 0.66 AHU-05-03
# VAG Predio 0.65 AHU-06-07
# VAG Predio 0.66 AHU-06-03
# VAG Predio 0.69 AHU-06-01
# VAG Predio 0.83 Ligados

# Ligados 0.64 AHU-01-07
# Ligados 0.76 AHU-02-02
# Ligados 0.65 AHU-02-05
# Ligados 0.75 AHU-03-01
# Ligados 0.75 AHU-03-02
# Ligados 0.65 AHU-03-03
# Ligados 0.63 AHU-05-03
# Ligados 0.57 AHU-06-03
# Ligados 0.7 AHU-06-01

# Pressao (mB)
#   -0.55 ur_correnteMotor
#   -0.55 UR_KWH
#   -0.54 temp_entrada_condensacao
#   -0.56 temp_saida_condensacao
#   -0.48 TR
#   -0.33 delta_AG
#   -0.56 delta_AC
#   -0.43 VAG Predio

# Temperatura (°C)
#   0.58 ur_correnteMotor
#   0.6 UR_KWH
#   0.52 temp_entrada_condensacao
#   0.57 temp_saida_condensacao
#   0.49 TR
#   0.34 delta_AG
#   0.62 delta_AC
#   0.61 VAG Predio
#   0.31 Ligados

# Umidade (%)
#   0.35 ur_correnteMotor
#   0.33 UR_KWH
#   0.39 temp_entrada_condensacao
#   0.38 temp_saida_condensacao
#   0.31 delta_AC

#%% Meteorológico externo


#%% Fim
