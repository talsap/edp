# -*- coding: utf-8 -*-
import wx
import time
import back.connection as con
from pubsub import pub
from threading import Thread

global A2 #área do corpo de prova, vinda do banco de dados do Ensaio
global A1 #área da seção do cilindro pneumático

########################################################################
'''DinamicaThread'''
class DinamicaThread(Thread):
    #-------------------------------------------------------------------
    def __init__(self, p2, p2Ant):
        Thread.__init__(self)
        self.start()
        self.p2 = p2
        self.p2Ant = p2Ant
        self.A1 = 0.007854
        self.A2 = 0.007854
        self._return = True

    #-------------------------------------------------------------------
    def run(self):
        con.modeS()
        wx.CallAfter(pub.sendMessage, "update", msg="Ativando válvula...")
        time.sleep(.5)
        con.modeE()
        wx.CallAfter(pub.sendMessage, "update", msg="       Regulando...")
        time.sleep(.5)
        valor2 = con.modeDIN((10000*self.A2/self.A1)*self.p2, (10000*self.A2/self.A1)*self.p2Ant)
        if valor2 == 'p2ok':
            print 'PRESSAO GOLPE OK'
            wx.CallAfter(pub.sendMessage, "update", msg="            σd - ok")
            time.sleep(1)

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return

########################################################################
'''DinamicaThreadZero'''
class DinamicaThreadZero(Thread):
    #-------------------------------------------------------------------
    def __init__(self, p2, p2Sen):
        Thread.__init__(self)
        self.start()
        self.p2 = p2
        self.p2Sen = p2Sen
        self._return = True

    #-------------------------------------------------------------------
    def run(self):
        con.modeS()
        wx.CallAfter(pub.sendMessage, "update", msg="Ativando válvula...")
        time.sleep(.5)
        con.modeES()
        wx.CallAfter(pub.sendMessage, "update", msg="         Zerando...")
        time.sleep(.5)
        valor2 = con.modeDINZERO(10000*self.p2, 10000*self.p2Sen)
        if valor2 == 'p2ok':
            print 'PRESSAO GOLPE ZERADO'
            wx.CallAfter(pub.sendMessage, "update", msg="       σd - Zerado!")
            time.sleep(1)
            wx.CallAfter(pub.sendMessage, "update", msg="")

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return
