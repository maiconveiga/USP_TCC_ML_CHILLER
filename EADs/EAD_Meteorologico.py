def DadosMeteorologicos(df):
    
    #%% Importações    
    import pandas as pd
    
    #%% Leitura do arquivo    
    df_meteo = pd.read_excel('Dados meteorologicos/meteo.xlsx')
    
    #%% Criação da coluna UTCDateTime
    df_meteo['Data'] = df_meteo['Data'].astype(str)
    df_meteo['Hora UTC'] = df_meteo['Hora UTC'].astype(str)
    
    df_meteo['Data'] = pd.to_datetime(df_meteo['Data'] + ' ' + df_meteo['Hora UTC'])
    
    df_meteo = df_meteo.rename(columns={'Data': 'UTCDateTime'})
    df_meteo['UTCDateTime'] = pd.to_datetime(df_meteo['UTCDateTime'])
    
    #%% Deletado dolunas que não serão úteis
    df_meteo = df_meteo.drop(columns=['Hora UTC'])
    df_meteo = df_meteo.drop(columns=['RADIACAO GLOBAL (Kj/m²)'])
    df_meteo = df_meteo.drop(columns=['VENTO, DIREÇÃO HORARIA (gr) (° (gr))'])
    df_meteo = df_meteo.drop(columns=['TEMPERATURA DO PONTO DE ORVALHO (°C)'])
    df_meteo = df_meteo.drop(columns=['TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)'])
    df_meteo = df_meteo.drop(columns=['TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)'])
    df_meteo = df_meteo.drop(columns=['VENTO, RAJADA MAXIMA (m/s)'])
    df_meteo = df_meteo.drop(columns=['VENTO, VELOCIDADE HORARIA (m/s)'])
    df_meteo = df_meteo.drop(columns=['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'])

    #%% Renomeado colunas
    df_meteo = df_meteo.rename(columns={'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)': 'Pressao (mB)'})
    df_meteo = df_meteo.rename(columns={'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'Temperatura (°C)'})
    df_meteo = df_meteo.rename(columns={'Data': 'UTCDateTime'})
    df_meteo = df_meteo.rename(columns={'UMIDADE RELATIVA DO AR, HORARIA (%)': 'Umidade (%)'})
    
    #%% Criação de calendário de acordo com o que temos de informação BMS
    inicio = pd.to_datetime('2023-06-01 03:00:00')
    
    fim = pd.to_datetime('2024-09-09 03:00:00')
    
    # Criar uma sequência de datas com intervalos de 30 minutos
    novos_horarios = pd.date_range(start=inicio, end=fim, freq='30T')
    # Criar um DataFrame vazio com a coluna 'UTCDateTime' preenchida com os novos horários
    df_novos_horarios = pd.DataFrame(novos_horarios, columns=['UTCDateTime'])
    
    df_meteo = pd.merge(df_novos_horarios, df_meteo, on='UTCDateTime', how='left')
    
    #%% Tratando dados faltantes
    
    df_meteo['Pressao (mB)'] = df_meteo['Pressao (mB)'].fillna(
        (df_meteo['PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)'].shift(-1) + 
         df_meteo['PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)'].shift(-1)) / 2
    )
    
    df_meteo['Temperatura (°C)'] = df_meteo['Temperatura (°C)'].fillna(
        (df_meteo['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].shift(-1) + 
         df_meteo['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'].shift(-1)) / 2
    )
    
    df_meteo['Umidade (%)'] = df_meteo['Umidade (%)'].fillna(
        (df_meteo['UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)'].shift(-1) + 
         df_meteo['UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)'].shift(-1)) / 2
    )
    
    df_meteo['Temperatura (°C)'] = df_meteo['Temperatura (°C)'].fillna(
        (df_meteo['Temperatura (°C)'].shift(1) + df_meteo['Temperatura (°C)'].shift(-1)) / 2
    )
    
    df_meteo['Pressao (mB)'] = df_meteo['Pressao (mB)'].fillna(
        (df_meteo['Pressao (mB)'].shift(1) + df_meteo['Pressao (mB)'].shift(-1)) / 2
    )
    
    df_meteo = df_meteo.drop(columns=['PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)'])
    df_meteo = df_meteo.drop(columns=['PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)'])
    df_meteo = df_meteo.drop(columns=['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'])
    df_meteo = df_meteo.drop(columns=['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'])
    df_meteo = df_meteo.drop(columns=['UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)'])
    df_meteo = df_meteo.drop(columns=['UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)'])
    

    #%% Copia de dataframe sem dados faltantes e join com o dataframe final
    
    df_SemNA = df_meteo.dropna()
    
    df_SemNA['UTCDateTime'] = pd.to_datetime(df_SemNA['UTCDateTime'], errors='coerce')
    df['UTCDateTime'] = pd.to_datetime(df['UTCDateTime'], errors='coerce')
    
    df_merged = pd.merge(df_SemNA, df, on='UTCDateTime', how='inner')
    #df_merged.to_excel('df.xlsx', index=False)
    df_merged.to_csv('Dados BMS\df_UR.csv')
    return df_merged
