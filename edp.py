# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import front.tela as tela

'''Inicializacao do programa'''
class main():
     version = '1.0.0'
     app = wx.App()
     app.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
     tela.Tela(version)
     app.MainLoop()
main()
