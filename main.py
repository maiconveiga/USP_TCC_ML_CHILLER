#%% Instalações
#!pip install pyodbc
#!pip install sqlalchemy 
#!pip install holidays

#%% Importações

from AED_UR_5MIN import go_UR_5MIN
from AED_UR_30MIN import go_UR_30MIN
from AED_AHU_VAG import go_AHU_VAG
from UTILS import go_LISTAR_PONTOS
from AED_UR_GRAFICOS import go_UR_GRAPHS
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

go_UR_GRAPHS(pd.read_excel('df_ur_5min.xlsx'))
go_UR_GRAPHS(pd.read_excel('df_ur_30min.xlsx'))

#%% Fim
