# -*- coding: utf-8 -*-
#SQL

import sqlite3
import time
import datetime
import math

pi = math.pi

connection = sqlite3.connect('banco/bdConfiguration.db', check_same_thread = False)
c = connection.cursor()

VETOR_134 = [[0.070,0.070,2],
             [0.070,0.210,4],
             [0.105,0.315,4],
             [0.020,0.020,2],
             [0.020,0.040,3],
             [0.020,0.060,4],
             [0.035,0.035,2],
             [0.035,0.070,3],
             [0.035,0.105,4],
             [0.050,0.050,2],
             [0.050,0.100,3],
             [0.050,0.150,4],
             [0.070,0.070,2],
             [0.070,0.140,3],
             [0.070,0.210,4],
             [0.105,0.105,2],
             [0.105,0.210,3],
             [0.105,0.315,4],
             [0.140,0.140,2],
             [0.140,0.280,3],
             [0.140,0.420,4]]

VETOR_179 = [[0.030,0.030,2],
             [0.040,0.040,2],
             [0.040,0.080,3],
             [0.040,0.120,4],
             [0.080,0.080,2],
             [0.080,0.160,3],
             [0.080,0.240,4],
             [0.120,0.120,2],
             [0.120,0.240,3],
             [0.120,0.360,4]]

VETOR_181 = [0.1,0.2,0.3,0.4,0.5]

######################################################################################
################################### INICIAL ##########################################
######################################################################################
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS s1s2 (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, C0 real, I1 text, A1 real, B1 real, C1 real)")
    c.execute("CREATE TABLE IF NOT EXISTS s3s4 (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, C0 real, I1 text, A1 real, B1 real, C1 real)")
    c.execute("CREATE TABLE IF NOT EXISTS d1 (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, C0 text, I1 text, A1 real, B1 real, C1 text)")
    c.execute("CREATE TABLE IF NOT EXISTS d2 (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, C0 text, I1 text, A1 real, B1 real, C1 text)")
    c.execute("CREATE TABLE IF NOT EXISTS mt (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, C0 text)")
    c.execute("CREATE TABLE IF NOT EXISTS config134 (id INTEGER PRIMARY KEY AUTOINCREMENT, cicloCOND int, cicloMR int, erro int, DPacum int)")
    c.execute("CREATE TABLE IF NOT EXISTS config179 (id INTEGER PRIMARY KEY AUTOINCREMENT, cicloCOND int, cicloDP int)")
    c.execute("CREATE TABLE IF NOT EXISTS config181 (id INTEGER PRIMARY KEY AUTOINCREMENT, cicloMR int, erro int)")
    c.execute("CREATE TABLE IF NOT EXISTS Quadro134 (id INTEGER PRIMARY KEY AUTOINCREMENT, sigma3 real, sigmad real, Razaosigma1sigma3 real)")
    c.execute("CREATE TABLE IF NOT EXISTS Quadro179 (id INTEGER PRIMARY KEY AUTOINCREMENT, sigma3 real, sigmad real, Razaosigma1sigma3 real)")
    c.execute("CREATE TABLE IF NOT EXISTS Quadro181 (id INTEGER PRIMARY KEY AUTOINCREMENT, sigma1 real)")
    c.execute("CREATE TABLE IF NOT EXISTS cilindro (id INTEGER PRIMARY KEY AUTOINCREMENT, A1 real)")

