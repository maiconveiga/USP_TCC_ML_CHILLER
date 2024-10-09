#%% Instalações
#!pip install pyodbc
#!pip install sqlalchemy 
#!pip install holidays

#%% Importações

from AED_UR_5MIN import go_UR_5MIN
from AED_UR_30MIN import go_UR_30MIN
from AED_AHU_VAG import go_AHU_VAG
from UTILS import go_LISTAR_PONTOS
from AED_UR_GRAFICOS import boxplot
from AED_UR_GRAFICOS import dispercao
from AED_UR_GRAFICOS import histograma
from AED_UR_GRAFICOS import infos
from AED_UR_GRAFICOS import mapacalor
from AED_UR_GRAFICOS import descricao
import pandas as pd

#%% Gerar lista de pontos do sistema que tem trend
go_LISTAR_PONTOS()

#%% Executa análise com 5 minutos de intervalo (Com acréscimo)
go_UR_5MIN()

#%% Executa análise com 30 minutos de internalo (Sem acréscimo)
go_UR_30MIN()

#%% Executa análise de VAG
go_AHU_VAG()

#%% Gerar gráficos

df_ur_5min = pd.read_excel('df_ur_5min.xlsx')
df_ur_30min = pd.read_excel('df_ur_30min.xlsx')


infos(df_ur_5min)
infos(df_ur_30min)

descricao(df_ur_5min)
descricao(df_ur_30min)

histograma(df_ur_5min, '5Min')
histograma(df_ur_30min, '30Min')

boxplot(df_ur_5min)
boxplot(df_ur_30min)

dispercao(df_ur_5min)
dispercao(df_ur_30min)

mapacalor(df_ur_5min)
mapacalor(df_ur_30min)

#%% Fim
