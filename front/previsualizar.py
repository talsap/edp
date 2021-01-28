# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx

'''Tela de Preview do Cabeçalho do PDF'''
class Preview(wx.Frame):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, None, -1, 'Pré-Visualização', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Iserção do IconeLogo'''
            ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)

            '''Configurações do Size'''
            self.SetSize((650,400))

            self.Bind(wx.EVT_PAINT, self.OnPaint)
            self.Centre()
            self.Show()

    #--------------------------------------------------
        def OnPaint(self, event):
            '''Opcao de Adicionar Logo'''
            dc = wx.ClientDC(self)

            dc.SetPen(wx.Pen('#4c4c4c', 1, wx.SOLID))
            dc.DrawRectangle(23, 30, 600, 350)
