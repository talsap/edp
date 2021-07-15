# -*- coding: utf-8 -*-
import wx
import time
import back.connection as con
from pubsub import pub
from threading import Thread

########################################################################
'''MotorThread'''
class CamaraThread(Thread):
    #-------------------------------------------------------------------
    def __init__(self, p1, p1Ant):
        Thread.__init__(self)
        self.start()
        self.p1 = p1
        self.p1Ant = p1Ant
        self._return = True

    #-------------------------------------------------------------------
    def run(self):
        wx.CallAfter(pub.sendMessage, "update", msg="Ativando válvula...")
        time.sleep(1)
        con.modeE()
        wx.CallAfter(pub.sendMessage, "update", msg="       Regulando...")
        time.sleep(1)
        valor2 = con.modeCAM(10000*self.p1, self.p1Ant)
        if valor2 == 'p1ok':
            print 'PRESSAO CAMARA OK'
            wx.CallAfter(pub.sendMessage, "update", msg="            σ3 - ok")
            time.sleep(1)

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return

########################################################################
'''MotorThread'''
class CamaraThreadZero(Thread):
    #-------------------------------------------------------------------
    def __init__(self, p1, p1Sen):
        Thread.__init__(self)
        self.start()
        self.p1 = p1
        self.p1Sen = p1Ant
        self._return = True

    #-------------------------------------------------------------------
    def run(self):
        wx.CallAfter(pub.sendMessage, "update", msg="Ativando válvula...")
        time.sleep(1)
        con.modeE()
        wx.CallAfter(pub.sendMessage, "update", msg="         Zerando...")
        time.sleep(1)
        valor2 = con.modeCAMZERO(10000*self.p1, self.p1Sen)
        if valor2 == 'p1ok':
            print 'PRESSAO CAMARA ZERADA'
            wx.CallAfter(pub.sendMessage, "update", msg="       σ3 - Zerado!")
            time.sleep(1)

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return
