# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import sys
import front.tela as tela

'''Inicializacao do programa'''
class main():
     version = '1.0.0'
     app = wx.App()
     app.locale = wx.Locale(wx.LANGUAGE_PORTUGUESE_BRAZILIAN)
     tela.Tela(version)
     app.MainLoop()
     app.RestoreStdio()
     app.__del__
main()
