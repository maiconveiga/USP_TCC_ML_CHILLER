#%% Tratamento Chiller
def tratarChiller(df):
    
    import pandas as pd
    import numpy as np
    
    print("Antes do tratamento")   
    nan_por_coluna = df.isna().sum()
    print("Valores NaN por coluna:")
    print(nan_por_coluna)
    print("--------------------------------------") 
    
    def preencher_media_vizinho_todas_colunas(df):
        # Iterar sobre cada coluna do DataFrame
        for column in df.columns:
            # Iterar sobre as linhas e substituir os valores NaN
            for i in range(1, len(df) - 1):
                if pd.isna(df.loc[i, column]):
                    # Substituir o NaN pela média entre a linha acima e a linha abaixo
                    df.loc[i, column] = (df.loc[i - 1, column] + df.loc[i + 1, column]) / 2
        return df
    
    df = preencher_media_vizinho_todas_colunas(df)
    
    # Excluir as linhas onde todas as colunas, exceto 'UTCDateTime', 'ur_kwhtr' e 'Pressao_PR_min', estão em branco
    df = df.dropna(subset=[col for col in df.columns if col not in ['UTCDateTime', 'ur_kwhtr', 'Pressao_PR_min']], how='all')

    
    df.loc[(df['ur_temp_saida'] < 0) & (df['ur_kwh'] == 0), 'ur_temp_saida'] = df['ur_temp_entrada']
    
    df.loc[df['ur_kwhtr'] < 0, 'ur_kwhtr'] = 0
    
    df['TR'] = df['ur_kwh'] / df['ur_kwhtr'] 
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df['TR'] = df['TR'].fillna(0)
    
    # inicio = pd.to_datetime(df['UTCDateTime'].min())
    
    # fim = pd.to_datetime(df['UTCDateTime'].max())
     
    # novos_horarios = pd.date_range(start=inicio, end=fim, freq='60min')
    # df_novos_horarios = pd.DataFrame(novos_horarios, columns=['UTCDateTime'])
    
    # df = pd.merge(df_novos_horarios, df, on='UTCDateTime', how='left')
 
    df['delta_AG'] = df['ur_temp_entrada'] - df['ur_temp_saida']
    df['delta_AC'] = df['ur_temp_saida_condensacao'] - df['ur_temp_entrada_condensacao']
     
    df['FimDeSemana'] = df['UTCDateTime'].apply(lambda x: 1 if x.weekday() >= 5 else 0)

    df['HorarioComercial'] = df['UTCDateTime'].apply(lambda x: 1 if 8 <= x.hour < 17 else 0)

    df = df.dropna(subset=[col for col in df.columns if col not in ['UTCDateTime', 'FimDeSemana', 'HorarioComercial']], how='all')
    
    #df = df.dropna()
    #df = df.fillna(df.median())
    print("Depois do tratamento")   
    nan_por_coluna = df.isna().sum()
    print("Valores NaN por coluna:")
    print(nan_por_coluna)
    print("--------------------------------------")     
    
    return df

#%% Tratamento fancoil
def tratarFancoil(df):
    
    print("Antes do tratamento")   
    nan_por_coluna = df.isna().sum()
    print("Valores NaN por coluna:")
    print(nan_por_coluna)
    print("--------------------------------------") 
    
    import pandas as pd

    def preencher_media_vizinho_todas_colunas(df):
        # Iterar sobre cada coluna do DataFrame
        for column in df.columns:
            # Iterar sobre as linhas e substituir os valores NaN
            for i in range(1, len(df) - 1):
                if pd.isna(df.loc[i, column]):
                    # Substituir o NaN pela média entre a linha acima e a linha abaixo
                    df.loc[i, column] = (df.loc[i - 1, column] + df.loc[i + 1, column]) / 2
        return df
    
    df = preencher_media_vizinho_todas_colunas(df)
    
    df = df.dropna(subset=[col for col in df.columns if col != 'UTCDateTime'], how='all')
 
    df['VAG Aberta %'] = (df.drop(columns=['UTCDateTime']).sum(axis=1)/(df.shape[1]-1))
    
    df['Fancoil ligado %'] =(((df.shape[1]-1) - (df.drop(columns=['UTCDateTime']).apply(lambda row: (row == 0).sum(), axis=1)))*100)/(df.shape[1]-1)
    
    #df = df.dropna()
    #df = df.fillna(df.median())
    print("Depois do tratamento")   
    nan_por_coluna = df.isna().sum()
    print("Valores NaN por coluna:")
    print(nan_por_coluna)
    print("--------------------------------------") 
    
    return df