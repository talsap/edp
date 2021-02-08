# -*- coding: utf-8 -*-
#SQL

import sqlite3
import math

connection = sqlite3.connect('bancoCAB.db', check_same_thread = False)
c = connection.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS Cabecalho (id INTEGER PRIMARY KEY AUTOINCREMENT, identificador text, instituicao text, fantasia text, cpfcnpj text, email text, fone text, uf text, cidade text, bairro text, rua text, numero text, complemento text, cep text, logo text)")
    c.execute('CREATE TABLE IF NOT EXISTS idDeletados (idDeletados integer)')
    c.execute("CREATE TABLE IF NOT EXISTS escolha (id)")

def data_entry():
    try:
        c.execute("INSERT INTO Cabecalho VALUES (0, '(Default)', 'UFRB - UNIVERSIDADE FEDERAL DO RECÔNCAVO DA BAHIA', 'EDP - Ensaios Dinâmicos para Pavimentação' ,'xxx.xxx.xxx-xx', 'tarcisiosapucaia27@gmail.com', '(xx) x.xxxx-xxxx', 'Ba', 'Cruz das Almas', 'Inocoop', 'R. Rui Barbosa', 'sn', 'Prédio', '44.380-000', 'logo\logoEDP.png')")
        c.execute("INSERT INTO escolha VALUES (0)")
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

'''Retorna uma lista com o identificadores dos Cabeçalhos já Cadastrados'''
def data_identificadores():
    list_idCab = []

    for row in c.execute('SELECT * FROM Cabecalho'):
        list_idCab.append(row[1])

    return list_idCab

'''Salva os dados de um novo Cabeçalho'''
def data_save_dados(identificador, instituicao, fantasia, cpfcnpj, email, fone, uf, cidade, bairro, rua, numero, complemento, cep, logo):
    c.execute("INSERT INTO Cabecalho (id, identificador, instituicao, fantasia, cpfcnpj, email, fone, uf, cidade, bairro, rua, numero, complemento, cep, logo) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (identificador, instituicao, fantasia, cpfcnpj, email, fone, uf, cidade, bairro, rua, numero, cep, complemento, logo))
    connection.commit()

'''Captura o id do Cabeçalho escolhido para impressão'''
def idEscolha():
    escolha = []

    for row in c.execute('SELECT * FROM escolha'):
        escolha.append(row[0])

    return escolha[0]

'''Compara a String identificador para encontrar o id'''
def identificador_id(ident):
    ult = []

    for row in c.execute('SELECT * FROM Cabecalho WHERE identificador = ?', (ident,)):
        ult.append(row[0])

    return ult[0] #retorna com id

'''Altera o Cabeçalho de escolha no banco de dados'''
def updateEscolha(id):
    c.execute("UPDATE escolha SET id = ?", (id,))
    connection.commit()

'''Retorna uma lista com os dados cadastrados no cabeçalho dado o id'''
def ListaDadosCab(id):
    lista = []
    for row in c.execute('SELECT * FROM Cabecalho WHERE id = ?', (id,)):
        lista.append(row[1])
        lista.append(row[2])
        lista.append(row[3])
        lista.append(row[4])
        lista.append(row[5])
        lista.append(row[6])
        lista.append(row[7])
        lista.append(row[8])
        lista.append(row[9])
        lista.append(row[10])
        lista.append(row[11])
        lista.append(row[12])
        lista.append(row[13])
        lista.append(row[14])

    return lista

'''Deleta um Cabeçalho no banco de dados de acordo com o id'''
def deleteCAB(id):
    c.execute("DELETE FROM Cabecalho WHERE id = ?", (id,))
    c.execute("INSERT INTO idDeletados (idDeletados) VALUES (?)", (id,))
    connection.commit()

'''Ver a quantidade de cabeçalhos que já foram deletados'''
def quant_CAB_deletados():
    identificador = []
    for rows in c.execute('SELECT * FROM idDeletados'):
        identificador.append(rows[0])

    id = len(identificador)
    return id

'''Ver os id dos cabeçalhos que foram deletados'''
def ler_ID_CAB_deletados():
    identificador = []
    for rows in c.execute('SELECT * FROM idDeletados'):
        identificador.append(rows[0])

    return identificador
