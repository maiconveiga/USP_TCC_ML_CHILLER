#%% Main

from connection import openconnection
from connection import pointlist
from connection import coletardados
from connection import tratamento

server = 'M5282650\\SQLEXPRESS'
database = 'JCIHistorianDB'
username = 'py'
password = 'py'

ur_temp_entrada = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-6.Present Value'
ur_temp_saida = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-5.Present Value'
ur_kwh = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-35.Present Value' 
ur_kwhtr = 'S1-ADX1:S1-ADX-NAE1/Programming.UR2_KWHTR.Present Value' 
ur_temp_entrada_condensacao = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-8.Present Value'
ur_temp_saida_condensacao = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-7.Present Value'
temp_externa = 'S1-ADX1:S1-ADX-NAE4/S1-ADX1-NAE4-TR1.QAC-6PV-03-B.TC-06-03.TC-06-03 - STE.Present Value'
ur_correnteMotor = 'S1-ADX1:S1-ADX-NAE1/S1-ADX1-NAE1-TR1.Chiller 2.Analog Values.AV-29.Present Value'
setpoint_ur = 9

engine = openconnection(server, database, username, password)

pointlist(engine)

df_ur, df_corrente, v2v = coletardados(ur_temp_entrada, ur_temp_saida, 
                 ur_kwh, ur_kwhtr, ur_temp_entrada_condensacao,
                 ur_temp_saida_condensacao,
                 temp_externa,
                 ur_correnteMotor,
                 setpoint_ur, engine)

df_ur = tratamento(df_ur, setpoint_ur, df_corrente)

#%% Deletar variáveis

del server 
del database 
del username 
del password 

del ur_temp_entrada
del ur_temp_saida 
del ur_kwh 
del ur_kwhtr
del ur_temp_entrada_condensacao
del ur_temp_saida_condensacao 
del temp_externa 
del ur_correnteMotor 
del setpoint_ur
del engine
