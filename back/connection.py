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
opcaoI = "I"    '''DNIT134'''
opcaoE = "E"    '''Camara'''
opcaoM = "M"    '''MOTOR DE PASSOS'''
opcaoB = "B"    '''Break'''
opcaoG = "G"    '''Golpes'''

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
                        print "conectado"
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
'''Desconectando'''
def modeD():
    conexao.write(opcaoD)

#-------------------------------------------------------------------
'''Ativando motor'''
def modeM():
    conexao.write(opcaoM)

#-------------------------------------------------------------------
'''Ativando motor'''
def modeE():
    conexao.write(opcaoE)

#-------------------------------------------------------------------
'''Conecxao com a DNIT134'''
def modeI():
    conexao.write(opcaoC)
    conexao.write(opcaoI)

#-------------------------------------------------------------------
'''Aplica os Golpes'''
def modeG(qtd, freq):
    conexao.write(opcaoG)
    time.sleep(1)
    conexao.write(bytes(qtd))
    time.sleep(1)
    conexao.write(bytes(freq))

#-------------------------------------------------------------------
'''Camara de ar'''
def modeCAM(p2):
    conexao.write(opcaoE)
    time.sleep(1)
    incremental = p2/10
    i = 1
    while i <= 10:
        conexao.write(str(incremental*i))
        time.sleep(.5)
        i += 1
        if i == 10:
            conexao.write(str(-1))
            return "p2ok"
            break
#-------------------------------------------------------------------
'''Ativacao do motor de passos'''
def modeMotor(p1):
    conexao.write(str(p1))
    contadorOK = 0
    while True:
        while (conexao.inWaiting() == 0):
            pass
        a = conexao.readline()
        print str(a).encode('utf-8')
        if a[0] == "o":
            contadorOK += 1
            if contadorOK == 5:
                conexao.write(str(-1))
                return "p1ok"
                break

        if a[0] == "n":
            contadorOK = 0

        '''if a[0] == "n":   # <--- so pra questao de testes. (apagar depois)
            contadorOK += 1
            if contadorOK == 2:
                conexao.write(str(-1))
                return "p1ok"
                break'''

#-------------------------------------------------------------------
def ColetaI():
    Media = np.zeros(5)
    y1mm = np.zeros(5)
    y2mm = np.zeros(5)
    y1v = np.zeros(5)
    y2v = np.zeros(5)
    sen = np.zeros(5)
    cam = np.zeros(5)

    i = 0
    while i < 5:
        while conexao.inWaiting() == 0:
            pass
        arduinoString = conexao.readline()
        Array = arduinoString.split(',')
        try:
            Media[i] = 1
            y1mm[i] = float(Array[0])*A1+B1
            y2mm[i] = float(Array[1])*A2+B2
            y1v[i] = float(Array[2])
            y2v[i] = float(Array[3])
            sen[i] = float(Array[4])
            cam[i] = float(Array[5])
        except:
            Media[i] = 0
            y1mm[i] = 0.0000
            y2mm[i] = 0.0000
            y1v[i] = 0.00
            y2v[i] = 0.00
            sen[i] = 0.00
            cam[i] = 0.00
        i+=1

    try:
        Divisor = Media[0]+Media[1]+Media[2]+Media[3]+Media[4]
        if Divisor == 0:
            Divisor = 1
        Y1mm = (y1mm[0]+y1mm[1]+y1mm[2]+y1mm[3]+y1mm[4])/Divisor
        Y2mm = (y2mm[0]+y2mm[1]+y2mm[2]+y2mm[3]+y2mm[4])/Divisor
        Y1v = (y1v[0]+y1v[1]+y1v[2]+y1v[3]+y1v[4])/Divisor
        Y2v = (y2v[0]+y2v[1]+y2v[2]+y2v[3]+y2v[4])/Divisor
        Sen = (sen[0]+sen[1]+sen[2]+sen[3]+sen[4])/Divisor
        Cam = (cam[0]+cam[1]+cam[2]+cam[3]+cam[4])/Divisor
    except:
        Y1mm = 0
        Y2mm = 0
        Y1v = 0
        Y2v = 0
        Sen = 0
        Cam = 0

    return Y1mm, Y2mm, Y1v, Y2v, Sen/1000, Cam/1000

#-------------------------------------------------------------------
def ColetaI2():
    while conexao.inWaiting() == 0:
        pass
    time.sleep(.1)
    arduinoString = conexao.readline()
    Array = arduinoString.split(',')
    try:
        glp = float(Array[6])
        sts = float(Array[7])
    except:
        glp = 1
        sts = 0

    return glp, sts
