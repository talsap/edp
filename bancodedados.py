# -*- coding: utf-8 -*-
#SQL

import sqlite3
import time
import datetime
import math

pi = math.pi

connection = sqlite3.connect('banco.db', check_same_thread = False)
c = connection.cursor()

######################################################################################
################################### INICIAL ##########################################
######################################################################################
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS dadosIniciais (id INTEGER PRIMARY KEY AUTOINCREMENT, ensaio text, status text, identificador text, tipo text, cp text, rodovia text, origem text, trecho text, estKm text, operador text, dataColeta text, dataInicio text, dataFim text, amostra text, diametro real, altura real, obs text)")
    c.execute("CREATE TABLE IF NOT EXISTS s1s2 (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, I1 text, A1 real, B1 real)")
    c.execute("CREATE TABLE IF NOT EXISTS s3s4 (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, I1 text, A1 real, B1 real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT134ADM (idt text, x real, y1 real, yt1 real, y2 real, yt2 real, pc real, pg real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT134 (idt text, pc real, pg real, dr real, r real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT179 (idt text, glp int, DR real, DP real, pc real, pg real)")
    c.execute("CREATE TABLE IF NOT EXISTS referenciaADM (idt text, r1 real, r2 real)")
    c.execute("CREATE TABLE IF NOT EXISTS referencia (idt text, r real)")
    c.execute("CREATE TABLE IF NOT EXISTS config134 (id integer, cicloCOND int, cicloMR int, erro int, DPacum int)")
    c.execute("CREATE TABLE IF NOT EXISTS config179 (id integer, cicloCOND int, cicloDP int)")
    c.execute("CREATE TABLE IF NOT EXISTS config181 (id integer, cicloMR int, erro int)")

def data_entry():
    try:
        c.execute("INSERT INTO s1s2 (id, I0, A0, B0, I1, A1, B1) VALUES (?, ?, ?, ?, ?, ?, ?)", (0, 'P2019113442', -0.0004, 25.394, 'P2019113443', -0.0004, 25.369))
        c.execute("INSERT INTO s3s4 (id, I0, A0, B0, I1, A1, B1) VALUES (?, ?, ?, ?, ?, ?, ?)", (0, 'P2019113340', -0.0002, 11.447, 'P2019113446', -0.0002, 11.362))
        c.execute("INSERT INTO config134 (id, cicloCOND, cicloMR, erro, DPacum) VALUES (?, ?, ?, ?, ?)", (0, 500, 10, 5, 5))
        c.execute("INSERT INTO config179 (id, cicloCOND, cicloDP) VALUES (?, ?, ?)", (0, 50, 150000))
        c.execute("INSERT INTO config181 (id, cicloMR, erro) VALUES (?, ?, ?)", (0, 50, 5))
        c.execute()
        connection.commit()
    except Exception:
        pass

create_table()
data_entry()

######################################################################################
####################################  GERAL  #########################################
######################################################################################
'''Lista com os ids'''
def ids():
    lista_id = []

    for row in c.execute('SELECT * FROM dadosIniciais'):
        lista_id.append([row[0]])

    return lista_id

'''Junta as informações para visualização em uma lista'''
def juncaoLista():
    a = IDE()
    b = dataInicial()
    c = datafinal()

    d = []
    cont = 0
    id = len(a) - 1
    e = ['']
    f = ['']

    while cont <= id:
        try:
            d.append([a[cont] + b[cont] + c[cont]])
            cont = cont +1
        except IndexError:
            d.append([a[cont] + e + f])
            cont = cont +1

    return d

'''Captura as datas iniciais dos ensaios para criar uma lista para visualização'''
def dataInicial():
    list_dateincial = []

    for row in c.execute('SELECT * FROM dadosIniciais'):
        list_dateincial.append([row[12]])

    return list_dateincial

'''Captura as datas finais dos ensaios para criar uma lista para visualização'''
def datafinal():
    list_datefinal = []

    for row in c.execute('SELECT * FROM dadosIniciais'):
        list_datefinal.append([row[13]])

    return list_datefinal

'''Captura os identificadores'''
def data_identificadores():
    list_id = []

    for row in c.execute('SELECT * FROM dadosIniciais'):
        list_id.append(row[3])

    return list_id

'''Captura os IDE (Identificadores de cada Ensaio)'''
def IDE():
    list_IDE = []

    for row in c.execute('SELECT * FROM dadosIniciais'):
        list_IDE.append([row[3]])

    return list_IDE

'''Cria uma Lista Index de visualização e indentificação'''
def ListaVisualizacao():
    a = ids()
    b = juncaoLista()
    cont = 0
    id = len(a) - 1
    c = []
    while cont <= id:
        c.append(a[cont] + b[cont])
        cont = cont +1

    return c

