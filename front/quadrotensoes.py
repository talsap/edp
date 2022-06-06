# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import bancodedados

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

            label = bancodedados.QD_134()
            labels1 = label[0]
            labels = label[1]

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
                    if coll == 2:
                        textCond = wx.TextCtrl(self, -1, "%.0f" % labels1[roww][coll], style = wx.TE_READONLY | wx.TE_CENTER)
                    else:
                        textCond = wx.TextCtrl(self, -1, "%.3f" % labels1[roww][coll], style = wx.TE_READONLY | wx.TE_CENTER)
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
                        if coll == 2:
                            text = wx.TextCtrl(self, -1, "%.0f" % labels[row][roww][coll], style = wx.TE_READONLY | wx.TE_CENTER)
                        else:
                            text = wx.TextCtrl(self, -1, "%.3f" % labels[row][roww][coll], style = wx.TE_READONLY | wx.TE_CENTER)
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

            label = bancodedados.QD_134()
            labels1 = label[0]
            labels = label[1]

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
            t01 = wx.StaticText(self, label = "1", style = wx.ALL | wx.ALIGN_RIGHT)
            t01.SetForegroundColour((119,118,114))
            h0_sizer.Add(t01, 1, wx.ALL | wx.CENTER, 5)
            self.tL0C0 = wx.TextCtrl(self, -1, "%.3f" % labels1[0][0], style = wx.TE_CENTER)
            self.tL0C0.Disable()
            h0_sizer.Add(self.tL0C0, 1, wx.ALL | wx.CENTER)
            h0_sizer.AddStretchSpacer(1)
            self.tL0C1 = wx.TextCtrl(self, -1, "%.3f" % labels1[0][1], style = wx.TE_CENTER)
            self.tL0C1.Disable()
            h0_sizer.Add(self.tL0C1, 1, wx.ALL | wx.CENTER)
            h0_sizer.AddStretchSpacer(1)

            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t02 = wx.StaticText(self, label = "2", style = wx.ALL | wx.ALIGN_RIGHT)
            t02.SetForegroundColour((119,118,114))
            h1_sizer.Add(t02, 1, wx.ALL | wx.CENTER, 5)
            self.tL1C0 = wx.TextCtrl(self, -1, "%.3f" % labels1[1][0], style = wx.TE_CENTER)
            self.tL1C0.Disable()
            h1_sizer.Add(self.tL1C0, 1, wx.ALL | wx.CENTER)
            h1_sizer.AddStretchSpacer(1)
            self.tL1C1 = wx.TextCtrl(self, -1, "%.3f" % labels1[1][1], style = wx.TE_CENTER)
            self.tL1C1.Disable()
            h1_sizer.Add(self.tL1C1, 1, wx.ALL | wx.CENTER)
            h1_sizer.AddStretchSpacer(1)

            h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t03 = wx.StaticText(self, label = "3", style = wx.ALL | wx.ALIGN_RIGHT)
            t03.SetForegroundColour((119,118,114))
            h2_sizer.Add(t03, 1, wx.ALL | wx.CENTER, 5)
            self.tL2C0 = wx.TextCtrl(self, -1, "%.3f" % labels1[2][0], style = wx.TE_CENTER)
            self.tL2C0.Disable()
            h2_sizer.Add(self.tL2C0, 1, wx.ALL | wx.CENTER)
            h2_sizer.AddStretchSpacer(1)
            self.tL2C1 = wx.TextCtrl(self, -1, "%.3f" % labels1[2][1], style = wx.TE_CENTER)
            self.tL2C1.Disable()
            h2_sizer.Add(self.tL2C1, 1, wx.ALL | wx.CENTER)
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
            t1 = wx.StaticText(self, label = "1   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t1.SetForegroundColour((119,118,114))
            h4_sizer.Add(t1, 1, wx.ALL | wx.CENTER)
            self.tmL1C0 = wx.TextCtrl(self, -1, "%.3f" % labels[0][0][0], style = wx.TE_CENTER)
            self.tmL1C0.Disable()
            h4_sizer.Add(self.tmL1C0, 1, wx.ALL | wx.CENTER)
            h4_sizer.AddStretchSpacer(1)
            self.tmL1C1 = wx.TextCtrl(self, -1, "%.3f" % labels[0][0][1], style = wx.TE_CENTER)
            self.tmL1C1.Disable()
            h4_sizer.Add(self.tmL1C1, 1, wx.ALL | wx.CENTER)
            h4_sizer.AddStretchSpacer(1)

            h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t2 = wx.StaticText(self, label = "2   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t2.SetForegroundColour((119,118,114))
            h5_sizer.Add(t2, 1, wx.ALL | wx.CENTER)
            self.tmL2C0 = wx.TextCtrl(self, -1, "%.3f" % labels[0][1][0], style = wx.TE_CENTER)
            self.tmL2C0.Disable()
            h5_sizer.Add(self.tmL2C0, 1, wx.ALL | wx.CENTER)
            h5_sizer.AddStretchSpacer(1)
            self.tmL2C1 = wx.TextCtrl(self, -1, "%.3f" % labels[0][1][1], style = wx.TE_CENTER)
            self.tmL2C1.Disable()
            h5_sizer.Add(self.tmL2C1, 1, wx.ALL | wx.CENTER)
            h5_sizer.AddStretchSpacer(1)

            h6_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t3 = wx.StaticText(self, label = "3   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t3.SetForegroundColour((119,118,114))
            h6_sizer.Add(t3, 1, wx.ALL | wx.CENTER)
            self.tmL3C0 = wx.TextCtrl(self, -1, "%.3f" % labels[0][2][0], style = wx.TE_CENTER)
            self.tmL3C0.Disable()
            h6_sizer.Add(self.tmL3C0, 1, wx.ALL | wx.CENTER)
            h6_sizer.AddStretchSpacer(1)
            self.tmL3C1 = wx.TextCtrl(self, -1, "%.3f" % labels[0][2][1], style = wx.TE_CENTER)
            self.tmL3C1.Disable()
            h6_sizer.Add(self.tmL3C1, 1, wx.ALL | wx.CENTER)
            h6_sizer.AddStretchSpacer(1)

            #---------------------------------------L4L5L6
            h7_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t4 = wx.StaticText(self, label = "4   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t4.SetForegroundColour((119,118,114))
            h7_sizer.Add(t4, 1, wx.ALL | wx.CENTER)
            self.tmL4C0 = wx.TextCtrl(self, -1, "%.3f" % labels[1][0][0], style = wx.TE_CENTER)
            self.tmL4C0.Disable()
            h7_sizer.Add(self.tmL4C0, 1, wx.ALL | wx.CENTER)
            h7_sizer.AddStretchSpacer(1)
            self.tmL4C1 = wx.TextCtrl(self, -1, "%.3f" % labels[1][0][1], style = wx.TE_CENTER)
            self.tmL4C1.Disable()
            h7_sizer.Add(self.tmL4C1, 1, wx.ALL | wx.CENTER)
            h7_sizer.AddStretchSpacer(1)

            h8_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t5 = wx.StaticText(self, label = "5   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t5.SetForegroundColour((119,118,114))
            h8_sizer.Add(t5, 1, wx.ALL | wx.CENTER)
            self.tmL5C0 = wx.TextCtrl(self, -1, "%.3f" % labels[1][1][0], style = wx.TE_CENTER)
            self.tmL5C0.Disable()
            h8_sizer.Add(self.tmL5C0, 1, wx.ALL | wx.CENTER)
            h8_sizer.AddStretchSpacer(1)
            self.tmL5C1 = wx.TextCtrl(self, -1, "%.3f" % labels[1][1][1], style = wx.TE_CENTER)
            self.tmL5C1.Disable()
            h8_sizer.Add(self.tmL5C1, 1, wx.ALL | wx.CENTER)
            h8_sizer.AddStretchSpacer(1)

            h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t6 = wx.StaticText(self, label = "6   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t6.SetForegroundColour((119,118,114))
            h9_sizer.Add(t6, 1, wx.ALL | wx.CENTER)
            self.tmL6C0 = wx.TextCtrl(self, -1, "%.3f" % labels[1][2][0], style = wx.TE_CENTER)
            self.tmL6C0.Disable()
            h9_sizer.Add(self.tmL6C0, 1, wx.ALL | wx.CENTER)
            h9_sizer.AddStretchSpacer(1)
            self.tmL6C1 = wx.TextCtrl(self, -1, "%.3f" % labels[1][2][1], style = wx.TE_CENTER)
            self.tmL6C1.Disable()
            h9_sizer.Add(self.tmL6C1, 1, wx.ALL | wx.CENTER)
            h9_sizer.AddStretchSpacer(1)

            #---------------------------------------L7L8L9
            h10_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t7 = wx.StaticText(self, label = "7   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t7.SetForegroundColour((119,118,114))
            h10_sizer.Add(t7, 1, wx.ALL | wx.CENTER)
            self.tmL7C0 = wx.TextCtrl(self, -1, "%.3f" % labels[2][0][0], style = wx.TE_CENTER)
            self.tmL7C0.Disable()
            h10_sizer.Add(self.tmL7C0, 1, wx.ALL | wx.CENTER)
            h10_sizer.AddStretchSpacer(1)
            self.tmL7C1 = wx.TextCtrl(self, -1, "%.3f" % labels[2][0][1], style = wx.TE_CENTER)
            self.tmL7C1.Disable()
            h10_sizer.Add(self.tmL7C1, 1, wx.ALL | wx.CENTER)
            h10_sizer.AddStretchSpacer(1)

            h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t8 = wx.StaticText(self, label = "8   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t8.SetForegroundColour((119,118,114))
            h11_sizer.Add(t8, 1, wx.ALL | wx.CENTER)
            self.tmL8C0 = wx.TextCtrl(self, -1, "%.3f" % labels[2][1][0], style = wx.TE_CENTER)
            self.tmL8C0.Disable()
            h11_sizer.Add(self.tmL8C0, 1, wx.ALL | wx.CENTER)
            h11_sizer.AddStretchSpacer(1)
            self.tmL8C1 = wx.TextCtrl(self, -1, "%.3f" % labels[2][1][1], style = wx.TE_CENTER)
            self.tmL8C1.Disable()
            h11_sizer.Add(self.tmL8C1, 1, wx.ALL | wx.CENTER)
            h11_sizer.AddStretchSpacer(1)

            h12_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t9 = wx.StaticText(self, label = "9   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t9.SetForegroundColour((119,118,114))
            h12_sizer.Add(t9, 1, wx.ALL | wx.CENTER)
            self.tmL9C0 = wx.TextCtrl(self, -1, "%.3f" % labels[2][2][0], style = wx.TE_CENTER)
            self.tmL9C0.Disable()
            h12_sizer.Add(self.tmL9C0, 1, wx.ALL | wx.CENTER)
            h12_sizer.AddStretchSpacer(1)
            self.tmL9C1 = wx.TextCtrl(self, -1, "%.3f" % labels[2][2][1], style = wx.TE_CENTER)
            self.tmL9C1.Disable()
            h12_sizer.Add(self.tmL9C1, 1, wx.ALL | wx.CENTER)
            h12_sizer.AddStretchSpacer(1)

            #---------------------------------------L10L11L12
            h13_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t10 = wx.StaticText(self, label = "10   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t10.SetForegroundColour((119,118,114))
            h13_sizer.Add(t10, 1, wx.ALL | wx.CENTER)
            self.tmL10C0 = wx.TextCtrl(self, -1, "%.3f" % labels[3][0][0], style = wx.TE_CENTER)
            self.tmL10C0.Disable()
            h13_sizer.Add(self.tmL10C0, 1, wx.ALL | wx.CENTER)
            h13_sizer.AddStretchSpacer(1)
            self.tmL10C1 = wx.TextCtrl(self, -1, "%.3f" % labels[3][0][1], style = wx.TE_CENTER)
            self.tmL10C1.Disable()
            h13_sizer.Add(self.tmL10C1, 1, wx.ALL | wx.CENTER)
            h13_sizer.AddStretchSpacer(1)

            h14_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t11 = wx.StaticText(self, label = "11   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t11.SetForegroundColour((119,118,114))
            h14_sizer.Add(t11, 1, wx.ALL | wx.CENTER)
            self.tmL11C0 = wx.TextCtrl(self, -1, "%.3f" % labels[3][1][0], style = wx.TE_CENTER)
            self.tmL11C0.Disable()
            h14_sizer.Add(self.tmL11C0, 1, wx.ALL | wx.CENTER)
            h14_sizer.AddStretchSpacer(1)
            self.tmL11C1 = wx.TextCtrl(self, -1, "%.3f" % labels[3][1][1], style = wx.TE_CENTER)
            self.tmL11C1.Disable()
            h14_sizer.Add(self.tmL11C1, 1, wx.ALL | wx.CENTER)
            h14_sizer.AddStretchSpacer(1)

            h15_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t12 = wx.StaticText(self, label = "12   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t12.SetForegroundColour((119,118,114))
            h15_sizer.Add(t12, 1, wx.ALL | wx.CENTER)
            self.tmL12C0 = wx.TextCtrl(self, -1, "%.3f" % labels[3][2][0], style = wx.TE_CENTER)
            self.tmL12C0.Disable()
            h15_sizer.Add(self.tmL12C0, 1, wx.ALL | wx.CENTER)
            h15_sizer.AddStretchSpacer(1)
            self.tmL12C1 = wx.TextCtrl(self, -1, "%.3f" % labels[3][2][1], style = wx.TE_CENTER)
            self.tmL12C1.Disable()
            h15_sizer.Add(self.tmL12C1, 1, wx.ALL | wx.CENTER)
            h15_sizer.AddStretchSpacer(1)

            #---------------------------------------L13L14L15
            h16_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t13 = wx.StaticText(self, label = "13   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t13.SetForegroundColour((119,118,114))
            h16_sizer.Add(t13, 1, wx.ALL | wx.CENTER)
            self.tmL13C0 = wx.TextCtrl(self, -1, "%.3f" % labels[4][0][0], style = wx.TE_CENTER)
            self.tmL13C0.Disable()
            h16_sizer.Add(self.tmL13C0, 1, wx.ALL | wx.CENTER)
            h16_sizer.AddStretchSpacer(1)
            self.tmL13C1 = wx.TextCtrl(self, -1, "%.3f" % labels[4][0][1], style = wx.TE_CENTER)
            self.tmL13C1.Disable()
            h16_sizer.Add(self.tmL13C1, 1, wx.ALL | wx.CENTER)
            h16_sizer.AddStretchSpacer(1)

            h17_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t14 = wx.StaticText(self, label = "14   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t14.SetForegroundColour((119,118,114))
            h17_sizer.Add(t14, 1, wx.ALL | wx.CENTER)
            self.tmL14C0 = wx.TextCtrl(self, -1, "%.3f" % labels[4][1][0], style = wx.TE_CENTER)
            self.tmL14C0.Disable()
            h17_sizer.Add(self.tmL14C0, 1, wx.ALL | wx.CENTER)
            h17_sizer.AddStretchSpacer(1)
            self.tmL14C1 = wx.TextCtrl(self, -1, "%.3f" % labels[4][1][1], style = wx.TE_CENTER)
            self.tmL14C1.Disable()
            h17_sizer.Add(self.tmL14C1, 1, wx.ALL | wx.CENTER)
            h17_sizer.AddStretchSpacer(1)

            h18_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t15 = wx.StaticText(self, label = "15   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t15.SetForegroundColour((119,118,114))
            h18_sizer.Add(t15, 1, wx.ALL | wx.CENTER)
            self.tmL15C0 = wx.TextCtrl(self, -1, "%.3f" % labels[4][2][0], style = wx.TE_CENTER)
            self.tmL15C0.Disable()
            h18_sizer.Add(self.tmL15C0, 1, wx.ALL | wx.CENTER)
            h18_sizer.AddStretchSpacer(1)
            self.tmL15C1 = wx.TextCtrl(self, -1, "%.3f" % labels[4][2][1], style = wx.TE_CENTER)
            self.tmL15C1.Disable()
            h18_sizer.Add(self.tmL15C1, 1, wx.ALL | wx.CENTER)
            h18_sizer.AddStretchSpacer(1)

            #---------------------------------------L16L17L18
            h19_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t16 = wx.StaticText(self, label = "16   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t16.SetForegroundColour((119,118,114))
            h19_sizer.Add(t16, 1, wx.ALL | wx.CENTER)
            self.tmL16C0 = wx.TextCtrl(self, -1, "%.3f" % labels[5][0][0], style = wx.TE_CENTER)
            self.tmL16C0.Disable()
            h19_sizer.Add(self.tmL16C0, 1, wx.ALL | wx.CENTER)
            h19_sizer.AddStretchSpacer(1)
            self.tmL16C1 = wx.TextCtrl(self, -1, "%.3f" % labels[5][0][1], style = wx.TE_CENTER)
            self.tmL16C1.Disable()
            h19_sizer.Add(self.tmL16C1, 1, wx.ALL | wx.CENTER)
            h19_sizer.AddStretchSpacer(1)

            h20_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t17 = wx.StaticText(self, label = "17   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t17.SetForegroundColour((119,118,114))
            h20_sizer.Add(t17, 1, wx.ALL | wx.CENTER)
            self.tmL17C0 = wx.TextCtrl(self, -1, "%.3f" % labels[5][1][0], style = wx.TE_CENTER)
            self.tmL17C0.Disable()
            h20_sizer.Add(self.tmL17C0, 1, wx.ALL | wx.CENTER)
            h20_sizer.AddStretchSpacer(1)
            self.tmL17C1 = wx.TextCtrl(self, -1, "%.3f" % labels[5][1][1], style = wx.TE_CENTER)
            self.tmL17C1.Disable()
            h20_sizer.Add(self.tmL17C1, 1, wx.ALL | wx.CENTER)
            h20_sizer.AddStretchSpacer(1)

            h21_sizer = wx.BoxSizer(wx.HORIZONTAL)
            t18 = wx.StaticText(self, label = "18   ", style = wx.ALL | wx.ALIGN_RIGHT)
            t18.SetForegroundColour((119,118,114))
            h21_sizer.Add(t18, 1, wx.ALL | wx.CENTER)
            self.tmL18C0 = wx.TextCtrl(self, -1, "%.3f" % labels[5][2][0], style = wx.TE_CENTER)
            self.tmL18C0.Disable()
            h21_sizer.Add(self.tmL18C0, 1, wx.ALL | wx.CENTER)
            h21_sizer.AddStretchSpacer(1)
            self.tmL18C1 = wx.TextCtrl(self, -1, "%.3f" % labels[5][2][1], style = wx.TE_CENTER)
            self.tmL18C1.Disable()
            h21_sizer.Add(self.tmL18C1, 1, wx.ALL | wx.CENTER)
            h21_sizer.AddStretchSpacer(1)

            #---------------------------------------
            self.editar1 = wx.Button(self, -1, 'Editar', style = wx.CENTER)
            self.Salvar1 = wx.Button(self, -1, 'Salvar', style = wx.CENTER)
            self.Salvar1.Disable()
            self.Bind(wx.EVT_BUTTON, self.Editar1, self.editar1)
            self.Bind(wx.EVT_BUTTON, self.Salva1, self.Salvar1)
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

        #--------------------------------------------------
        def Editar1(self, event):
                '''Edita...'''
                self.tL0C0.Enable()
                self.tL0C1.Enable()
                self.tL1C0.Enable()
                self.tL1C1.Enable()
                self.tL2C0.Enable()
                self.tL2C1.Enable()

                self.tmL1C0.Enable()
                self.tmL1C1.Enable()
                self.tmL2C0.Enable()
                self.tmL2C1.Enable()
                self.tmL3C0.Enable()
                self.tmL3C1.Enable()

                self.tmL4C0.Enable()
                self.tmL4C1.Enable()
                self.tmL5C0.Enable()
                self.tmL5C1.Enable()
                self.tmL6C0.Enable()
                self.tmL6C1.Enable()

                self.tmL7C0.Enable()
                self.tmL7C1.Enable()
                self.tmL8C0.Enable()
                self.tmL8C1.Enable()
                self.tmL9C0.Enable()
                self.tmL9C1.Enable()

                self.tmL10C0.Enable()
                self.tmL10C1.Enable()
                self.tmL11C0.Enable()
                self.tmL11C1.Enable()
                self.tmL12C0.Enable()
                self.tmL12C1.Enable()

                self.tmL13C0.Enable()
                self.tmL13C1.Enable()
                self.tmL14C0.Enable()
                self.tmL14C1.Enable()
                self.tmL15C0.Enable()
                self.tmL15C1.Enable()

                self.tmL16C0.Enable()
                self.tmL16C1.Enable()
                self.tmL17C0.Enable()
                self.tmL17C1.Enable()
                self.tmL18C0.Enable()
                self.tmL18C1.Enable()

                self.editar1.Disable()
                self.Salvar1.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva1(self, event):
                '''Salva...'''
                CL1C0 = self.tL0C0.GetValue()
                CL1C1 = self.tL0C1.GetValue()
                CL2C0 = self.tL1C0.GetValue()
                CL2C1 = self.tL1C1.GetValue()
                CL3C0 = self.tL2C0.GetValue()
                CL3C1 = self.tL2C1.GetValue()

                ML1C0 = self.tmL1C0.GetValue()
                ML1C1 = self.tmL1C1.GetValue()
                ML2C0 = self.tmL2C0.GetValue()
                ML2C1 = self.tmL2C1.GetValue()
                ML3C0 = self.tmL3C0.GetValue()
                ML3C1 = self.tmL3C1.GetValue()

                ML4C0 = self.tmL4C0.GetValue()
                ML4C1 = self.tmL4C1.GetValue()
                ML5C0 = self.tmL5C0.GetValue()
                ML5C1 = self.tmL5C1.GetValue()
                ML6C0 = self.tmL6C0.GetValue()
                ML6C1 = self.tmL6C1.GetValue()

                ML7C0 = self.tmL7C0.GetValue()
                ML7C1 = self.tmL7C1.GetValue()
                ML8C0 = self.tmL8C0.GetValue()
                ML8C1 = self.tmL8C1.GetValue()
                ML9C0 = self.tmL9C0.GetValue()
                ML9C1 = self.tmL9C1.GetValue()

                ML10C0 = self.tmL10C0.GetValue()
                ML10C1 = self.tmL10C1.GetValue()
                ML11C0 = self.tmL11C0.GetValue()
                ML11C1 = self.tmL11C1.GetValue()
                ML12C0 = self.tmL12C0.GetValue()
                ML12C1 = self.tmL12C1.GetValue()

                ML13C0 = self.tmL13C0.GetValue()
                ML13C1 = self.tmL13C1.GetValue()
                ML14C0 = self.tmL14C0.GetValue()
                ML14C1 = self.tmL14C1.GetValue()
                ML15C0 = self.tmL15C0.GetValue()
                ML15C1 = self.tmL15C1.GetValue()

                ML16C0 = self.tmL16C0.GetValue()
                ML16C1 = self.tmL16C1.GetValue()
                ML17C0 = self.tmL17C0.GetValue()
                ML17C1 = self.tmL17C1.GetValue()
                ML18C0 = self.tmL18C0.GetValue()
                ML18C1 = self.tmL18C1.GetValue()
                #------------------------------
                CL1C0 = format(CL1C0).replace(',','.')
                CL1C1 = format(CL1C1).replace(',','.')
                CL2C0 = format(CL2C0).replace(',','.')
                CL2C1 = format(CL2C1).replace(',','.')
                CL3C0 = format(CL3C0).replace(',','.')
                CL3C1 = format(CL3C1).replace(',','.')

                ML1C0 = format(ML1C0).replace(',','.')
                ML1C1 = format(ML1C1).replace(',','.')
                ML2C0 = format(ML2C0).replace(',','.')
                ML2C1 = format(ML2C1).replace(',','.')
                ML3C0 = format(ML3C0).replace(',','.')
                ML3C1 = format(ML3C1).replace(',','.')

                ML4C0 = format(ML4C0).replace(',','.')
                ML4C1 = format(ML4C1).replace(',','.')
                ML5C0 = format(ML5C0).replace(',','.')
                ML5C1 = format(ML5C1).replace(',','.')
                ML6C0 = format(ML6C0).replace(',','.')
                ML6C1 = format(ML6C1).replace(',','.')

                ML7C0 = format(ML7C0).replace(',','.')
                ML7C1 = format(ML7C1).replace(',','.')
                ML8C0 = format(ML8C0).replace(',','.')
                ML8C1 = format(ML8C1).replace(',','.')
                ML9C0 = format(ML9C0).replace(',','.')
                ML9C1 = format(ML9C1).replace(',','.')

                ML10C0 = format(ML10C0).replace(',','.')
                ML10C1 = format(ML10C1).replace(',','.')
                ML11C0 = format(ML11C0).replace(',','.')
                ML11C1 = format(ML11C1).replace(',','.')
                ML12C0 = format(ML12C0).replace(',','.')
                ML12C1 = format(ML12C1).replace(',','.')

                ML13C0 = format(ML13C0).replace(',','.')
                ML13C1 = format(ML13C1).replace(',','.')
                ML14C0 = format(ML14C0).replace(',','.')
                ML14C1 = format(ML14C1).replace(',','.')
                ML15C0 = format(ML15C0).replace(',','.')
                ML15C1 = format(ML15C1).replace(',','.')

                ML16C0 = format(ML16C0).replace(',','.')
                ML16C1 = format(ML16C1).replace(',','.')
                ML17C0 = format(ML17C0).replace(',','.')
                ML17C1 = format(ML17C1).replace(',','.')
                ML18C0 = format(ML18C0).replace(',','.')
                ML18C1 = format(ML18C1).replace(',','.')

                l = []
                q = []
                try:
                    CL1C0 = abs(float(CL1C0))
                    CL1C1 = abs(float(CL1C1))
                    CL2C0 = abs(float(CL2C0))
                    CL2C1 = abs(float(CL2C1))
                    CL3C0 = abs(float(CL3C0))
                    CL3C1 = abs(float(CL3C1))

                    if CL1C0 <= 0:
                        CL1C0 = 0.001
                    l.append(CL1C0)
                    l.append(CL1C1)
                    l.append((CL1C0+CL1C1)/CL1C0)
                    q.append(l)
                    l = []
                    if CL2C0 <= 0:
                        CL2C0 = 0.001
                    l.append(CL2C0)
                    l.append(CL2C1)
                    l.append((CL2C0+CL2C1)/CL2C0)
                    q.append(l)
                    l = []
                    if CL3C0 <= 0:
                        CL3C0 = 0.001
                    l.append(CL3C0)
                    l.append(CL3C1)
                    l.append((CL3C0+CL3C1)/CL3C0)
                    q.append(l)
                    l = []

                    ML1C0 = abs(float(ML1C0))
                    ML1C1 = abs(float(ML1C1))
                    ML2C0 = abs(float(ML2C0))
                    ML2C1 = abs(float(ML2C1))
                    ML3C0 = abs(float(ML3C0))
                    ML3C1 = abs(float(ML3C1))

                    if ML1C0 <= 0:
                        ML1C0 = 0.001
                    l.append(ML1C0)
                    l.append(ML1C1)
                    l.append((ML1C0+ML1C1)/ML1C0)
                    q.append(l)
                    l = []
                    if ML2C0 <= 0:
                        ML2C0 = 0.001
                    l.append(ML2C0)
                    l.append(ML2C1)
                    l.append((ML2C0+ML2C1)/ML2C0)
                    q.append(l)
                    l = []
                    if ML3C0 <= 0:
                        ML3C0 = 0.001
                    l.append(ML3C0)
                    l.append(ML3C1)
                    l.append((ML3C0+ML3C1)/ML3C0)
                    q.append(l)
                    l = []

                    ML4C0 = abs(float(ML4C0))
                    ML4C1 = abs(float(ML4C1))
                    ML5C0 = abs(float(ML5C0))
                    ML5C1 = abs(float(ML5C1))
                    ML6C0 = abs(float(ML6C0))
                    ML6C1 = abs(float(ML6C1))

                    if ML4C0 <= 0:
                        ML4C0 = 0.001
                    l.append(ML4C0)
                    l.append(ML4C1)
                    l.append((ML4C0+ML4C1)/ML4C0)
                    q.append(l)
                    l = []
                    if ML5C0 <= 0:
                        ML5C0 = 0.001
                    l.append(ML5C0)
                    l.append(ML5C1)
                    l.append((ML5C0+ML5C1)/ML5C0)
                    q.append(l)
                    l = []
                    if ML6C0 <= 0:
                        ML6C0 = 0.001
                    l.append(ML6C0)
                    l.append(ML6C1)
                    l.append((ML6C0+ML6C1)/ML6C0)
                    q.append(l)
                    l = []

                    ML7C0 = abs(float(ML7C0))
                    ML7C1 = abs(float(ML7C1))
                    ML8C0 = abs(float(ML8C0))
                    ML8C1 = abs(float(ML8C1))
                    ML9C0 = abs(float(ML9C0))
                    ML9C1 = abs(float(ML9C1))

                    if ML7C0 <= 0:
                        ML7C0 = 0.001
                    l.append(ML7C0)
                    l.append(ML7C1)
                    l.append((ML7C0+ML7C1)/ML7C0)
                    q.append(l)
                    l = []
                    if ML8C0 <= 0:
                        ML8C0 = 0.001
                    l.append(ML8C0)
                    l.append(ML8C1)
                    l.append((ML8C0+ML8C1)/ML8C0)
                    q.append(l)
                    l = []
                    if ML9C0 <= 0:
                        ML9C0 = 0.001
                    l.append(ML9C0)
                    l.append(ML9C1)
                    l.append((ML9C0+ML9C1)/ML9C0)
                    q.append(l)
                    l = []

                    ML10C0 = abs(float(ML10C0))
                    ML10C1 = abs(float(ML10C1))
                    ML11C0 = abs(float(ML11C0))
                    ML11C1 = abs(float(ML11C1))
                    ML12C0 = abs(float(ML12C0))
                    ML12C1 = abs(float(ML12C1))

                    if ML10C0 <= 0:
                        ML10C0 = 0.001
                    l.append(ML10C0)
                    l.append(ML10C1)
                    l.append((ML10C0+ML10C1)/ML10C0)
                    q.append(l)
                    l = []
                    if ML11C0 <= 0:
                        ML11C0 = 0.001
                    l.append(ML11C0)
                    l.append(ML11C1)
                    l.append((ML11C0+ML11C1)/ML11C0)
                    q.append(l)
                    l = []
                    if ML12C0 <= 0:
                        ML12C0 = 0.001
                    l.append(ML12C0)
                    l.append(ML12C1)
                    l.append((ML12C0+ML12C1)/ML12C0)
                    q.append(l)
                    l = []

                    ML13C0 = abs(float(ML13C0))
                    ML13C1 = abs(float(ML13C1))
                    ML14C0 = abs(float(ML14C0))
                    ML14C1 = abs(float(ML14C1))
                    ML15C0 = abs(float(ML15C0))
                    ML15C1 = abs(float(ML15C1))

                    if ML13C0 <= 0:
                        ML13C0 = 0.001
                    l.append(ML13C0)
                    l.append(ML13C1)
                    l.append((ML13C0+ML13C1)/ML13C0)
                    q.append(l)
                    l = []
                    if ML14C0 <= 0:
                        ML14C0 = 0.001
                    l.append(ML14C0)
                    l.append(ML14C1)
                    l.append((ML14C0+ML14C1)/ML14C0)
                    q.append(l)
                    l = []
                    if ML15C0 <= 0:
                        ML15C0 = 0.001
                    l.append(ML15C0)
                    l.append(ML15C1)
                    l.append((ML15C0+ML15C1)/ML15C0)
                    q.append(l)
                    l = []

                    ML16C0 = abs(float(ML16C0))
                    ML16C1 = abs(float(ML16C1))
                    ML17C0 = abs(float(ML17C0))
                    ML17C1 = abs(float(ML17C1))
                    ML18C0 = abs(float(ML18C0))
                    ML18C1 = abs(float(ML18C1))

                    if ML16C0 <= 0:
                        ML16C0 = 0.001
                    l.append(ML16C0)
                    l.append(ML16C1)
                    l.append((ML16C0+ML16C1)/ML16C0)
                    q.append(l)
                    l = []
                    if ML17C0 <= 0:
                        ML17C0 = 0.001
                    l.append(ML17C0)
                    l.append(ML17C1)
                    l.append((ML17C0+ML17C1)/ML17C0)
                    q.append(l)
                    l = []
                    if ML18C0 <= 0:
                        ML18C0 = 0.001
                    l.append(ML18C0)
                    l.append(ML18C1)
                    l.append((ML18C0+ML18C1)/ML18C0)
                    q.append(l)
                    l = []
                    condicional = 1

                except:
                    print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                    menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    condicional = -1

                if CL1C0 > 0.15 or CL2C0 > 0.15 or CL3C0 > 0.15 or CL1C1 > 0.5 or CL2C1 > 0.5 or CL2C1 > 0.5 or CL2C1 > 0.5 or ML1C0 > 0.15 or ML2C0 > 0.15 or ML3C0 > 0.15 or ML4C0 > 0.15 or ML5C0 > 0.15 or ML6C0 > 0.15 or ML7C0 > 0.15 or  ML8C0 > 0.15 or ML9C0 > 0.15 or ML10C0 > 0.15 or ML11C0 > 0.15 or ML12C0 > 0.15 or ML13C0 > 0.15 or ML14C0 > 0.15 or ML15C0 > 0.15 or ML16C0 > 0.15 or ML17C0 > 0.15 or ML18C0 > 0.15 or ML1C1 > 0.5 or ML2C1 > 0.5 or ML3C1 > 0.5 or ML4C1 > 0.5 or ML5C1 > 0.5 or ML6C1 > 0.5 or ML7C1 > 0.5 or  ML8C1 > 0.5 or ML9C1 > 0.5 or ML10C1 > 0.5 or ML11C1 > 0.5 or ML12C1 > 0.5 or ML13C1 > 0.5 or ML14C1 > 0.5 or ML15C1 > 0.5 or ML16C1 > 0.5 or ML17C1 > 0.5 or ML18C1 > 0.5:
                    '''Diálogo para forçar preenchimento de pressões sigma3 < 0.15 e sigmad <0.5'''
                    dlg = wx.MessageDialog(None, 'Esses limites devem ser respeitados! \nσ3 < 0.150 (MPa) e  σd < 0.500 (MPa)', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

                else:
                    if(condicional>0):
                        bancodedados.update_QD_134(q)
                        self.tL0C0.Disable()
                        self.tL0C1.Disable()
                        self.tL1C0.Disable()
                        self.tL1C1.Disable()
                        self.tL2C0.Disable()
                        self.tL2C1.Disable()

                        self.tmL1C0.Disable()
                        self.tmL1C1.Disable()
                        self.tmL2C0.Disable()
                        self.tmL2C1.Disable()
                        self.tmL3C0.Disable()
                        self.tmL3C1.Disable()

                        self.tmL4C0.Disable()
                        self.tmL4C1.Disable()
                        self.tmL5C0.Disable()
                        self.tmL5C1.Disable()
                        self.tmL6C0.Disable()
                        self.tmL6C1.Disable()

                        self.tmL7C0.Disable()
                        self.tmL7C1.Disable()
                        self.tmL8C0.Disable()
                        self.tmL8C1.Disable()
                        self.tmL9C0.Disable()
                        self.tmL9C1.Disable()

                        self.tmL10C0.Disable()
                        self.tmL10C1.Disable()
                        self.tmL11C0.Disable()
                        self.tmL11C1.Disable()
                        self.tmL12C0.Disable()
                        self.tmL12C1.Disable()

                        self.tmL13C0.Disable()
                        self.tmL13C1.Disable()
                        self.tmL14C0.Disable()
                        self.tmL14C1.Disable()
                        self.tmL15C0.Disable()
                        self.tmL15C1.Disable()

                        self.tmL16C0.Disable()
                        self.tmL16C1.Disable()
                        self.tmL17C0.Disable()
                        self.tmL17C1.Disable()
                        self.tmL18C0.Disable()
                        self.tmL18C1.Disable()

                        self.editar1.Enable()
                        self.Salvar1.Disable()

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

            label = bancodedados.QD_179()
            labels1 = label[0]
            labels = label[1]

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
            self.tL0C0 = wx.TextCtrl(self, -1, "%.3f" % labels1[0][0], style =  wx.TE_CENTER)
            self.tL0C0.Disable()
            h0_sizer.Add(self.tL0C0, 1, wx.ALL | wx.CENTER)
            h0_sizer.AddStretchSpacer(1)
            self.tL0C1 = wx.TextCtrl(self, -1, "%.3f" % labels1[0][1], style =  wx.TE_CENTER)
            self.tL0C1.Disable()
            h0_sizer.Add(self.tL0C1, 1, wx.ALL | wx.CENTER)
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
            self.tmL1C0 = wx.TextCtrl(self, -1, "%.3f" % labels[0][0][0], style =  wx.TE_CENTER)
            self.tmL1C0.Disable()
            h4_sizer.Add(self.tmL1C0, 1, wx.ALL | wx.CENTER)
            h4_sizer.AddStretchSpacer(1)
            self.tmL1C1 = wx.TextCtrl(self, -1, "%.3f" % labels[0][0][1], style =  wx.TE_CENTER)
            self.tmL1C1.Disable()
            h4_sizer.Add(self.tmL1C1, 1, wx.ALL | wx.CENTER)
            h4_sizer.AddStretchSpacer(1)

            h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h5_sizer.AddStretchSpacer(1)
            self.tmL2C0 = wx.TextCtrl(self, -1, "%.3f" % labels[0][1][0], style =  wx.TE_CENTER)
            self.tmL2C0.Disable()
            h5_sizer.Add(self.tmL2C0, 1, wx.ALL | wx.CENTER)
            h5_sizer.AddStretchSpacer(1)
            self.tmL2C1 = wx.TextCtrl(self, -1, "%.3f" % labels[0][1][1], style =  wx.TE_CENTER)
            self.tmL2C1.Disable()
            h5_sizer.Add(self.tmL2C1, 1, wx.ALL | wx.CENTER)
            h5_sizer.AddStretchSpacer(1)

            h6_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h6_sizer.AddStretchSpacer(1)
            self.tmL3C0 = wx.TextCtrl(self, -1, "%.3f" % labels[0][2][0], style =  wx.TE_CENTER)
            self.tmL3C0.Disable()
            h6_sizer.Add(self.tmL3C0, 1, wx.ALL | wx.CENTER)
            h6_sizer.AddStretchSpacer(1)
            self.tmL3C1 = wx.TextCtrl(self, -1, "%.3f" % labels[0][2][1], style =  wx.TE_CENTER)
            self.tmL3C1.Disable()
            h6_sizer.Add(self.tmL3C1, 1, wx.ALL | wx.CENTER)
            h6_sizer.AddStretchSpacer(1)

            #---------------------------------------L4L5L6
            h7_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h7_sizer.AddStretchSpacer(1)
            self.tmL4C0 = wx.TextCtrl(self, -1, "%.3f" % labels[1][0][0], style =  wx.TE_CENTER)
            self.tmL4C0.Disable()
            h7_sizer.Add(self.tmL4C0, 1, wx.ALL | wx.CENTER)
            h7_sizer.AddStretchSpacer(1)
            self.tmL4C1 = wx.TextCtrl(self, -1, "%.3f" % labels[1][0][1], style =  wx.TE_CENTER)
            self.tmL4C1.Disable()
            h7_sizer.Add(self.tmL4C1, 1, wx.ALL | wx.CENTER)
            h7_sizer.AddStretchSpacer(1)

            h8_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h8_sizer.AddStretchSpacer(1)
            self.tmL5C0 = wx.TextCtrl(self, -1, "%.3f" % labels[1][1][0], style =  wx.TE_CENTER)
            self.tmL5C0.Disable()
            h8_sizer.Add(self.tmL5C0, 1, wx.ALL | wx.CENTER)
            h8_sizer.AddStretchSpacer(1)
            self.tmL5C1 = wx.TextCtrl(self, -1, "%.3f" % labels[1][1][1], style =  wx.TE_CENTER)
            self.tmL5C1.Disable()
            h8_sizer.Add(self.tmL5C1, 1, wx.ALL | wx.CENTER)
            h8_sizer.AddStretchSpacer(1)

            h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h9_sizer.AddStretchSpacer(1)
            self.tmL6C0 = wx.TextCtrl(self, -1, "%.3f" % labels[1][2][0], style =  wx.TE_CENTER)
            self.tmL6C0.Disable()
            h9_sizer.Add(self.tmL6C0, 1, wx.ALL | wx.CENTER)
            h9_sizer.AddStretchSpacer(1)
            self.tmL6C1 = wx.TextCtrl(self, -1, "%.3f" % labels[1][2][1], style =  wx.TE_CENTER)
            self.tmL6C1.Disable()
            h9_sizer.Add(self.tmL6C1, 1, wx.ALL | wx.CENTER)
            h9_sizer.AddStretchSpacer(1)

            #---------------------------------------L7L8L9
            h10_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h10_sizer.AddStretchSpacer(1)
            self.tmL7C0 = wx.TextCtrl(self, -1, "%.3f" % labels[2][0][0], style =  wx.TE_CENTER)
            self.tmL7C0.Disable()
            h10_sizer.Add(self.tmL7C0, 1, wx.ALL | wx.CENTER)
            h10_sizer.AddStretchSpacer(1)
            self.tmL7C1 = wx.TextCtrl(self, -1, "%.3f" % labels[2][0][1], style =  wx.TE_CENTER)
            self.tmL7C1.Disable()
            h10_sizer.Add(self.tmL7C1, 1, wx.ALL | wx.CENTER)
            h10_sizer.AddStretchSpacer(1)

            h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h11_sizer.AddStretchSpacer(1)
            self.tmL8C0 = wx.TextCtrl(self, -1, "%.3f" % labels[2][1][0], style =  wx.TE_CENTER)
            self.tmL8C0.Disable()
            h11_sizer.Add(self.tmL8C0, 1, wx.ALL | wx.CENTER)
            h11_sizer.AddStretchSpacer(1)
            self.tmL8C1 = wx.TextCtrl(self, -1, "%.3f" % labels[2][1][1], style =  wx.TE_CENTER)
            self.tmL8C1.Disable()
            h11_sizer.Add(self.tmL8C1, 1, wx.ALL | wx.CENTER)
            h11_sizer.AddStretchSpacer(1)

            h12_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h12_sizer.AddStretchSpacer(1)
            self.tmL9C0 = wx.TextCtrl(self, -1, "%.3f" % labels[2][2][0], style =  wx.TE_CENTER)
            self.tmL9C0.Disable()
            h12_sizer.Add(self.tmL9C0, 1, wx.ALL | wx.CENTER)
            h12_sizer.AddStretchSpacer(1)
            self.tmL9C1 = wx.TextCtrl(self, -1, "%.3f" % labels[2][2][1], style =  wx.TE_CENTER)
            self.tmL9C1.Disable()
            h12_sizer.Add(self.tmL9C1, 1, wx.ALL | wx.CENTER)
            h12_sizer.AddStretchSpacer(1)

            #---------------------------------------
            self.editar1 = wx.Button(self, -1, 'Editar', style = wx.CENTER)
            self.Salvar1 = wx.Button(self, -1, 'Salvar', style = wx.CENTER)
            self.Salvar1.Disable()
            self.Bind(wx.EVT_BUTTON, self.Editar1, self.editar1)
            self.Bind(wx.EVT_BUTTON, self.Salva1, self.Salvar1)
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
        #--------------------------------------------------
        def Editar1(self, event):
            '''Edita...'''
            self.tL0C0.Enable()
            self.tL0C1.Enable()

            self.tmL1C0.Enable()
            self.tmL1C1.Enable()
            self.tmL2C0.Enable()
            self.tmL2C1.Enable()
            self.tmL3C0.Enable()
            self.tmL3C1.Enable()

            self.tmL4C0.Enable()
            self.tmL4C1.Enable()
            self.tmL5C0.Enable()
            self.tmL5C1.Enable()
            self.tmL6C0.Enable()
            self.tmL6C1.Enable()

            self.tmL7C0.Enable()
            self.tmL7C1.Enable()
            self.tmL8C0.Enable()
            self.tmL8C1.Enable()
            self.tmL9C0.Enable()
            self.tmL9C1.Enable()

            self.editar1.Disable()
            self.Salvar1.Enable()
            self.Update()
            self.Refresh()
        #--------------------------------------------------
        def Salva1(self, event):
            '''Salva...'''
            CL1C0 = self.tL0C0.GetValue()
            CL1C1 = self.tL0C1.GetValue()

            DPL1C0 = self.tmL1C0.GetValue()
            DPL1C1 = self.tmL1C1.GetValue()
            DPL2C0 = self.tmL2C0.GetValue()
            DPL2C1 = self.tmL2C1.GetValue()
            DPL3C0 = self.tmL3C0.GetValue()
            DPL3C1 = self.tmL3C1.GetValue()

            DPL4C0 = self.tmL4C0.GetValue()
            DPL4C1 = self.tmL4C1.GetValue()
            DPL5C0 = self.tmL5C0.GetValue()
            DPL5C1 = self.tmL5C1.GetValue()
            DPL6C0 = self.tmL6C0.GetValue()
            DPL6C1 = self.tmL6C1.GetValue()

            DPL7C0 = self.tmL7C0.GetValue()
            DPL7C1 = self.tmL7C1.GetValue()
            DPL8C0 = self.tmL8C0.GetValue()
            DPL8C1 = self.tmL8C1.GetValue()
            DPL9C0 = self.tmL9C0.GetValue()
            DPL9C1 = self.tmL9C1.GetValue()
            #------------------------------
            CL1C0 = format(CL1C0).replace(',','.')
            CL1C1 = format(CL1C1).replace(',','.')

            DPL1C0 = format(DPL1C0).replace(',','.')
            DPL1C1 = format(DPL1C1).replace(',','.')
            DPL2C0 = format(DPL2C0).replace(',','.')
            DPL2C1 = format(DPL2C1).replace(',','.')
            DPL3C0 = format(DPL3C0).replace(',','.')
            DPL3C1 = format(DPL3C1).replace(',','.')

            DPL4C0 = format(DPL4C0).replace(',','.')
            DPL4C1 = format(DPL4C1).replace(',','.')
            DPL5C0 = format(DPL5C0).replace(',','.')
            DPL5C1 = format(DPL5C1).replace(',','.')
            DPL6C0 = format(DPL6C0).replace(',','.')
            DPL6C1 = format(DPL6C1).replace(',','.')

            DPL7C0 = format(DPL7C0).replace(',','.')
            DPL7C1 = format(DPL7C1).replace(',','.')
            DPL8C0 = format(DPL8C0).replace(',','.')
            DPL8C1 = format(DPL8C1).replace(',','.')
            DPL9C0 = format(DPL9C0).replace(',','.')
            DPL9C1 = format(DPL9C1).replace(',','.')

            l = []
            q = []
            try:
                CL1C0 = abs(float(CL1C0))
                CL1C1 = abs(float(CL1C1))

                if CL1C0 <= 0:
                    CL1C0 = 0.001
                l.append(CL1C0)
                l.append(CL1C1)
                l.append((CL1C0+CL1C1)/CL1C0)
                q.append(l)
                l = []

                DPL1C0 = abs(float(DPL1C0))
                DPL1C1 = abs(float(DPL1C1))
                DPL2C0 = abs(float(DPL2C0))
                DPL2C1 = abs(float(DPL2C1))
                DPL3C0 = abs(float(DPL3C0))
                DPL3C1 = abs(float(DPL3C1))

                if DPL1C0 <= 0:
                    DPL1C0 = 0.001
                l.append(DPL1C0)
                l.append(DPL1C1)
                l.append((DPL1C0+DPL1C1)/DPL1C0)
                q.append(l)
                l = []
                if DPL2C0 <= 0:
                    DPL2C0 = 0.001
                l.append(DPL2C0)
                l.append(DPL2C1)
                l.append((DPL2C0+DPL2C1)/DPL2C0)
                q.append(l)
                l = []
                if DPL3C0 <= 0:
                    DPL3C0 = 0.001
                l.append(DPL3C0)
                l.append(DPL3C1)
                l.append((DPL3C0+DPL3C1)/DPL3C0)
                q.append(l)
                l = []

                DPL4C0 = abs(float(DPL4C0))
                DPL4C1 = abs(float(DPL4C1))
                DPL5C0 = abs(float(DPL5C0))
                DPL5C1 = abs(float(DPL5C1))
                DPL6C0 = abs(float(DPL6C0))
                DPL6C1 = abs(float(DPL6C1))

                if DPL4C0 <= 0:
                    DPL4C0 = 0.001
                l.append(DPL4C0)
                l.append(DPL4C1)
                l.append((DPL4C0+DPL4C1)/DPL4C0)
                q.append(l)
                l = []
                if DPL5C0 <= 0:
                    DPL5C0 = 0.001
                l.append(DPL5C0)
                l.append(DPL5C1)
                l.append((DPL5C0+DPL5C1)/DPL5C0)
                q.append(l)
                l = []
                if DPL6C0 <= 0:
                    DPL6C0 = 0.001
                l.append(DPL6C0)
                l.append(DPL6C1)
                l.append((DPL6C0+DPL6C1)/DPL6C0)
                q.append(l)
                l = []

                DPL7C0 = abs(float(DPL7C0))
                DPL7C1 = abs(float(DPL7C1))
                DPL8C0 = abs(float(DPL8C0))
                DPL8C1 = abs(float(DPL8C1))
                DPL9C0 = abs(float(DPL9C0))
                DPL9C1 = abs(float(DPL9C1))

                if DPL7C0 <= 0:
                    DPL7C0 = 0.001
                l.append(DPL7C0)
                l.append(DPL7C1)
                l.append((DPL7C0+DPL7C1)/DPL7C0)
                q.append(l)
                l = []
                if DPL8C0 <= 0:
                    DPL8C0 = 0.001
                l.append(DPL8C0)
                l.append(DPL8C1)
                l.append((DPL8C0+DPL8C1)/DPL8C0)
                q.append(l)
                l = []
                if DPL9C0 <= 0:
                    DPL9C0 = 0.001
                l.append(DPL9C0)
                l.append(DPL9C1)
                l.append((DPL9C0+DPL9C1)/DPL9C0)
                q.append(l)
                l = []
                condicional = 1
            except:
                print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                condicional = -1

            if CL1C0 > 0.15 or CL1C1 > 0.5 or DPL1C0 > 0.15 or DPL2C0 > 0.15 or DPL3C0 > 0.15 or DPL4C0 > 0.15 or DPL5C0 > 0.15 or DPL6C0 > 0.15 or DPL7C0 > 0.15 or DPL8C0 > 0.15 or DPL9C0 > 0.15 or DPL1C1 > 0.5 or DPL2C1 > 0.5 or DPL3C1 > 0.5 or DPL4C1 > 0.5 or DPL5C1 > 0.5 or DPL6C1 > 0.5 or DPL7C1 > 0.5 or DPL8C1 > 0.5 or DPL9C1 > 0.5:
                '''Diálogo para forçar preenchimento de pressões sigma3 < 0.15 e sigmad <0.5'''
                dlg = wx.MessageDialog(None, 'Esses limites devem ser respeitados! \nσ3 < 0.150 (MPa) e  σd < 0.500 (MPa)', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
            else:
                if(condicional>0):
                    bancodedados.update_QD_179(q)
                    self.tL0C0.Disable()
                    self.tL0C1.Disable()

                    self.tmL1C0.Disable()
                    self.tmL1C1.Disable()
                    self.tmL2C0.Disable()
                    self.tmL2C1.Disable()
                    self.tmL3C0.Disable()
                    self.tmL3C1.Disable()

                    self.tmL4C0.Disable()
                    self.tmL4C1.Disable()
                    self.tmL5C0.Disable()
                    self.tmL5C1.Disable()
                    self.tmL6C0.Disable()
                    self.tmL6C1.Disable()

                    self.tmL7C0.Disable()
                    self.tmL7C1.Disable()
                    self.tmL8C0.Disable()
                    self.tmL8C1.Disable()
                    self.tmL9C0.Disable()
                    self.tmL9C1.Disable()

                    self.editar1.Enable()
                    self.Salvar1.Disable()
                    self.Update()
                    self.Refresh()


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

            labels1 = bancodedados.QD_181()

            TextoTitle = wx.StaticText(self, label = "QUADRO DE TENSÕES - M. R.", style = wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            TextoTitle.SetFont(FontTitle)
            TextoTitle.SetForegroundColour((0,51,188))

            #---------------------------------------
            text1= wx.StaticText(self, label = "σ1 (MPa)", style = wx.ALL | wx.CENTER)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h_sizer.Add(text1, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h0_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.tL0C0 = wx.TextCtrl(self, -1, "%.3f" % labels1[0][0], style =  wx.TE_CENTER)
            self.tL0C0.Disable()
            h0_sizer.Add(self.tL0C0, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.tL1C0 = wx.TextCtrl(self, -1, "%.3f" % labels1[1][0], style =  wx.TE_CENTER)
            self.tL1C0.Disable()
            h1_sizer.Add(self.tL1C0, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.tL2C0 = wx.TextCtrl(self, -1, "%.3f" % labels1[2][0], style =  wx.TE_CENTER)
            self.tL2C0.Disable()
            h2_sizer.Add(self.tL2C0, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.tL3C0 = wx.TextCtrl(self, -1, "%.3f" % labels1[3][0], style =  wx.TE_CENTER)
            self.tL3C0.Disable()
            h3_sizer.Add(self.tL3C0, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            h4_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.tL4C0 = wx.TextCtrl(self, -1, "%.3f" % labels1[4][0], style =  wx.TE_CENTER)
            self.tL4C0.Disable()
            h4_sizer.Add(self.tL4C0, 1, wx.ALL | wx.CENTER)

            #---------------------------------------
            self.editar1 = wx.Button(self, -1, 'Editar', style = wx.CENTER)
            self.Salvar1 = wx.Button(self, -1, 'Salvar', style = wx.CENTER)
            self.Salvar1.Disable()
            self.Bind(wx.EVT_BUTTON, self.Editar1, self.editar1)
            self.Bind(wx.EVT_BUTTON, self.Salva1, self.Salvar1)

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

        #--------------------------------------------------
        def Editar1(self, event):
            '''Edita...'''
            self.tL0C0.Enable()
            self.tL1C0.Enable()
            self.tL2C0.Enable()
            self.tL3C0.Enable()
            self.tL4C0.Enable()
            self.editar1.Disable()
            self.Salvar1.Enable()
            self.Update()
            self.Refresh()

        #--------------------------------------------------
        def Salva1(self, event):
            '''Salva...'''
            MRL1 = self.tL0C0.GetValue()
            MRL2 = self.tL1C0.GetValue()
            MRL3 = self.tL2C0.GetValue()
            MRL4 = self.tL3C0.GetValue()
            MRL5 = self.tL4C0.GetValue()
            #------------------------------
            MRL1 = format(MRL1).replace(',','.')
            MRL2 = format(MRL2).replace(',','.')
            MRL3 = format(MRL3).replace(',','.')
            MRL4 = format(MRL4).replace(',','.')
            MRL5 = format(MRL5).replace(',','.')
            q = []
            try:
                MRL1 = abs(float(MRL1))
                MRL2 = abs(float(MRL2))
                MRL3 = abs(float(MRL3))
                MRL4 = abs(float(MRL4))
                MRL5 = abs(float(MRL5))
                if MRL1 <= 0:
                    MRL1 = 0.001
                if MRL2 <= 0:
                    MRL2 = 0.001
                if MRL3 <= 0:
                    MRL3 = 0.001
                if MRL4 <= 0:
                    MRL4 = 0.001
                if MRL5 <= 0:
                    MRL5 = 0.001
                condicional = 1
                q.append(MRL1)
                q.append(MRL2)
                q.append(MRL3)
                q.append(MRL4)
                q.append(MRL5)

            except:
                print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                condicional = -1

            if MRL1 > 0.5 or MRL2 > 0.5 or MRL3 > 0.5 or MRL4 > 0.5 or MRL5 > 0.5:
                '''Diálogo para forçar preenchimento de pressões sigma1 < 0.5'''
                dlg = wx.MessageDialog(None, 'Esse limite deve ser respeitado! \nσ1 < 0.500 (MPa)', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
            else:
                if(condicional>0):
                    bancodedados.update_QD_181(q)
                    self.tL0C0.Disable()
                    self.tL1C0.Disable()
                    self.tL2C0.Disable()
                    self.tL3C0.Disable()
                    self.tL4C0.Disable()
                    self.editar1.Enable()
                    self.Salvar1.Disable()
                    self.Update()
                    self.Refresh()
