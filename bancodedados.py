# -*- coding: utf-8 -*-
#SQL

import sqlite3
import time
import datetime
import math

pi = math.pi

connection = sqlite3.connect('banco.db', check_same_thread = False)
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
    c.execute("CREATE TABLE IF NOT EXISTS dadosIniciais (id INTEGER PRIMARY KEY AUTOINCREMENT, ensaio text, status text, identificacao text, tipo text, naturazaDaAmostra text, teorUmidade text, pesoEspecifico text, umidadeOtima text, energiaCompactacao text, grauCompactacao text, dataColeta text, dataInicio text, dataFim text, amostra text, diametro real, altura real, obs text, freq int, pressaoConf text, pressaoDesvio text, tipoEstabilizante text, pesoEstabilizante int, tempoCura text, tecnico text, formacao text)")
    c.execute("CREATE TABLE IF NOT EXISTS s1s2 (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, C0 real, I1 text, A1 real, B1 real, C1 real)")
    c.execute("CREATE TABLE IF NOT EXISTS s3s4 (id INTEGER PRIMARY KEY AUTOINCREMENT, I0 text, A0 real, B0 real, C0 real, I1 text, A1 real, B1 real, C1 real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT134ADM (idt text, fase text, x real, y1 real, yt1 real, y2 real, yt2 real, pc real, pg real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT134 (idt text, fase text, pc real, pg real, dr real, r real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT179 (idt text, glp int, DR real, DP real, pc real, pg real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT181 (idt text, fase text, pg real, dr real, r real)")
    c.execute("CREATE TABLE IF NOT EXISTS referenciaADM (idt text, fase text, r1 real, r2 real)")
    c.execute("CREATE TABLE IF NOT EXISTS referencia (idt text, fase text, r real)")
    c.execute("CREATE TABLE IF NOT EXISTS config134 (id INTEGER PRIMARY KEY AUTOINCREMENT, cicloCOND int, cicloMR int, erro int, DPacum int)")
    c.execute("CREATE TABLE IF NOT EXISTS config179 (id INTEGER PRIMARY KEY AUTOINCREMENT, cicloCOND int, cicloDP int)")
    c.execute("CREATE TABLE IF NOT EXISTS config181 (id INTEGER PRIMARY KEY AUTOINCREMENT, cicloMR int, erro int)")
    c.execute("CREATE TABLE IF NOT EXISTS Quadro134 (id INTEGER PRIMARY KEY AUTOINCREMENT, sigma3 real, sigmad real, Razaosigma1sigma3 real)")
    c.execute("CREATE TABLE IF NOT EXISTS Quadro179 (id INTEGER PRIMARY KEY AUTOINCREMENT, sigma3 real, sigmad real, Razaosigma1sigma3 real)")
    c.execute("CREATE TABLE IF NOT EXISTS Quadro181 (id INTEGER PRIMARY KEY AUTOINCREMENT, sigma1 real)")

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
        c.execute("INSERT INTO config134 (id, cicloCOND, cicloMR, erro, DPacum) VALUES (?, ?, ?, ?, ?)", (0, 500, 10, 5, 5))
        c.execute("INSERT INTO config179 (id, cicloCOND, cicloDP) VALUES (?, ?, ?)", (0, 50, 150000))
        c.execute("INSERT INTO config181 (id, cicloMR, erro) VALUES (?, ?, ?)", (0, 50, 5))
        connection.commit()
    except Exception:
        pass

create_table()
data_entry()

######################################################################################
####################################  GERAL  #########################################
######################################################################################
'''Atualiza a frequencia do Ensaio de acordo com a idt'''
def Update_freq(idt, freq):
    c.execute("UPDATE dadosIniciais SET freq = ? WHERE identificacao = ?", (freq, idt,))
    connection.commit()

'''Data de quando finaliza o ensaio acordo com o idt'''
def data_final_Update_idt(idt):
    date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M:%S  %d/%m/%Y'))
    status = '2'
    c.execute("UPDATE dadosIniciais SET status = ? WHERE identificacao = ?", (status, idt,))
    c.execute("UPDATE dadosIniciais SET dataFim = ? WHERE identificacao = ?", (date, idt,))
    connection.commit()

