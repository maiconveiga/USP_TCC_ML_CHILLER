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
    Pressao_PR_min = df_title.iloc[7,0]
    
    #%% Coleta de dados 

    
    ur_query = f"""
    
    SELECT 
        UTCDateTime,
        MAX(CASE 
            WHEN PointName = '{ur_temp_entrada}'
            THEN ActualValue 
            ELSE NULL 
        END) AS ur_temp_entrada,
        MAX(CASE 
            WHEN PointName = '{ur_temp_saida}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS ur_temp_saida,
        MAX(CASE 
            WHEN PointName = '{ur_kwh}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS ur_kwh,
        MAX(CASE 
            WHEN PointName = '{ur_kwhtr}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS ur_kwhtr,
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
            WHEN PointName = '{ur_correnteMotor}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS ur_correnteMotor,
        MAX(CASE 
            WHEN PointName = '{Pressao_PR_min}' 
            THEN ActualValue 
            ELSE NULL 
        END) AS Pressao_PR_min
    FROM 
        [JCIHistorianDB].[dbo].[RawAnalog]
    WHERE 
        PointName IN (
            '{ur_temp_entrada}',
            '{ur_temp_saida}',
            '{ur_kwh}',
            '{ur_kwhtr}',
            '{ur_temp_entrada_condensacao}',
            '{ur_temp_saida_condensacao}',
            '{ur_correnteMotor}',
            '{Pressao_PR_min}'        
        )
    GROUP BY 
        UTCDateTime
    ORDER BY 
        UTCDateTime;
    
    """

    df_ur = pd.read_sql(ur_query, engine)

    #%% Tratando outliers
    
    df_ur['ur_kwh'] = df_ur['ur_kwh'].ffill()
    df_ur['ur_kwhtr'] = df_ur['ur_kwhtr'].ffill()
    df_ur.loc[(df_ur['ur_temp_saida'] < 0) & (df_ur['ur_kwh'] == 0), 'ur_temp_saida'] = df_ur['ur_temp_entrada']

    df_ur['ur_temp_saida'] = df_ur['ur_temp_saida'].ffill()
    df_ur['ur_temp_entrada'] = df_ur['ur_temp_entrada'].ffill()
    df_ur['ur_temp_entrada_condensacao'] = df_ur['ur_temp_entrada_condensacao'].ffill()
    df_ur['ur_temp_saida_condensacao'] = df_ur['ur_temp_saida_condensacao'].ffill()
    df_ur['ur_correnteMotor'] = df_ur['ur_correnteMotor'].ffill()
    df_ur['Pressao_PR_min'] = df_ur['Pressao_PR_min'].ffill()

    df_ur.info()
    #%% Calculo para TR
    
    df_ur['TR'] = df_ur['ur_kwh'] / df_ur['ur_kwhtr'] 
    df_ur.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_ur['TR'] = df_ur['TR'].fillna(0)


    #%% Ajustando a periodicidade de leitura de corrente

    inicio = pd.to_datetime(df_ur['UTCDateTime'].min())
    
    fim = pd.to_datetime(df_ur['UTCDateTime'].max())
     
    novos_horarios = pd.date_range(start=inicio, end=fim, freq='30min')
    df_novos_horarios = pd.DataFrame(novos_horarios, columns=['UTCDateTime'])
    
    df_ur = pd.merge(df_novos_horarios, df_ur, on='UTCDateTime', how='left')
    
    #df_ur = df_ur.dropna()
    
    #%% Criando deltas
    
    df_ur['delta_AG'] = df_ur['ur_temp_entrada'] - df_ur['ur_temp_saida']
    df_ur['delta_AC'] = df_ur['ur_temp_saida_condensacao'] - df_ur['ur_temp_entrada_condensacao']
    #%% Criar coluna FimDeSemana
    
    df_ur['FimDeSemana'] = df_ur['UTCDateTime'].apply(lambda x: 1 if x.weekday() >= 5 else 0)
    
    #%% Horario comercial
    
    df_ur['HorarioComercial'] = df_ur['UTCDateTime'].apply(lambda x: 1 if 8 <= x.hour < 17 else 0)
    
#%% Retorno
    #df_ur.to_csv('Dados BMS\df_UR.csv', index=False)
    return df_ur