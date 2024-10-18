#%% Importações

#from EADs.AED_UR import getUR
from EADs.AED_Tratar import tratarChiller, tratarFancoil
#from EADs.AED_AHU_VAG import getVAG
from EADs.AED_BMS import getBMS
from UTILS import getListaEquipamentos, juntarDF
from EADs.AED_Graph import boxplot, histograma, mapacalor# printModelStats
from EADs.EAD_Meteorologico import DadosMeteorologicos
from Models.MODEL_UR_CORRENTEMOTOR import preverCorrente
from Models.MODEL_TR import preverTR
from Models.MODEL_delta_AC import preverDeltaAC
from Models.MODEL_VAG_Predio import preverVAG
from Models.MODEL_Ligados import preverLigados
from Models.MODEL_KWH import preverkwh
import pandas as pd


#%% Gerar lista de pontos do sistema que tem trend

getListaEquipamentos()

#%% Coleta
df_all = getBMS()

#%%Separação
df_fancoil = df_all['Fancoil'].copy()
df_ur1 = df_all['Chiller 1'].copy()
df_ur2 = df_all['Chiller 2'].copy()

linhas_com_nan_Fancoil = df_fancoil[df_fancoil.isna().any(axis=1)]
linhas_com_nan_ur1 = df_ur1[df_ur1.isna().any(axis=1)]
linhas_com_nan_ur2 = df_ur2[df_ur2.isna().any(axis=1)]


#%% Tratamento inicial
df_fancoil_Tratado = tratarFancoil(df_fancoil).copy()
df_ur1_Tratado = tratarChiller(df_ur1).copy()
df_ur2_Tratado = tratarChiller(df_ur2).copy()

linhas_com_nan_Fancoil = df_fancoil_Tratado[df_fancoil_Tratado.isna().any(axis=1)]
linhas_com_nan_ur1 = df_ur1_Tratado[df_ur1_Tratado.isna().any(axis=1)]
linhas_com_nan_ur2 = df_ur2_Tratado[df_ur2_Tratado.isna().any(axis=1)]

#%% Tratamento refatorado
df_fancoil_Tratado = df_fancoil_Tratado.dropna()
df_ur1_Tratado = df_ur1_Tratado.dropna()
df_ur2_Tratado = df_ur2_Tratado.dropna()

linhas_com_nan_Fancoil = df_fancoil_Tratado[df_fancoil_Tratado.isna().any(axis=1)]
linhas_com_nan_ur1 = df_ur1_Tratado[df_ur1_Tratado.isna().any(axis=1)]
linhas_com_nan_ur2 = df_ur2_Tratado[df_ur2_Tratado.isna().any(axis=1)]

#%% Juntar dataframes
df_ur1_Tratado_Fancoil = juntarDF(df_ur1_Tratado, df_fancoil_Tratado)
df_ur2_Tratado_Fancoil = juntarDF(df_ur2_Tratado, df_fancoil_Tratado)

linhas_com_nan_ur1 = df_ur1_Tratado_Fancoil[df_ur1_Tratado_Fancoil.isna().any(axis=1)]
linhas_com_nan_ur2 = df_ur2_Tratado_Fancoil[df_ur2_Tratado_Fancoil.isna().any(axis=1)]

#%% Tratar dados meteorologicos
df_ur1_Tratado_Fancoil_Clima = DadosMeteorologicos(df_ur1_Tratado_Fancoil)
df_ur2_Tratado_Fancoil_Clima = DadosMeteorologicos(df_ur2_Tratado_Fancoil)

linhas_com_nan_ur1 = df_ur1_Tratado_Fancoil_Clima[df_ur1_Tratado_Fancoil_Clima.isna().any(axis=1)]
linhas_com_nan_ur2 = df_ur2_Tratado_Fancoil_Clima[df_ur2_Tratado_Fancoil_Clima.isna().any(axis=1)]

#%% Atribuir aos dataframes finais
df_ur_1 = df_ur1_Tratado_Fancoil_Clima.copy()
df_ur_2 = df_ur2_Tratado_Fancoil_Clima.copy()

df_ur_1.to_csv('Dados BMS\df_ur_1.csv', index=False)
df_ur_2.to_csv('Dados BMS\df_ur_2.csv', index=False)

#%% Antigo

# #Coleta e tratamento
# df_ur_0 = getUR()

# df_VAG = getVAG(df_ur_0)

# # Juntar dataframes
# df_ur_0 = juntarDF(df_ur_0, df_VAG)
# del df_VAG

# # Tratar dados meteorologicos
# df_ur_0 = DadosMeteorologicos(df_ur_0)

# linhas_com_nan_ur = df_ur_0[df_ur_0.isna().any(axis=1)]


#%% Seguir a análise daqui.

df_ur_1 = pd.read_csv('Dados BMS\df_ur_1.csv', delimiter=',')
df_ur_2 = pd.read_csv('Dados BMS\df_ur_2.csv', delimiter=',')

#%% Análise UR 

histograma(df_ur_1)
histograma(df_ur_2)

mapacalor(df_ur_1)
mapacalor(df_ur_2)

boxplot(df_ur_1)
boxplot(df_ur_2)

#%% Modelos

df_indicators_Delta_AC_df_ur_1 = preverDeltaAC(df_ur_1)
df_indicators_Delta_AC_df_ur_2 = preverDeltaAC(df_ur_2)


df_indicators_VAG_df_ur_1 = preverVAG(df_ur_1)
df_indicators_VAG_df_ur_2 = preverVAG(df_ur_2)


df_indicators_TR_df_ur_1 = preverTR(df_ur_1)
df_indicators_TR_df_ur_2 = preverTR(df_ur_2)


df_indicators_Corrente_df_ur_1 = preverCorrente(df_ur_1)
df_indicators_Corrente_df_ur_2 = preverCorrente(df_ur_2)


df_indicators_Ligados_df_ur_1 = preverLigados(df_ur_1)
df_indicators_Ligados_df_ur_2 = preverLigados(df_ur_2)


df_indicators_KWH_df_ur_1 = preverkwh(df_ur_1)
df_indicators_KWH_df_ur_2 = preverkwh(df_ur_2)

# printModelStats(df_indicators_Delta_AC_df_ur_0, 'Chiller 1 Antigo')
# printModelStats(df_indicators_Delta_AC_df_ur_1, 'Chiller 1 Novo')
# printModelStats(df_indicators_Delta_AC_df_ur_2, 'Chiller 2 Novo')

# df_estudo = df_ur_0[['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)','ur_temp_saida','FimDeSemana', 'HorarioComercial','ur_correnteMotor','VAG Aberta %','Fancoil ligado %','delta_AC','TR', 'ur_kwh', 'UTCDateTime']]
# df_estudo = df_ur_1[['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)','ur_temp_saida','FimDeSemana', 'HorarioComercial','ur_correnteMotor','VAG Aberta %','Fancoil ligado %','delta_AC','TR', 'ur_kwh', 'UTCDateTime']]
# df_estudo = df_ur_2[['Pressao (mB)', 'Temperatura (°C)', 'Umidade (%)','ur_temp_saida','FimDeSemana', 'HorarioComercial','ur_correnteMotor','VAG Aberta %','Fancoil ligado %','delta_AC','TR', 'ur_kwh', 'UTCDateTime']]

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
