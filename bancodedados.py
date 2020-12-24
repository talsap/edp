# -*- coding: utf-8 -*-
#SQL

import sqlite3
import math

connection = sqlite3.connect('banco.db', check_same_thread = False)
c = connection.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS Cabecalho (id INTEGER PRIMARY KEY AUTOINCREMENT, identificador text, instituicao text, fantasia text, cpfcnpj text, email text, fone text, uf text, cidade text, bairro text, rua text, numero text, complemento text, cep text, logo text)")

def data_entry():
    try:
        c.execute("INSERT INTO Cabecalho VALUES (0, '(Default)', 'UFRB', 'EDP - Ensaios Dinâmicos para Pavimentação' ,'xxx.xxx.xxx-xx', 'tarcisiosapucaia27@gmail.com', '(xx) x.xxxx-xxxx', 'Ba', 'Cruz das Almas', 'Inocoop', 'R. Rui Barbosa', 'sn', 'Prédio', '44.380-000', 'diretório')")
        connection.commit()
    except Exception:
        pass

create_table()
data_entry()

'''Cria uma Lista Index de visualização dos Cabecalhos Cadastrados'''
def ListaVisualizacaoCab():
    a = idsCab()
    b = idCabecalho()
    cont = 0
    id = len(a) - 1
    c = []
    while cont <= id:
        c.append(a[cont] + [b[cont]])
        cont = cont + 1

    return c

'''Lista com os ids dos Cabecalhos cadastrados'''
def idsCab():
    lista_id = []

    for row in c.execute('SELECT * FROM Cabecalho'):
        lista_id.append([row[0]])

    return lista_id


'''Captura os nomes dos indetificadores dos Cabecalhos'''
def idCabecalho():
    list_idCab = []

    for row in c.execute('SELECT * FROM Cabecalho'):
        list_idCab.append([row[1]])

    return list_idCab
