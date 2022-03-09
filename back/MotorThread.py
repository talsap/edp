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
    def __init__(self, p2, A1, A2, golpeTeste):
        Thread.__init__(self)
        self.start()
        self.p2 = p2
        self.a1 = A1
        self.a2 = A2
        self.golpeTeste = golpeTeste
        self._return = True

    #-------------------------------------------------------------------
    def run(self):
        con.modeS()
        wx.CallAfter(pub.sendMessage, "update", msg="  Ativando motor...")
        time.sleep(.5)
        con.modeM()
        time.sleep(.5)
        wx.CallAfter(pub.sendMessage, "update", msg="       Ajustando...")
        valor = con.modeMotor((10000*self.a2/self.a1)*(self.p2))
        if valor == 'p2ok':
            print 'PRESSAO GOLPES OK'
            wx.CallAfter(pub.sendMessage, "update", msg="            σd - ok")
            time.sleep(.2)
            wx.CallAfter(pub.sendMessage, "update", msg="")

        #Parte do golpe teste
        if self.golpeTeste == True:
            time.sleep(.5)
            con.modeG()
            wx.CallAfter(pub.sendMessage, "update", msg="     golpe teste...")
            con.modeGOLPES(1,1)
            con.modeS()
            time.sleep(2)
            wx.CallAfter(pub.sendMessage, "update", msg="  Ativando motor...")
            time.sleep(.5)
            con.modeM()
            time.sleep(.5)
            wx.CallAfter(pub.sendMessage, "update", msg="       Ajustando...")
            valor = con.modeMotor((10000*self.a2/self.a1)*self.p2)
            if valor == 'p2ok':
                print 'PRESSAO GOLPES OK'
                wx.CallAfter(pub.sendMessage, "update", msg="            σd - ok")
                time.sleep(.2)
                wx.CallAfter(pub.sendMessage, "update", msg="")
                con.modeI()
                self._return = True
        else:
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            con.modeI()
            self._return = True

        '''i = 0
        cond = True
        while i < 3 and cond == True:
            i = i+1
            time.sleep(1)
            con.modeG()
            wx.CallAfter(pub.sendMessage, "update", msg="     golpe teste...")
            con.modeGOLPES(1,1)
            time.sleep(12)
            kj = 0
            while True:
                kj += 1
                a = con.modeBuffer()
                if a == True:
                    break
                if kj > 500:
                    break

            kj = 0
            try:
                con.modeJ()
                time.sleep(1)
                val = con.ColetaII()
            except:
                while True:
                    kj += 1
                    a = con.modeBuffer()
                    if a == True:
                        break
                    if kj > 500:
                        break
            kj = 0
            try:
                con.modeJ()
                time.sleep(1)
                val = con.ColetaII()
            except:
                while True:
                    kj += 1
                    a = con.modeBuffer()
                    if a == True:
                        break
                    if kj > 500:
                        break

            con.modeJ()
            time.sleep(1)
            val = con.ColetaII()
            print val
            if val < (self.p2 - self.p2/10):
                cond = True
                con.modeS()
                wx.CallAfter(pub.sendMessage, "update", msg="  Ativando motor...")
                time.sleep(.5)
                con.modeM()
                time.sleep(.5)
                wx.CallAfter(pub.sendMessage, "update", msg="       Ajustando...")
                valor = con.modeMotor((10000*self.a2/self.a1)*self.p2)
                if valor == 'p2ok':
                    print 'PRESSAO GOLPES OK'
                    wx.CallAfter(pub.sendMessage, "update", msg="            σd - ok")
                    time.sleep(.2)
            else:
                cond = False
                wx.CallAfter(pub.sendMessage, "update", msg=" teste realizado...")
                wx.CallAfter(pub.sendMessage, "update", msg="               _ok_")
                wx.CallAfter(pub.sendMessage, "update", msg="            σd - ok")
                break

        if i == 1:
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            con.modeI()
            self._return = True

        if i == 2:
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            wx.CallAfter(pub.sendMessage, "update", msg="")
            con.modeI()
            self._return = True

        if i == 3:
            con.modeI()
            self._return = False'''
        #Parte do golpe teste
    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return

########################################################################
'''MotorThread'''
class MotorThreadZero(Thread):
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
        con.modeS()
        wx.CallAfter(pub.sendMessage, "update", msg="  Ativando motor...")
        time.sleep(.5)
        con.modeMS()
        time.sleep(.5)
        wx.CallAfter(pub.sendMessage, "update", msg="         Zerando...")
        valor = con.modeMotorZero((10000*self.a2/self.a1)*self.p2)
        if valor == 'p2ok':
            print 'PRESSAO GOLPES OK'
            wx.CallAfter(pub.sendMessage, "update", msg="        σd - Zerado")
            time.sleep(1)
            wx.CallAfter(pub.sendMessage, "update", msg="")
            con.modeI()
