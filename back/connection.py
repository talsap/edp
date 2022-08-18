# -*- coding: utf-8 -*-

'''Bibliotecas'''

import time
import serial
import banco.bancodedados as bancodedados
import banco.bdConfiguration as bdConfiguration
import numpy as np
from sys import *
from serial.tools import list_ports

'''Variaveis Globais'''
opcaoC = "C"    '''conectado'''
opcaoD = "D"    '''desconectado'''
opcaoI = "I"    '''DNIT134 e imprimir diversos'''
opcaoE = "E"    '''VALVULA DINÂMICA DE PRESSAO 1'''
opcaoF = "F"    '''VALVULA DINÂMICA DE PRESSAO 2'''
opcaoM = "M"    '''MOTOR DE PASSOS'''
opcaoB = "B"    '''Break'''
opcaoG = "G"    '''Golpes'''
opcaoJ = "J"    '''DNIT134 e imprimir 1 valor'''
opcaoK = "K"    '''Mudar Limite de discrepância'''
opcaoS = "S"    '''Stoped'''
Y = []          #Array Deformações
T = []          #Array tempo grafico'''

'''Port Serial'''
portlist = [port for port,desc,hwin in list_ports.comports()]
conexao = serial.Serial()
conexao.baudrate = 115200

'''Coeficientes da calibracao dos sensores S1 e S2'''
L1 = bdConfiguration.S1S2()
A1_S1 = float(L1[1])
B1_S1= float(L1[2])
A2_S2 = float(L1[5])
B2_S2 = float(L1[6])

'''Coeficientes da calibracao dos sensores S3 e S4'''
L2 = bdConfiguration.S3S4()
A3_S3 = float(L2[1])
B3_S3 = float(L2[2])
A4_S4 = float(L2[5])
B4_S4 = float(L2[6])

'''Coeficientes da calibracao da valvula DINAMICA 1'''
E = bdConfiguration.DadosD1()
AE1 = float(E[5])
BE1 = float(E[6])

'''Coeficientes da calibracao da valvula DINAMICA 2'''
F = bdConfiguration.DadosD2()
AF1 = float(F[5])
BF1 = float(F[6])

#-------------------------------------------------------------------
def connect(DISCREP):
    print 'connect'
    i = 0
    condicaoConeccao = False
    try:
        while i < len(portlist):
            conexao.port = portlist[i]
            try:
                conexao.open()
                if conexao.isOpen() == True:
                    print("Verificando Conexao com porta serial "+conexao.port+"...\n")
                    conexao.write(opcaoC)
                    conexao.timeout = 1
                    a = conexao.readline()
                    if a[0] == "c":
                        print a
                        if DISCREP != 1.05:
                            print "MUDANDO DISCREPANCIA"
                            try:
                                discrep = int((DISCREP - 1)*100)
                                conexao.write(opcaoK)
                                conexao.timeout = .3
                                conexao.write(str(discrep))
                                conexao.timeout = .3
                                conexao.write(str(3))
                                print "\nDiscrepancia Alterada\n"
                            except:
                                print "\nDiscrepancia NÃO Alterada\n"
                        condicaoConeccao = True
                        return conexao.port, "connectado"
                    else:
                        print "notconectado"
                        conexao.close()
            except:
                conexao.close()
                time.sleep(.2)
                print("Nao foi possivel manter a conexao com "+conexao.port+"! Verifique a conexao usb.\n")
                if i == len(portlist):
                    return conexao.port, "notconnectado"
                else:
                    i = i+1
    except:
        time.sleep(.2)
        print("Nao foi possivel manter a conexao! Verifique a conexao usb.\n")
        condicaoConeccao = False
        return "0", "notconnectado"

    else:
        if condicaoConeccao == True:
            pass
        else:
            time.sleep(.2)
            print("Nao foi possivel manter a conexao! Verifique a conexao usb.\n")
            condicaoConeccao = False
            return "0", "notconnectado"

#-------------------------------------------------------------------
'''modo Break'''
def modeB():
    print 'modeB'
    conexao.write(opcaoB)

#-------------------------------------------------------------------
'''Desconectando'''
def modeD():
    print 'modeD'
    conexao.write(opcaoD)

#-------------------------------------------------------------------
'''Modo Imprimir'''
def modeI():
    print 'modeI'
    conexao.write(opcaoI)

#-------------------------------------------------------------------
'''Modo Imprimir 1 valor'''
def modeJ():
    print 'modeJ'
    conexao.write(opcaoJ)

#-------------------------------------------------------------------
'''Fim'''
def modeFIM():
    print 'modeFIM'
    conexao.write(str(3))  #O valor responsável em parar o ensaio é 3