def data_entry():
    try:
        i = 0
        while i < len(VETOR_134):
            c.execute("INSERT INTO Quadro134 (id, sigma3, sigmad, Razaosigma1sigma3) VALUES (?, ?, ?, ?)", (i+1, VETOR_134[i][0], VETOR_134[i][1], VETOR_134[i][2]))
            i+=1
        j = 0
        while j < len(VETOR_179):
            c.execute("INSERT INTO Quadro179 (id, sigma3, sigmad, Razaosigma1sigma3) VALUES (?, ?, ?, ?)", (j+1, VETOR_179[j][0], VETOR_179[j][1], VETOR_179[j][2]))
            j+=1
        k = 0
        while k < len(VETOR_181):
            c.execute("INSERT INTO Quadro181 (id, sigma1) VALUES (?, ?)", (k+1, VETOR_181[k],))
            k+=1
        c.execute("INSERT INTO s1s2 (id, I0, A0, B0, C0, I1, A1, B1, C1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (0, 'P2019113442', -0.0004, 25.394, 25, 'P2019113443', -0.0004, 25.369, 25))
        c.execute("INSERT INTO s3s4 (id, I0, A0, B0, C0, I1, A1, B1, C1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (0, 'P2019113340', -0.0002, 11.447, 10, 'P2019113446', -0.0002, 11.362, 10))
        c.execute("INSERT INTO d1 (id, I0, A0, B0, C0, I1, A1, B1, C1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (0, 'DIN1_INPUT', 0.6153, 16.281, '', 'DIN1_OUTPUT', 0.0002, 0.0112, ''))
        c.execute("INSERT INTO d2 (id, I0, A0, B0, C0, I1, A1, B1, C1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (0, 'DIN2_INPUT', 2.7566, 12.500, '', 'DIN2_OUTPUT', 0.0001,-0.1325, ''))
        c.execute("INSERT INTO mt (id, I0, A0, B0, C0) VALUES (?, ?, ?, ?, ?)", (0, 'MOTOR_DE_PASSOS', 2.0677, 10.01, ''))
        c.execute("INSERT INTO config134 (id, cicloCOND, cicloMR, erro, DPacum) VALUES (?, ?, ?, ?, ?)", (0, 500, 10, 5, 5))
        c.execute("INSERT INTO config179 (id, cicloCOND, cicloDP) VALUES (?, ?, ?)", (0, 50, 150000))
        c.execute("INSERT INTO config181 (id, cicloMR, erro) VALUES (?, ?, ?)", (0, 50, 5))
        c.execute("INSERT INTO cilindro (id, A1) VALUES (?, ?)", (0, 7853.98163397))
        connection.commit()
    except Exception:
        pass

create_table()
data_entry()

######################################################################################
############################# CALIBRAÇÕES DOS SENSORES ###############################
######################################################################################
'''Atualiza os dados I, A e B de Calibração dos sensores S1 e S2'''
def update_dados_S1S2(i0, a0, b0, c0, i1, a1, b1, c1):
    id = 0;
    c.execute("UPDATE s1s2 SET I0 = ? WHERE id = ?", (i0, id,))
    c.execute("UPDATE s1s2 SET A0 = ? WHERE id = ?", (a0, id,))
    c.execute("UPDATE s1s2 SET B0 = ? WHERE id = ?", (b0, id,))
    c.execute("UPDATE s1s2 SET C0 = ? WHERE id = ?", (c0, id,))
    c.execute("UPDATE s1s2 SET I1 = ? WHERE id = ?", (i1, id,))
    c.execute("UPDATE s1s2 SET A1= ? WHERE id = ?", (a1, id,))
    c.execute("UPDATE s1s2 SET B1 = ? WHERE id = ?", (b1, id,))
    c.execute("UPDATE s1s2 SET C1 = ? WHERE id = ?", (c1, id,))
    connection.commit()

'''Atualiza os dados I, A e B de Calibração dos sensores S3 e S4'''
def update_dados_S3S4(i0, a0, b0, c0, i1, a1, b1, c1):
    id = 0;
    c.execute("UPDATE s3s4 SET I0 = ? WHERE id = ?", (i0, id,))
    c.execute("UPDATE s3s4 SET A0 = ? WHERE id = ?", (a0, id,))
    c.execute("UPDATE s3s4 SET B0 = ? WHERE id = ?", (b0, id,))
    c.execute("UPDATE s3s4 SET C0 = ? WHERE id = ?", (c0, id,))
    c.execute("UPDATE s3s4 SET I1 = ? WHERE id = ?", (i1, id,))
    c.execute("UPDATE s3s4 SET A1= ? WHERE id = ?", (a1, id,))
    c.execute("UPDATE s3s4 SET B1 = ? WHERE id = ?", (b1, id,))
    c.execute("UPDATE s3s4 SET C1 = ? WHERE id = ?", (c1, id,))
    connection.commit()

'''Retorna uma lista as variaveis I, A e B de Calibração dos sensores S1 e S2'''
def S1S2():
    list = []

    for row in c.execute('SELECT * FROM s1s2'):
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
        list.append(row[5])
        list.append(row[6])
        list.append(row[7])
        list.append(row[8])

    return list

'''Retorna uma lista as variaveis I, A e B de Calibração dos sensores S3 e S4'''
def S3S4():
    list = []

    for row in c.execute('SELECT * FROM s3s4'):
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
        list.append(row[5])
        list.append(row[6])
        list.append(row[7])
        list.append(row[8])

    return list

######################################################################################
######################## CALIBRAÇÕES DAS VÁLVULAS PNEUMÁTICAS ########################
######################################################################################
'''Atualiza os dados I, A e B de Calibração da Válvula Dinâmica 1'''
def update_dados_D1(i0, a0, b0, c0, i1, a1, b1, c1):
    id = 0;
    c.execute("UPDATE d1 SET I0 = ? WHERE id = ?", (i0, id,))
    c.execute("UPDATE d1 SET A0 = ? WHERE id = ?", (a0, id,))
    c.execute("UPDATE d1 SET B0 = ? WHERE id = ?", (b0, id,))
    c.execute("UPDATE d1 SET C0 = ? WHERE id = ?", (c0, id,))
    c.execute("UPDATE d1 SET I1 = ? WHERE id = ?", (i1, id,))
    c.execute("UPDATE d1 SET A1= ? WHERE id = ?", (a1, id,))
    c.execute("UPDATE d1 SET B1 = ? WHERE id = ?", (b1, id,))
    c.execute("UPDATE d1 SET C1 = ? WHERE id = ?", (c1, id,))
    connection.commit()

'''Atualiza os dados I, A e B de Calibração da Válvula Dinâmica 2'''
def update_dados_D2(i0, a0, b0, c0, i1, a1, b1, c1):
    id = 0;
    c.execute("UPDATE d2 SET I0 = ? WHERE id = ?", (i0, id,))
    c.execute("UPDATE d2 SET A0 = ? WHERE id = ?", (a0, id,))
    c.execute("UPDATE d2 SET B0 = ? WHERE id = ?", (b0, id,))
    c.execute("UPDATE d2 SET C0 = ? WHERE id = ?", (c0, id,))
    c.execute("UPDATE d2 SET I1 = ? WHERE id = ?", (i1, id,))
    c.execute("UPDATE d2 SET A1= ? WHERE id = ?", (a1, id,))
    c.execute("UPDATE d2 SET B1 = ? WHERE id = ?", (b1, id,))
    c.execute("UPDATE d2 SET C1 = ? WHERE id = ?", (c1, id,))
    connection.commit()

'''Retorna uma lista as variaveis I, A e B de Calibração da Válvula Dinâmica 1'''
def DadosD1():
    list = []

    for row in c.execute('SELECT * FROM d1'):
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
        list.append(row[5])
        list.append(row[6])
        list.append(row[7])
        list.append(row[8])

    return list

'''Retorna uma lista as variaveis I, A e B de Calibração da Válvula Dinâmica 2'''
def DadosD2():
    list = []

    for row in c.execute('SELECT * FROM d2'):
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
        list.append(row[5])
        list.append(row[6])
        list.append(row[7])
        list.append(row[8])

    return list

######################################################################################
############################ CALIBRAÇÃO DO MOTOR DE PASSOS ###########################
######################################################################################
'''Atualiza os dados I, A e B de Calibração do motor de passos'''
def update_dados_MT(i0, a0, b0, c0):
    id = 0;
    c.execute("UPDATE mt SET I0 = ? WHERE id = ?", (i0, id,))
    c.execute("UPDATE mt SET A0 = ? WHERE id = ?", (a0, id,))
    c.execute("UPDATE mt SET B0 = ? WHERE id = ?", (b0, id,))
    c.execute("UPDATE mt SET C0 = ? WHERE id = ?", (c0, id,))
    connection.commit()

'''Retorna uma lista com as variaveis I, A e B de Calibração do motor de passos'''
def DadosMT():
    list = []

    for row in c.execute('SELECT * FROM mt'):
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
    return list

######################################################################################
################################# CILINDRO DE PRESSÃO ################################
######################################################################################
'''Atualiza a área do cilindro em mm²'''
def update_dados_CL(A1):
    id = 0;
    c.execute("UPDATE cilindro SET A1 = ? WHERE id = ?", (A1, id,))
    connection.commit()

'''Retorna a área do cilindro em mm²'''
def DadosCL():
    list = []
    for row in c.execute('SELECT * FROM cilindro'):
        list.append(row[1])
    
    return list[0]

######################################################################################
###################################  DNIT 134  #######################################
######################################################################################
'''Atualiza a lista das pressões do DNIT 134'''
def update_QD_134(VETOR):
    i = 0
    while i < len(VETOR):
        c.execute("UPDATE Quadro134 SET sigma3 = ? WHERE id = ?", (VETOR[i][0], i+1,))
        c.execute("UPDATE Quadro134 SET sigmad = ? WHERE id = ?", (VETOR[i][1], i+1,))
        c.execute("UPDATE Quadro134 SET Razaosigma1sigma3 = ? WHERE id = ?", (VETOR[i][2], i+1,))
        i+=1
    connection.commit()

'''Cria um lista com as pressões do DNIT 134 modificado'''
def QD_134_MOD():
    l = []
    list = []
    listCOND = []
    listMR = []
    i = 0
    for row in c.execute('SELECT * FROM Quadro134'):
        l.append(row[1])
        l.append(row[2]+row[1])
        list.append(l)
        if i == 2:
            listCOND = list
            list = []
        if i > 2:
            listMR.append(l)
            list = []
        i+=1
        l = []

    return listCOND, listMR

'''Cria um lista com as pressões do DNIT 134'''
def QD_134():
    l = []
    list = []
    listCOND = []
    listMR = []

    i = 0
    j = 0
    for row in c.execute('SELECT * FROM Quadro134'):
        l.append(row[1])
        l.append(row[2])
        l.append(row[3])
        list.append(l)
        l = []
        if i == 2:
            i = -1
            if j == 0:
                listCOND = list
                list = []
            j+=1
            if j > 1:
                listMR.append(list)
                list = []
        i+=1
    return listCOND, listMR

'''Atualiza as configurações do ensaio DNIT 134'''
def update_dados_CONFIG_134(CICLOCOND, CICLOMR, ERRO, DP_ACUM):
    id = 0;
    c.execute("UPDATE config134 SET cicloCOND = ? WHERE id = ?", (CICLOCOND, id,))
    c.execute("UPDATE config134 SET cicloMR = ? WHERE id = ?", (CICLOMR, id,))
    c.execute("UPDATE config134 SET erro = ? WHERE id = ?", (ERRO, id,))
    c.execute("UPDATE config134 SET DPacum = ? WHERE id = ?", (DP_ACUM, id,))
    connection.commit()

'''Retorna uma lista as variaveis de configurações do DNIT 134'''
def CONFIG_134():
    list = []

    for row in c.execute('SELECT * FROM config134'):
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])

    return list

######################################################################################
###################################  DNIT 135  #######################################
######################################################################################
'''Funções referente a 135 aqui...'''

######################################################################################
###################################  DNIT 179  #######################################
######################################################################################
'''Atualiza a lista das pressões do DNIT 179'''
def update_QD_179(VETOR):
    i = 0
    while i < len(VETOR):
        c.execute("UPDATE Quadro179 SET sigma3 = ? WHERE id = ?", (VETOR[i][0], i+1,))
        c.execute("UPDATE Quadro179 SET sigmad = ? WHERE id = ?", (VETOR[i][1], i+1,))
        c.execute("UPDATE Quadro179 SET Razaosigma1sigma3 = ? WHERE id = ?", (VETOR[i][2], i+1,))
        i+=1
    connection.commit()

'''Cria um lista com os pares de tensão do DNIT 179'''
def Pares_Tensoes():
    l = []
    j = 0
    for row in c.execute('SELECT * FROM Quadro179'):
        if j == 0:
            pass
        else:
            l.append("σ3="+"%.3f" % row[1]+" / σd="+"%.3f" % row[2])
        j+=1
    return l

'''Cria um lista com as pressões do DNIT 134 modificado'''
def QD_179_MOD():
    l = []
    list = []
    listCOND = []
    listMR = []
    i = 0
    for row in c.execute('SELECT * FROM Quadro179'):
        l.append(row[1])
        l.append(row[2]+row[1])
        list.append(l)
        if i == 0:
            listCOND = list
            list = []
        if i > 0:
            listMR.append(l)
            list = []
        i+=1
        l = []

    return listCOND, listMR

'''Cria um lista com as pressões do DNIT 179'''
def QD_179():
    l = []
    list = []
    listCOND = []
    listDP = []

    i = -1
    j = 0
    for row in c.execute('SELECT * FROM Quadro179'):
        l.append(row[1])
        l.append(row[2])
        l.append(row[3])
        list.append(l)
        l = []
        if j == 0:
            listCOND = list
            list = []
        j+=1
        if i == 2:
            i = -1
            listDP.append(list)
            list = []
        i+=1
    return listCOND, listDP

'''Atualiza as configurações do ensaio DNIT 179'''
def update_dados_CONFIG_179(CICLOCOND, CICLODP):
    id = 0;
    c.execute("UPDATE config179 SET cicloCOND = ? WHERE id = ?", (CICLOCOND, id,))
    c.execute("UPDATE config179 SET cicloDP = ? WHERE id = ?", (CICLODP, id,))
    connection.commit()

'''Retorna uma lista as variaveis CICLO e ERRO'''
def CONFIG_179():
    list = []

    for row in c.execute('SELECT * FROM config179'):
        list.append(row[1])
        list.append(row[2])

    return list

######################################################################################
###################################  DNIT 181 ########################################
######################################################################################
'''Atualiza a lista das pressões do DNIT 181'''
def update_QD_181(VETOR):
    i = 0
    while i < len(VETOR):
        c.execute("UPDATE Quadro181 SET sigma1 = ? WHERE id = ?", (VETOR[i], i+1,))
        i+=1
    connection.commit()

'''Cria um lista com as pressões do DNIT 181'''
def QD_181():
    l = []
    for row in c.execute('SELECT * FROM Quadro181'):
        l.append([row[1]])

    return l

'''Atualiza as configurações do ensaio DNIT 181'''
def update_dados_CONFIG_181(CICLOMR, ERRO):
    id = 0;
    c.execute("UPDATE config181 SET cicloMR = ? WHERE id = ?", (CICLOMR, id,))
    c.execute("UPDATE config181 SET erro = ? WHERE id = ?", (ERRO, id,))
    connection.commit()

'''Retorna uma lista as variaveis CICLO e ERRO'''
def CONFIG_181():
    list = []

    for row in c.execute('SELECT * FROM config181'):
        list.append(row[1])
        list.append(row[2])

    return list
