# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import time
import threading
import matplotlib
import numpy as np
import bancodedados
import back.connection as con
import matplotlib.pyplot as plt
import back.MyProgressDialog as My
import back.SaveThread as SaveThread
import back.MotorThread as MotorThread
import back.CamaraThread as CamaraThread
import back.ConexaoThread as ConexaoThread
from drawnow import *
from front.quadrotensoes import quadro
from front.dialogoDinamico import dialogoDinamico
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

'''plt.style.use('ggplot')'''
frequencias = ['1', '2', '3', '4']

'''Variáveis Globais'''


########################################################################
'''Painel Superior'''
class TopPanel(wx.Panel):
        def __init__(self, parent, _self):
            wx.Panel.__init__(self, parent = parent)

            self._self = _self

            FontTitle = wx.Font(-1, wx.SWISS, wx.NORMAL, wx.BOLD)

            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.v_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.figure = plt.figure(constrained_layout=True)
            #plt.subplot()
            #plt.ion()
            self.axes = self.figure.add_subplot(111)
            self.canvas = FigureCanvas(self, -1, self.figure)
            #self.axes.set_xlabel("TEMPO (seg)")
            #self.axes.set_ylabel("DESLOCAMENTO (mm)")
            #self.axes.set_ylim(float(0), float(5))
            #self.axes.set_xlim(float(0), float(5))

            rect = self.figure.patch
            rect.set_facecolor('#D7D7D7')

            #rect1 = self.axes.patch
            #rect1.set_facecolor('#A0BA8C')

            self.avanca = wx.Button(self, -1, 'AVANÇA')
            self.pausa = wx.Button(self, -1, 'PAUSA')
            self.continua = wx.Button(self, -1, 'CONTINUA')
            self.fim_inicio = wx.Button(self, -1, 'INICIO')

            #self.Bind(wx.EVT_BUTTON, self.AVANCA, self.avanca)
            #self.Bind(wx.EVT_BUTTON, self.PAUSA, self.pausa)
            #self.Bind(wx.EVT_BUTTON, self.CONTINUA, self.continua)
            #self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)

            self.avanca.Disable()
            self.pausa.Disable()
            self.continua.Disable()
            self.fim_inicio.Disable()

            self.avanca.SetFont(FontTitle)
            self.pausa.SetFont(FontTitle)
            self.continua.SetFont(FontTitle)
            self.fim_inicio.SetFont(FontTitle)

            self.v_sizer.Add(self.avanca, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.pausa, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.continua, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.fim_inicio, 1, wx.EXPAND | wx.ALL, 5)


            self.h_sizer.Add(self.canvas, 12, wx.EXPAND | wx.ALL, 5)
            self.h_sizer.Add(self.v_sizer, 1, wx.EXPAND | wx.ALL)
            self.h_sizer.AddStretchSpacer(4)

            self.sizer.Add(self.h_sizer, 0, wx.EXPAND | wx.ALL, 10)
            self.SetSizer(self.sizer)
            self.CAMARA_ANTERIOR = 0
            self.AVANCA = False

    #--------------------------------------------------
        def draww(self):
            self.axes.clear()
            self.axes.set_xlim(float(0), float(1))
            self.axes.set_ylim(float(0), float(0.01))
            self.axes.set_xlabel("TEMPO (seg)")
            self.axes.set_ylabel("DESLOCAMENTO (mm)")
            self.canvas.draw()