#-------------------------------------------------------------------
'''Continua'''
def modeC():
    print 'modeC'
    conexao.write(str(2))  #O valor responsável em continuar o ensaio é 1

#-------------------------------------------------------------------
'''Pausa'''
def modeP():
    print 'modeP'
    conexao.write(str(4))  #O valor responsável em pausar o ensaio é 4

#-------------------------------------------------------------------
'''Pede para parar de imprimir'''
def modeS():
    print 'modoS'
    conexao.write(opcaoS)

#-------------------------------------------------------------------
'''Pede para parar de imprimir'''
def modeStoped():
    print 'modoStoped'
    conexao.write(opcaoS)
    while True:
        while (conexao.inWaiting() == 0):
            pass
        a = conexao.readline()
        if a == '\n' or a[0] == 'F' or a[0] == 'D' or a[0] == 'C' or a[0] == '':
            print a
            break

#-------------------------------------------------------------------
'''Ativando válvula dinamica - saída'''
def modeES():
    print 'modeES'
    conexao.write(opcaoE)
    while (conexao.inWaiting() == 0):
            pass
    print(conexao.readline())

#-------------------------------------------------------------------
'''Ativando válvula dinamica 2 - saída'''
def modeFS():
    print 'modeFS'
    conexao.write(opcaoF)
    while (conexao.inWaiting() == 0):
            pass
    print(conexao.readline())

#-------------------------------------------------------------------
'''Ativando motor Saída'''
def modeMS():
    print 'modeMS'
    conexao.write(opcaoM)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())

#-------------------------------------------------------------------
'''Ativando valvula dinamica'''
def modeE():
    print 'modeE'
    buf = modeBuffer()
    while buf == False:
        buf = modeBuffer()
    if buf == True:
        conexao.write(opcaoE)
        while (conexao.inWaiting() == 0):
            pass
        print(conexao.readline())
    else:
        print '#Erro no modeE'

#-------------------------------------------------------------------
'''Ativando valvula dinamica 2'''
def modeF():
    print 'modeF'
    buf = modeBuffer()
    while buf == False:
        buf = modeBuffer()
    if buf == True:
        conexao.write(opcaoF)
        while (conexao.inWaiting() == 0):
            pass
        print(conexao.readline())
    else:
        print '#Erro no modeF'

#-------------------------------------------------------------------
'''Ativando motor'''
def modeM():
    print 'modeM'
    conexao.flushOutput()
    buf = modeBuffer()
    while buf == False:
        buf = modeBuffer()
    if buf == True:
        conexao.write(opcaoM)
        while (conexao.inWaiting() == 0):
            pass
        print(conexao.readline())
    else:
        print '#Erro no modeM'

#-------------------------------------------------------------------
'''Ativando golpes'''
def modeG():
    print 'modeG'
    conexao.write(opcaoG)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())


#-------------------------------------------------------------------
'''Conecxao com a DNIT134'''
def modeConectDNIT134():
    print 'modeConectDNIT134'
    conexao.write(opcaoC)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    conexao.write(opcaoI)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())

#-------------------------------------------------------------------
'''Conecxao com a DNIT135'''
def modeConectDNIT135():
    print 'modeConectDNIT135'
    conexao.write(opcaoC)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    conexao.write(opcaoJ)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())

#-------------------------------------------------------------------
'''Aplica os Golpes'''
def modeGOLPES(qtd, freq):
    print 'modeGOLPES'
    conexao.write(str(int(round(qtd,0))))
    while (conexao.inWaiting() == 0):
        pass
    print (conexao.readline())
    time.sleep(1)
    conexao.write(str(int(round(freq,0)))+'\n')
    while (conexao.inWaiting() == 0):
        pass
    print (conexao.readline())

#-------------------------------------------------------------------
'''Válvula dinamica pressao zero'''
def modeDINZERO(p2, p2Sen):
    print 'modeDINZERO'
    incremental = p2Sen/5
    i = 4
    time.sleep(1)
    #conexao.flushInput()

    while i <= 4 and i >= 0:
        conexao.write(str(int(round((p2 + incremental*i),0))))
        while (conexao.inWaiting() == 0):
            pass
        print (conexao.readline())
        time.sleep(1)
        i = i - 1
        if i == 0:
            conexao.write(str(int(round(p2,0))))
            while (conexao.inWaiting() == 0):
                pass
            print (conexao.readline())
            time.sleep(1)
            conexao.write(str(3))
            return "p_ok"
            break

#-------------------------------------------------------------------
'''Válvula dinâmica'''
def modeDIN(p2, p2Ant):
    print 'modeDIN'
    incremental = (p2 - p2Ant)/5
    i = 1
    time.sleep(1)
    #conexao.flushInput()

    while i <= 6:
        conexao.write(str(int(round((p2Ant + incremental*i),0))))
        while (conexao.inWaiting() == 0):
            pass
        print (conexao.readline())
        time.sleep(1)
        i += 1
        if i == 6:
            conexao.write(str(3))
            return "p_ok"
            break

