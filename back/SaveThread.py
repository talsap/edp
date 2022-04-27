# -*- coding: utf-8 -*-
import wx
import time
import bancodedados
import back.connection as con
from pubsub import pub
from threading import Thread

########################################################################
'''SaveThreadADM'''
class SaveThreadADM(Thread):
    #-------------------------------------------------------------------
    def __init__(self, idt, x, y1, yt1, y2, yt2, pc, pg, r1, r2):
        Thread.__init__(self)
        self.idt = idt
        self.x = x
        self.y1 = y1
        self.yt1 = yt1
        self.y2 = y2
        self.yt2 = yt2
        self.pc = pc
        self.pg = pg
        self.r1 = r1
        self.r2 = r2
        self._return = True
        self.start()

    #-------------------------------------------------------------------
    def run(self):
        x =  self.x
        i = 0
        bancodedados.saveReferenciaADM(self.idt, self.r1, self.r2)
        while i < len(x)-2:
            wx.CallAfter(pub.sendMessage, "update", msg="  Salvando dados...")
            bancodedados.saveDNIT134ADM(self.idt, x[i], self.y1[i], self.yt1[i], self.y2[i], self.yt2[i], self.pc[i], self.pg[i])
            i += 1

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return