'''Data de quando inicia o ensaio de acordo com o idt'''
def data_inicio_Update_idt(idt):
    date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M:%S  %d/%m/%Y'))
    status = '1'
    c.execute("UPDATE dadosIniciais SET status = ? WHERE identificacao = ?", (status, idt,))
    c.execute("UPDATE dadosIniciais SET dataInicio = ? WHERE identificacao = ?", (date, idt,))
    connection.commit()

'''coleta uma lista com os dados iniciais dos ensaio de acordo com o ID'''
def dados_iniciais_(idt):
    list = []
    for row in c.execute('SELECT * FROM dadosIniciais WHERE identificacao = ?', (idt,)):
        list.append(row[1]) #0 ensaio
        list.append(row[2]) #1 status
        list.append(row[4]) #2 tipo
        list.append(row[5]) #3 naturazaDaAmostra
        list.append(row[6]) #4 teorUmidade
        list.append(row[7]) #5 pesoEspecifico
        list.append(row[8]) #6 umidadeOtima
        list.append(row[9]) #7 energiaCompactacao
        list.append(row[10]) #8 grauCompactacao
        list.append(row[11]) #9 datadacoleta
        list.append(row[12]) #10 datainicio
        list.append(row[13]) #11 datafim
        list.append(row[14]) #12 amostra
        list.append(row[15]) #13 diametro
        list.append(row[16]) #14 altura
        list.append(row[17]) #15 obs
        list.append(row[18]) #16 freq
        list.append(row[19]) #17 pressaoConf
        list.append(row[20]) #18 pressaoDesvio
        list.append(row[21]) #19 tipoEstabilizante
        list.append(row[22]) #20 pesoEstabilizante
        list.append(row[23]) #21 tempoCura
        list.append(row[24]) #22 tecnico
        list.append(row[25]) #23 formacao

    return list

'''pega os tipo e a identificação do ensaio de acordo com o ID'''
def qual_identificador(id):
    list = []
    for row in c.execute('SELECT * FROM dadosIniciais WHERE id = ?', (id,)):
        list.append(row[1])
        list.append(row[3])

    return list

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

'''Captura as identificacoes'''
def data_identificadores():
    list_id = []

    for row in c.execute('SELECT * FROM dadosIniciais'):
        list_id.append(row[3])

    return list_id

'''Captura os IDE (identificacaoes de cada Ensaio)'''
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

    return c[::-1] #retorna a lista c de mado invertido

'''Deleta o ensaio no banco de dados'''
def delete(idt):
    c.execute("DELETE FROM dadosIniciais WHERE identificacao = ?", (idt,))
    c.execute("DELETE FROM dadosDNIT134ADM WHERE idt = ?", (idt,))
    c.execute("DELETE FROM dadosDNIT134 WHERE idt = ?", (idt,))
    c.execute("DELETE FROM dadosDNIT179 WHERE idt = ?", (idt,))
    c.execute("DELETE FROM dadosDNIT181 WHERE idt = ?", (idt,))
    c.execute("DELETE FROM referenciaADM WHERE idt = ?", (idt,))
    c.execute("DELETE FROM referencia WHERE idt = ?", (idt,))
    connection.commit()

######################################################################################
################################## CALIBRAÇÕES #######################################
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
###################################  DNIT 134  #######################################
######################################################################################
'''pega a altura do CP de acordo com a identificação'''
def altura_cp_134(idt):
    for row in c.execute('SELECT * FROM dadosIniciais WHERE identificacao = ?', (idt,)):
        altura = row[16]
    return altura

'''Cria Lista com a Coleta do resultado do ensaio no banco de dados'''
def dados_da_coleta_134_pdf(idt):
    l =[]
    alturaCP = float(altura_cp_134(idt))
    acumulado = 0
    list  = [['FASE', 'TC[MPa]', 'TD[MPa]', 'Desl. R. [mm]', 'DEF. R [%]', 'MOD. R. [MPa]']]
    for row in c.execute('SELECT * FROM dadosDNIT134 WHERE idt = ?', (idt,)):
        l.append(row[1]) #Fase
        l.append(format("%.3f" % float(row[2])).replace('.',',')) #TC
        l.append(format("%.3f" % float(row[3])).replace('.',',')) #TD
        l.append(format("%.3f" % float(row[4])).replace('.',',')) #Desl. R.
        acumulado = acumulado + float(row[5])
        alturaRF = alturaCP - acumulado
        l.append(format(str("%.3f" % (100*float(row[4])/alturaRF))).replace('.',',')) #DEF.R
        l.append(format(str("%.3f" % (float(row[3])/(float(row[4])/alturaRF)))).replace('.',',')) #MOD. R.
        list.append(l)
        l = []

    return list

