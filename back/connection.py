# -*- coding: utf-8 -*-

'''Bibliotecas'''

import time
import serial
from sys import *
from serial.tools import list_ports

'''Variaveis Globais'''
rate = 19200
opcaoC = "C"
opcaoD = "D"
opcaoI = "I"
condicaoConeccao = False

'''Port Serial'''
portlist = [port for port,desc,hwin in list_ports.comports()]
conexao = serial.Serial()
conexao.baudrate = 19200


def connect():
    i = 0
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
                    return portlist[i], "connectado"
                else:
                    print "notconectado"
                    condicaoConeccao = False
                    conexao.close()
        except:
            conexao.close()
            time.sleep(.2)
            print("Nao foi possivel manter a conexao com "+str(portlist[i])+"! Verifique a conexao usb.\n")
            i = i+1

print connect()
