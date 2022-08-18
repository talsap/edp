# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import back.HexForRGB as HexRGB
import banco.bdPreferences as bdPreferences 

'''Tela Dialogo Dinamico'''
class dialogoDinamico(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, indicador, info, texto0, texto1, texto2, texto3, texto4, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, "%s" %info, style = wx.CLOSE_BOX)

            colors = bdPreferences.ListColors()
            colorBackground = colors[2]

            self.SetBackgroundColour(colorBackground)
            
            self.v_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.Bind(wx.EVT_CLOSE, self.onExit)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo2 = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

            if indicador == 1:
                TextoTitle = wx.StaticText(self, label = texto0, style = wx.ALIGN_CENTRE)
                TextoTitle.SetFont(FontTitle)
                TextoTitle.SetForegroundColour((0,51,188))
                TextoCorpo1 = wx.StaticText(self, label = texto1, style = wx.ALIGN_CENTRE)
                TextoCorpo1.SetFont(FontCorpo1)
                TextoCorpo2 = wx.StaticText(self, label = texto2, style = wx.ALIGN_CENTRE)
                TextoCorpo2.SetFont(FontCorpo2)
                TextoCorpo2.SetForegroundColour((231,160,48))
                TextoCorpo3 = wx.StaticText(self, label = texto3, style = wx.ALIGN_CENTRE)
                TextoCorpo3.SetFont(FontCorpo1)
                Button = wx.Button(self, id = wx.ID_CANCEL, label = "OK", style = wx.BORDER_NONE)
                self.v_sizer.Add(TextoTitle, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo1, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo2, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo3, 1, wx.CENTER)
                self.v_sizer.Add(Button, 1, wx.ALL | wx.CENTER)
                self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
                self.SetSize((400,185))

            if indicador == 2:
                FontCorpo2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
                TextoTitle = wx.StaticText(self, label = texto0, style = wx.ALIGN_CENTRE)
                TextoTitle.SetFont(FontTitle)
                TextoTitle.SetForegroundColour((0,51,188))
                TextoCorpo1 = wx.StaticText(self, label = texto1, style = wx.ALIGN_CENTRE)
                TextoCorpo1.SetFont(FontCorpo1)
                TextoCorpo2 = wx.StaticText(self, label = texto2, style = wx.ALIGN_CENTRE)
                TextoCorpo2.SetFont(FontCorpo2)
                TextoCorpo2.SetForegroundColour((231,160,48))
                Button = wx.Button(self, label = "OK", style = wx.BORDER_NONE)
                self.v_sizer.Add(TextoTitle, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo1, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo2, 2, wx.CENTER)
                self.v_sizer.Add(Button, 1, wx.ALL | wx.CENTER)
                self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
                self.SetSize((620,185))

            if indicador == 3:
                FontCorpo2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
                TextoTitle = wx.StaticText(self, label = texto0, style = wx.ALIGN_CENTRE)
                TextoTitle.SetFont(FontTitle)
                TextoTitle.SetForegroundColour((0,51,188))
                TextoCorpo1 = wx.StaticText(self, label = texto1, style = wx.ALIGN_CENTRE)
                TextoCorpo1.SetFont(FontCorpo1)
                TextoCorpo2 = wx.StaticText(self, label = texto2, style = wx.ALIGN_CENTRE)
                TextoCorpo2.SetFont(FontCorpo2)
                TextoCorpo2.SetForegroundColour((231,160,48))
                Button = wx.Button(self, label = "OK", style = wx.BORDER_NONE)
                self.v_sizer.Add(TextoTitle, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo1, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo2, 2, wx.CENTER)
                self.v_sizer.Add(Button, 1, wx.ALL | wx.CENTER)
                self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
                self.SetSize((620,185))

            self.Bind(wx.EVT_BUTTON, self.Button, Button)
            self.SetSizer(self.h_sizer)

            self.Centre()
            self.Show()
            
    #--------------------------------------------------
        def Button(self, event):
            self.EndModal(wx.ID_OK)
            self.Destroy()
        
    #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()
