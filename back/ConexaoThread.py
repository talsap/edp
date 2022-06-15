# -*- coding: utf-8 -*-
import wx
import back.connection as con
from threading import Thread
from pubsub import pub

########################################################################
'''ConexaoThread'''
class ConexaoThread(Thread):
    #-------------------------------------------------------------------
    def __init__(self, DISCREP):
        Thread.__init__(self)
        self.start()
        self.DISCREP = DISCREP
    #-------------------------------------------------------------------
    def run(self):
        wx.CallAfter(pub.sendMessage, "update", msg="      Conectando...")
        try:
            valor = con.connect(self.DISCREP)
            if valor[1] == 'connectado':
                print 'CONECTADO'
                wx.CallAfter(pub.sendMessage, "update", msg="          CONECTADO")
                self._return = 'connectado', valor[0]
            else:
                print 'DESCONECTADO'
                wx.CallAfter(pub.sendMessage, "update", msg="       DESCONECTADO")
                self._return = 'desconnectado'
        except:
            print 'ERRO VALOR DISCREP'
            wx.CallAfter(pub.sendMessage, "update", msg="       DESCONECTADO")
            self._return = 'desconnectado'
    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return
