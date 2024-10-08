def openconnection(s, d, u, p):
    from sqlalchemy import create_engine
    
    server = s
    database = d
    username = u
    password = p

    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server"
    engine = create_engine(connection_string)
    return engine

def pointlist(e):
    import pandas as pd
    engine = e
    query = """

    SELECT DISTINCT PointName
    FROM [JCIHistorianDB].[dbo].[RawAnalog]

    """
    df = pd.read_sql(query, engine)

    # Exportar para CSV
    df.to_csv("Lista_Pontos.csv", index=False)
    
def coletardados(ur_temp_entrada, ur_temp_saida, 
                 ur_kwh, ur_kwhtr, ur_temp_entrada_condensacao,
                 ur_temp_saida_condensacao,
                 temp_externa,
                 ur_correnteMotor,
                 setpoint_ur, engine):
    
    import pandas as pd
    
    ur_temp_entrada = ur_temp_entrada
    ur_temp_saida = ur_temp_saida
    ur_kwh = ur_kwh
    ur_kwhtr = ur_kwhtr
    ur_temp_entrada_condensacao = ur_temp_entrada_condensacao
    ur_temp_saida_condensacao = ur_temp_saida_condensacao
    temp_externa = temp_externa
    ur_correnteMotor =ur_correnteMotor
    setpoint_ur = setpoint_ur
    engine = engine
    
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

    v2v = """

    SELECT 
        UTCDateTime,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.QAC-1SS-02.AHU-SS1-04.AHU-SS1-04 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1SS_02_AHU_SS1_04_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.QAC-1SS-02.AHU-SS1-05.AHU-SS1-05 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1SS_02_AHU_SS1_05_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.QAC-1SS-03.AHU-SS1-01.AHU-SS1-01 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1SS_03_AHU_SS1_01_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.QAC-1SS-03.AHU-SS1-02.AHU-SS1-02 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1SS_03_AHU_SS1_02_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.QAC-1SS-03.AHU-SS1-03.AHU-SS1-03 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1SS_03_AHU_SS1_03_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-01.AHU-01-02.AHU-01-02 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1PAV_01_AHU_01_02_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-01.AHU-01-03.AHU-01-03 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1PAV_01_AHU_01_03_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-01.AHU-01-09.AHU-01-09 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1PAV_01_AHU_01_09_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-02.AHU-01-04.AHU-01-04 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1PAV_02_AHU_01_04_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-03.AHU-01-01.AHU-01-01 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1PAV_03_AHU_01_01_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-03.AHU-01-01.Setpoint V2V AHU-01-01.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1PAV_03_AHU_01_01_Setpoint_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-03.AHU-01-07.AHU-01-07 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1PAV_03_AHU_01_07_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-05.AHU-01-08.AHU-01-08 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_1PAV_05_AHU_01_08_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-01.AHU-02-01.AHU-02-01 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_2PV_01_AHU_02_01_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-01.AHU-02-02.AHU-02-02 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_2PV_01_AHU_02_02_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-02.AHU-02-04.AHU-02-04 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_2PV_02_AHU_02_04_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-03.AHU-02-05.AHU-02-05 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_2PV_03_AHU_02_05_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-03.AHU-02-07.AHU-02-07 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_2PV_03_AHU_02_07_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-03.AHU-02-07.AHU-02-07 - V2V-FB.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_2PV_03_AHU_02_07_V2V_FB,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-04.AHU-02-03.AHU-02-03 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_2PV_04_AHU_02_03_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-04.AHU-02-08.AHU-02-08 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_2PV_04_AHU_02_08_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-3PV-01.AHU-03-01.AHU-03-01 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_3PV_01_AHU_03_01_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-3PV-01.AHU-03-02.AHU-03-02 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_3PV_01_AHU_03_02_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-3PV-02.AHU-03-03.AHU-03-03 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_3PV_02_AHU_03_03_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-4PV-02.AHU-04-03.AHU-04-03 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_4PV_02_AHU_04_03_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-4PV-03.AHU-04-04.AHU-04-04 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_4PV_03_AHU_04_04_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-4PV-04.AHU-04-01.AHU-04-01 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_4PV_04_AHU_04_01_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-4PV-04.AHU-04-02.AHU-04-02 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAS_4PV_04_AHU_04_02_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-01.AHU-05-01.AHU-05-01 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_5PV_01_AHU_05_01_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-01.AHU-05-02.AHU-05-02 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_5PV_01_AHU_05_02_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-02.AHU-05-03.AHU-05-03 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_5PV_02_AHU_05_03_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-03.AHU-05-04.AHU-05-04A - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_5PV_03_AHU_05_04A_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-03.AHU-05-04.AHU-05-04A-V2VST.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_5PV_03_AHU_05_04A_V2VST,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-03.AHU-05-04.AHU-05-04B - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_5PV_03_AHU_05_04B_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-01.AHU-06-06.AHU-06-06 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_6PV_01_AHU_06_06_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-01.AHU-06-07.AHU-06-07 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_6PV_01_AHU_06_07_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-02.AHU-06-03.AHU-06-03 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_6PV_02_AHU_06_03_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-02.AHU-06-08.AHU-06-08 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_6PV_02_AHU_06_08_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-A.AHU-06-04.AHU-06-04 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_6PV_03A_AHU_06_04_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-A.AHU-06-09.AHU-06-09 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_6PV_03A_AHU_06_09_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-A.AHU-06-10.AHU-06-10 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_6PV_03A_AHU_06_10_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-B.AHU-06-10.AHU-06-10-1 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_6PV_03B_AHU_06_10_1_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-B.AHU-06-10.AHU-06-10-2 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_6PV_03B_AHU_06_10_2_V2V,
        MAX(CASE 
            WHEN PointName = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-04.AHU-06-01.AHU-06-01 - V2V.Present Value' 
            THEN ActualValue 
            ELSE NULL 
        END) AS QAC_6PV_04_AHU_06_01_V2V
    FROM 
        [JCIHistorianDB].[dbo].[RawAnalog]
    WHERE 
        PointName IN (
            'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.QAC-1SS-02.AHU-SS1-04.AHU-SS1-04 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.QAC-1SS-02.AHU-SS1-05.AHU-SS1-05 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.QAC-1SS-03.AHU-SS1-01.AHU-SS1-01 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.QAC-1SS-03.AHU-SS1-02.AHU-SS1-02 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.QAC-1SS-03.AHU-SS1-03.AHU-SS1-03 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-01.AHU-01-02.AHU-01-02 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-01.AHU-01-03.AHU-01-03 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-01.AHU-01-09.AHU-01-09 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-02.AHU-01-04.AHU-01-04 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-03.AHU-01-01.AHU-01-01 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-03.AHU-01-01.Setpoint V2V AHU-01-01.Present Value',
            'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-03.AHU-01-07.AHU-01-07 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE2/S1-ADX1-NAE2-TR1.QAC-1PAV-05.AHU-01-08.AHU-01-08 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-01.AHU-02-01.AHU-02-01 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-01.AHU-02-02.AHU-02-02 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-02.AHU-02-04.AHU-02-04 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-03.AHU-02-05.AHU-02-05 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-03.AHU-02-07.AHU-02-07 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-03.AHU-02-07.AHU-02-07 - V2V-FB.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-04.AHU-02-03.AHU-02-03 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-2PV-04.AHU-02-08.AHU-02-08 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-3PV-01.AHU-03-01.AHU-03-01 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-3PV-01.AHU-03-02.AHU-03-02 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-3PV-02.AHU-03-03.AHU-03-03 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-4PV-02.AHU-04-03.AHU-04-03 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-4PV-03.AHU-04-04.AHU-04-04 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-4PV-04.AHU-04-01.AHU-04-01 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE3/S1-ADX1-NAE3-TR1.QAS-4PV-04.AHU-04-02.AHU-04-02 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-01.AHU-05-01.AHU-05-01 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-01.AHU-05-02.AHU-05-02 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-02.AHU-05-03.AHU-05-03 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-03.AHU-05-04.AHU-05-04A - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-03.AHU-05-04.AHU-05-04A-V2VST.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-5PV-03.AHU-05-04.AHU-05-04B - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-01.AHU-06-06.AHU-06-06 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-01.AHU-06-07.AHU-06-07 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-02.AHU-06-03.AHU-06-03 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-02.AHU-06-08.AHU-06-08 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-A.AHU-06-04.AHU-06-04 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-A.AHU-06-09.AHU-06-09 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-A.AHU-06-10.AHU-06-10 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-B.AHU-06-10.AHU-06-10-1 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-B.AHU-06-10.AHU-06-10-2 - V2V.Present Value',
            'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-04.AHU-06-01.AHU-06-01 - V2V.Present Value'
        )
    GROUP BY 
        UTCDateTime
    ORDER BY 
        UTCDateTime;
    """

    df_ur = pd.read_sql(ur_query, engine)
    df_corrente = pd.read_sql(corrente_query, engine)
    v2v = pd.read_sql(v2v, engine)
    return df_ur, df_corrente, v2v