######################################################################################
################################## CALIBRAÇÕES #######################################
######################################################################################
'''Atualiza os dados I, A e B de Calibração dos sensores S1 e S2'''
def update_dados_S1S2(i0, a0, b0, i1, a1, b1):
    id = 0;
    c.execute("UPDATE s1s2 SET I0 = ? WHERE id = ?", (i0, id,))
    c.execute("UPDATE s1s2 SET A0 = ? WHERE id = ?", (a0, id,))
    c.execute("UPDATE s1s2 SET B0 = ? WHERE id = ?", (b0, id,))
    c.execute("UPDATE s1s2 SET I1 = ? WHERE id = ?", (i1, id,))
    c.execute("UPDATE s1s2 SET A1= ? WHERE id = ?", (a1, id,))
    c.execute("UPDATE s1s2 SET B1 = ? WHERE id = ?", (b1, id,))
    connection.commit()

'''Atualiza os dados I, A e B de Calibração dos sensores S3 e S4'''
def update_dados_S3S4(i0, a0, b0, i1, a1, b1):
    id = 0;
    c.execute("UPDATE s3s4 SET I0 = ? WHERE id = ?", (i0, id,))
    c.execute("UPDATE s3s4 SET A0 = ? WHERE id = ?", (a0, id,))
    c.execute("UPDATE s3s4 SET B0 = ? WHERE id = ?", (b0, id,))
    c.execute("UPDATE s3s4 SET I1 = ? WHERE id = ?", (i1, id,))
    c.execute("UPDATE s3s4 SET A1= ? WHERE id = ?", (a1, id,))
    c.execute("UPDATE s3s4 SET B1 = ? WHERE id = ?", (b1, id,))
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

    return list

######################################################################################
###################################  DNIT 134  #######################################
######################################################################################
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

'''Salva os dados iniciais do ensaio 134'''
def data_save_dados_134(identificador, tipo, cp, rodovia, origem, trecho, estKm, operador, dataColeta, amostra, diametro, altura, obs):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    ensaio = '134'
    status = '0'  #0 - apenas salvou os dados de início / 1 - O ensaio foi finalizado com sucesso! / 2 - O ensaio foi interrompido pelo critério de rompimento / 3 - O ensaio foi interrompido por algum erro inesperado
    c.execute("INSERT INTO dadosIniciais (id, ensaio, status, identificador, tipo, cp, rodovia, origem, trecho, estKm, operador, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ensaio, status, identificador, tipo, cp, rodovia, origem, trecho, estKm, operador, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs))
    connection.commit()

def saveDNIT134(idt, pc, pg, dr, r):
    c.execute("INSERT INTO dadosDNIT134 (idt, pc, pg, dr, r) VALUES (?, ?, ?, ?, ?)", (idt, pc, pg, dr, r))
    connection.commit()

def saveDNIT134ADM(idt, x, y1, yt1, y2, yt2, pc, pg):
    c.execute("INSERT INTO dadosDNIT134ADM (idt, x, y1, yt1, y2, yt2, pc, pg) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (idt, x, y1, yt1, y2, yt2, pc, pg))
    connection.commit()

def saveReferencia(idt, r):
    c.execute("INSERT INTO referencia (idt, r) VALUES (?, ?)", (idt, r))
    connection.commit()

def saveReferenciaADM(idt, r1, r2):
    c.execute("INSERT INTO referenciaADM (idt, r1, r2) VALUES (?, ?, ?)", (idt, r1, r2))
    connection.commit()

######################################################################################
###################################  DNIT 135  #######################################
######################################################################################
'''Funções referente a 135 aqui...'''

######################################################################################
###################################  DNIT 179  #######################################
######################################################################################
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

'''Salva os dados iniciais do ensaio 179'''
def data_save_dados_179(identificador, cp, rodovia, origem, trecho, estKm, operador, dataColeta, amostra, diametro, altura, obs):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    ensaio = '179'
    status = '0'  #0 - apenas salvou os dados de início / 1 - O ensaio foi finalizado com sucesso! / 2 - O ensaio foi interrompido pelo critério de rompimento / 3 - O ensaio foi interrompido por algum erro inesperado
    tipo = ''
    c.execute("INSERT INTO dadosIniciais (id, ensaio, status, identificador, tipo, cp, rodovia, origem, trecho, estKm, operador, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ensaio, status, identificador, tipo, cp, rodovia, origem, trecho, estKm, operador, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs))
    connection.commit()

def saveDNIT179(idt, glp, DR, DP, pc, pg):
    c.execute("INSERT INTO dadosDNIT179 (idt, glp, DR, DP, pc, pg) VALUES (?, ?, ?, ?, ?, ?)", (idt, glp, DR, DP, pc, pg))
    connection.commit()

######################################################################################
###################################  DNIT 181 ########################################
######################################################################################
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
