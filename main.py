# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import front.tela as tela

'''Inicializacao do programa'''
class main():
     app = wx.App()
     app.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
     tela.Tela(None)
     app.MainLoop()

main()
