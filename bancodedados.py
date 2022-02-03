# -*- coding: utf-8 -*-
#SQL

import sqlite3
import time
import datetime
import math

pi = math.pi

connection = sqlite3.connect('banco.db', check_same_thread = False)
c = connection.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS dadosIniciais (id INTEGER PRIMARY KEY AUTOINCREMENT, identificador text, cp text, rodovia text, origem text, trecho text, estKm text, operador text, interesse text, dataColeta text, dataInicio text, dataFim text, amostra text, diametro real, altura real, obs text)")
    c.execute("CREATE TABLE IF NOT EXISTS calibrador134 (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, I1 text, A1 real, B1 real)")
    c.execute("CREATE TABLE IF NOT EXISTS calibrador135 (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, I1 text, A1 real, B1 real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT134 (idt text, x real, y1 real, yt1 real, y2 real, yt2 real, pc real, pg real)")
    c.execute("CREATE TABLE IF NOT EXISTS referencia (idt text, r1 real, r2 real)")

def saveReferencia(idt, r1, r2):
    c.execute("INSERT INTO referencia (idt, r1, r2) VALUES (?, ?, ?)", (idt, r1, r2))
    connection.commit()

def saveDNIT134(idt, x, y1, yt1, y2, yt2, pc, pg):
    c.execute("INSERT INTO dadosDNIT134 (idt, x, y1, yt1, y2, yt2, pc, pg) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (idt, x, y1, yt1, y2, yt2, pc, pg))
    connection.commit()

def data_entry():
    try:
        c.execute("INSERT INTO calibrador134 (id, I0, A0, B0, I1, A1, B1) VALUES (?, ?, ?, ?, ?, ?, ?)", (0, 'P2019113340', -0.0002, 11.447, 'P2019113446', -0.0002, 11.362))
        c.execute("INSERT INTO calibrador135 (id, I0, A0, B0, I1, A1, B1) VALUES (?, ?, ?, ?, ?, ?, ?)", (0,'P1',0,0,'P2',0,0))
        connection.commit()
    except Exception:
        pass


create_table()
data_entry()

'''Atualiza os dados I, A e B de Calibração do LVDT134'''
def update_dados_LVDT_134(i0, a0, b0, i1, a1, b1):
    id = 0;
    c.execute("UPDATE calibrador134 SET I0 = ? WHERE id = ?", (i0, id,))
    c.execute("UPDATE calibrador134 SET A0 = ? WHERE id = ?", (a0, id,))
    c.execute("UPDATE calibrador134 SET B0 = ? WHERE id = ?", (b0, id,))
    c.execute("UPDATE calibrador134 SET I1 = ? WHERE id = ?", (i1, id,))
    c.execute("UPDATE calibrador134 SET A1= ? WHERE id = ?", (a1, id,))
    c.execute("UPDATE calibrador134 SET B1 = ? WHERE id = ?", (b1, id,))
    connection.commit()

'''Atualiza os dados I, A e B de Calibração do LVDT135'''
def update_dados_LVDT_135(i0, a0, b0, i1, a1, b1):
    id = 0;
    c.execute("UPDATE calibrador135 SET I0 = ? WHERE id = ?", (i0, id,))
    c.execute("UPDATE calibrador135 SET A0 = ? WHERE id = ?", (a0, id,))
    c.execute("UPDATE calibrador135 SET B0 = ? WHERE id = ?", (b0, id,))
    c.execute("UPDATE calibrador135 SET I1 = ? WHERE id = ?", (i1, id,))
    c.execute("UPDATE calibrador135 SET A1= ? WHERE id = ?", (a1, id,))
    c.execute("UPDATE calibrador135 SET B1 = ? WHERE id = ?", (b1, id,))
    connection.commit()

'''Retorna uma lista as variaveis I, A e B de Calibração do LVDT134'''
def LVDT_134():
    list = []

    for row in c.execute('SELECT * FROM calibrador134'):
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
        list.append(row[5])
        list.append(row[6])

    return list

'''Retorna uma lista as variaveis I, A e B de Calibração do LVDT135'''
def LVDT_135():
    list = []

    for row in c.execute('SELECT * FROM calibrador135'):
        list.append(row[1])
        list.append(row[2])
        list.append(row[3])
        list.append(row[4])
        list.append(row[5])
        list.append(row[6])

    return list

'''Salva os dados iniciais de um ensaio'''
def data_save_dados_134(identificador, cp, rodovia, origem, trecho, estKm, operador, interesse, dataColeta, amostra, diametro, altura, obs):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    c.execute("INSERT INTO dadosIniciais (id, identificador, cp, rodovia, origem, trecho, estKm, operador, interesse, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (identificador, cp, rodovia, origem, trecho, estKm, operador, interesse, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs))
    connection.commit()

'''Retorna uma lista com o identificadores de ensaios já Cadastrados'''
def data_identificadores():
    list_idCab = []

    for row in c.execute('SELECT * FROM dadosIniciais'):
        list_idCab.append(row[1])

    return list_idCab

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
        list_dateincial.append([row[10]])

    return list_dateincial

'''Captura as datas finais dos ensaios para criar uma lista para visualização'''
def datafinal():
    list_datefinal = []

    for row in c.execute('SELECT * FROM dadosIniciais'):
        list_datefinal.append([row[11]])

    return list_datefinal

'''Captura os IDE (Identificadores de cada Ensaio)'''
def IDE():
    list_IDE = []

    for row in c.execute('SELECT * FROM dadosIniciais'):
        list_IDE.append([row[1]])

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
