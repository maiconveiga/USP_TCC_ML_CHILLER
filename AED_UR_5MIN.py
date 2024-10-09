#%% Importações

def go_UR_5MIN():
       
    import pandas as pd
    from sqlalchemy import create_engine
    import numpy as np
    
    #%% Conexão
    
    server = 'M5282650\\SQLEXPRESS'
    database = 'JCIHistorianDB'
    username = 'py'
    password = 'py'
    
    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server"
    engine = create_engine(connection_string)
    
    #%% Variáveis
    
    ur_temp_entrada = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-6.Present Value'
    ur_temp_saida = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-5.Present Value'
    ur_kwh = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-35.Present Value' 
    ur_kwhtr = 'S1-ADX1:S1-ADX-NAE1/Programming.UR2_KWHTR.Present Value' 
    ur_temp_entrada_condensacao = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-8.Present Value'
    ur_temp_saida_condensacao = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-7.Present Value'
    temp_externa = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-B.TC-06-03.TC-06-03 - STE.Present Value'
    ur_correnteMotor = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-29.Present Value'
    setpoint_ur = 9
    
    #%% Coleta de dados 
    
    ur_query = f"""
    
    SELECT 
        UTCDateTime,
        MAX(CASE 
            WHEN PointName = '{ur_kwh}'
            THEN ActualValue 
            ELSE NULL 
        END) AS UR_KWH,
        MAX(CASE 
            WHEN PointName = '{ur_kwhtr}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS UR_KWh_TR,
        MAX(CASE 
            WHEN PointName = '{ur_temp_entrada}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS UR_TEMP_ENTRADA,
        MAX(CASE 
            WHEN PointName = '{ur_temp_saida}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS UR_TEMP_SAIDA,
        MAX(CASE 
            WHEN PointName = '{ur_temp_entrada_condensacao}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS ur_temp_entrada_condensacao,
        MAX(CASE 
            WHEN PointName = '{ur_temp_saida_condensacao}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS ur_temp_saida_condensacao,
        MAX(CASE 
            WHEN PointName = '{temp_externa}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS temp_externa
    FROM 
        [JCIHistorianDB].[dbo].[RawAnalog]
    WHERE 
        PointName IN (
            '{ur_kwh}',
            '{ur_kwhtr}',
            '{ur_temp_entrada}',
            '{ur_temp_saida}',
            '{ur_temp_entrada_condensacao}',
            '{ur_temp_saida_condensacao}',
            '{temp_externa}' 
            
        )
    GROUP BY 
        UTCDateTime
    ORDER BY 
        UTCDateTime;
    
    """
    
    
    corrente_query = f"""
    
    SELECT 
        UTCDateTime,
        MAX(CASE 
            WHEN PointName = '{ur_correnteMotor}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS ur_correnteMotor
    FROM 
        [JCIHistorianDB].[dbo].[RawAnalog]
    WHERE 
        PointName IN (
            '{ur_correnteMotor}'    
        )
    GROUP BY 
        UTCDateTime
    ORDER BY 
        UTCDateTime;
    
    """
 
    df_ur = pd.read_sql(ur_query, engine)
    df_corrente = pd.read_sql(corrente_query, engine)

    #%% Tratando outliers
    
    df_ur.loc[(df_ur['UR_TEMP_SAIDA'] < 0) & (df_ur['UR_KWH'] == 0), 'UR_TEMP_SAIDA'] = df_ur['UR_TEMP_ENTRADA']
    df_ur = df_ur[df_ur['UR_TEMP_SAIDA'] >= 4]
    df_ur = df_ur[df_ur['UR_TEMP_ENTRADA'] >= 4]
    df_ur = df_ur[df_ur['temp_externa'] >= 10]
    df_ur = df_ur[df_ur['ur_temp_entrada_condensacao'] >= 10]
    df_ur = df_ur[df_ur['ur_temp_saida_condensacao'] >= 10] 
    
    #%% Interpolação
    
    df_ur = df_ur.interpolate(method='linear', limit_direction='both')
    
    #%% Calculo para TR
    
    df_ur['TR'] = df_ur['UR_KWH'] / df_ur['UR_KWh_TR'] 
    
    df_ur = df_ur.fillna(0)
      
    #%% Limpeza dos inf e nan
    
    df_ur.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    df_ur = df_ur.dropna()
    
    #df_ur = df_ur[~(df_ur['UR_KWH'] == 0) & (df_ur['UR_KWh_TR'] != 0)]
    
    #%% Atribuição de setpoint
    
    df_ur['Setpoint_AG'] = setpoint_ur
    
    
    #%% Ajustando a periodicidade de leitura de corrente
    
    # Definir o intervalo de tempo desejado
    inicio = pd.to_datetime('2023-06-01 03:00:00')
    
    fim = pd.to_datetime('2024-09-09 18:30:00')
    
    # Criar uma sequência de datas com intervalos de 30 minutos
    novos_horarios = pd.date_range(start=inicio, end=fim, freq='5T')
    # Criar um DataFrame vazio com a coluna 'UTCDateTime' preenchida com os novos horários
    df_novos_horarios = pd.DataFrame(novos_horarios, columns=['UTCDateTime'])
    
    # Fazer um merge entre o DataFrame original e o novo DataFrame de horários
    # Vamos usar um merge para alinhar com os dados existentes
    df_corrente['UTCDateTime'] = pd.to_datetime(df_corrente['UTCDateTime'])
    
    
    df_corrente = pd.merge(df_novos_horarios, df_corrente, on='UTCDateTime', how='left')
    df_ur2 = pd.merge(df_novos_horarios, df_ur, on='UTCDateTime', how='left')
    
    df_corrente['ur_correnteMotor'].fillna(method='ffill', inplace=True)
    df_ur2['UR_KWH'].fillna(method='ffill', inplace=True)
    df_ur2['UR_KWh_TR'].fillna(method='ffill', inplace=True)
    df_ur2['UR_TEMP_ENTRADA'].fillna(method='ffill', inplace=True)
    df_ur2['UR_TEMP_SAIDA'].fillna(method='ffill', inplace=True)
    df_ur2['ur_temp_entrada_condensacao'].fillna(method='ffill', inplace=True)
    df_ur2['ur_temp_saida_condensacao'].fillna(method='ffill', inplace=True)
    df_ur2['temp_externa'].fillna(method='ffill', inplace=True)
    df_ur2['TR'].fillna(method='ffill', inplace=True)
    df_ur2['Setpoint_AG'].fillna(method='ffill', inplace=True)
      
      
    df_ur = pd.merge(df_corrente, df_ur2, on='UTCDateTime', how='left')
       
    #%% Criando deltas
    
    df_ur['delta_AG'] = df_ur['UR_TEMP_ENTRADA'] - df_ur['UR_TEMP_SAIDA']
    df_ur['delta_AC'] = df_ur['ur_temp_saida_condensacao'] - df_ur['ur_temp_entrada_condensacao']
    
    
    #%% Criar coluna FimDeSemana
    
    df_ur['FimDeSemana'] = df_ur['UTCDateTime'].apply(lambda x: 1 if x.weekday() >= 5 else 0)
    
    #%% Horario comercial
    
    df_ur['HorarioComercial'] = df_ur['UTCDateTime'].apply(lambda x: 1 if 8 <= x.hour < 17 else 0)
    
#%% Retorno
    df_ur.to_excel('df_ur_5min.xlsx', index=False)
    return df_ur