# -*- coding: utf-8 -*-

'''Bibliotecas'''

import time
import serial
import bancodedados
from sys import *
from serial.tools import list_ports

'''Variaveis Globais'''
opcaoC = "C"    '''conectado'''
opcaoD = "D"    '''desconectado'''
opcaoI = "I"    '''DNIT134'''
opcaoE = "E"    '''Camara'''
opcaoM = "M"    '''MOTOR DE PASSOS'''
opcaoB = "B"    '''Break'''

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
def modeD():
    conexao.write(opcaoD)

#-------------------------------------------------------------------
'''Conecxao com a DNIT134'''
def modeI():
    conexao.write(opcaoC)
    conexao.write(opcaoI)

#-------------------------------------------------------------------
'''Ativacao do motor de passos'''
def modeCAM(p2):
    conexao.write(opcaoE)
    incremental = p2/10
    i = 1
    while i <= 10:
        conexao.write(str(int(incremental*i)))
        time.sleep(.5)
        i += 1
        if i == 10:
            conexao.write('-1')
            return "p2ok"
            break
#-------------------------------------------------------------------
'''Ativacao do motor de passos'''
def modeM(p1):
    conexao.write(opcaoM)
    time.sleep(.1)
    conexao.write(str(int(p1)))
    contadorOK = 0
    while True:
        while (conexao.inWaiting() == 0):
            pass
        a = conexao.readline()
        if a[0] == "o":
            contadorOK += 1
            if contadorOK == 5:
                conexao.write('-1')
                return "p1ok"
                break

        if a[0] == "n":   # <--- so pra questao de testes. (apagar depois)
            contadorOK += 1
            if contadorOK == 2:
                conexao.write('-1')
                return "p1ok"
                break

#-------------------------------------------------------------------
def ColetaI():
    while conexao.inWaiting() == 0:
        pass
    time.sleep(.005)
    arduinoString = conexao.readline()
    Array = arduinoString.split(',')
    try:
        y1mm = float(Array[0])*A1+B1
        y2mm = float(Array[1])*A2+B2
        y1v = float(Array[2])
        y2v = float(Array[3])
        sen = float(Array[4])
        cam = float(Array[5])
    except:
        y1mm = 0.0000
        y2mm = 0.0000
        y1v = 0.00
        y2v = 0.00
        sen = 0.00
        cam = 0.00

    return y1mm, y2mm, y1v, y2v, sen/1000, cam/1000
