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
    c.execute('CREATE TABLE IF NOT EXISTS dadosIniciais (id INTEGER PRIMARY KEY AUTOINCREMENT, identificador text, cp text, rodovia text, origem text, trecho text, estKm text, operador text, interesse text, dataColeta text, dataInicio text, dataFim text, amostra text, diametro real, altura real, energia real, distAp real, obs text)')

create_table()


'''Salva os dados iniciais de um ensaio'''
def data_save_dados(identificador, cp, rodovia, origem, trecho, estKm, operador, interesse, dataColeta, amostra, diametro, altura, energia, distAp, obs):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    c.execute("INSERT INTO dadosIniciais (id, identificador, cp, rodovia, origem, trecho, estKm, operador, interesse, dataColeta, dataInicio, dataFim, amostra, diametro, altura, energia, distAp, obs) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (identificador, cp, rodovia, origem, trecho, estKm, operador, interesse, dataColeta, dataInicio, dataFim, amostra, diametro, altura, energia, distAp, obs))
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
