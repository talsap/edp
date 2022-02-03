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
frequencias = ['1']

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
            #staticbox2 = wx.StaticBox(self, -1, '')
            staticbox3 = wx.StaticBox(self, -1, '')
            staticbox4 = wx.StaticBox(self, -1, '')
            staticbox5 = wx.StaticBox(self, -1, '')
            staticbox6 = wx.StaticBox(self, -1, '')

            staticboxSizer1 = wx.StaticBoxSizer(staticbox1, wx.VERTICAL)
            #staticboxSizer2 = wx.StaticBoxSizer(staticbox2, wx.VERTICAL)
            staticboxSizer3 = wx.StaticBoxSizer(staticbox3, wx.VERTICAL)
            staticboxSizer4 = wx.StaticBoxSizer(staticbox4, wx.VERTICAL)
            staticboxSizer5 = wx.StaticBoxSizer(staticbox5, wx.VERTICAL)
            staticboxSizer6 = wx.StaticBoxSizer(staticbox6, wx.VERTICAL)

            staticbox1.SetBackgroundColour(wx.Colour(215,215,215))
            #staticbox2.SetBackgroundColour(wx.Colour(215,215,215))
            staticbox3.SetBackgroundColour(wx.Colour(215,215,215))
            staticbox4.SetBackgroundColour(wx.Colour(215,215,215))
            staticbox5.SetBackgroundColour(wx.Colour(215,215,215))
            staticbox6.SetBackgroundColour(wx.Colour(215,215,215))

            self.qTensoes = wx.Button(self, -1, 'CONDIC.\nTÉRMICO')
            self.condic = wx.Button(self, -1, 'CONDIC.')
            self.mr = wx.Button(self, -1, 'M. R.')
            self.LTeste = wx.Button(self, -1, "L. TESTE", size = wx.DefaultSize)
            self.LZero = wx.Button(self, -1, "L. ZERO", size = wx.DefaultSize)

            #self.Bind(wx.EVT_BUTTON, self.QT, self.qTensoes)
            #self.Bind(wx.EVT_BUTTON, self.CONDIC, self.condic)
            #self.Bind(wx.EVT_BUTTON, self.MR, self.mr)
            self.Bind(wx.EVT_BUTTON, self.LTESTE, self.LTeste)
            self.Bind(wx.EVT_BUTTON, self.LZERO, self.LZero)

            self.qTensoes.Disable()
            self.condic.Disable()
            self.mr.Disable()
            self.LZero.Disable()

            self.qTensoes.SetFont(FontTitle1)
            self.condic.SetFont(FontTitle1)
            self.mr.SetFont(FontTitle1)
            self.LTeste.SetFont(FontTitle1)
            self.LZero.SetFont(FontTitle1)

            texto1 = wx.StaticText(self, label = "EIXO X", style = wx.ALIGN_CENTRE)
            texto2 = wx.StaticText(self, label = "T - Temperatura (ºC)", style = wx.ALIGN_CENTRE)
            texto3 = wx.StaticText(self, label = "Pc - Carga de Contato (N)", style = wx.ALIGN_CENTRE)
            texto4 = wx.StaticText(self, label = "P - Carga Cíclica (N)", style = wx.ALIGN_CENTRE)
            texto5 = wx.StaticText(self, label = "Y1 (V)", style = wx.ALIGN_CENTER)
            texto6 = wx.StaticText(self, label = "Y2 (V)", style = wx.ALIGN_CENTER)
            texto7 = wx.StaticText(self, label = "Y1 (mm)", style = wx.ALIGN_CENTER)
            texto8 = wx.StaticText(self, label = "Y2 (mm)", style = wx.ALIGN_CENTER)
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
            texto21.SetBackgroundColour(wx.Colour(215,215,215))
            texto22.SetBackgroundColour(wx.Colour(215,215,215))
            texto23.SetBackgroundColour(wx.Colour(215,215,215))
            texto24.SetBackgroundColour(wx.Colour(215,215,215))

            self.y1V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y2V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y1mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y2mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.P = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.Pc = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.Temperatura = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.Ciclo = wx.TextCtrl(self, -1, '1', size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.NGolpes = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.GolpeAtual = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTRE)
            self.freq = wx.ComboBox(self, -1, frequencias[0], choices = frequencias, size = (50, 35), style = wx.CB_READONLY)

            self.y1V.Disable()
            self.y2V.Disable()
            self.y1mm.Disable()
            self.y2mm.Disable()
            self.P.Disable()
            self.Pc.Disable()
            self.Temperatura.Disable()
            self.Ciclo.Disable()
            self.NGolpes.Disable()
            self.GolpeAtual.Disable()
            self.freq.Disable()

            self.y1V.SetFont(Fonttext)
            self.y2V.SetFont(Fonttext)
            self.y1mm.SetFont(Fonttext)
            self.y2mm.SetFont(Fonttext)
            self.P.SetFont(Fonttext)
            self.Pc.SetFont(Fonttext)
            self.Temperatura.SetFont(Fonttext)
            self.Ciclo.SetFont(Fonttext)
            self.NGolpes.SetFont(Fonttext)
            self.GolpeAtual.SetFont(Fonttext)
            self.freq.SetFont(Fonttext)

            self.y1V.SetForegroundColour((119,118,114))
            self.y2V.SetForegroundColour((119,118,114))
            self.y1mm.SetForegroundColour((119,118,114))
            self.y2mm.SetForegroundColour((119,118,114))
            self.P.SetForegroundColour((119,118,114))
            self.Pc.SetForegroundColour((119,118,114))
            self.Temperatura.SetForegroundColour((119,118,114))
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

            #--------------------------------------------------
            '''Static Box 3'''
            self.v12_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v13_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h12_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.v12_sizer.Add(self.Pc, 2, wx.ALL | wx.CENTER)

            self.h11_sizer.AddStretchSpacer(1)
            self.h11_sizer.Add(self.v12_sizer, 6, wx.CENTER)
            self.h11_sizer.AddStretchSpacer(1)

            self.v13_sizer.Add(texto3, 1, wx.ALL | wx.CENTER)
            self.v13_sizer.Add(self.h11_sizer, 3, wx.ALL | wx.CENTER)

            self.h12_sizer.Add(self.v13_sizer, 1, wx.CENTER)
            staticboxSizer3.Add(self.h12_sizer, 0, wx.ALL | wx.CENTER, 10)

            #--------------------------------------------------
            '''Static Box 4'''
            self.v11_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v10_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h10_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.v10_sizer.Add(self.P, 2, wx.ALL | wx.CENTER)

            self.h9_sizer.AddStretchSpacer(1)
            self.h9_sizer.Add(self.v10_sizer, 6, wx.CENTER)
            self.h9_sizer.AddStretchSpacer(1)

            self.v11_sizer.Add(texto4, 1, wx.ALL | wx.CENTER)
            self.v11_sizer.Add(self.h9_sizer, 3, wx.ALL | wx.CENTER)

            self.h10_sizer.Add(self.v11_sizer, 1, wx.CENTER)
            staticboxSizer4.Add(self.h10_sizer, 0, wx.ALL | wx.CENTER, 10)

            #--------------------------------------------------
            '''Static Box 5'''
            self.v8_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v9_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h6_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.v8_sizer.Add(self.Temperatura, 2, wx.ALL | wx.CENTER)

            self.h5_sizer.AddStretchSpacer(1)
            self.h5_sizer.Add(self.v8_sizer, 6, wx.CENTER)
            self.h5_sizer.AddStretchSpacer(1)

            self.v9_sizer.Add(texto2, 1, wx.ALL | wx.CENTER)
            self.v9_sizer.Add(self.h5_sizer, 3, wx.ALL | wx.CENTER)

            self.h6_sizer.Add(self.v9_sizer, 1, wx.CENTER)
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
            self.v3_sizer.Add(self.GolpeAtual, 2, wx.ALL | wx.CENTER, 5)

            self.v4_sizer.Add(texto23, 1, wx.ALL | wx.CENTER)
            self.v4_sizer.Add(self.freq, 2, wx.ALL | wx.CENTER, 5)

            self.v5_sizer.Add(texto22, 1, wx.ALL | wx.CENTER)
            self.v5_sizer.Add(self.NGolpes, 2, wx.ALL | wx.CENTER, 5)

            self.v6_sizer.Add(texto21, 1, wx.ALL | wx.CENTER)
            self.v6_sizer.Add(self.Ciclo, 2, wx.ALL | wx.CENTER, 5)

            self.h2_sizer.Add(self.v4_sizer, 3, wx.CENTER)
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

            self.v1_sizer.Add(staticboxSizer3, 20, wx.EXPAND | wx.ALL)
            self.v1_sizer.AddStretchSpacer(1)
            self.v1_sizer.Add(staticboxSizer5, 20, wx.EXPAND | wx.ALL)

            self.v2_sizer.Add(staticboxSizer4, 20, wx.EXPAND | wx.ALL)
            self.v2_sizer.AddStretchSpacer(1)
            self.v2_sizer.Add(staticboxSizer6, 20, wx.EXPAND | wx.ALL)

            self.h1_sizer.Add(staticboxSizer1, 1, wx.EXPAND | wx.ALL, 3)
            self.h1_sizer.Add(self.v1_sizer, 1, wx.EXPAND | wx.ALL, 3)
            self.h1_sizer.Add(self.v2_sizer, 1, wx.EXPAND | wx.ALL, 3)

            self.h_sizer.Add(self.h1_sizer, 12, wx.EXPAND | wx.ALL, 5)
            self.h_sizer.Add(self.v_sizer, 1, wx.EXPAND | wx.ALL)
            self.h_sizer.AddStretchSpacer(4)

            self.sizer.Add(self.h_sizer, 0,  wx.EXPAND | wx.ALL, 10)
            self.SetSizer(self.sizer)

            self.timer = wx.Timer(self)
            #self.Bind(wx.EVT_TIMER, self.TimeInterval, self.timer)
            #self.Bind(wx.EVT_CHECKBOX, self.onCheck, self.ensaioAuto)
            self._ciclo = 0  #condicao dos ciclos inicia com zero
            self.erro = False  #indica se há erros na execução
            self.Automatico = True #inicia  com o ensaio Automatico sendo falso
            #self.ensaioAuto.SetValue(True)


    #--------------------------------------------------
        '''Função responsável em realizar a CONECÇÃO'''
        def LTESTE(self, event):
            threadConection = ConexaoThread.ConexaoThread()
            dlg = My.MyProgressDialog(2)
            dlg.ShowModal()
            cond = threadConection.ret()
            if cond[0] == 'connectado':
                menssagError = wx.MessageDialog(self, 'CONECTADO!', 'EDP', wx.OK|wx.ICON_AUTH_NEEDED)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                con.modeConectDNIT135() #acessa o ensaio da 135 no arduino
                self.LTeste.Disable()
                self.LZero.Enable()

                #--------------------------------------------------
                def worker(self):
                    global condition
                    global conditionEnsaio
                    global Fase
                    global Ti
                    global Pausa
                    global X
                    global Y
                    global H
                    global amplitudeMax
                    global amplitudeMin
                    global xz1
                    global yz1
                    global yt1
                    global yz2
                    global yt2
                    global pc1
                    global pg1
                    global tm1
                    global REFERENCIA1
                    global REFERENCIA2
                    con.modeI()  #inicia o modo de impressão de dados
                    condition = True
                    conditionEnsaio = False
                    cnt = 0
                    cont = 0
                    cont1 = 0
                    GolpeAnterior = -1
                    self.leituraZerob1 = 0
                    self.leituraZerob2 = 0
                    self.x_counter = 0
                    valores = [0,0,0,0,0,0,0]
                    while True:
                        while condition == True:
                            valores = con.ColetaJ(valores)
                            if cont1 >= 10:
                                self.y1mm.Clear()
                                self.y2mm.Clear()
                                self.y1V.Clear()
                                self.y2V.Clear()
                                self.Temperatura.Clear()
                                self.y1mm.AppendText(str(round((valores[1]-self.leituraZerob1), 4)))
                                self.y2mm.AppendText(str(round((valores[2]-self.leituraZerob2), 4)))
                                self.y1V.AppendText(str(round((valores[3]), 2)))
                                self.y2V.AppendText(str(round((valores[4]), 2)))
                                self.Temperatura.AppendText(str(round((valores[5]), 3)))
                                if cont1 == 10:
                                    cont1 = 0
                            cont1 = cont1 + 1

                            y1 = valores[1]-self.leituraZerob2
                            y2 = valores[2]-self.leituraZerob2  #alterar essa linha quando usar os 2 sensores
                            ymedio = (y1 + y2)/2
                            #print ymedio
                            
                            '''if conditionEnsaio == True:'''
                            if conditionEnsaio == True and valores[0] > 0:
                                X = np.append(X, valores[0])
                                Y = np.append(Y, ymedio+H0)
                                self.x_counter = len(X)
                                if self.x_counter >= 1500:
                                    X = np.delete(X, 0, 0)
                                    Y = np.delete(Y, 0, 0)

                                if Fase == 'CONDICIONAMENTO' and Pausa == False:
                                    if valores[0] == 0.01:
                                        REFERENCIA1 = y1+H0
                                        REFERENCIA2 = y2+H0
                                    if int(valores[0]) > 494 and int(valores[0]) <= 500:
                                        xz1.append(valores[0])
                                        yz1.append(y1+H0)
                                        yz2.append(y2+H0)
                                        tm1.append(valores[5])

                                if Fase == 'MR' and Pausa == False:
                                    if valores[0] == 0.01:
                                        REFERENCIA1 = y1+H0
                                        REFERENCIA2 = y2+H0
                                    if int(valores[0]) > 4 and int(valores[0]) <= 10:
                                        xz1.append(valores[0])
                                        yz1.append(y1+H0)
                                        yz2.append(y2+H0)
                                        tm1.append(valores[5])

                                if int(valores[6]) != GolpeAnterior:
                                    GolpeAnterior = int(valores[6])
                                    self.GolpeAtual.Clear()
                                    self.GolpeAtual.AppendText(str(int(valores[6])))

                #--------------------------------------------------
                self.t = threading.Thread(target=worker, args=(self,))
                self.t.start()

            else:
                menssagError = wx.MessageDialog(self, 'Não é possível manter uma conexão serial!', 'EDP', wx.OK|wx.ICON_EXCLAMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()

    #--------------------------------------------------
        '''Função responsável pela leitura zero'''
        def LZERO(self, event):
            print 'LZERO'
            self.freq.Enable()
            self.qTensoes.Enable()
            self.condic.Enable()
            self.mr.Enable()
            self.LTeste.Disable()
            self.y1mmm = self.y1mm.GetValue()
            self.y2mmm = self.y2mm.GetValue()
            self.leituraZerob1 = float(self.valorLeitura0)
            self.leituraZerob2 = float(self.valorLeitura1)
            print self.leituraZerob1
            print self.leituraZerob2

'''Tela Realização do Ensaio'''
class TelaRealizacaoEnsaioDNIT135(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, parent = None, title = 'EDP - DNIT 135/2018ME - Tela_Ensaio_Beta', size = (1000,750), style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

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

if __name__ == "__main__":
	app = wx.App()
	frame = TelaRealizacaoEnsaioDNIT135(None)
	frame.ShowModal()
	app.MainLoop()