'''Painel Inferior'''
class BottomPanel(wx.Panel):
        def __init__(self, parent, top):
            wx.Panel.__init__(self, parent = parent)

            self.graph = top

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontTitle1 = wx.Font(-1, wx.SWISS, wx.NORMAL, wx.BOLD)
            Fonttext = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

            staticbox1 = wx.StaticBox(self, -1, '')
            staticbox2 = wx.StaticBox(self, -1, '')
            staticbox3 = wx.StaticBox(self, -1, '')
            staticbox4 = wx.StaticBox(self, -1, '')
            staticbox5 = wx.StaticBox(self, -1, '')
            staticbox6 = wx.StaticBox(self, -1, '')

            staticboxSizer1 = wx.StaticBoxSizer(staticbox1, wx.VERTICAL)
            staticboxSizer2 = wx.StaticBoxSizer(staticbox2, wx.VERTICAL)
            staticboxSizer3 = wx.StaticBoxSizer(staticbox3, wx.VERTICAL)
            staticboxSizer4 = wx.StaticBoxSizer(staticbox4, wx.VERTICAL)
            staticboxSizer5 = wx.StaticBoxSizer(staticbox5, wx.VERTICAL)
            staticboxSizer6 = wx.StaticBoxSizer(staticbox6, wx.VERTICAL)

            staticbox1.SetBackgroundColour(wx.Colour(215,215,215))
            staticbox2.SetBackgroundColour(wx.Colour(215,215,215))
            staticbox3.SetBackgroundColour(wx.Colour(215,215,215))
            staticbox4.SetBackgroundColour(wx.Colour(215,215,215))
            staticbox5.SetBackgroundColour(wx.Colour(215,215,215))
            staticbox6.SetBackgroundColour(wx.Colour(215,215,215))

            self.qTensoes = wx.Button(self, -1, 'Q. Tensões')
            self.condic = wx.Button(self, -1, 'CONDIC.')
            self.mr = wx.Button(self, -1, 'M. R.')
            self.LTeste = wx.Button(self, -1, "L. TESTE", size = wx.DefaultSize)
            self.LZero = wx.Button(self, -1, "L. ZERO", size = wx.DefaultSize)

            #self.Bind(wx.EVT_BUTTON, self.QT, self.qTensoes)
            #self.Bind(wx.EVT_BUTTON, self.CONDIC, self.condic)
            #self.Bind(wx.EVT_BUTTON, self.MR, self.mr)
            #self.Bind(wx.EVT_BUTTON, self.LTESTE, self.LTeste)
            #self.Bind(wx.EVT_BUTTON, self.LZERO, self.LZero)

            self.qTensoes.Disable()
            self.condic.Disable()
            self.mr.Disable()
            self.LZero.Disable()

            self.qTensoes.SetFont(FontTitle1)
            self.condic.SetFont(FontTitle1)
            self.mr.SetFont(FontTitle1)
            self.LTeste.SetFont(FontTitle1)
            self.LZero.SetFont(FontTitle1)

            texto1 = wx.StaticText(self, label = "EIXO Y", style = wx.ALIGN_CENTRE)
            texto2 = wx.StaticText(self, label = "EIXO Y (mm)", style = wx.ALIGN_CENTRE)
            texto3 = wx.StaticText(self, label = "σ3 - Tensão confinante (MPa)", style = wx.ALIGN_CENTRE)
            texto4 = wx.StaticText(self, label = "σd - Tensão desvio (MPa)", style = wx.ALIGN_CENTRE)
            texto5 = wx.StaticText(self, label = "Y1 (V)", style = wx.ALIGN_CENTER)
            texto6 = wx.StaticText(self, label = "Y2 (V)", style = wx.ALIGN_CENTER)
            texto7 = wx.StaticText(self, label = "Y1 (mm)", style = wx.ALIGN_CENTER)
            texto8 = wx.StaticText(self, label = "Y2 (mm)", style = wx.ALIGN_CENTER)
            texto9 = wx.StaticText(self, label = "Def. Elástica", style = wx.ALIGN_CENTER)
            texto10 = wx.StaticText(self, label = "Def. Plástica", style = wx.ALIGN_CENTER)
            texto11 = wx.StaticText(self, label = "Def. P. Cond.", style = wx.ALIGN_CENTER)
            texto12 = wx.StaticText(self, label = "Def. P. Acum.", style = wx.ALIGN_CENTER)
            texto13 = wx.StaticText(self, label = "Altura Final", style = wx.ALIGN_CENTER)
            texto14 = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
            texto15 = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
            texto16 = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
            texto17 = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
            texto18 = wx.StaticText(self, label = "Altura (mm)", style = wx.ALIGN_LEFT)
            texto19 = wx.StaticText(self, label = "Diâmetro (mm)", style = wx.ALIGN_LEFT)
            texto20 = wx.StaticText(self, label = "Def. Crítica (mm)", style = wx.ALIGN_LEFT)
            texto21 = wx.StaticText(self, label = "CICLO", style = wx.ALIGN_CENTER)
            texto22 = wx.StaticText(self, label = "Nº de Golpes", style = wx.ALIGN_CENTER)
            texto23 = wx.StaticText(self, label = "Freq. (Hz)", style = wx.ALIGN_CENTER)
            texto24 = wx.StaticText(self, label = "Golpe Atual", style = wx.ALIGN_CENTER)

            texto1.SetFont(FontTitle)
            texto2.SetFont(FontTitle)
            texto3.SetFont(FontTitle)
            texto4.SetFont(FontTitle)
            texto5.SetFont(Fonttext)
            texto6.SetFont(Fonttext)
            texto7.SetFont(Fonttext)
            texto8.SetFont(Fonttext)
            texto9.SetFont(Fonttext)
            texto10.SetFont(Fonttext)
            texto11.SetFont(Fonttext)
            texto12.SetFont(Fonttext)
            texto13.SetFont(FontTitle)
            texto14.SetFont(Fonttext)
            texto15.SetFont(Fonttext)
            texto16.SetFont(Fonttext)
            texto17.SetFont(Fonttext)
            texto18.SetFont(Fonttext)
            texto19.SetFont(Fonttext)
            texto20.SetFont(FontTitle)
            texto21.SetFont(FontTitle)
            texto22.SetFont(Fonttext)
            texto23.SetFont(Fonttext)
            texto24.SetFont(Fonttext)

            texto1.SetBackgroundColour(wx.Colour(215,215,215))
            texto2.SetBackgroundColour(wx.Colour(215,215,215))
            texto3.SetBackgroundColour(wx.Colour(215,215,215))
            texto4.SetBackgroundColour(wx.Colour(215,215,215))
            texto5.SetBackgroundColour(wx.Colour(215,215,215))
            texto6.SetBackgroundColour(wx.Colour(215,215,215))
            texto7.SetBackgroundColour(wx.Colour(215,215,215))
            texto8.SetBackgroundColour(wx.Colour(215,215,215))
            texto9.SetBackgroundColour(wx.Colour(215,215,215))
            texto10.SetBackgroundColour(wx.Colour(215,215,215))
            texto11.SetBackgroundColour(wx.Colour(215,215,215))
            texto12.SetBackgroundColour(wx.Colour(215,215,215))
            texto13.SetBackgroundColour(wx.Colour(215,215,215))
            texto14.SetBackgroundColour(wx.Colour(215,215,215))
            texto15.SetBackgroundColour(wx.Colour(215,215,215))
            texto16.SetBackgroundColour(wx.Colour(215,215,215))
            texto17.SetBackgroundColour(wx.Colour(215,215,215))
            texto18.SetBackgroundColour(wx.Colour(215,215,215))
            texto19.SetBackgroundColour(wx.Colour(215,215,215))
            texto20.SetBackgroundColour(wx.Colour(215,215,215))
            texto21.SetBackgroundColour(wx.Colour(215,215,215))
            texto22.SetBackgroundColour(wx.Colour(215,215,215))
            texto23.SetBackgroundColour(wx.Colour(215,215,215))
            texto24.SetBackgroundColour(wx.Colour(215,215,215))

            self.y1V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y2V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y1mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y2mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.defElastica = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.defPlastica = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.defPCond = wx.TextCtrl(self, -1, '', size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.defPAcum = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.AlturaFinal = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.PCreal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.PCalvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.SigmaReal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.SigmaAlvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.AlturaMM = wx.TextCtrl(self, -1, '200,00', size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.DiametroMM = wx.TextCtrl(self, -1, '100,0', size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.DefCritica = wx.TextCtrl(self, -1, wx.EmptyString, size = (80, 41.5), style = wx.TE_READONLY | wx.TE_CENTER)
            self.Ciclo = wx.TextCtrl(self, -1, '1', size = (50, -1), style = wx.TE_READONLY | wx.TE_CENTER)
            self.NGolpes = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, -1), style = wx.TE_READONLY | wx.TE_CENTER)
            self.GolpeAtual = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, -1), style = wx.TE_READONLY | wx.TE_CENTRE)
            self.freq = wx.ComboBox(self, -1, frequencias[0], choices = frequencias, style = wx.CB_READONLY)
            self.ensaioAuto = wx.CheckBox(self, -1, 'Ensaio automático', (20,0), (260,-1), style = wx.ALIGN_LEFT)

            self.y1V.Disable()
            self.y2V.Disable()
            self.y1mm.Disable()
            self.y2mm.Disable()
            self.defElastica.Disable()
            self.defPlastica.Disable()
            self.defPCond.Disable()
            self.defPAcum.Disable()
            self.AlturaFinal.Disable()
            self.PCreal.Disable()
            self.PCalvo.Disable()
            self.SigmaReal.Disable()
            self.SigmaAlvo.Disable()
            self.AlturaMM.Disable()
            self.DiametroMM.Disable()
            self.DefCritica.Disable()
            self.Ciclo.Disable()
            self.NGolpes.Disable()
            self.GolpeAtual.Disable()
            self.freq.Disable()

            self.y1V.SetFont(Fonttext)
            self.y2V.SetFont(Fonttext)
            self.y1mm.SetFont(Fonttext)
            self.y2mm.SetFont(Fonttext)
            self.defElastica.SetFont(Fonttext)
            self.defPlastica.SetFont(Fonttext)
            self.defPCond.SetFont(Fonttext)
            self.defPAcum.SetFont(Fonttext)
            self.AlturaFinal.SetFont(Fonttext)
            self.PCreal.SetFont(Fonttext)
            self.PCalvo.SetFont(Fonttext)
            self.SigmaReal.SetFont(Fonttext)
            self.SigmaAlvo.SetFont(Fonttext)
            self.AlturaMM.SetFont(Fonttext)
            self.DiametroMM.SetFont(Fonttext)
            self.DefCritica.SetFont(Fonttext)
            self.Ciclo.SetFont(Fonttext)
            self.NGolpes.SetFont(Fonttext)
            self.GolpeAtual.SetFont(Fonttext)
            self.freq.SetFont(Fonttext)

            self.y1V.SetForegroundColour((119,118,114))
            self.y2V.SetForegroundColour((119,118,114))
            self.y1mm.SetForegroundColour((119,118,114))
            self.y2mm.SetForegroundColour((119,118,114))
            self.defElastica.SetForegroundColour((119,118,114))
            self.defPlastica.SetForegroundColour((119,118,114))
            self.defPCond.SetForegroundColour((119,118,114))
            self.defPAcum.SetForegroundColour((119,118,114))
            self.AlturaFinal.SetForegroundColour((119,118,114))
            self.PCreal.SetForegroundColour((119,118,114))
            self.PCalvo.SetForegroundColour((119,118,114))
            self.SigmaReal.SetForegroundColour((119,118,114))
            self.SigmaAlvo.SetForegroundColour((119,118,114))
            self.AlturaMM.SetForegroundColour((119,118,114))
            self.DiametroMM.SetForegroundColour((119,118,114))
            self.DefCritica.SetForegroundColour((119,118,114))
            self.Ciclo.SetForegroundColour((119,118,114))
            self.NGolpes.SetForegroundColour((119,118,114))
            self.GolpeAtual.SetForegroundColour((119,118,114))

            #--------------------------------------------------
            '''Static Box 1'''
            self.v16_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v17_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v18_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v19_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v20_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v21_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h19_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h20_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h21_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h22_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.v16_sizer.Add(texto8, 1, wx.CENTER)
            self.v16_sizer.Add(self.y2mm, 2, wx.CENTER)

            self.v17_sizer.Add(texto6, 1, wx.CENTER)
            self.v17_sizer.Add(self.y2V, 2, wx.CENTER)

            self.v18_sizer.Add(texto7, 1, wx.CENTER)
            self.v18_sizer.Add(self.y1mm, 2, wx.CENTER)

            self.v19_sizer.Add(texto5, 1, wx.CENTER)
            self.v19_sizer.Add(self.y1V, 2, wx.CENTER)

            self.h19_sizer.Add(self.v17_sizer, 5, wx.ALL | wx.CENTER)
            self.h19_sizer.AddStretchSpacer(1)
            self.h19_sizer.Add(self.v16_sizer, 5, wx.ALL | wx.CENTER)

            self.h20_sizer.Add(self.v19_sizer, 5, wx.ALL | wx.CENTER)
            self.h20_sizer.AddStretchSpacer(1)
            self.h20_sizer.Add(self.v18_sizer, 5, wx.ALL | wx.CENTER)

            self.h21_sizer.Add(self.LTeste, 5, wx.EXPAND)
            self.h21_sizer.AddStretchSpacer(2)
            self.h21_sizer.Add(self.LZero, 5, wx.EXPAND)

            self.v20_sizer.Add(self.h20_sizer, 3, wx.CENTER)
            self.v20_sizer.AddStretchSpacer(1)
            self.v20_sizer.Add(self.h19_sizer, 3, wx.CENTER)
            self.v20_sizer.AddStretchSpacer(2)
            self.v20_sizer.Add(self.h21_sizer, 2, wx.CENTER)

            self.v21_sizer.Add(texto1, 1, wx.CENTER)
            self.v21_sizer.Add(self.v20_sizer, 7, wx.CENTER)

            self.h22_sizer.Add(self.v21_sizer, 1, wx.CENTER)
            staticboxSizer1.Add(self.h22_sizer, 0,  wx.ALL | wx.EXPAND  | wx.CENTER, 10)

            #--------------------------------------------------
            '''Static Box 2'''
            self.v15_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h13_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h14_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h15_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h16_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h17_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h18_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.h13_sizer.Add(texto13, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h13_sizer.AddStretchSpacer(1)
            self.h13_sizer.Add(self.AlturaFinal, 5, wx.CENTER)

            self.h14_sizer.Add(texto12, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h14_sizer.AddStretchSpacer(1)
            self.h14_sizer.Add(self.defPAcum, 5, wx.CENTER)

            self.h15_sizer.Add(texto11, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h15_sizer.AddStretchSpacer(1)
            self.h15_sizer.Add(self.defPCond, 5, wx.CENTER)

            self.h16_sizer.Add(texto10, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h16_sizer.AddStretchSpacer(1)
            self.h16_sizer.Add(self.defPlastica, 5, wx.CENTER)

            self.h17_sizer.Add(texto9, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h17_sizer.AddStretchSpacer(1)
            self.h17_sizer.Add(self.defElastica, 5, wx.CENTER)

            self.v15_sizer.Add(texto2, 3, wx.ALL | wx.EXPAND  | wx.CENTER)
            self.v15_sizer.Add(self.h17_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            self.v15_sizer.AddStretchSpacer(1)
            self.v15_sizer.Add(self.h16_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            self.v15_sizer.AddStretchSpacer(1)
            self.v15_sizer.Add(self.h15_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            self.v15_sizer.AddStretchSpacer(1)
            self.v15_sizer.Add(self.h14_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            self.v15_sizer.AddStretchSpacer(1)
            self.v15_sizer.Add(self.h13_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)

            self.h18_sizer.Add(self.v15_sizer, 1, wx.CENTER)
            staticboxSizer2.Add(self.h18_sizer, 0, wx.ALL | wx.EXPAND  | wx.CENTER, 10)

            #--------------------------------------------------
            '''Static Box 3'''
            self.v12_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v13_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v14_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h12_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.v12_sizer.Add(texto16, 1, wx.ALL | wx.CENTER)
            self.v12_sizer.Add(self.PCalvo, 2, wx.ALL | wx.CENTER)

            self.v13_sizer.Add(texto14, 1, wx.ALL | wx.CENTER)
            self.v13_sizer.Add(self.PCreal, 2, wx.ALL | wx.CENTER)

            self.h11_sizer.Add(self.v13_sizer, 6, wx.CENTER)
            self.h11_sizer.AddStretchSpacer(1)
            self.h11_sizer.Add(self.v12_sizer, 6, wx.CENTER)

            self.v14_sizer.Add(texto3, 1, wx.ALL | wx.CENTER)
            self.v14_sizer.Add(self.h11_sizer, 3, wx.ALL | wx.CENTER)

            self.h12_sizer.Add(self.v14_sizer, 1, wx.CENTER)
            staticboxSizer3.Add(self.h12_sizer, 0, wx.ALL | wx.CENTER, 10)

            #--------------------------------------------------
            '''Static Box 4'''
            self.v11_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h7_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h8_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h10_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.h7_sizer.Add(texto18, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h7_sizer.AddStretchSpacer(1)
            self.h7_sizer.Add(self.AlturaMM, 5, wx.CENTER)

            self.h8_sizer.Add(texto19, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h8_sizer.AddStretchSpacer(1)
            self.h8_sizer.Add(self.DiametroMM, 5, wx.CENTER)

            self.h9_sizer.Add(texto20, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h9_sizer.AddStretchSpacer(1)
            self.h9_sizer.Add(self.DefCritica, 5, wx.CENTER)

            self.v11_sizer.Add(self.h7_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            self.v11_sizer.AddStretchSpacer(1)
            self.v11_sizer.Add(self.h8_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            self.v11_sizer.AddStretchSpacer(1)
            self.v11_sizer.Add(self.h9_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)

            self.h10_sizer.Add(self.v11_sizer, 1, wx.CENTER)
            staticboxSizer4.Add(self.h10_sizer, 0, wx.ALL | wx.EXPAND  | wx.CENTER, 10)

            #--------------------------------------------------
            '''Static Box 5'''
            self.v8_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v9_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v10_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h6_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.v8_sizer.Add(texto17, 1, wx.ALL | wx.CENTER)
            self.v8_sizer.Add(self.SigmaAlvo, 2, wx.ALL | wx.CENTER)

            self.v9_sizer.Add(texto15, 1, wx.ALL | wx.CENTER)
            self.v9_sizer.Add(self.SigmaReal, 2, wx.ALL | wx.CENTER)

            self.h5_sizer.Add(self.v9_sizer, 6, wx.CENTER)
            self.h5_sizer.AddStretchSpacer(1)
            self.h5_sizer.Add(self.v8_sizer, 6, wx.CENTER)

            self.v10_sizer.Add(texto4, 1, wx.ALL | wx.CENTER)
            self.v10_sizer.Add(self.h5_sizer, 3, wx.ALL | wx.CENTER)

            self.h6_sizer.Add(self.v10_sizer, 1, wx.CENTER)
            staticboxSizer5.Add(self.h6_sizer, 0, wx.ALL | wx.CENTER, 10)

            #--------------------------------------------------
            '''Static Box 6'''
            self.v3_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v4_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v5_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v6_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v7_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h4_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.v3_sizer.Add(texto24, 1, wx.ALL | wx.CENTER)
            self.v3_sizer.Add(self.GolpeAtual, 2, wx.ALL | wx.CENTER)

            self.v4_sizer.Add(texto23, 1, wx.ALL | wx.CENTER)
            self.v4_sizer.AddStretchSpacer(1)
            self.v4_sizer.Add(self.freq, 1, wx.ALL | wx.CENTER)

            self.v5_sizer.Add(texto22, 1, wx.ALL | wx.CENTER)
            self.v5_sizer.Add(self.NGolpes, 2, wx.ALL | wx.CENTER)

            self.v6_sizer.Add(texto21, 1, wx.ALL | wx.CENTER)
            self.v6_sizer.Add(self.Ciclo, 2, wx.ALL | wx.CENTER)

            self.h2_sizer.Add(self.v4_sizer, 3, wx.EXPAND | wx.CENTER)
            self.h2_sizer.AddStretchSpacer(1)
            self.h2_sizer.Add(self.v3_sizer, 4, wx.CENTER)

            self.h3_sizer.Add(self.v6_sizer, 3, wx.CENTER)
            self.h3_sizer.AddStretchSpacer(1)
            self.h3_sizer.Add(self.v5_sizer, 4, wx.CENTER)

            self.v7_sizer.Add(self.h3_sizer, 3, wx.ALL | wx.CENTER)
            self.v7_sizer.AddStretchSpacer(1)
            self.v7_sizer.Add(self.h2_sizer, 3, wx.ALL | wx.CENTER)

            self.h4_sizer.Add(self.v7_sizer, 1, wx.CENTER)
            staticboxSizer6.Add(self.h4_sizer, 0, wx.ALL | wx.CENTER, 10)

            #--------------------------------------------------
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.v_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v1_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v2_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h1_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.v_sizer.Add(self.qTensoes, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.condic, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.mr, 1, wx.EXPAND | wx.ALL, 5)

            self.v1_sizer.Add(staticboxSizer3, 15, wx.EXPAND | wx.ALL)
            self.v1_sizer.AddStretchSpacer(1)
            self.v1_sizer.Add(staticboxSizer4, 20, wx.EXPAND | wx.ALL)

            self.v2_sizer.Add(staticboxSizer5, 15, wx.EXPAND | wx.ALL)
            self.v2_sizer.AddStretchSpacer(1)
            self.v2_sizer.Add(staticboxSizer6, 20, wx.EXPAND | wx.ALL)

            self.h1_sizer.Add(staticboxSizer1, 1, wx.EXPAND | wx.ALL, 3)
            self.h1_sizer.Add(staticboxSizer2, 1, wx.EXPAND | wx.ALL, 3)
            self.h1_sizer.Add(self.v1_sizer, 1, wx.EXPAND | wx.ALL, 3)
            self.h1_sizer.Add(self.v2_sizer, 1, wx.EXPAND | wx.ALL, 3)

            self.h_sizer.Add(self.h1_sizer, 14, wx.EXPAND | wx.ALL, 5)
            self.h_sizer.Add(self.v_sizer, 1, wx.EXPAND | wx.ALL)

            self.sizer.Add(self.h_sizer, 0,  wx.EXPAND | wx.ALL, 10)
            self.SetSizer(self.sizer)

            self.timer = wx.Timer(self)
            #self.Bind(wx.EVT_TIMER, self.TimeInterval, self.timer)
            #self.Bind(wx.EVT_CHECKBOX, self.onCheck, self.ensaioAuto)
            self._ciclo = 0  #condicao dos ciclos inicia com zero
            self.erro = False  #indica se há erros na execução
            self.Automatico = True #inicia  com o ensaio Automatico sendo falso
            self.ensaioAuto.SetValue(True)

'''Tela Realização do Ensaio'''
class TelaRealizacaoEnsaioDNIT135(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, parent = None, title = 'EDP - DNIT 135/2018ME - Tela_Ensaio_Beta', size = (1000,700), style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

            '''Configurações do SPLITTER'''
            splitter = wx.SplitterWindow(self)
            top = TopPanel(splitter, self)
            self.bottom = BottomPanel(splitter, top)
            splitter.SplitHorizontally(top, self.bottom, 0)
            splitter.SetMinimumPaneSize(390)
            top.draww()
            #top.draw(X,Y)
            '''plt.ion()'''

            self.Centre()
            self.Show()
            self.Maximize(True)

            '''Dialogo Inicial'''
            info = "EDP 135/2018ME"
            titulo = "Ajuste o Zero dos LVDTs"
            message1 = "Com o valor entre:"
            message2 = "1.0 e 1.5 Volts"
            message3 = "realizando a L. TESTE"
            dlg = dialogoDinamico(1, info, titulo, message1, message2, message3, None)
            dlg.ShowModal()

if __name__ == "__main__":
	app = wx.App()
	frame = TelaRealizacaoEnsaioDNIT135(None)
	frame.ShowModal()
	app.MainLoop()
