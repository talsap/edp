# -*- coding: utf-8 -*-

'''Bibliotecas'''

import time
import serial
from sys import *
from serial.tools import list_ports

'''Variaveis Globais'''
opcaoC = "C"
opcaoD = "D"
opcaoI = "I"

'''Port Serial'''
portlist = [port for port,desc,hwin in list_ports.comports()]
conexao = serial.Serial()
conexao.baudrate = 115200

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
def modeI():
    conexao.write(opcaoC)
    conexao.write(opcaoI)

#-------------------------------------------------------------------
def ColetaI():
    while conexao.inWaiting() == 0:
        pass
    time.sleep(.005)
    arduinoString = conexao.readline()
    Array = arduinoString.split(',')
    try:
        y1mm = float(Array[0])
        y2mm = float(Array[1])
        y1v = float(Array[2])
        y2v = float(Array[3])
    except:
        y1mm = ''
        y2mm = ''
        y1v = ''
        y2v = ''

    return y1mm, y2mm, y1v, y2v
