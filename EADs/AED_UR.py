#%% Importações

def getUR():
    
    import pandas as pd
    import numpy as np
    from UTILS import conexaoBanco
    
    #%% Conexão
    
    engine = conexaoBanco()
    
    #%% Variáveis
    
    df_title = pd.read_excel('Dados BMS/Lista_Pontos_Chiller.xlsx')
    
    ur_temp_entrada = df_title.iloc[0,0]
    ur_temp_saida = df_title.iloc[1,0]
    ur_kwh = df_title.iloc[2,0]
    ur_kwhtr = df_title.iloc[3,0]
    ur_temp_entrada_condensacao = df_title.iloc[4,0]
    ur_temp_saida_condensacao = df_title.iloc[5,0]
    ur_correnteMotor = df_title.iloc[6,0]
    temp_externa = df_title.iloc[7,0]

 
    
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
    
    #%% Calculo para TR
    
    df_ur['TR'] = df_ur['UR_KWH'] / df_ur['UR_KWh_TR'] 
    
    df_ur = df_ur.fillna(0)
    
    #%% Limpeza dos inf e nan
    
    df_ur.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    df_ur = df_ur.dropna()

    #%% Ajustando a periodicidade de leitura de corrente

    inicio = pd.to_datetime(df_ur['UTCDateTime'].min())
    
    fim = pd.to_datetime(df_ur['UTCDateTime'].max())
     
    novos_horarios = pd.date_range(start=inicio, end=fim, freq='30min')
    df_novos_horarios = pd.DataFrame(novos_horarios, columns=['UTCDateTime'])
    df_corrente['UTCDateTime'] = pd.to_datetime(df_corrente['UTCDateTime'])
    df_corrente = pd.merge(df_novos_horarios, df_corrente, on='UTCDateTime', how='left')
    df_ur = pd.merge(df_corrente, df_ur, on='UTCDateTime', how='left')
    df_ur = df_ur.dropna()
    
    
    #%% Criando deltas
    
    df_ur['delta_AG'] = df_ur['UR_TEMP_ENTRADA'] - df_ur['UR_TEMP_SAIDA']
    df_ur['delta_AC'] = df_ur['ur_temp_saida_condensacao'] - df_ur['ur_temp_entrada_condensacao']
    
    #%% Criar coluna FimDeSemana
    
    df_ur['FimDeSemana'] = df_ur['UTCDateTime'].apply(lambda x: 1 if x.weekday() >= 5 else 0)
    
    #%% Horario comercial
    
    df_ur['HorarioComercial'] = df_ur['UTCDateTime'].apply(lambda x: 1 if 8 <= x.hour < 17 else 0)
    
#%% Retorno
    df_ur.to_csv('Dados BMS\df_UR.csv', index=False)
    return df_ur