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
    def __init__(self, p1, A1, A2, p1Ant):
        Thread.__init__(self)
        self.start()
        self.p1 = p1
        self.a1 = A1
        self.a2 = A2
        self.p1Ant = p1Ant

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
