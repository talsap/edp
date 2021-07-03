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
opcaoE = "E"    '''CAMARA DE PRESSAO'''
opcaoM = "M"    '''MOTOR DE PASSOS'''
opcaoB = "B"    '''Break'''
opcaoG = "G"    '''Golpes'''
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
'''Fim'''
def modeF():
    conexao.write(str(-3))  #O valor responsável em parar o ensaio é -3

#-------------------------------------------------------------------
'''Continua'''
def modeC():
    conexao.write(str(-1))  #O valor responsável em continuar o ensaio é -1

#-------------------------------------------------------------------
'''Pausa'''
def modeP():
    conexao.write(str(-4))  #O valor responsável em pausar o ensaio é -4

#-------------------------------------------------------------------
'''Desconectando'''
def modeD():
    conexao.write(opcaoD)

#-------------------------------------------------------------------
'''Ativando camara'''
def modeE():
    conexao.write(opcaoE)
    while (conexao.inWaiting() == 0):
        pass
    L = conexao.readline()
    print L

#-------------------------------------------------------------------
'''Conecxao com a DNIT134'''
def modeI():
    conexao.write(opcaoC)
    conexao.write(opcaoI)
    while (conexao.inWaiting() == 0):
        pass
    L = conexao.readline()
    while (conexao.inWaiting() == 0):
        pass
    L = conexao.readline()
    print L

#-------------------------------------------------------------------
'''Aplica os Golpes'''
def modeG(qtd, freq):
    print "OPC G"
    conexao.write(opcaoG)
    time.sleep(1)
    conexao.write(str(int(round(qtd,0))))
    time.sleep(1)
    conexao.write(str(int(round(freq,0))))

#-------------------------------------------------------------------
'''Camara de ar'''
def modeCAM(p2):
    incremental = p2/5
    i = 1
    time.sleep(1)
    while i <= 6:
        conexao.write(str(int(round(incremental*i,0))))
        print str(int(round(incremental*i,0)))
        time.sleep(2)
        i += 1
        if i == 6:
            conexao.write(str(-1))
            return "p2ok"
            break

#-------------------------------------------------------------------
'''Ativando motor'''
def modeM():
    conexao.write(opcaoM)

#-------------------------------------------------------------------
'''Ativacao do motor de passos'''
def modeMotor(p1):
    conexao.write(str(int(round(p1,0))))
    while (conexao.inWaiting() == 0):
        pass
    contadorOK = 0
    time.sleep(.5)
    while True:
        while (conexao.inWaiting() == 0):
            pass
        a = conexao.readline()
        #print a
        try:
            if a[0] == "o":
                contadorOK += 1
                if contadorOK == 25: #contadorOK igual a 25
                    conexao.write(str(-1))
                    return "p1ok"
                    break
            else: #else apenas para testes
                time.sleep(5)
                conexao.write(str(-1))
                return "p1ok"
                break
        except:
            pass

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
        while (conexao.inWaiting() == 0):
            pass
        arduinoString = conexao.readline()
        Array = arduinoString.split(',')
        print arduinoString
        try:
            Media[i] = 1
            y1mm[i] = float(Array[0])*A1+B1
            y2mm[i] = float(Array[1])*A2+B2
            y1v[i] = float(Array[2])
            y2v[i] = float(Array[3])
            sen[i] = float(Array[4])
            cam[i] = float(Array[5])
            glp = float(Array[6])
            sts = float(Array[7])
        except:
            Media[i] = 0
            y1mm[i] = 0.0000
            y2mm[i] = 0.0000
            y1v[i] = 0.00
            y2v[i] = 0.00
            sen[i] = 0.00
            cam[i] = 0.00
            glp = 0
            sts = 0
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

    return Y1mm, Y2mm, Y1v, Y2v, Sen/1000, Cam/1000, glp, sts
