# -*- coding: utf-8 -*-
import wx
import time
import back.connection as con
from pubsub import pub
from threading import Thread

VETOR_COND = [[0.070,0.070],
              [0.070,0.210],
              [0.105,0.315]]

VETOR_MR =  [[0.020,0.020],
             [0.020,0.040],
             [0.020,0.060],
             [0.035,0.035],
             [0.035,0.070],
             [0.035,0.105],
             [0.050,0.050],
             [0.050,0.100],
             [0.050,0.150],
             [0.070,0.070],
             [0.070,0.140],
             [0.070,0.210],
             [0.105,0.105],
             [0.105,0.210],
             [0.105,0.315],
             [0.140,0.140],
             [0.140,0.280],
             [0.140,0.420]]

########################################################################
'''MotorThread'''
class MotorThread(Thread):
    #-------------------------------------------------------------------
    def __init__(self, p1, p2, A1, A2):
        Thread.__init__(self)
        self.start()
        self.p1 = p1
        self.p2 = p2
        self.a1 = A1
        self.a2 = A2

    #-------------------------------------------------------------------
    def run(self):
        wx.CallAfter(pub.sendMessage, "update", msg="Ativando válvula")
        time.sleep(1)
        con.modeE()
        time.sleep(1)
        wx.CallAfter(pub.sendMessage, "update", msg="Regulando...")
        valor2 = con.modeCAM(10000*self.p2)
        if valor2 == 'p2ok':
            print 'PRESSAO CAMARA OK'
            wx.CallAfter(pub.sendMessage, "update", msg="σ3 - ok")
            time.sleep(1)

        wx.CallAfter(pub.sendMessage, "update", msg="Ativando motor")
        time.sleep(1)
        con.modeM()
        time.sleep(1)
        wx.CallAfter(pub.sendMessage, "update", msg="Ajustando...")
        valor = con.modeMotor((10000*self.a2/self.a1)*self.p1)
        if valor == 'p1ok':
            print 'PRESSAO GOLPES OK'
            wx.CallAfter(pub.sendMessage, "update", msg="σd - ok")
            time.sleep(1)

        i = 0
        cond = True
        while i <3 and cond == True:
            i = i+1
            time.sleep(1)
            wx.CallAfter(pub.sendMessage, "update", msg="...golpe teste")
            con.modeG(1,1)
            time.sleep(15)
            valor = con.ColetaI()
            if valor[4] < (10*self.p1 - 1*self.p1):
                cond = True
                wx.CallAfter(pub.sendMessage, "update", msg="Ativando motor")
                time.sleep(1)
                con.modeM()
                time.sleep(1)
                wx.CallAfter(pub.sendMessage, "update", msg="Ajustando...")
                valor = con.modeMotor((10000*self.a2/self.a1)*self.p1)
                if valor == 'p1ok':
                    print 'PRESSAO GOLPES OK'
                    wx.CallAfter(pub.sendMessage, "update", msg="σd - ok")
                    time.sleep(1)
            else:
                cond = False
                wx.CallAfter(pub.sendMessage, "update", msg="teste")
                wx.CallAfter(pub.sendMessage, "update", msg="...ok")
                wx.CallAfter(pub.sendMessage, "update", msg="σd - ok")

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return

########################################################################
'''MyProgressDialog'''
class MyProgressDialog(wx.Dialog):
    #-------------------------------------------------------------------
    def __init__(self, k):
        """Construtor"""
        wx.Dialog.__init__(self, None, -1, size=(500,15), style=0)
        self.Centre()
        self.k = k
        self.count = 0
        self.progress = wx.Gauge(self, range = self.k)
        self.texto = wx.StaticText(self, label = wx.EmptyString, style = wx.ALIGN_CENTRE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        sizer1.AddStretchSpacer(1)
        sizer1.Add(self.texto, 2, wx.ALIGN_CENTER)
        sizer1.Add(sizer, 8, wx.ALIGN_CENTER)
        self.SetSizer(sizer1)
        # create a pubsub receiver
        pub.subscribe(self.updateProgress, "update")

    #-------------------------------------------------------------------
    def updateProgress(self, msg):
        self.count += 1
        if self.count < self.k:
            self.texto.SetLabel(msg)
        if self.count >= self.k:
            self.Destroy()
        self.progress.SetValue(self.count)
