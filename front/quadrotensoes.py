# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx

'''Tela Dialogo Dinamico'''
class quadro(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, "Quadro de Tensões")

            v_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo2 = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

            labels0 = [["  σ3 (MPa)          ","          σd (MPa)            ","             σ1/σ3     "]]

            labels1 = [["0.070","0.070","2"],
                        ["0.070","0.210","4"],
                        ["0.105","0.315","4"]]

            labels = [[["0.020","0.020","2"],
                       ["0.020","0.040","3"],
                       ["0.020","0.060","4"]],
                       [["0.035","0.035","2"],
                       ["0.035","0.070","3"],
                       ["0.035","0.105","4"]],
                       [["0.050","0.050","2"],
                       ["0.050","0.100","3"],
                       ["0.050","0.150","4"]],
                       [["0.070","0.070","2"],
                       ["0.070","0.140","3"],
                       ["0.070","0.210","4"]],
                       [["0.105","0.105","2"],
                       ["0.105","0.210","3"],
                       ["0.105","0.315","4"]],
                       [["0.140","0.140","2"],
                       ["0.140","0.280","3"],
                       ["0.140","0.420","4"]]]


            v_sizer = wx.BoxSizer(wx.VERTICAL)
            TextoTitle = wx.StaticText(self, label = "QUADRO DE TENSÕES - CONDIC.", style = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            TextoTitle.SetFont(FontTitle)
            TextoTitle.SetForegroundColour((0,51,188))
            v_sizer.Add(TextoTitle, 1, wx.ALL | wx.CENTER, 10)

            s1 = wx.GridBagSizer(hgap=0, vgap=3)
            for coll in range(3):
                textUnidades = wx.StaticText(self, label = labels0[0][coll], style = wx.ALIGN_CENTER)
                s1.Add(textUnidades, pos=(0,coll), span=(1,1), flag = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            v_sizer.Add(s1, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)

            s2 = wx.GridBagSizer(hgap=3, vgap=3)
            for coll in range(3):
                for roww in range(3):
                    textCond = wx.TextCtrl(self, -1, labels1[roww][coll], style = wx.TE_READONLY | wx.TE_CENTER)
                    textCond.Disable()
                    s2.Add(textCond, pos=(roww,coll))
            v_sizer.Add(s2, 1, wx.ALL, 4)

            v_sizer.AddStretchSpacer(1)

            TextoTitle2 = wx.StaticText(self, label = "QUADRO DE TENSÕES - M.R.", style = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            TextoTitle2.SetFont(FontTitle)
            TextoTitle2.SetForegroundColour((0,51,188))
            v_sizer.Add(TextoTitle2, 1, wx.ALL | wx.CENTER, 10)

            s3 = wx.GridBagSizer(hgap=0, vgap=3)
            for coll in range(3):
                textUnidades2 = wx.StaticText(self, label = labels0[0][coll], style = wx.ALIGN_CENTER)
                s3.Add(textUnidades2, pos=(0,coll), span=(1,1), flag = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            v_sizer.Add(s3, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)

            sizer = wx.GridBagSizer(hgap=6, vgap=0)
            for row in range(6):
                s4 = wx.GridBagSizer(hgap=3, vgap=3)
                for coll in range(3):
                    for roww in range(3):
                        text = wx.TextCtrl(self, -1, labels[row][roww][coll], style = wx.TE_READONLY | wx.TE_CENTER)
                        text.Disable()
                        s4.Add(text, pos=(roww,coll))
                sizer.Add(s4, pos=(row,0), flag= wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)

            v_sizer.Add(sizer, wx.ALL, border=20)


            v_sizer.Add(sizer, 1, wx.ALL | wx.EXPAND  | wx.CENTER)
            h_sizer.Add(v_sizer, 1, wx.ALL | wx.CENTER, 10)
            self.SetSizer(h_sizer)
            self.SetSize((369,745))
            self.Centre()
            self.Show()
