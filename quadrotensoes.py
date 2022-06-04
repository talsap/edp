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

'''Quadro de Tensões Editável DNIT134'''
class quadroEditavelDNIT134(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, "Quadro de Tensões")

            v_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)

            FontTitle = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo2 = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

            labels0 = [["σ3 (MPa)","σd (MPa)","σ1/σ3"]]

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

            TextoTitle = wx.StaticText(self, label = "QUADRO DE TENSÕES - CONDIC.", style = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            TextoTitle.SetFont(FontTitle)
            TextoTitle.SetForegroundColour((0,51,188))
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            v_sizer.Add(TextoTitle, 1, wx.ALL | wx.CENTER, 10)

            #---------------------------------------
            text1= wx.StaticText(self, label = "σ3 (MPa)", style = wx.ALL | wx.CENTER)
            text2= wx.StaticText(self, label = "σd (MPa)", style = wx.ALL | wx.CENTER)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h_sizer.Add(text1, 1, wx.ALL | wx.CENTER)
            h_sizer.AddStretchSpacer(2)
            h_sizer.Add(text2, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h0_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h0_sizer.AddStretchSpacer(1)
            tL0C0 = wx.TextCtrl(self, -1, labels1[0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tL0C0.Disable()
            h0_sizer.Add(tL0C0, 1, wx.ALL | wx.CENTER)
            h0_sizer.AddStretchSpacer(1)
            tL0C1 = wx.TextCtrl(self, -1, labels1[0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tL0C1.Disable()
            h0_sizer.Add(tL0C1, 1, wx.ALL | wx.CENTER)
            h0_sizer.AddStretchSpacer(1)

            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h1_sizer.AddStretchSpacer(1)
            tL1C0 = wx.TextCtrl(self, -1, labels1[1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tL1C0.Disable()
            h1_sizer.Add(tL1C0, 1, wx.ALL | wx.CENTER)
            h1_sizer.AddStretchSpacer(1)
            tL1C1 = wx.TextCtrl(self, -1, labels1[1][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tL1C1.Disable()
            h1_sizer.Add(tL1C1, 1, wx.ALL | wx.CENTER)
            h1_sizer.AddStretchSpacer(1)

            h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h2_sizer.AddStretchSpacer(1)
            tL2C0 = wx.TextCtrl(self, -1, labels1[2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tL2C0.Disable()
            h2_sizer.Add(tL2C0, 1, wx.ALL | wx.CENTER)
            h2_sizer.AddStretchSpacer(1)
            tL2C1 = wx.TextCtrl(self, -1, labels1[2][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tL2C1.Disable()
            h2_sizer.Add(tL2C1, 1, wx.ALL | wx.CENTER)
            h2_sizer.AddStretchSpacer(1)

            #---------------------------------------
            v1_sizer = wx.BoxSizer(wx.VERTICAL)
            v1_sizer.Add(h_sizer, 1, wx.ALL | wx.CENTER)
            v1_sizer.Add(h0_sizer, 1, wx.ALL | wx.CENTER)
            v1_sizer.Add(h1_sizer, 1, wx.ALL | wx.CENTER)
            v1_sizer.Add(h2_sizer, 1, wx.ALL | wx.CENTER)
            v1_sizer.AddStretchSpacer(1)

            v_sizer.Add(v1_sizer, 4, wx.ALL | wx.CENTER)

            #---------------------------------------
            TextoTitle2 = wx.StaticText(self, label = "QUADRO DE TENSÕES - M. R.", style = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            TextoTitle2.SetFont(FontTitle)
            TextoTitle2.SetForegroundColour((0,51,188))
            v_sizer.AddStretchSpacer(1)
            v_sizer.Add(TextoTitle2, 1, wx.ALL | wx.CENTER, 10)

            #---------------------------------------
            text3= wx.StaticText(self, label = "σ3 (MPa)", style = wx.ALL | wx.CENTER)
            text4= wx.StaticText(self, label = "σd (MPa)", style = wx.ALL | wx.CENTER)
            h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h3_sizer.Add(text3, 1, wx.ALL | wx.CENTER)
            h3_sizer.AddStretchSpacer(2)
            h3_sizer.Add(text4, 1, wx.ALL | wx.CENTER)

            #---------------------------------------L1L2L3
            h4_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h4_sizer.AddStretchSpacer(1)
            tmL1C0 = wx.TextCtrl(self, -1, labels[0][0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL1C0.Disable()
            h4_sizer.Add(tmL1C0, 1, wx.ALL | wx.CENTER)
            h4_sizer.AddStretchSpacer(1)
            tmL1C1 = wx.TextCtrl(self, -1, labels[0][0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL1C1.Disable()
            h4_sizer.Add(tmL1C1, 1, wx.ALL | wx.CENTER)
            h4_sizer.AddStretchSpacer(1)

            h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h5_sizer.AddStretchSpacer(1)
            tmL2C0 = wx.TextCtrl(self, -1, labels[0][1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL2C0.Disable()
            h5_sizer.Add(tmL2C0, 1, wx.ALL | wx.CENTER)
            h5_sizer.AddStretchSpacer(1)
            tmL2C1 = wx.TextCtrl(self, -1, labels[0][1][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL2C1.Disable()
            h5_sizer.Add(tmL2C1, 1, wx.ALL | wx.CENTER)
            h5_sizer.AddStretchSpacer(1)

            h6_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h6_sizer.AddStretchSpacer(1)
            tmL3C0 = wx.TextCtrl(self, -1, labels[0][2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL3C0.Disable()
            h6_sizer.Add(tmL3C0, 1, wx.ALL | wx.CENTER)
            h6_sizer.AddStretchSpacer(1)
            tmL3C1 = wx.TextCtrl(self, -1, labels[0][2][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL3C1.Disable()
            h6_sizer.Add(tmL3C1, 1, wx.ALL | wx.CENTER)
            h6_sizer.AddStretchSpacer(1)

            #---------------------------------------L4L5L6
            h7_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h7_sizer.AddStretchSpacer(1)
            tmL4C0 = wx.TextCtrl(self, -1, labels[1][0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL4C0.Disable()
            h7_sizer.Add(tmL4C0, 1, wx.ALL | wx.CENTER)
            h7_sizer.AddStretchSpacer(1)
            tmL4C1 = wx.TextCtrl(self, -1, labels[1][0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL4C1.Disable()
            h7_sizer.Add(tmL4C1, 1, wx.ALL | wx.CENTER)
            h7_sizer.AddStretchSpacer(1)

            h8_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h8_sizer.AddStretchSpacer(1)
            tmL5C0 = wx.TextCtrl(self, -1, labels[1][1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL5C0.Disable()
            h8_sizer.Add(tmL5C0, 1, wx.ALL | wx.CENTER)
            h8_sizer.AddStretchSpacer(1)
            tmL5C1 = wx.TextCtrl(self, -1, labels[1][1][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL5C1.Disable()
            h8_sizer.Add(tmL5C1, 1, wx.ALL | wx.CENTER)
            h8_sizer.AddStretchSpacer(1)

            h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h9_sizer.AddStretchSpacer(1)
            tmL6C0 = wx.TextCtrl(self, -1, labels[1][2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL6C0.Disable()
            h9_sizer.Add(tmL6C0, 1, wx.ALL | wx.CENTER)
            h9_sizer.AddStretchSpacer(1)
            tmL6C1 = wx.TextCtrl(self, -1, labels[1][2][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL6C1.Disable()
            h9_sizer.Add(tmL6C1, 1, wx.ALL | wx.CENTER)
            h9_sizer.AddStretchSpacer(1)

            #---------------------------------------L7L8L9
            h10_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h10_sizer.AddStretchSpacer(1)
            tmL7C0 = wx.TextCtrl(self, -1, labels[2][0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL7C0.Disable()
            h10_sizer.Add(tmL7C0, 1, wx.ALL | wx.CENTER)
            h10_sizer.AddStretchSpacer(1)
            tmL7C1 = wx.TextCtrl(self, -1, labels[2][0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL7C1.Disable()
            h10_sizer.Add(tmL7C1, 1, wx.ALL | wx.CENTER)
            h10_sizer.AddStretchSpacer(1)

            h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h11_sizer.AddStretchSpacer(1)
            tmL8C0 = wx.TextCtrl(self, -1, labels[2][1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL8C0.Disable()
            h11_sizer.Add(tmL8C0, 1, wx.ALL | wx.CENTER)
            h11_sizer.AddStretchSpacer(1)
            tmL8C1 = wx.TextCtrl(self, -1, labels[2][1][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL8C1.Disable()
            h11_sizer.Add(tmL8C1, 1, wx.ALL | wx.CENTER)
            h11_sizer.AddStretchSpacer(1)

            h12_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h12_sizer.AddStretchSpacer(1)
            tmL9C0 = wx.TextCtrl(self, -1, labels[2][2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL9C0.Disable()
            h12_sizer.Add(tmL9C0, 1, wx.ALL | wx.CENTER)
            h12_sizer.AddStretchSpacer(1)
            tmL9C1 = wx.TextCtrl(self, -1, labels[2][2][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL9C1.Disable()
            h12_sizer.Add(tmL9C1, 1, wx.ALL | wx.CENTER)
            h12_sizer.AddStretchSpacer(1)

            #---------------------------------------L10L11L12
            h13_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h13_sizer.AddStretchSpacer(1)
            tmL10C0 = wx.TextCtrl(self, -1, labels[3][0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL10C0.Disable()
            h13_sizer.Add(tmL10C0, 1, wx.ALL | wx.CENTER)
            h13_sizer.AddStretchSpacer(1)
            tmL10C1 = wx.TextCtrl(self, -1, labels[3][0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL10C1.Disable()
            h13_sizer.Add(tmL10C1, 1, wx.ALL | wx.CENTER)
            h13_sizer.AddStretchSpacer(1)

            h14_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h14_sizer.AddStretchSpacer(1)
            tmL11C0 = wx.TextCtrl(self, -1, labels[3][1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL11C0.Disable()
            h14_sizer.Add(tmL11C0, 1, wx.ALL | wx.CENTER)
            h14_sizer.AddStretchSpacer(1)
            tmL11C1 = wx.TextCtrl(self, -1, labels[3][1][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL11C1.Disable()
            h14_sizer.Add(tmL11C1, 1, wx.ALL | wx.CENTER)
            h14_sizer.AddStretchSpacer(1)

            h15_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h15_sizer.AddStretchSpacer(1)
            tmL12C0 = wx.TextCtrl(self, -1, labels[3][2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL12C0.Disable()
            h15_sizer.Add(tmL12C0, 1, wx.ALL | wx.CENTER)
            h15_sizer.AddStretchSpacer(1)
            tmL12C1 = wx.TextCtrl(self, -1, labels[3][2][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL12C1.Disable()
            h15_sizer.Add(tmL12C1, 1, wx.ALL | wx.CENTER)
            h15_sizer.AddStretchSpacer(1)

            #---------------------------------------L13L14L15
            h16_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h16_sizer.AddStretchSpacer(1)
            tmL13C0 = wx.TextCtrl(self, -1, labels[4][0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL13C0.Disable()
            h16_sizer.Add(tmL13C0, 1, wx.ALL | wx.CENTER)
            h16_sizer.AddStretchSpacer(1)
            tmL13C1 = wx.TextCtrl(self, -1, labels[4][0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL13C1.Disable()
            h16_sizer.Add(tmL13C1, 1, wx.ALL | wx.CENTER)
            h16_sizer.AddStretchSpacer(1)

            h17_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h17_sizer.AddStretchSpacer(1)
            tmL14C0 = wx.TextCtrl(self, -1, labels[4][1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL14C0.Disable()
            h17_sizer.Add(tmL14C0, 1, wx.ALL | wx.CENTER)
            h17_sizer.AddStretchSpacer(1)
            tmL14C1 = wx.TextCtrl(self, -1, labels[4][1][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL14C1.Disable()
            h17_sizer.Add(tmL14C1, 1, wx.ALL | wx.CENTER)
            h17_sizer.AddStretchSpacer(1)

            h18_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h18_sizer.AddStretchSpacer(1)
            tmL15C0 = wx.TextCtrl(self, -1, labels[4][2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL15C0.Disable()
            h18_sizer.Add(tmL15C0, 1, wx.ALL | wx.CENTER)
            h18_sizer.AddStretchSpacer(1)
            tmL15C1 = wx.TextCtrl(self, -1, labels[4][2][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL15C1.Disable()
            h18_sizer.Add(tmL15C1, 1, wx.ALL | wx.CENTER)
            h18_sizer.AddStretchSpacer(1)

            #---------------------------------------L16L17L18
            h19_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h19_sizer.AddStretchSpacer(1)
            tmL16C0 = wx.TextCtrl(self, -1, labels[5][0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL16C0.Disable()
            h19_sizer.Add(tmL16C0, 1, wx.ALL | wx.CENTER)
            h19_sizer.AddStretchSpacer(1)
            tmL16C1 = wx.TextCtrl(self, -1, labels[5][0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL16C1.Disable()
            h19_sizer.Add(tmL16C1, 1, wx.ALL | wx.CENTER)
            h19_sizer.AddStretchSpacer(1)

            h20_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h20_sizer.AddStretchSpacer(1)
            tmL17C0 = wx.TextCtrl(self, -1, labels[5][1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL17C0.Disable()
            h20_sizer.Add(tmL17C0, 1, wx.ALL | wx.CENTER)
            h20_sizer.AddStretchSpacer(1)
            tmL17C1 = wx.TextCtrl(self, -1, labels[5][1][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL17C1.Disable()
            h20_sizer.Add(tmL17C1, 1, wx.ALL | wx.CENTER)
            h20_sizer.AddStretchSpacer(1)

            h21_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h21_sizer.AddStretchSpacer(1)
            tmL18C0 = wx.TextCtrl(self, -1, labels[5][2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL18C0.Disable()
            h21_sizer.Add(tmL18C0, 1, wx.ALL | wx.CENTER)
            h21_sizer.AddStretchSpacer(1)
            tmL18C1 = wx.TextCtrl(self, -1, labels[5][2][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL18C1.Disable()
            h21_sizer.Add(tmL18C1, 1, wx.ALL | wx.CENTER)
            h21_sizer.AddStretchSpacer(1)

            #---------------------------------------
            self.editar1 = wx.Button(self, -1, 'Editar', style = wx.CENTER)
            self.Salvar1 = wx.Button(self, -1, 'Salvar', style = wx.CENTER)
            self.Salvar1.Disable()
            h22_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h22_sizer.Add(self.editar1, 1)
            h22_sizer.AddStretchSpacer(2)
            h22_sizer.Add(self.Salvar1, 1)

            #---------------------------------------
            v2_sizer = wx.BoxSizer(wx.VERTICAL)
            v2_sizer.Add(h3_sizer, 1, wx.ALL | wx.CENTER)

            v2_sizer.Add(h4_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h5_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h6_sizer, 2, wx.ALL | wx.CENTER)

            v2_sizer.Add(h7_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h8_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h9_sizer, 2, wx.ALL | wx.CENTER)

            v2_sizer.Add(h10_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h11_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h12_sizer, 2, wx.ALL | wx.CENTER)

            v2_sizer.Add(h13_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h14_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h15_sizer, 2, wx.ALL | wx.CENTER)

            v2_sizer.Add(h16_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h17_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h18_sizer, 2, wx.ALL | wx.CENTER)

            v2_sizer.Add(h19_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h20_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h21_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.AddStretchSpacer(1)
            v2_sizer.Add(h22_sizer, 1, wx.ALL | wx.CENTER)
            v2_sizer.AddStretchSpacer(1)

            v_sizer.Add(v2_sizer, 18, wx.ALL | wx.CENTER)

            self.SetSizer(v_sizer)
            self.SetSize((369,710))
            self.Centre()
            self.Show()

'''Quadro de Tensões Editável DNIT179'''
class quadroEditavelDNIT179(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, "Quadro de Tensões")

            v_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)

            FontTitle = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo2 = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

            labels0 = [["σ3 (MPa)","σd (MPa)","σ1/σ3"]]

            labels1 = [["0.030","0.030","2"]]

            labels = [[["0.040","0.040","2"],
                       ["0.040","0.080","3"],
                       ["0.040","0.120","4"]],
                       [["0.080","0.080","2"],
                       ["0.080","0.160","3"],
                       ["0.080","0.240","4"]],
                       [["0.120","0.120","2"],
                       ["0.120","0.240","3"],
                       ["0.120","0.360","4"]]]

            TextoTitle = wx.StaticText(self, label = "QUADRO DE TENSÕES - CONDIC.", style = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            TextoTitle.SetFont(FontTitle)
            TextoTitle.SetForegroundColour((0,51,188))
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            v_sizer.Add(TextoTitle, 1, wx.ALL | wx.CENTER, 10)

            #---------------------------------------
            text1= wx.StaticText(self, label = "σ3 (MPa)", style = wx.ALL | wx.CENTER)
            text2= wx.StaticText(self, label = "σd (MPa)", style = wx.ALL | wx.CENTER)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h_sizer.Add(text1, 1, wx.ALL | wx.CENTER)
            h_sizer.AddStretchSpacer(2)
            h_sizer.Add(text2, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h0_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h0_sizer.AddStretchSpacer(1)
            tL0C0 = wx.TextCtrl(self, -1, labels1[0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tL0C0.Disable()
            h0_sizer.Add(tL0C0, 1, wx.ALL | wx.CENTER)
            h0_sizer.AddStretchSpacer(1)
            tL0C1 = wx.TextCtrl(self, -1, labels1[0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tL0C1.Disable()
            h0_sizer.Add(tL0C1, 1, wx.ALL | wx.CENTER)
            h0_sizer.AddStretchSpacer(1)

            #---------------------------------------
            v1_sizer = wx.BoxSizer(wx.VERTICAL)
            v1_sizer.Add(h_sizer, 1, wx.ALL | wx.CENTER)
            v1_sizer.Add(h0_sizer, 1, wx.ALL | wx.CENTER)
            v1_sizer.AddStretchSpacer(1)

            v_sizer.Add(v1_sizer, 4, wx.ALL | wx.CENTER)

            #---------------------------------------
            TextoTitle2 = wx.StaticText(self, label = "QUADRO DE TENSÕES - D. P.", style = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            TextoTitle2.SetFont(FontTitle)
            TextoTitle2.SetForegroundColour((0,51,188))
            v_sizer.AddStretchSpacer(1)
            v_sizer.Add(TextoTitle2, 1, wx.ALL | wx.CENTER, 10)

            #---------------------------------------
            text3= wx.StaticText(self, label = "σ3 (MPa)", style = wx.ALL | wx.CENTER)
            text4= wx.StaticText(self, label = "σd (MPa)", style = wx.ALL | wx.CENTER)
            h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h3_sizer.Add(text3, 1, wx.ALL | wx.CENTER)
            h3_sizer.AddStretchSpacer(2)
            h3_sizer.Add(text4, 1, wx.ALL | wx.CENTER)

            #---------------------------------------L1L2L3
            h4_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h4_sizer.AddStretchSpacer(1)
            tmL1C0 = wx.TextCtrl(self, -1, labels[0][0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL1C0.Disable()
            h4_sizer.Add(tmL1C0, 1, wx.ALL | wx.CENTER)
            h4_sizer.AddStretchSpacer(1)
            tmL1C1 = wx.TextCtrl(self, -1, labels[0][0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL1C1.Disable()
            h4_sizer.Add(tmL1C1, 1, wx.ALL | wx.CENTER)
            h4_sizer.AddStretchSpacer(1)

            h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h5_sizer.AddStretchSpacer(1)
            tmL2C0 = wx.TextCtrl(self, -1, labels[0][1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL2C0.Disable()
            h5_sizer.Add(tmL2C0, 1, wx.ALL | wx.CENTER)
            h5_sizer.AddStretchSpacer(1)
            tmL2C1 = wx.TextCtrl(self, -1, labels[0][1][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL2C1.Disable()
            h5_sizer.Add(tmL2C1, 1, wx.ALL | wx.CENTER)
            h5_sizer.AddStretchSpacer(1)

            h6_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h6_sizer.AddStretchSpacer(1)
            tmL3C0 = wx.TextCtrl(self, -1, labels[0][2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL3C0.Disable()
            h6_sizer.Add(tmL3C0, 1, wx.ALL | wx.CENTER)
            h6_sizer.AddStretchSpacer(1)
            tmL3C1 = wx.TextCtrl(self, -1, labels[0][2][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL3C1.Disable()
            h6_sizer.Add(tmL3C1, 1, wx.ALL | wx.CENTER)
            h6_sizer.AddStretchSpacer(1)

            #---------------------------------------L4L5L6
            h7_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h7_sizer.AddStretchSpacer(1)
            tmL4C0 = wx.TextCtrl(self, -1, labels[1][0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL4C0.Disable()
            h7_sizer.Add(tmL4C0, 1, wx.ALL | wx.CENTER)
            h7_sizer.AddStretchSpacer(1)
            tmL4C1 = wx.TextCtrl(self, -1, labels[1][0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL4C1.Disable()
            h7_sizer.Add(tmL4C1, 1, wx.ALL | wx.CENTER)
            h7_sizer.AddStretchSpacer(1)

            h8_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h8_sizer.AddStretchSpacer(1)
            tmL5C0 = wx.TextCtrl(self, -1, labels[1][1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL5C0.Disable()
            h8_sizer.Add(tmL5C0, 1, wx.ALL | wx.CENTER)
            h8_sizer.AddStretchSpacer(1)
            tmL5C1 = wx.TextCtrl(self, -1, labels[1][1][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL5C1.Disable()
            h8_sizer.Add(tmL5C1, 1, wx.ALL | wx.CENTER)
            h8_sizer.AddStretchSpacer(1)

            h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h9_sizer.AddStretchSpacer(1)
            tmL6C0 = wx.TextCtrl(self, -1, labels[1][2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL6C0.Disable()
            h9_sizer.Add(tmL6C0, 1, wx.ALL | wx.CENTER)
            h9_sizer.AddStretchSpacer(1)
            tmL6C1 = wx.TextCtrl(self, -1, labels[1][2][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL6C1.Disable()
            h9_sizer.Add(tmL6C1, 1, wx.ALL | wx.CENTER)
            h9_sizer.AddStretchSpacer(1)

            #---------------------------------------L7L8L9
            h10_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h10_sizer.AddStretchSpacer(1)
            tmL7C0 = wx.TextCtrl(self, -1, labels[2][0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL7C0.Disable()
            h10_sizer.Add(tmL7C0, 1, wx.ALL | wx.CENTER)
            h10_sizer.AddStretchSpacer(1)
            tmL7C1 = wx.TextCtrl(self, -1, labels[2][0][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL7C1.Disable()
            h10_sizer.Add(tmL7C1, 1, wx.ALL | wx.CENTER)
            h10_sizer.AddStretchSpacer(1)

            h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h11_sizer.AddStretchSpacer(1)
            tmL8C0 = wx.TextCtrl(self, -1, labels[2][1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL8C0.Disable()
            h11_sizer.Add(tmL8C0, 1, wx.ALL | wx.CENTER)
            h11_sizer.AddStretchSpacer(1)
            tmL8C1 = wx.TextCtrl(self, -1, labels[2][1][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL8C1.Disable()
            h11_sizer.Add(tmL8C1, 1, wx.ALL | wx.CENTER)
            h11_sizer.AddStretchSpacer(1)

            h12_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h12_sizer.AddStretchSpacer(1)
            tmL9C0 = wx.TextCtrl(self, -1, labels[2][2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL9C0.Disable()
            h12_sizer.Add(tmL9C0, 1, wx.ALL | wx.CENTER)
            h12_sizer.AddStretchSpacer(1)
            tmL9C1 = wx.TextCtrl(self, -1, labels[2][2][1], style = wx.TE_READONLY | wx.TE_CENTER)
            tmL9C1.Disable()
            h12_sizer.Add(tmL9C1, 1, wx.ALL | wx.CENTER)
            h12_sizer.AddStretchSpacer(1)

            #---------------------------------------
            self.editar1 = wx.Button(self, -1, 'Editar', style = wx.CENTER)
            self.Salvar1 = wx.Button(self, -1, 'Salvar', style = wx.CENTER)
            self.Salvar1.Disable()
            h22_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h22_sizer.Add(self.editar1, 1)
            h22_sizer.AddStretchSpacer(2)
            h22_sizer.Add(self.Salvar1, 1)

            #---------------------------------------
            v2_sizer = wx.BoxSizer(wx.VERTICAL)
            v2_sizer.Add(h3_sizer, 1, wx.ALL | wx.CENTER)

            v2_sizer.Add(h4_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h5_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h6_sizer, 2, wx.ALL | wx.CENTER)

            v2_sizer.Add(h7_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h8_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h9_sizer, 2, wx.ALL | wx.CENTER)

            v2_sizer.Add(h10_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h11_sizer, 2, wx.ALL | wx.CENTER)
            v2_sizer.Add(h12_sizer, 2, wx.ALL | wx.CENTER)

            v2_sizer.AddStretchSpacer(1)
            v2_sizer.Add(h22_sizer, 1, wx.ALL | wx.CENTER)
            v2_sizer.AddStretchSpacer(1)

            v_sizer.Add(v2_sizer, 18, wx.ALL | wx.CENTER)

            self.SetSizer(v_sizer)
            self.SetSize((369,460))
            self.Centre()
            self.Show()

'''Quadro de Tensões Editável DNIT181'''
class quadroEditavelDNIT181(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, "Quadro de Tensões")

            v_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)

            FontTitle = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo2 = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

            labels1 = [["0.100"],
                      ["0.200"],
                      ["0.300"],
                      ["0.400"],
                      ["0.500"]]

            TextoTitle = wx.StaticText(self, label = "QUADRO DE TENSÕES - M. R.", style = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            TextoTitle.SetFont(FontTitle)
            TextoTitle.SetForegroundColour((0,51,188))

            #---------------------------------------
            text1= wx.StaticText(self, label = "σ1 (MPa)", style = wx.ALL | wx.CENTER)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h_sizer.Add(text1, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h0_sizer = wx.BoxSizer(wx.HORIZONTAL)
            tL0C0 = wx.TextCtrl(self, -1, labels1[0][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tL0C0.Disable()
            h0_sizer.Add(tL0C0, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            tL1C0 = wx.TextCtrl(self, -1, labels1[1][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tL1C0.Disable()
            h1_sizer.Add(tL1C0, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            tL2C0 = wx.TextCtrl(self, -1, labels1[2][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tL2C0.Disable()
            h2_sizer.Add(tL2C0, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            tL3C0 = wx.TextCtrl(self, -1, labels1[3][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tL3C0.Disable()
            h3_sizer.Add(tL3C0, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h4_sizer = wx.BoxSizer(wx.HORIZONTAL)
            tL4C0 = wx.TextCtrl(self, -1, labels1[4][0], style = wx.TE_READONLY | wx.TE_CENTER)
            tL4C0.Disable()
            h4_sizer.Add(tL4C0, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            self.editar1 = wx.Button(self, -1, 'Editar', style = wx.CENTER)
            self.Salvar1 = wx.Button(self, -1, 'Salvar', style = wx.CENTER)
            self.Salvar1.Disable()

            h22_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h22_sizer.Add(self.editar1, 1)
            h22_sizer.AddStretchSpacer(2)
            h22_sizer.Add(self.Salvar1, 1)

            #---------------------------------------
            v1_sizer = wx.BoxSizer(wx.VERTICAL)
            v1_sizer.Add(TextoTitle, 1, wx.ALL | wx.CENTER)
            v1_sizer.Add(h_sizer, 2, wx.ALL | wx.CENTER)
            v1_sizer.Add(h0_sizer, 2, wx.ALL | wx.CENTER)
            v1_sizer.Add(h1_sizer, 2, wx.ALL | wx.CENTER)
            v1_sizer.Add(h2_sizer, 2, wx.ALL | wx.CENTER)
            v1_sizer.Add(h3_sizer, 2, wx.ALL | wx.CENTER)
            v1_sizer.Add(h4_sizer, 2, wx.ALL | wx.CENTER)
            v1_sizer.AddStretchSpacer(1)
            v1_sizer.Add(h22_sizer, 1, wx.ALL | wx.CENTER)

            v_sizer = wx.BoxSizer(wx.VERTICAL)
            v_sizer.Add(v1_sizer, 4, wx.ALL | wx.CENTER, 15)

            self.SetSizer(v_sizer)
            self.SetSize((369,260))
            self.Centre()
            self.Show()

if __name__ == "__main__":
	app = wx.App()
	frame = quadroEditavelDNIT181(None)
	frame.Show()
	app.MainLoop()
