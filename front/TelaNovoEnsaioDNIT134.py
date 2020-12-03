# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx

'''Tela Selecão de Ensaio'''
class TelaNovoEnsaioDNIT134(wx.Frame):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, None, -1, 'EDP - DNIT 134/2018ME', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Iserção do IconeLogo'''
            ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)

            '''Configurações do Size'''
            self.SetSize((450,600))
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self)


            self.Centre()
            self.Show()


    #--------------------------------------------------
        def Prosseguir(self, event):
            pass
