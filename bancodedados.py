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
    c.execute('CREATE TABLE IF NOT EXISTS dadosIniciais (id INTEGER PRIMARY KEY AUTOINCREMENT, identificador text, cp text, rodovia text, origem text, trecho text, estKm text, operador text, interesse text, data text, amostra text, diametro real, altura real, energia real, distAp real, obs text)')

create_table()


'''Salva os dados iniciais de um ensaio'''
def data_save_dados(identificador, cp, rodovia, origem, trecho, estKm, operador, interesse, data, amostra, diametro, altura, energia, distAp, obs):
    data = str(datetime.datetime.strptime(str(data), '%m/%d/%Y %H:%M:%S').strftime('%m-%d-%Y'))
    c.execute("INSERT INTO dadosIniciais (id, identificador, cp, rodovia, origem, trecho, estKm, operador, interesse, data, amostra, diametro, altura, energia, distAp, obs) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (identificador, cp, rodovia, origem, trecho, estKm, operador, interesse, data, amostra, diametro, altura, energia, distAp, obs))
    connection.commit()

'''Retorna uma lista com o identificadores de ensaios já Cadastrados'''
def data_identificadores():
    list_idCab = []

    for row in c.execute('SELECT * FROM dadosIniciais'):
        list_idCab.append(row[1])

    return list_idCab
