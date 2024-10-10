
#%% Conhecendo o dataframe
def infos(df_ur):
    
    df_ur.info()
    
#%% Histograma
def histograma(df_ur,titulo):
    import matplotlib.pyplot as plt

    df_ur.drop(columns=['UTCDateTime']).hist(figsize=(10, 8), bins=40, edgecolor='black')
    plt.tight_layout()
    plt.suptitle(titulo, fontsize=16)
    plt.show()
    
#%% Dispersão par a par
def dispercao(df_ur):
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    sns.pairplot(df_ur.drop(columns=['UTCDateTime']))
    plt.show()
    
#%% Mapa de calor e correlação  
def mapacalor(df_ur):
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Definindo um tamanho maior para a figura
    plt.figure(figsize=(20, 18))  # Tamanho ajustado para ser mais largo e alto
    corr = df_ur.drop(columns=['UTCDateTime']).corr()
    
    # Criando o heatmap
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
    
    # Ajustando o título e espaçamento
    plt.title('Mapa de Calor - Correlação de df_ur', fontsize=18)
    plt.xticks(rotation=45, ha='right')  # Rotacionar os labels do eixo x para 45 graus para melhor legibilidade
    plt.yticks(rotation=0)  # Manter os labels do eixo y na horizontal
    plt.tight_layout()  # Ajusta o layout para evitar cortes nos rótulos
    
    plt.show()


#%% Boxplot analíticos
def boxplot(df_ur): 
    import matplotlib.pyplot as plt
    import seaborn as sns  
    
    #Boxplot de corrente Dia Semana
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='FimDeSemana', y='ur_correnteMotor', data=df_ur)
    plt.title('Corrente separado por FimDeSemana (0 = Dia de Semana, 1 = Fim de Semana)')
    plt.xlabel('Fim de Semana')
    plt.ylabel('Corrente')
    plt.show()
    
    #Boxplot de Delta AG Dia Semana
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='FimDeSemana', y='delta_AG', data=df_ur)
    plt.title('Delta AG separado por FimDeSemana (0 = Dia de Semana, 1 = Fim de Semana)')
    plt.xlabel('Fim de Semana')
    plt.ylabel('Delta')
    plt.show()
    
    #Boxplot de Delta AC Dia Semana
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='FimDeSemana', y='delta_AC', data=df_ur)
    plt.title('Delta AC separado por FimDeSemana (0 = Dia de Semana, 1 = Fim de Semana)')
    plt.xlabel('Fim de Semana')
    plt.ylabel('Delta')
    plt.show()
    
    #Boxplot de TR Dia Semana
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='FimDeSemana', y='TR', data=df_ur)
    plt.title('TR separado por FimDeSemana (0 = Dia de Semana, 1 = Fim de Semana)')
    plt.xlabel('Fim de Semana')
    plt.ylabel('TR')
    plt.show()
    
    #Boxplot de corrente HorarioComercial
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='HorarioComercial', y='ur_correnteMotor', data=df_ur)
    plt.title('Corrente separado por HorarioComercial (0 = Não, 1 = HorarioComercial)')
    plt.xlabel('HorarioComercial')
    plt.ylabel('Corrente')
    plt.show()
    
    #Boxplot de Delta AG HorarioComercial
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='HorarioComercial', y='delta_AG', data=df_ur)
    plt.title('Delta AG separado por HorarioComercial (0 = Não, 1 = HorarioComercial)')
    plt.xlabel('HorarioComercial')
    plt.ylabel('Delta')
    plt.show()
    
    #Boxplot de Delta AC HorarioComercial
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='HorarioComercial', y='delta_AC', data=df_ur)
    plt.title('Delta AC separado por HorarioComercial (0 = Não, 1 = HorarioComercial)')
    plt.xlabel('HorarioComercial')
    plt.ylabel('Delta')
    plt.show()
    
    #Boxplot de TR HorarioComercial
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='HorarioComercial', y='TR', data=df_ur)
    plt.title('TR separado por HorarioComercial (0 = Não, 1 = HorarioComercial)')
    plt.xlabel('HorarioComercial')
    plt.ylabel('TR')
    plt.show()
    
    #Boxplot de % VAG
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='HorarioComercial', y='VAG Predio', data=df_ur)
    plt.title('TR separado por HorarioComercial (0 = Não, 1 = HorarioComercial)')
    plt.xlabel('HorarioComercial')
    plt.ylabel('VAG %')
    plt.show()
    
    #Boxplot de % AHUs ligados
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='HorarioComercial', y='Ligados', data=df_ur)
    plt.title('TR separado por HorarioComercial (0 = Não, 1 = HorarioComercial)')
    plt.xlabel('HorarioComercial')
    plt.ylabel('AHUs ligadas %')
    plt.show()
    
    #%% Correlações
    
    # ur_correnteMotor
    ## 0.98 UR_KWH
    ## -0.61 UR_TEMP_SAIDA
    ## 0.84 ur_temp_entrada_condensacao
    ## 0.91 ur_temp_saida_condensacao
    ## 0.86 TR
    ## -0.92 delta_AC
    
    # UR_KWH
    ## -0.55 UR_TEMP_SAIDA
    ## 0.83 ur_temp_entrada_condensacao
    ## 0.9 ur_temp_saida_condensacao
    ## 0.6 temp_externa
    ## 0.86 TR
    ## -0.93 delta_AC
    
    #UR_TEMP_SAIDA
    # 0.75 delta_AG
    
    #UR_TEMP_SAIDA
    ## -0.63 ur_temp_entrada_condensacao
    ## -0.62 ur_temp_saida_condensacao
    ## -0.62 TR
    
    #ur_temp_entrada_condensacao
    ## 0.98 ur_temp_saida_condensacao
    ## 0.74 TR
    ## -0.79 delta_AC
    
    #ur_temp_saida_condensacao
    ## 0.8 TR
    ## -0.89 delta_AC
    
    #temp_externa
    ## -0.62 delta_AC
    
    #TR
    ## -0.81 delta_AC
    