def tratamento(df_ur, setpoint_ur, df_corrente):
    
    import numpy as np
    import pandas as pd
    import holidays
    
    #Interpolação
    df_ur = df_ur.interpolate(method='linear', limit_direction='both')
    #Calculo para TR
    df_ur['TR'] = df_ur['UR_KWH'] / df_ur['UR_KWh_TR'] 
    #Preencher os valores em branco
    df_ur = df_ur.fillna(0)
    #Limpeza de valores negativos
    df_ur = df_ur[df_ur['UR_TEMP_SAIDA'] >= 4]
    #Limpeza dos inf e nan
    df_ur.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_ur = df_ur.dropna()
    #Atribuição de setpoint
    df_ur['Setpoint_AG'] = setpoint_ur
    
    #%% Ajustando a periodicidade de leitura de corrente

    # Definir o intervalo de tempo desejado
    inicio = pd.to_datetime('2023-06-01 03:00:00')
    fim = pd.to_datetime('2024-09-09 18:30:00')

    # Criar uma sequência de datas com intervalos de 5 minutos
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
    df_ur['delta_AC'] = df_ur['ur_temp_entrada_condensacao'] - df_ur['ur_temp_saida_condensacao']

    #%% Criar coluna FimDeSemana

    df_ur['FimDeSemana'] = df_ur['UTCDateTime'].apply(lambda x: 1 if x.weekday() >= 5 else 0)

    #%% Horario comercial

    df_ur['HorarioComercial'] = df_ur['UTCDateTime'].apply(lambda x: 1 if 8 <= x.hour < 17 else 0)

    #%% Feriados

    # Função para verificar se a data é um feriado nacional ou estadual
    def verifica_feriado(data):
        feriados_brasil = holidays.Brazil(years=[2023, 2024])
        feriados_rj = holidays.Brazil(years=[2023, 2024], subdiv='RJ')
        if data in feriados_brasil or data in feriados_rj:
            return 1  # Feriado
        else:
            return 0  # Não é feriado

    # Aplicando a função ao DataFrame
    df_ur['Feriado'] = df_ur['UTCDateTime'].apply(verifica_feriado)

    return df_ur