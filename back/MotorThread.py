# -*- coding: utf-8 -*-
import wx
import time
import back.connection as con
from pubsub import pub
from threading import Thread

########################################################################
'''MotorThread'''
class MotorThread(Thread):
    #-------------------------------------------------------------------
    def __init__(self, p1):
        Thread.__init__(self)
        self.start()
        self.p1 = p1
        self._return = True

    #-------------------------------------------------------------------
    def run(self):
        con.modeS()
        wx.CallAfter(pub.sendMessage, "update", msg="  Ativando motor...")
        time.sleep(.5)
        con.modeM()
        time.sleep(.5)
        wx.CallAfter(pub.sendMessage, "update", msg="       Ajustando...")
        valor = con.modeMotor(10000*self.p1)
        if valor == 'p1ok':
            print 'PRESSAO CAMARA OK'
            wx.CallAfter(pub.sendMessage, "update", msg="            σ3 - ok")
            time.sleep(.2)

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return

########################################################################
'''MotorThread'''
class MotorThreadZero(Thread):
    #-------------------------------------------------------------------
    def __init__(self, p1):
        Thread.__init__(self)
        self.start()
        self.p1 = p1
        self._return = True

    #-------------------------------------------------------------------
    def run(self):
        con.modeS()
        wx.CallAfter(pub.sendMessage, "update", msg="  Ativando motor...")
        time.sleep(.5)
        con.modeMS()
        time.sleep(.5)
        wx.CallAfter(pub.sendMessage, "update", msg="         Zerando...")
        valor = con.modeMotorZero(10000*self.p1)
        if valor == 'p1ok':
            print 'PRESSAO CAMARA OK'
            wx.CallAfter(pub.sendMessage, "update", msg="        σ3 - Zerado")
            time.sleep(1)
            wx.CallAfter(pub.sendMessage, "update", msg="")
            con.modeI()
