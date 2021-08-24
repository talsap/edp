# -*- coding: utf-8 -*-

'''Bibliotecas'''

import time
import serial
import bancodedados
import numpy as np
from sys import *
from serial.tools import list_ports

'''Variaveis Globais'''
opcaoC = "C"    '''conectado'''
opcaoD = "D"    '''desconectado'''
opcaoI = "I"    '''DNIT134 e imprimir diversos'''
opcaoE = "E"    '''CAMARA DE PRESSAO'''
opcaoM = "M"    '''MOTOR DE PASSOS'''
opcaoB = "B"    '''Break'''
opcaoG = "G"    '''Golpes'''
opcaoJ = "J"    '''Imprimir 1 valor'''
opcaoS = "S"    '''Stoped'''
Y = []          #Array Deformações
T = []          #Array tempo grafico'''

'''Port Serial'''
portlist = [port for port,desc,hwin in list_ports.comports()]
conexao = serial.Serial()
conexao.baudrate = 115200

'''Coeficientes da calibracao'''
L = bancodedados.LVDT()
A1 = float(L[0])
B1 = float(L[1])
A2 = float(L[2])
B2 = float(L[3])

#-------------------------------------------------------------------
def connect():
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
def modeF():
    print 'modeF'
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
        if a[0] == 'D':
            print a
            break

#-------------------------------------------------------------------
'''Ativando camara'''
def modeE():
    print 'modeE'
    conexao.write(opcaoE)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())

#-------------------------------------------------------------------
'''Ativando motor'''
def modeM():
    print 'modeM'
    conexao.flushOutput()
    conexao.write(opcaoM)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())

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
    #print 'modeConectDNIT134'
    conexao.write(opcaoC)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    conexao.write(opcaoI)
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
'''Camara de ar pressao zero'''
def modeCAMZERO(p1, p1Sen):
    print 'modeCAMZERO'
    incremental = p1Sen/5
    i = 4
    time.sleep(1)
    #conexao.flushInput()

    while i <= 4 and i >= 0:
        conexao.write(str(int(round((p1 + incremental*i),0))))
        while (conexao.inWaiting() == 0):
            pass
        print (conexao.readline())
        time.sleep(1)
        i = i - 1
        if i == 0:
            conexao.write(str(3))
            return "p1ok"
            break

#-------------------------------------------------------------------
'''Camara de ar'''
def modeCAM(p1, p1Ant):
    print 'modeCAM'
    incremental = (p1 - p1Ant)/5
    i = 1
    time.sleep(1)
    #conexao.flushInput()

    while i <= 6:
        conexao.write(str(int(round((p1Ant + incremental*i),0))))
        while (conexao.inWaiting() == 0):
            pass
        print (conexao.readline())
        time.sleep(1)
        i += 1
        if i == 6:
            conexao.write(str(3))
            return "p1ok"
            break

#-------------------------------------------------------------------
'''Modo motor de passos'''
def modeMotor(p2):
    print 'modeMotor'
    conexao.write(str(int(round(p2,0))))
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
                if contadorOK == 25: #contadorOK igual a 25
                    conexao.write(str(3))
                    while (conexao.inWaiting() == 0):
                        pass
                    print(conexao.readline())
                    return "p2ok"
                    break
            '''if a[0] == "n": #apenas para situaçõs de teste
                contadorOK += 1
                if contadorOK == 25: #contadorOK igual a 25
                    conexao.write(str(3))
                    while (conexao.inWaiting() == 0):
                        pass
                    print(conexao.readline())
                    return "p2ok"
                    break'''
        except:
            pass

#-------------------------------------------------------------------
'''Modo motor pressao zero'''
def modeMotorZero(p2):
    print 'modeMotorZero'
    conexao.write(str(int(round(p2,0))))
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
                    return "p2ok"
                    break
            if a[0] == "n":
                contadorNOK += 1
                if contadorNOK == 5 and condic == True:
                    contadorNOK = 0
                    condic = False
                    conexao.write(str(2))
                    while (conexao.inWaiting() == 0):
                        pass
                    print(conexao.readline())
                    conexao.write(str(int(round(p2,0))))
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
    if a == '\n':
        print "BufferLimpo"
        return True
    if a[0] == 'F':
        print "BufferLimpo"
        return True
    if a[0] == 'D':
        print "BufferLimpo"
        return True
    if a[0] == 'C':
        print "BufferLimpo"
        return True
    else:
        return False

#-------------------------------------------------------------------
'''Ativando motor'''
def modeBuffer():
    print 'modeBuffer'
    while (conexao.inWaiting() == 0):
        pass
    a = conexao.readline()
    print a
    if a[0] == 'D':
        print a
        print "BufferLimpo"
        return True
    else:
        return False

#-------------------------------------------------------------------
def ColetaI(valores):
    #print 'ColetaI'
    while (conexao.inWaiting() == 0):
        pass
    arduinoString = conexao.readline()
    Array = arduinoString.split(',')
    try:
        temp = float(Array[0])
        y1mm = float(Array[1])*A1+B1
        y2mm = float(Array[2])*A2+B2
        y1v = float(Array[3])
        y2v = float(Array[4])
        sen = float(Array[5])
        cam = float(Array[6])
        sts = int(Array[7])
        glp = int(Array[8])

    except:
        #print 'ColetaIexcept'
        temp = valores[0]
        y1mm = valores[1]
        y2mm = valores[2]
        y1v = valores[3]
        y2v = valores[4]
        sen = valores[5]
        cam = valores[6]
        sts = valores[7]
        glp = valores[8]

    return temp, y1mm, y2mm, y1v, y2v, sen/10000, cam/10000, sts, glp

#-------------------------------------------------------------------
def ColetaII():
    #print 'ColetaI'
    while (conexao.inWaiting() == 0):
        pass
    arduinoString = conexao.readline()
    Array = arduinoString.split(',')
    try:
        sen = float(Array[5])
    except:
        print "Error Coleta Sensor"

    return sen/10000
