
#%% Conhecendo o dataframe
def infos(df_ur):
    
    df_ur.info()
    
#%% Histograma
def histograma(df_ur):
    import matplotlib.pyplot as plt

    df_ur.drop(columns=['UTCDateTime','FimDeSemana','HorarioComercial']).hist(figsize=(10, 8), bins=40, edgecolor='black')
    plt.tight_layout()
    plt.show()
    
#%% Dispersão par a par
def dispercao(df_ur):
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    sns.pairplot(df_ur.drop(columns=['UTCDateTime','FimDeSemana','HorarioComercial']))
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
    plt.title('Mapa de Calor - Correlação de df_ur', fontsize=16)
    plt.xticks(rotation=45, ha='right')  # Rotacionar os labels do eixo x para 45 graus para melhor legibilidade
    plt.yticks(rotation=0)  # Manter os labels do eixo y na horizontal
    plt.tight_layout()  # Ajusta o layout para evitar cortes nos rótulos
    
    plt.show()


#%% Boxplot analíticos
def boxplot(df):

    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Definir estilo e cores mais sofisticadas usando seaborn
    sns.set(style="whitegrid")
    
    # Excluir as colunas 'UTCDateTime' e 'Setpoint_AG', se existirem
    df = df.drop(columns=['UTCDateTime','HorarioComercial','FimDeSemana'], errors='ignore')
    
    # Criar um boxplot mais estilizado para cada coluna separadamente
    for column in df.columns:
        plt.figure(figsize=(4, 4))
        # Usar seaborn para gerar o boxplot com mais controle visual
        sns.boxplot(data=df[column], color="skyblue", linewidth=2.5)
        
        # Adicionar título e rótulo com mais formatação
        plt.title(f'Boxplot de {column}', fontsize=16, fontweight='bold')
        plt.ylabel(column, fontsize=9)
        
        # Melhorar a rotação e a formatação dos rótulos no eixo x (se houver)
        plt.xticks(rotation=0, fontsize=10)
        
        # Adicionar grid suave
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Exibir o gráfico
        plt.show()

def printModelStats(df, titulo):
    import matplotlib.pyplot as plt

    df = df.round(3)

    fig, ax = plt.subplots(figsize=(6, 3))  # Ajuste o tamanho da figura se necessário

    ax.axis('tight')
    ax.axis('off')

    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)
    
    
    plt.title(titulo, fontsize=16, pad=20)


    plt.savefig('dataframe_image.png', bbox_inches='tight', dpi=300)

    # Exibir a tabela
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
    