'''Cria Lista com a Coleta do resultado do ensaio no banco de dados'''
def dados_da_coleta_134(idt):
    l =[]
    alturaCP = float(altura_cp_134(idt))
    acumulado = 0
    list  = [['FASE', 'TC[MPa]', 'TD[MPa]', 'Desl. R. [mm]', 'DEF. R [%]', 'MOD. R. [MPa]']]
    for row in c.execute('SELECT * FROM dadosDNIT134 WHERE idt = ?', (idt,)):
        l.append(row[1]) #Fase
        l.append(format(row[2]).replace('.',',')) #TC
        l.append(format(row[3]).replace('.',',')) #TD
        l.append(format(row[4]).replace('.',',')) #Desl. R.
        acumulado = acumulado + float(row[5])
        alturaRF = alturaCP - acumulado
        l.append(format(str(100*float(row[4])/alturaRF)).replace('.',',')) #DEF.R
        l.append(format(str(float(row[3])/(float(row[4])/alturaRF))).replace('.',',')) #MOD. R.
        list.append(l)
        l = []

    return list

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

'''Atualiza os dados iniciais do ensaio 134'''
def update_dados_134(identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, amostra, diametro, altura, obs, tecnico, formacao):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    c.execute("UPDATE dadosIniciais SET tipo = ? WHERE identificacao = ?", (tipo, identificacao,))
    c.execute("UPDATE dadosIniciais SET naturazaDaAmostra = ? WHERE identificacao = ?", (naturazaDaAmostra, identificacao,))
    c.execute("UPDATE dadosIniciais SET teorUmidade = ? WHERE identificacao = ?", (teorUmidade, identificacao,))
    c.execute("UPDATE dadosIniciais SET pesoEspecifico = ? WHERE identificacao = ?", (pesoEspecifico, identificacao,))
    c.execute("UPDATE dadosIniciais SET umidadeOtima = ? WHERE identificacao = ?", (umidadeOtima, identificacao,))
    c.execute("UPDATE dadosIniciais SET energiaCompactacao = ? WHERE identificacao = ?", (energiaCompactacao, identificacao,))
    c.execute("UPDATE dadosIniciais SET grauCompactacao = ? WHERE identificacao = ?", (grauCompactacao, identificacao,))
    c.execute("UPDATE dadosIniciais SET dataColeta = ? WHERE identificacao = ?", (dataColeta, identificacao,))
    c.execute("UPDATE dadosIniciais SET amostra = ? WHERE identificacao = ?", (amostra, identificacao,))
    c.execute("UPDATE dadosIniciais SET diametro = ? WHERE identificacao = ?", (diametro, identificacao,))
    c.execute("UPDATE dadosIniciais SET altura = ? WHERE identificacao = ?", (altura, identificacao,))
    c.execute("UPDATE dadosIniciais SET obs = ? WHERE identificacao = ?", (obs, identificacao,))
    c.execute("UPDATE dadosIniciais SET tecnico = ? WHERE identificacao = ?", (tecnico, identificacao,))
    c.execute("UPDATE dadosIniciais SET formacao = ? WHERE identificacao = ?", (formacao, identificacao,))
    connection.commit()

