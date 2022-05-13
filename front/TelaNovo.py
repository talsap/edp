# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
from TelaNovoEnsaioDNIT134 import TelaNovoEnsaioDNIT134

#normas = ['DNIT 134/2018ME', 'DNIT 135/2018ME', 'DNIT 179/2018IE', 'DNIT 184/2018ME', 'DNIT 416/2019ME']
normas = ['DNIT 134/2018ME']

'''Tela Selecão de Ensaio'''
class TelaNovo(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, None, -1, 'EDP - Beta', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

            '''Configurações do Size'''
            self.SetSize((250,200))
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            title = wx.StaticText(panel, label = "ENSAIOS DINÂMICOS", style = wx.ALIGN_CENTRE)
            title.SetFont(FontTitle)
            '''title.SetBackgroundColour("green")'''
            v_sizer.Add(title, 1, wx.EXPAND | wx.ALL, 15)

            texto1 = wx.StaticText(panel, label = "NORMA", style = wx.ALIGN_CENTER_VERTICAL)
            h_sizer.Add(texto1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
            self.combo = wx.ComboBox(panel, choices = normas, style = wx.EXPAND | wx.CB_READONLY)
            h_sizer.Add(self.combo, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

            v_sizer.Add(h_sizer, 1, wx.EXPAND | wx.ALL, 12)
            v_sizer.AddStretchSpacer(1)
            continuar = wx.Button(panel, -1, 'Continuar')
            v_sizer.Add(continuar, 1,  wx.EXPAND| wx.ALL, 15)

            panel.SetSizer(v_sizer)
            self.Centre()
            self.Show()

            continuar.Bind(wx.EVT_BUTTON, self.Prosseguir)

    #--------------------------------------------------
        def Prosseguir(self, event):
            a = self.combo.GetSelection()
            '''Acessa a DNIT 134/2018ME'''
            if a == 0:
                self.Close(True)
                frame = TelaNovoEnsaioDNIT134().ShowModal()
