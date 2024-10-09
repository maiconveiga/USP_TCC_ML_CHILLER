#%% Importações

def go_AHU_VAG():
       
    import pandas as pd
    from sqlalchemy import create_engine
    
    #%% Conexão
    
    server = 'M5282650\\SQLEXPRESS'
    database = 'JCIHistorianDB'
    username = 'py'
    password = 'py'
    
    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server"
    engine = create_engine(connection_string)
    
    del server
    del database
    del username
    del password
    del connection_string
    
    #%% Variáveis
    
    
    
    #%% Coleta de dados 
    
    AHU_VAG_query = """
    
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

    df_AHU_VAG = pd.read_sql(AHU_VAG_query, engine)
    
    #%% Trabalhando com o bd V2V
    
    df_AHU_VAG.info()
    return df_AHU_VAG
    # Precisamos saber:
    #  % de AHUS funcionando
    #  % de VAGs abertas (Somar todas as VAGs)