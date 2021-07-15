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
    def __init__(self, p2, A1, A2):
        Thread.__init__(self)
        self.start()
        self.p2 = p2
        self.a1 = A1
        self.a2 = A2
        self._return = True

    #-------------------------------------------------------------------
    def run(self):
        wx.CallAfter(pub.sendMessage, "update", msg="  Ativando motor...")
        time.sleep(1)
        con.modeM()
        time.sleep(1)
        wx.CallAfter(pub.sendMessage, "update", msg="       Ajustando...")
        valor = con.modeMotor((10000*self.a2/self.a1)*self.p2)
        if valor == 'p2ok':
            print 'PRESSAO GOLPES OK'
            wx.CallAfter(pub.sendMessage, "update", msg="            σd - ok")
            time.sleep(1)

        i = 0
        cond = True
        while i < 3 and cond == True:
            i = i+1
            time.sleep(1)
            wx.CallAfter(pub.sendMessage, "update", msg="     golpe teste...")
            con.modeG(1,1)
            time.sleep(10)
            while True:
                a = con.modeBuffer()
                if a == True:
                    break

            val = con.ColetaI()
            print val[4]
            if val[4] < (self.p2 - self.p2/10):
                cond = True
                wx.CallAfter(pub.sendMessage, "update", msg="  Ativando motor...")
                time.sleep(1)
                con.modeM()
                time.sleep(1)
                wx.CallAfter(pub.sendMessage, "update", msg="       Ajustando...")
                valor = con.modeMotor((10000*self.a2/self.a1)*self.p2)
                if valor == 'p2ok':
                    print 'PRESSAO GOLPES OK'
                    wx.CallAfter(pub.sendMessage, "update", msg="            σd - ok")
                    time.sleep(1)
            else:
                cond = False
                wx.CallAfter(pub.sendMessage, "update", msg=" teste realizado...")
                wx.CallAfter(pub.sendMessage, "update", msg="               _ok_")
                wx.CallAfter(pub.sendMessage, "update", msg="            σd - ok")

        if i == 1:
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            self._return = True

        if i == 2:
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            self._return = True

        if i == 3:
            self._return = False

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return
