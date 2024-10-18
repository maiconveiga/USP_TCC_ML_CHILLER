#%% Conexão com o banco
def conexaoBanco():
    
    from sqlalchemy import create_engine
    
    #Dados para inserir
    machine = 'M5282650'
    instance = 'SQLEXPRESS'
    username = 'py'
    password = 'py'
    
    server = f'{machine}\\{instance}'
    database = 'JCIHistorianDB'
    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server"
    engine = create_engine(connection_string)
    return engine

#%% Listagem de pontos
def getListaEquipamentos():

    import pandas as pd

    # Função de conexão com o banco de dados
    engine = conexaoBanco()
    
    # Query para obter os dados
    query = """
    SELECT DISTINCT PointName
    FROM [JCIHistorianDB].[dbo].[RawAnalog]
    """
    df = pd.read_sql(query, engine)
    df['Tipo'] = ''
    df['Equipamento'] = ''
    df['Ponto'] = ''
    
    # Salvar o DataFrame como um arquivo Excel
    df.to_csv('Lista_Pontos_Equipamento.csv', index=False)
 
def juntarDF(df_UR, df_VAG):
    import pandas as pd
    
    colunas_para_juntar = ['VAG Aberta %', 'Fancoil ligado %']
    df = pd.merge(df_UR, df_VAG[['UTCDateTime'] + colunas_para_juntar], on='UTCDateTime', how='left') 
    
    df = df.dropna()
    
    return df

def juntarDF1(df_ur, df_fancoil):
    
    print("Antes do tratamento")   
    nan_por_coluna = df_ur.isna().sum()
    print("Valores NaN por coluna:")
    print(nan_por_coluna)
    print("--------------------------------------") 

    import pandas as pd

    colunas_para_juntar = ['VAG Aberta %','Fancoil ligado %']
    df = pd.merge(df_ur, df_fancoil[['UTCDateTime'] + colunas_para_juntar], on='UTCDateTime', how='left') 
    
    df = df.dropna()
    
    print("Depois do tratamento")   
    nan_por_coluna = df.isna().sum()
    print("Valores NaN por coluna:")
    print(nan_por_coluna)
    print("--------------------------------------")  
    
    return df
