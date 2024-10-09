#%% Importações

def go_LISTAR_PONTOS():
       
    import pandas as pd
    from sqlalchemy import create_engine
    
    #%% Conexão
    
    server = 'M5282650\\SQLEXPRESS'
    database = 'JCIHistorianDB'
    username = 'py'
    password = 'py'
    
    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server"
    engine = create_engine(connection_string)
  
    #%% Exportação de lista de potos
    
    query = """
    
    SELECT DISTINCT PointName
    FROM [JCIHistorianDB].[dbo].[RawAnalog]
    
    """
    df = pd.read_sql(query, engine)
    
    # Exportar para CSV
    df.to_csv("Lista_Pontos.csv", index=False)
