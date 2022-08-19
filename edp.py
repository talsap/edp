# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import sys
import front.tela as tela
import ctypes

'''usado para ocultar o console'''
#ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )

'''Inicializacao do programa'''
class main():
     version = '1.0.0'
     app = wx.App()
     app.locale = wx.Locale(wx.LANGUAGE_PORTUGUESE_BRAZILIAN)
     app.SetTopWindow(tela.Tela(version))
     app.MainLoop()
     app.RestoreStdio()
     app.__del__
     app.Destroy()
main()