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

'''ComboBox Port Serial'''
portlist = [port for port,desc,hwin in list_ports.comports()]

def connect():
    for item in portlist:
        try:
            conexao = serial.Serial(item, rate)
            print conexao.inWaiting()
            print("Verificando Conexao com porta serial "+str(item)+"...\n")
            time.sleep(1)
            print 'a'
            conexao.write(opcaoC)
            print 'a'
            a = conexao.read()
            if a == '':
                print "bb"
                condicaoConeccao = True
                return a[0]
            else:
                print "aa"
            print "cc"
        except:
            time.sleep(1)
            print("Nao foi possivel manter a conexao com "+str(item)+"! Verifique a conexao usb.\n")
            return 0

connect()
