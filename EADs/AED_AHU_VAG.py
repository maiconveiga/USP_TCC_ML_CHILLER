#%% Importações

def getVAG():
       
    import pandas as pd
    import pyodbc
    
#%% Conexão
    
    df_lista = pd.read_csv('Dados BMS\Lista_Pontos.csv')
    
    conexao = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=M5282650\\SQLEXPRESS;'
    'DATABASE=JCIHistorianDB;'
    'UID=py;'
    'PWD=py;')

#%% Coleta

    # Definir o intervalo de datas
    inicio = pd.to_datetime('2023-06-01 03:00:00')
    fim = pd.to_datetime('2024-09-09 03:00:00')
    
    # Criar um índice de tempo com intervalos de 30 minutos e 5 minutos
    index_30min = pd.date_range(start=inicio, end=fim, freq='30T')
    #index_5min = pd.date_range(start=inicio, end=fim, freq='5T')
    
    # Inicializar os DataFrames finais com os índices de tempo
    df_VAG_30min = pd.DataFrame(index=index_30min)
    #df_VAG_5min = pd.DataFrame(index=index_5min)
    
    for PointName in df_lista['PointName']:
        # Construção da query
        query = f"SELECT UTCDateTime, PointName, ActualValue FROM [JCIHistorianDB].[dbo].[RawAnalog] WHERE PointName = '{PointName}'"
        
        # Executando a query e armazenando o resultado em um DataFrame temporário
        df_temp = pd.read_sql(query, conexao)
        
        # Converta a coluna UTCDateTime para datetime, caso ainda não esteja
        df_temp['UTCDateTime'] = pd.to_datetime(df_temp['UTCDateTime'])
        
        # Renomear a coluna 'ActualValue' para o valor de 'PointName'
        df_temp = df_temp.rename(columns={'ActualValue': PointName})
        
        # Deletar a coluna 'PointName'
        df_temp = df_temp.drop(columns=['PointName'])
        
        # Definir UTCDateTime como índice temporariamente
        df_temp.set_index('UTCDateTime', inplace=True)
    
        # Fazer o merge com os DataFrames finais de 30min e 5min
        df_VAG_30min = df_VAG_30min.merge(df_temp, how='left', left_index=True, right_index=True)
        #df_VAG_5min = df_VAG_5min.merge(df_temp, how='left', left_index=True, right_index=True)
    
    # Preencher os valores ausentes com o valor da linha anterior
    df_VAG_30min.fillna(method='ffill', inplace=True)
    #df_VAG_5min.fillna(method='ffill', inplace=True)
    
    # Substituir valores ausentes (NaN) por zero
    df_VAG_30min.fillna(0, inplace=True)
    #df_VAG_5min.fillna(0, inplace=True)

    # Resetar o índice para trazer UTCDateTime de volta como uma coluna, se necessário
    df_VAG_30min.reset_index(inplace=True)
    #df_VAG_5min.reset_index(inplace=True)
    
    # Renomear o índice para UTCDateTime
    df_VAG_30min.rename(columns={'index': 'UTCDateTime'}, inplace=True)
    #df_VAG_5min.rename(columns={'index': 'UTCDateTime'}, inplace=True)
    
    df_VAG_30min.fillna(0)
    #df_VAG_5min.fillna(0)
    
#%% Criar total de %VAG

    #df_VAG_5min['VAG Predio'] = (df_VAG_5min.drop(columns=['UTCDateTime']).sum(axis=1)/36)
    df_VAG_30min['VAG Predio'] = (df_VAG_30min.drop(columns=['UTCDateTime']).sum(axis=1)/36)

#%% Criar total de AHU ligada

    #df_VAG_5min['Ligados'] = ((36 - (df_VAG_5min.drop(columns=['UTCDateTime']).apply(lambda row: (row == 0).sum(), axis=1)))*100)/36
    df_VAG_30min['Ligados'] =((36 - (df_VAG_30min.drop(columns=['UTCDateTime']).apply(lambda row: (row == 0).sum(), axis=1)))*100)/36
    
#%% Gerar excel
    df_VAG_30min.to_csv('Dados BMS\df_VAG.csv', index=False)
    