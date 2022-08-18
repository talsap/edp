# -*- coding: utf-8 -*-
#SQL

import sqlite3
import time
import datetime
import math
import banco.bdConfiguration as bdConfiguration 

pi = math.pi

connection = sqlite3.connect('banco.db', check_same_thread = False)
c = connection.cursor()

######################################################################################
################################### INICIAL ##########################################
######################################################################################
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS dadosIniciais (id INTEGER PRIMARY KEY AUTOINCREMENT, ensaio text, status text, identificacao text, tipo text, naturazaDaAmostra text, teorUmidade text, pesoEspecifico text, umidadeOtima text, energiaCompactacao text, grauCompactacao text, dataColeta text, dataInicio text, dataFim text, amostra text, diametro real, altura real, obs text, freq int, pressaoConf text, pressaoDesvio text, tipoEstabilizante text, pesoEstabilizante int, tempoCura text, tecnico text, formacao text)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT134ADM (idt text, fase text, x real, y1 real, yt1 real, y2 real, yt2 real, pc real, pg real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT134 (idt text, fase text, pc real, pg real, dr real, r real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT179 (idt text, glp int, DR real, DP real, pc real, pg real)")
    c.execute("CREATE TABLE IF NOT EXISTS dadosDNIT181 (idt text, fase text, pg real, dr real, r real)")
    c.execute("CREATE TABLE IF NOT EXISTS referenciaADM (idt text, fase text, r1 real, r2 real)")
    c.execute("CREATE TABLE IF NOT EXISTS referencia (idt text, fase text, r real)")

create_table()

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

'''pega a altura do CP de acordo com a identificação'''
def altura_cp(idt):
    for row in c.execute('SELECT * FROM dadosIniciais WHERE identificacao = ?', (idt,)):
        altura = row[16]
    return altura

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

######################################################################################
###################################  DNIT 134  #######################################
######################################################################################
'''Cria Lista com a Coleta do resultado do ensaio no banco de dados'''
def dados_da_coleta_134_pdf(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    list  = [['FASE', 'Tesão\nconfinante\nσ3\n[MPa]', 'Tensão\ndesvio\nσd\n[MPa]', 'Deslocamento\nrecuperável\nδ\n[mm]', 'Deformação\nresiliente\nε\n[%]', 'Módulo de\nResiliência\nMR\n[MPa]']]
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

'''Cria Lista com a Coleta do resultado do ensaio no banco de dados (PARA GERAR ARQUIVO CSV)'''
def dados_da_coleta_134(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
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
'''Cria Lista com a Coleta para criar grafico local'''
def dados_GDP_179(idt):
    x = []
    y = []
    for row in c.execute('SELECT * FROM dadosDNIT179 WHERE idt = ?', (idt,)):
        x.append(int(row[1])) #golpe
        y.append(float(row[3])) #Desl. Permanente.
        
    return x, y

'''Cria Lista com a Coleta dos resultados do ensaio no banco de dados'''
def dados_da_coleta_179_pdf(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    list  = [['Número\nde ciclos\nN', 'Deslocamanto plástico\nou permanente\nacumulado\nδp\n[mm]', 'Deslocamanto\nelástico ou\nrecuperável\nδ\n[mm]', 'Deformação\nplástica ou\npermanente\nεp\n[%]', 'Deformação\nresiliente ou\nelástica\nε\n[%]']]
    for row in c.execute('SELECT * FROM dadosDNIT179 WHERE idt = ?', (idt,)):
        l.append(row[1]) #CICLO
        l.append(format("%.3f" % float(row[3])).replace('.',',')) #Desl. Permanente.
        l.append(format("%.3f" % float(row[2])).replace('.',',')) #Desl. R.
        acumulado = float(row[3])
        alturaRF = alturaCP - acumulado
        l.append(format(str("%.3f" % (100*float(row[3])/alturaRF))).replace('.',',')) #DEF. Permanente.
        l.append(format(str("%.3f" % (100*float(row[2])/alturaRF))).replace('.',',')) #DEF. R.
        list.append(l)
        l = []

    return list

'''Cria Lista com a Coleta do resultado do ensaio no banco de dados (PARA GERAR ARQUIVO CSV)'''
def dados_da_coleta_179(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    list  = [['N', 'Desl. P. [mm]', 'Desl. R. [mm]', 'DEF. P. [%]', 'DEF. R. [%]']]
    for row in c.execute('SELECT * FROM dadosDNIT179 WHERE idt = ?', (idt,)):
        l.append(row[1]) #CICLOS
        l.append(format(row[3]).replace('.',',')) #Desl. Permanente.
        l.append(format(row[2]).replace('.',',')) #Desl. R.
        acumulado = float(row[3])
        alturaRF = alturaCP - acumulado
        l.append(format(str(100*float(row[3])/alturaRF)).replace('.',',')) #DEF.Permanente.
        l.append(format(str(100*float(row[2])/alturaRF)).replace('.',',')) #DEF.R.
        list.append(l)
        l = []

    return list

'''Atualiza os dados iniciais do ensaio 179'''
def update_dados_179(identificacao, tipo, naturazaDaAmostra, teorUmidade, pesoEspecifico, umidadeOtima, energiaCompactacao, grauCompactacao, dataColeta, amostra, diametro, altura, obs, tecnico, formacao):
    dataColeta = str(datetime.datetime.strptime(str(dataColeta), '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y'))
    pressaoConf = bdConfiguration.QD_179_MOD()[1][tipo][0]
    pressaoDesvio = bdConfiguration.QD_179_MOD()[1][tipo][1] - pressaoConf
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
    pressaoConf = bdConfiguration.QD_179_MOD()[1][tipo][0]
    pressaoDesvio = bdConfiguration.QD_179_MOD()[1][tipo][1] - pressaoConf
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
'''Cria Lista com a Coleta do resultado do ensaio no banco de dados'''
def dados_da_coleta_181_pdf(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    list  = [['FASE', 'Tesão\nvertical\nσd\n[MPa]', 'Deslocamento\nrecuperável\nδ\n[mm]', 'Deformação\nresiliente\nε\n[%]', 'Módulo de\nResiliência\nMR\n[MPa]']]
    for row in c.execute('SELECT * FROM dadosDNIT181 WHERE idt = ?', (idt,)):
        l.append(row[1]) #Fase
        l.append(format("%.3f" % float(row[2])).replace('.',',')) #TV
        l.append(format("%.3f" % float(row[3])).replace('.',',')) #Desl. R.
        acumulado = acumulado + float(row[4])
        alturaRF = alturaCP - acumulado
        l.append(format(str("%.3f" % (100*float(row[3])/alturaRF))).replace('.',',')) #DEF.R
        l.append(format(str("%.3f" % (float(row[2])/(float(row[3])/alturaRF)))).replace('.',',')) #MOD. R.
        list.append(l)
        l = []

    return list

'''Cria Lista com a Coleta do resultado do ensaio no banco de dados (PARA GERAR ARQUIVO CSV)'''
def dados_da_coleta_181(idt):
    l =[]
    alturaCP = float(altura_cp(idt))
    acumulado = 0
    list  = [['FASE', 'Tensao V. [MPa]', 'Desl. R. [mm]', 'DEF. R. [%]', 'MOD. R. [MPa]']]
    for row in c.execute('SELECT * FROM dadosDNIT181 WHERE idt = ?', (idt,)):
        l.append(row[1]) #Fase
        l.append(format(row[2]).replace('.',',')) #TV
        l.append(format(row[3]).replace('.',',')) #Desl. R.
        acumulado = acumulado + float(row[4])
        alturaRF = alturaCP - acumulado
        l.append(format(str(100*float(row[3])/alturaRF)).replace('.',',')) #DEF.R
        l.append(format(str(float(row[2])/(float(row[3])/alturaRF))).replace('.',',')) #MOD. R.
        list.append(l)
        l = []

    return list

'''Salva os dados do ensaio 181'''
def saveDNIT181(idt, fase, pg, dr, r):
    c.execute("INSERT INTO dadosDNIT181 (idt, fase, pg, dr, r) VALUES (?, ?, ?, ?, ?)", (idt, fase, pg, dr, r))
    connection.commit()

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