#-------------------------------------------------------------------
'''Modo motor de passos'''
def modeMotor(p1):
    print 'modeMotor'
    conexao.write(str(int(round(p1,0))))
    #conexao.flushInput()        #linha que foi adicionada
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    contadorOK = 0
    time.sleep(.5)
    while True:
        while (conexao.inWaiting() == 0):
            pass
        a = conexao.readline()
        print a
        try:
            if a[0] == "o":
                contadorOK += 1
                if contadorOK == 200: #contadorOK igual a 200
                    conexao.write(str(3))
                    while (conexao.inWaiting() == 0):
                        pass
                    print(conexao.readline())
                    return "p1ok"
                    break
            '''if a[0] == "n": #apenas para situaçõs de teste
                contadorOK += 1
                if contadorOK == 25: #contadorOK igual a 25
                    conexao.write(str(3))
                    while (conexao.inWaiting() == 0):
                        pass
                    print(conexao.readline())
                    return "p1ok"
                    break'''
        except:
            pass

#-------------------------------------------------------------------
'''Modo motor pressao zero'''
def modeMotorZero(p1):
    print 'modeMotorZero'
    conexao.write(str(int(round(p1,0))))
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    contadorOK = 0
    contadorNOK = 0
    condic = True
    time.sleep(.5)
    while True:
        while (conexao.inWaiting() == 0):
            pass
        a = conexao.readline()
        print a
        try:
            if a[0] == "o":
                contadorOK += 1
                if contadorOK == 25:
                    conexao.write(str(3))
                    return "p1ok"
                    break
        except:
            pass

#-------------------------------------------------------------------
'''Limpando Buffer para coleta'''
def Buffer():
    print 'Buffer'
    while (conexao.inWaiting() == 0):
        pass
    a = conexao.readline()
    print a
    if a == '\n' or a[0] == 'F' or a[0] == 'D' or a[0] == 'C' or a[0] == '':
        print "BufferLimpo"
        return True
    else:
        return False

#-------------------------------------------------------------------
'''Ativando motor'''
def modeBuffer():
    print 'modeBuffer'
    a = conexao.readline()
    #print a
    try:
        if a[0] == 'D':
            print a
            print "BufferLimpo"
            return True
        else:
            return False
    except:
        return True


#-------------------------------------------------------------------
def ColetaI(valores):
    #print 'ColetaI' #formatação dos dados da 134
    while (conexao.inWaiting() == 0):
        pass
    arduinoString = conexao.readline()
    Array = arduinoString.split(',')
    try:
        temp = float(Array[0])
        y1mm = float(Array[1])*A1_S1+B1_S1
        y2mm = float(Array[2])*A2_S2+B2_S2
        y1v = float(Array[3])
        y2v = float(Array[4])
        sen = float(Array[5])*AE1+BE1
        cam = float(Array[6])*AF1+BF1
        sts = int(Array[7])
        glp = int(Array[8])
        ntglp = int(Array[9])

    except:
        print 'ColetaI - except'
        temp = valores[0]
        y1mm = valores[1]
        y2mm = valores[2]
        y1v = valores[3]
        y2v = valores[4]
        sen = valores[5]
        cam = valores[6]
        sts = valores[7]
        glp = valores[8]
        ntglp = valores[9]

    return temp, y1mm, y2mm, y1v, y2v, sen, cam, sts, glp, ntglp

#-------------------------------------------------------------------
def ColetaJ(valores):
    print 'ColetaJ' #formatação dos dados da 135
    while (conexao.inWaiting() == 0):
        pass
    arduinoString = conexao.readline()
    Array = arduinoString.split(',')
    try:
        temp = float(Array[0])
        y3mm = float(Array[1])*A3_S3+B3_S3
        y4mm = float(Array[2])*A4_S4+B4_S4
        y3v = float(Array[3])
        y4v = float(Array[4])
        est = float(Array[5])
        glp = int(Array[6])

    except:
        print 'ColetaJ - except'
        temp = valores[0]
        y3mm = valores[1]
        y4mm = valores[2]
        y3v = valores[3]
        y4v = valores[4]
        est = valores[5]
        glp = valores[6]

    return temp, y3mm, y4mm, y3v, y4v, est, glp

#-------------------------------------------------------------------
def ColetaII():
    print 'ColetaII'
    while (conexao.inWaiting() == 0):
        pass
    arduinoString = conexao.readline()
    Array = arduinoString.split(',')
    try:
        sen = float(Array[9])
    except:
        print "Error Coleta Sensor"

    return sen/10000
