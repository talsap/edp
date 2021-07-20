# -*- coding: utf-8 -*-
import wx
import time
import bancodedados
import back.connection as con
from pubsub import pub
from threading import Thread

########################################################################
'''SaveThread'''
class SaveThread(Thread):
    #-------------------------------------------------------------------
    def __init__(self, idt, x, y, pc, pg):
        Thread.__init__(self)
        self.idt = idt
        self.x = x
        self.y = y
        self.pc = pc
        self.pg = pg
        self._return = True
        self.start()

    #-------------------------------------------------------------------
    def run(self):
        x =  self.x
        i = 0
        while i < len(x):
            wx.CallAfter(pub.sendMessage, "update", msg="  Salvando dados...")
            bancodedados.saveDNIT134(self.idt, x[i], self.y[i], self.pc[i], self.pg[i])
            i += 1

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return