'''Salva os dados iniciais do ensaio 134'''
def data_save_dados_134(identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, amostra, diametro, altura, obs, tecnico, formacao):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    ensaio = '134'
    status = '0'  #0 - apenas salvou os dados de início / 1 - O ensaio já foi iniciado em algum momento / 2 - O ensaio foi finalizado com sucesso! / 3 - O ensaio foi interrompido pelo critério de rompimento / 4 - O ensaio foi interrompido por algum erro inesperado
    freq = ''
    pressaoConf = ''
    pressaoDesvio = ''
    tipoEstabilizante = ''
    pesoEstabilizante = ''
    tempoCura = ''
    c.execute("INSERT INTO dadosIniciais (id, ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao))
    connection.commit()

def saveDNIT134(idt, fase, pc, pg, dr, r):
    c.execute("INSERT INTO dadosDNIT134 (idt, fase, pc, pg, dr, r) VALUES (?, ?, ?, ?, ?, ?)", (idt, fase, pc, pg, dr, r))
    connection.commit()

def saveReferencia(idt, fase, r):
    c.execute("INSERT INTO referencia (idt, fase, r) VALUES (?, ?, ?)", (idt, fase, r))
    connection.commit()

def saveDNIT134ADM(idt, fase, x, y1, yt1, y2, yt2, pc, pg):
    c.execute("INSERT INTO dadosDNIT134ADM (idt, fase, x, y1, yt1, y2, yt2, pc, pg) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (idt, fase, x, y1, yt1, y2, yt2, pc, pg))
    connection.commit()

def saveReferenciaADM(idt, fase, r1, r2):
    c.execute("INSERT INTO referenciaADM (idt, fase, r1, r2) VALUES (?, ?, ?, ?)", (idt, fase, r1, r2))
    connection.commit()

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

'''Atualiza os dados iniciais do ensaio 179'''
def update_dados_179(identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, amostra, diametro, altura, obs, tecnico, formacao):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    pressaoConf = QD_179_MOD()[1][tipo][0]
    pressaoDesvio = QD_179_MOD()[1][tipo][1] - pressaoConf
    c.execute("UPDATE dadosIniciais SET tipo = ? WHERE identificacao = ?", (tipo, identificacao,))
    c.execute("UPDATE dadosIniciais SET naturazaDaAmostra = ? WHERE identificacao = ?", (naturazaDaAmostra, identificacao,))
    c.execute("UPDATE dadosIniciais SET teorUmidade = ? WHERE identificacao = ?", (teorUmidade, identificacao,))
    c.execute("UPDATE dadosIniciais SET pesoEspecifico = ? WHERE identificacao = ?", (pesoEspecifico, identificacao,))
    c.execute("UPDATE dadosIniciais SET umidadeOtima = ? WHERE identificacao = ?", (umidadeOtima, identificacao,))
    c.execute("UPDATE dadosIniciais SET energiaCompactacao = ? WHERE identificacao = ?", (energiaCompactacao, identificacao,))
    c.execute("UPDATE dadosIniciais SET grauCompactacao = ? WHERE identificacao = ?", (grauCompactacao, identificacao,))
    c.execute("UPDATE dadosIniciais SET dataColeta = ? WHERE identificacao = ?", (dataColeta, identificacao,))
    c.execute("UPDATE dadosIniciais SET amostra = ? WHERE identificacao = ?", (amostra, identificacao,))
    c.execute("UPDATE dadosIniciais SET diametro = ? WHERE identificacao = ?", (diametro, identificacao,))
    c.execute("UPDATE dadosIniciais SET altura = ? WHERE identificacao = ?", (altura, identificacao,))
    c.execute("UPDATE dadosIniciais SET obs = ? WHERE identificacao = ?", (obs, identificacao,))
    c.execute("UPDATE dadosIniciais SET tecnico = ? WHERE identificacao = ?", (tecnico, identificacao,))
    c.execute("UPDATE dadosIniciais SET formacao = ? WHERE identificacao = ?", (formacao, identificacao,))
    c.execute("UPDATE dadosIniciais SET pressaoConf = ? WHERE identificacao = ?", (pressaoConf, identificacao,))
    c.execute("UPDATE dadosIniciais SET pressaoDesvio = ? WHERE identificacao = ?", (pressaoDesvio, identificacao,))
    connection.commit()

'''Salva os dados iniciais do ensaio 179'''
def data_save_dados_179(identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, amostra, diametro, altura, obs, tecnico, formacao):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    ensaio = '179'
    status = '0'  #0 - apenas salvou os dados de início / 1 - O ensaio já foi iniciado em algum momento / 2 - O ensaio foi finalizado com sucesso! / 3 - O ensaio foi interrompido pelo critério de rompimento / 4 - O ensaio foi interrompido por algum erro inesperado
    freq = ''
    pressaoConf = QD_179_MOD()[1][tipo][0]
    pressaoDesvio = QD_179_MOD()[1][tipo][1] - pressaoConf
    tipoEstabilizante = ''
    pesoEstabilizante = ''
    tempoCura = ''
    c.execute("INSERT INTO dadosIniciais (id, ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao))
    connection.commit()

def saveDNIT179(idt, glp, DR, DP, pc, pg):
    c.execute("INSERT INTO dadosDNIT179 (idt, glp, DR, DP, pc, pg) VALUES (?, ?, ?, ?, ?, ?)", (idt, glp, DR, DP, pc, pg))
    connection.commit()

######################################################################################
###################################  DNIT 181 ########################################
######################################################################################
def saveDNIT181(idt, fase, pg, dr, r):
    c.execute("INSERT INTO dadosDNIT181 (idt, fase, pg, dr, r) VALUES (?, ?, ?, ?, ?)", (idt, fase, pg, dr, r))
    connection.commit()

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

'''Atualiza os dados iniciais do ensaio 181'''
def update_dados_181(identificacao, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, diametro, altura, obs, tecnico, formacao, tipoEstabilizante, tempoCura, pesoEstabilizante):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    c.execute("UPDATE dadosIniciais SET naturazaDaAmostra = ? WHERE identificacao = ?", (naturazaDaAmostra, identificacao,))
    c.execute("UPDATE dadosIniciais SET teorUmidade = ? WHERE identificacao = ?", (teorUmidade, identificacao,))
    c.execute("UPDATE dadosIniciais SET pesoEspecifico = ? WHERE identificacao = ?", (pesoEspecifico, identificacao,))
    c.execute("UPDATE dadosIniciais SET umidadeOtima = ? WHERE identificacao = ?", (umidadeOtima, identificacao,))
    c.execute("UPDATE dadosIniciais SET energiaCompactacao = ? WHERE identificacao = ?", (energiaCompactacao, identificacao,))
    c.execute("UPDATE dadosIniciais SET grauCompactacao = ? WHERE identificacao = ?", (grauCompactacao, identificacao,))
    c.execute("UPDATE dadosIniciais SET dataColeta = ? WHERE identificacao = ?", (dataColeta, identificacao,))
    c.execute("UPDATE dadosIniciais SET diametro = ? WHERE identificacao = ?", (diametro, identificacao,))
    c.execute("UPDATE dadosIniciais SET altura = ? WHERE identificacao = ?", (altura, identificacao,))
    c.execute("UPDATE dadosIniciais SET obs = ? WHERE identificacao = ?", (obs, identificacao,))
    c.execute("UPDATE dadosIniciais SET tecnico = ? WHERE identificacao = ?", (tecnico, identificacao,))
    c.execute("UPDATE dadosIniciais SET formacao = ? WHERE identificacao = ?", (formacao, identificacao,))
    c.execute("UPDATE dadosIniciais SET tipoEstabilizante = ? WHERE identificacao = ?", (tipoEstabilizante, identificacao,))
    c.execute("UPDATE dadosIniciais SET pesoEstabilizante = ? WHERE identificacao = ?", (pesoEstabilizante, identificacao,))
    c.execute("UPDATE dadosIniciais SET tempoCura = ? WHERE identificacao = ?", (tempoCura, identificacao,))
    connection.commit()

'''Salva os dados iniciais do ensaio 181'''
def data_save_dados_181(identificacao, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, diametro, altura, obs, tecnico, formacao, tipoEstabilizante, tempoCura, pesoEstabilizante):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    dataInicio = ''
    dataFim = ''
    ensaio = '181'
    status = '0'  #0 - apenas salvou os dados de início / 1 - O ensaio já foi iniciado em algum momento / 2 - O ensaio foi finalizado com sucesso! / 3 - O ensaio foi interrompido pelo critério de rompimento / 4 - O ensaio foi interrompido por algum erro inesperado
    freq = ''
    pressaoConf = ''
    pressaoDesvio = ''
    amostra = 0
    tipo = 0
    c.execute("INSERT INTO dadosIniciais (id, ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ensaio, status, identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, dataInicio, dataFim, amostra, diametro, altura, obs, freq, pressaoConf, pressaoDesvio, tipoEstabilizante, pesoEstabilizante, tempoCura, tecnico, formacao))
    connection.commit()
