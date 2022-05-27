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
import back.DinamicaThread as DinamicaThread
import back.ConexaoThread as ConexaoThread
from drawnow import *
from front.quadrotensoes import quadro
from front.dialogoDinamico import dialogoDinamico
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

'''Frequencias para o ensaio'''
frequencias = ['1', '2']

'''Variáveis Globais'''
global leituraZerob1 #leitura zero do sensor 1
global leituraZerob2 #leitura zero do sensor 2
global H  #Altura do corpo de prova em milímetros
global H0 #Altura de referência do medididor de deslocamento
global X  #valores X do gráfico
global Y  #valores Y do gráfico
global pc #pressão confinante
global pg #pressão dos golpes (desvio)
global DefResiliente #Deformação resiliente ou recuperável
global DefPermanente #Deformação Permanente
global REFERENCIA1 #referencia de ponto de partida para o sensor 1
global REFERENCIA2 #referencia de ponto de partida para o sensor 2
global REFERENCIA_MEDIA #referencia de ponto de partidada MÉDIA
global Ti #valor temporal
global Fase #valor para identificar se esta no CONDICIONAMENTO ou no MR
global Automatico #idica se o ensaio será automático ou não
global Pausa #indica se o ensaio foi pausado
global mult  #Multiplo de 5 que ajuda a arrumar o gráfico em 5 em 5
global glpCOND #quantidade de golpes do CONDICIONAMENTO
global ntglp #quantidade total de golpes disponíveis
global modeADM #modo Administrador de salvar dados (apenas para dbug)
global freq #frequencia do ensaio
global idt
global temposDNIT179_01
global temposDNIT179_02

H0 = 0.01
H = 200
mult = 0
Pausa = False
idt = 'DNIT179-2605-' #identificador do ensaio no banco de dados
subleito = False  #recebe valor de True ou False
X = np.array([])
Y = np.array([])
Fase = ''
glpCOND = 50 #número total de golpes do condicionamento
glpDP = 150000 #número total de golpes da deformação permanente
modeADM = False
freq = 1  #a frequencia inicia sendo 1 (default)

VETOR_COND = [[0.030,0.060]]

VETOR_DP =  [[0.040,0.120]]

temposDNIT179_01 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,
                    100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950]
temposDNIT179_02 = [1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,
                    10500,11000,11500,12000,12500,13000,13500,14000,14500,15000,15500,16000,16500,17000,17500,18000,
                    18500,19000,19500,20000,20500,21000,21500,22000,22500,23000,23500,24000,24500,25000,25500,26000,
                    26500,27000,27500,28000,28500,29000,29500,30000,30500,31000,31500,32000,32500,33000,33500,34000,
                    34500,35000,35500,36000,36500,37000,37500,38000,38500,39000,39500,40000,40500,41000,41500,42000,
                    42500,43000,43500,44000,44500,45000,45500,46000,46500,47000,47500,48000,48500,49000,49500,50000,
                    52500,55000,57500,60000,62500,65000,67500,70000,72500,75000,77500,80000,82500,85000,87500,90000,
                    92500,95000,97500,100000,105000,110000,115000,120000,125000,130000,135000,140000,145000,150000]

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
            self.axes = self.figure.add_subplot(111)
            self.canvas = FigureCanvas(self, -1, self.figure)

            rect = self.figure.patch
            rect.set_facecolor('#D7D7D7')

            self.pausa = wx.Button(self, -1, 'PAUSA')
            self.Bind(wx.EVT_BUTTON, self.PAUSA, self.pausa)
            self.continua = wx.Button(self, -1, 'CONTINUA')
            self.Bind(wx.EVT_BUTTON, self.CONTINUA, self.continua)
            self.fim_inicio = wx.Button(self, -1, 'INICIO')
            self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)

            self.pausa.Disable()
            self.continua.Disable()
            self.fim_inicio.Disable()

            self.pausa.SetFont(FontTitle)
            self.continua.SetFont(FontTitle)
            self.fim_inicio.SetFont(FontTitle)

            self.v_sizer.Add(self.pausa, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.continua, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.fim_inicio, 1, wx.EXPAND | wx.ALL, 5)

            self.h_sizer.Add(self.canvas, 12, wx.EXPAND | wx.ALL, 5)
            self.h_sizer.Add(self.v_sizer, 1, wx.EXPAND | wx.ALL)
            self.h_sizer.AddStretchSpacer(4)

            self.sizer.Add(self.h_sizer, 0, wx.EXPAND | wx.ALL, 10)
            self.SetSizer(self.sizer)
            self.DINAMICA2_ANTERIOR = 0
            self.DINAMICA1_ANTERIOR = 0

    #--------------------------------------------------
        '''Função PAUSA'''
        def PAUSA(self, event):
            print '\nTopPanel - PAUSA'
            global conditionEnsaio
            global Pausa

            Pausa = True
            con.modeP()
            conditionEnsaio = False
            self._self.bottom.timer.Stop()
            self.continua.Enable()
            self.fim_inicio.Enable()
            self.pausa.Disable()

    #--------------------------------------------------
        '''Função CONTINUA'''
        def CONTINUA(self, event):
            print '\nTopPanel - CONTINUA'
            global conditionEnsaio
            global Ti
            global Pausa

            con.modeC()
            conditionEnsaio = True
            Pausa = False
            self._self.bottom.timer.Start(int('2500'))
            self.pausa.Enable()
            self.fim_inicio.Disable()
            self.continua.Disable()

    #--------------------------------------------------
        '''Função INICIO'''
        def INICIO(self, event):
            print '\nTopPanel - INICIO'
            global Fase
            global condition
            global conditionEnsaio
            global freq
            self.fim_inicio.Disable()

            if Fase == 'CONDICIONAMENTO':
                condition = False
                threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_COND[0][1], self.DINAMICA2_ANTERIOR)
                dlgC1 = My.MyProgressDialog(3)
                dlgC1.ShowModal()
                time.sleep(1)
                threadConection = DinamicaThread.DinamicaThreadOne(VETOR_COND[0][0], self.DINAMICA1_ANTERIOR)
                dlgC2 = My.MyProgressDialog(3)
                dlgC2.ShowModal()
                time.sleep(1)
                self.DINAMICA2_ANTERIOR = VETOR_COND[0][1]
                self.DINAMICA1_ANTERIOR = VETOR_COND[0][0]

            if Fase == 'DP':
                condition = False
                threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_DP[0][1], self.DINAMICA2_ANTERIOR)
                dlgC1 = My.MyProgressDialog(3)
                dlgC1.ShowModal()
                time.sleep(1)
                threadConection = DinamicaThread.DinamicaThreadOne(VETOR_DP[0][0], self.DINAMICA1_ANTERIOR)
                dlgC2 = My.MyProgressDialog(3)
                dlgC2.ShowModal()
                time.sleep(1)
                self.DINAMICA2_ANTERIOR = VETOR_DP[0][1]
                self.DINAMICA1_ANTERIOR = VETOR_DP[0][0]

            condition = False
            con.modeStoped()
            gl = self._self.bottom.NGolpes.GetValue()
            freq = self._self.bottom.freq.GetValue()
            con.modeG()
            time.sleep(0.5)
            con.modeGOLPES(int(gl)+1, int(freq))
            condition = True
            conditionEnsaio = True
            time.sleep(0.5)
            self._self.bottom.timer.Start(int('2500'))
            self.pausa.Enable()
            self.fim_inicio.SetLabel('FIM')
            self.Bind(wx.EVT_BUTTON, self.FIM, self.fim_inicio)

            #--------------------------------------------------
            #-------- Thread de parada e de salvamento --------
            def worker1(self):
                import bancodedados
                global condition
                global conditionEnsaio
                global Fase
                global X
                global Y
                global pc
                global pg
                global mult
                global glpCOND
                global ntglp
                global DefResiliente
                global DefPermanente
                global REFERENCIA_MEDIA
                global idt
                global temposDNIT179_01
                global temposDNIT179_02
                valorGolpeAnterior = 0
                golpe = []
                vDR = []
                vDP = []
                ppc = []
                ppg = []

                if Fase == 'CONDICIONAMENTO':
                    while True:
                        try:
                            valorGolpe = int(self._self.bottom.GolpeAtual.GetValue())
                            if valorGolpe == int(glpCOND):
                                time.sleep(4)
                                con.modeI()
                                self.pausa.Disable()
                                conditionEnsaio = False
                                valorGolpe = 0
                                self._self.bottom.timer.Stop()
                                X = np.array([])
                                Y = np.array([])
                                mult = 0
                                self.draww()
                                self.pausa.Disable()
                                evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self._self.bottom.dp.GetId())
                                wx.PostEvent(self._self.bottom.condic, evt)
                                break
                        except:
                            pass

                if Fase == 'DP':
                    while True:
                        try:
                            valorGolpe = int(self._self.bottom.GolpeAtual.GetValue())
                            if valorGolpe != valorGolpeAnterior:
                                valorGolpeAnterior = valorGolpe
                                if valorGolpe in temposDNIT179_02:
                                    bancodedados.saveDNIT179(idt+"DP", valorGolpe, DefResiliente, DefPermanente, pc, pg)
                                if valorGolpe in temposDNIT179_01:
                                    golpe.append(valorGolpe)
                                    vDR.append(DefResiliente)
                                    vDP.append(DefPermanente)
                                    ppc.append(pc)
                                    ppg.append(pg)
                                    if valorGolpe == 200:
                                        self._self.bottom.gDP.Enable()
                                    if valorGolpe == 100:
                                        ix = 0
                                        while ix < len(golpe):
                                            bancodedados.saveDNIT179(idt+"DP", golpe[ix], vDR[ix], vDP[ix], ppc[ix], ppg[ix])
                                            ix += 1
                                        golpe *= 0 #limpa a lista
                                        vDR *= 0 #limpa a lista
                                        vDP *= 0 #limpa a lista
                                        ppc *= 0 #limpa a lista
                                        ppg *= 0 #limpa a lista
                                    if valorGolpe == 950:
                                        ix = 0
                                        while ix < len(golpe):
                                            bancodedados.saveDNIT179(idt+"DP", golpe[ix], vDR[ix], vDP[ix], ppc[ix], ppg[ix])
                                            ix += 1
                                        golpe *= 0 #limpa a lista
                                        vDR *= 0 #limpa a lista
                                        vDP *= 0 #limpa a lista
                                        ppc *= 0 #limpa a lista
                                        ppg *= 0 #limpa a lista

                            if valorGolpe == int(ntglp):
                                time.sleep(4)
                                con.modeI()
                                self.pausa.Disable()
                                self._ciclo = self._self.bottom._ciclo + 1
                                self._self.bottom._ciclo = self._ciclo
                                valorGolpe = 0
                                conditionEnsaio = False
                                self._self.bottom.timer.Stop()
                                X = np.array([])
                                Y = np.array([])
                                mult = 0
                                self.draww()
                                self.pausa.Disable()
                                evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self._self.bottom.dp.GetId())
                                wx.PostEvent(self._self.bottom.dp, evt)
                                break
                        except:
                            pass
            #--------------------------------------------------
            self.t1 = threading.Thread(target=worker1, args=(self,))
            self.t1.start()

    #--------------------------------------------------
        '''Função FIM'''
        def FIM(self, event):
            print '\nTopPanel - FIM'
            global condition
            global conditionEnsaio
            global Fase
            global mult

            '''Diálogo se deseja realmente finalizar o CONDICIONAMENTO'''
            dlg = wx.MessageDialog(None, 'Deseja realmente finalizar o '+Fase+'?', 'EDP', wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
            result = dlg.ShowModal()

            if result == wx.ID_YES:
                dlg.Destroy()
                self.fim_inicio.Disable()
                con.modeFIM()
                self.continua.Disable()

                conditionEnsaio = False
                self._self.bottom.timer.Stop()
                X = np.array([])
                Y = np.array([])
                mult = 0
                self.draww()

            if Fase == 'CONDICIONAMENTO':
                self._self.bottom._ciclo = 0
                self._self.bottom.dp.Enable()
                self.fim_inicio.SetLabel('INICIO')
                self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)
                self._self.bottom.pressao_zero(VETOR_COND[0][0], VETOR_COND[0][1])
                con.modeI()

            if Fase == 'DP':
                con.modeI()
                self._self.bottom.pressao_zero(VETOR_DP[0][0], VETOR_DP[0][1])
                dlg3 = dialogoDinamico(3, "EDP 179/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatórios de extração são gerados na tela inicial.", "FIM!", "", None)
                dlg3.ShowModal()
                con.modeI()

    #--------------------------------------------------
        '''Ajusta min e max EIXO X'''
        def changeAxesX(self, min, max):
            print '\nTopPanel - changeAxesY'
            self.axes.set_xlim(float(min), float(max))
            self.canvas.draw()

    #--------------------------------------------------
        '''Ajusta min e max EIXO Y'''
        def changeAxesY(self, min, max):
            print '\nTopPanel - changeAxesY'
            self.axes.set_ylim(float(min), float(max))
            self.canvas.draw()

    #--------------------------------------------------
        def draww(self):
            print '\nTopPanel - draww'
            self.axes.clear()
            self.axes.set_xlim(float(0), float(1))
            self.axes.set_ylim(float(0), float(0.01))
            self.axes.set_xlabel("TEMPO (seg)")
            self.axes.set_ylabel("DESLOCAMENTO (mm)")
            self.canvas.draw()

    #--------------------------------------------------
        def draw(self):
            print '\nTopPanel - draw'
            global mult
            self.axes.clear()
            #self.axes.set_xlim(mult*5-5, mult*5)
            self.axes.set_xlabel("TEMPO (seg)")
            self.axes.set_ylabel("DESLOCAMENTO (mm)")
            self.axes.plot(X, Y, 'r-')
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

            self.gDP = wx.Button(self, -1, 'TEMPO\nX\nDEF.P.')
            self.Bind(wx.EVT_BUTTON, self.GDP, self.gDP)
            self.condic = wx.Button(self, -1, 'CONDIC.')
            self.Bind(wx.EVT_BUTTON, self.CONDIC, self.condic)
            self.dp = wx.Button(self, -1, 'DEF.P.')
            self.Bind(wx.EVT_BUTTON, self.DP, self.dp)
            self.LTeste = wx.Button(self, -1, "L. TESTE", size = wx.DefaultSize)
            self.Bind(wx.EVT_BUTTON, self.LTESTE, self.LTeste)
            self.LZero = wx.Button(self, -1, "L. ZERO", size = wx.DefaultSize)
            self.Bind(wx.EVT_BUTTON, self.LZERO, self.LZero)

            self.gDP.Disable()
            self.condic.Disable()
            self.dp.Disable()
            self.LZero.Disable()

            self.gDP.SetFont(FontTitle1)
            self.condic.SetFont(FontTitle1)
            self.dp.SetFont(FontTitle1)
            self.LTeste.SetFont(FontTitle1)
            self.LZero.SetFont(FontTitle1)

            texto1 = wx.StaticText(self, label = "EIXO Y", style = wx.ALIGN_CENTRE)
            texto3 = wx.StaticText(self, label = "σ3 - Tensão confinante (MPa)", style = wx.ALIGN_CENTRE)
            texto4 = wx.StaticText(self, label = "σd - Tensão desvio (MPa)", style = wx.ALIGN_CENTRE)
            texto5 = wx.StaticText(self, label = "Y1 (V)", style = wx.ALIGN_CENTER)
            texto6 = wx.StaticText(self, label = "Y2 (V)", style = wx.ALIGN_CENTER)
            texto7 = wx.StaticText(self, label = "Y1 (mm)", style = wx.ALIGN_CENTER)
            texto8 = wx.StaticText(self, label = "Y2 (mm)", style = wx.ALIGN_CENTER)
            texto13 = wx.StaticText(self, label = "Altura Final (mm)", style = wx.ALIGN_LEFT)
            texto14 = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
            texto15 = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
            texto16 = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
            texto17 = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
            texto18 = wx.StaticText(self, label = "Altura (mm)", style = wx.ALIGN_LEFT)
            texto19 = wx.StaticText(self, label = "Diâmetro (mm)", style = wx.ALIGN_LEFT)
            texto21 = wx.StaticText(self, label = "CICLO", style = wx.ALIGN_CENTER)
            texto22 = wx.StaticText(self, label = "Nº de Golpes", style = wx.ALIGN_CENTER)
            texto23 = wx.StaticText(self, label = "Freq. (Hz)", style = wx.ALIGN_CENTER)
            texto24 = wx.StaticText(self, label = "Golpe Atual", style = wx.ALIGN_CENTER)

            texto1.SetFont(FontTitle)
            texto3.SetFont(FontTitle)
            texto4.SetFont(FontTitle)
            texto5.SetFont(Fonttext)
            texto6.SetFont(Fonttext)
            texto7.SetFont(Fonttext)
            texto8.SetFont(Fonttext)
            texto13.SetFont(FontTitle)
            texto14.SetFont(Fonttext)
            texto15.SetFont(Fonttext)
            texto16.SetFont(Fonttext)
            texto17.SetFont(Fonttext)
            texto18.SetFont(Fonttext)
            texto19.SetFont(Fonttext)
            texto21.SetFont(FontTitle)
            texto22.SetFont(Fonttext)
            texto23.SetFont(Fonttext)
            texto24.SetFont(Fonttext)

            texto1.SetBackgroundColour(wx.Colour(215,215,215))
            texto3.SetBackgroundColour(wx.Colour(215,215,215))
            texto4.SetBackgroundColour(wx.Colour(215,215,215))
            texto5.SetBackgroundColour(wx.Colour(215,215,215))
            texto6.SetBackgroundColour(wx.Colour(215,215,215))
            texto7.SetBackgroundColour(wx.Colour(215,215,215))
            texto8.SetBackgroundColour(wx.Colour(215,215,215))
            texto13.SetBackgroundColour(wx.Colour(215,215,215))
            texto14.SetBackgroundColour(wx.Colour(215,215,215))
            texto15.SetBackgroundColour(wx.Colour(215,215,215))
            texto16.SetBackgroundColour(wx.Colour(215,215,215))
            texto17.SetBackgroundColour(wx.Colour(215,215,215))
            texto18.SetBackgroundColour(wx.Colour(215,215,215))
            texto19.SetBackgroundColour(wx.Colour(215,215,215))
            texto21.SetBackgroundColour(wx.Colour(215,215,215))
            texto22.SetBackgroundColour(wx.Colour(215,215,215))
            texto23.SetBackgroundColour(wx.Colour(215,215,215))
            texto24.SetBackgroundColour(wx.Colour(215,215,215))

            self.y1V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y2V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y1mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y2mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.AlturaFinal = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.PCreal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.PCalvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.SigmaReal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.SigmaAlvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.AlturaMM = wx.TextCtrl(self, -1, '200.0', size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.DiametroMM = wx.TextCtrl(self, -1, '100.0', size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.Ciclo = wx.TextCtrl(self, -1, '1', size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.NGolpes = wx.TextCtrl(self, -1, wx.EmptyString, size = (70, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.GolpeAtual = wx.TextCtrl(self, -1, wx.EmptyString, size = (70, 35), style = wx.TE_READONLY | wx.TE_CENTRE)
            self.freq = wx.ComboBox(self, -1, frequencias[0], choices = frequencias, size = (50, 35), style = wx.CB_READONLY)
            self.ensaioAuto = wx.CheckBox(self, -1, 'Ensaio automático', (20,0), (260,-1), style = wx.ALIGN_LEFT)

            self.y1V.Disable()
            self.y2V.Disable()
            self.y1mm.Disable()
            self.y2mm.Disable()
            self.AlturaFinal.Disable()
            self.PCreal.Disable()
            self.PCalvo.Disable()
            self.SigmaReal.Disable()
            self.SigmaAlvo.Disable()
            self.AlturaMM.Disable()
            self.DiametroMM.Disable()
            self.Ciclo.Disable()
            self.NGolpes.Disable()
            self.GolpeAtual.Disable()
            self.freq.Disable()

            self.y1V.SetFont(Fonttext)
            self.y2V.SetFont(Fonttext)
            self.y1mm.SetFont(Fonttext)
            self.y2mm.SetFont(Fonttext)
            self.AlturaFinal.SetFont(Fonttext)
            self.PCreal.SetFont(Fonttext)
            self.PCalvo.SetFont(Fonttext)
            self.SigmaReal.SetFont(Fonttext)
            self.SigmaAlvo.SetFont(Fonttext)
            self.AlturaMM.SetFont(Fonttext)
            self.DiametroMM.SetFont(Fonttext)
            self.Ciclo.SetFont(Fonttext)
            self.NGolpes.SetFont(Fonttext)
            self.GolpeAtual.SetFont(Fonttext)
            self.freq.SetFont(Fonttext)

            self.y1V.SetForegroundColour((119,118,114))
            self.y2V.SetForegroundColour((119,118,114))
            self.y1mm.SetForegroundColour((119,118,114))
            self.y2mm.SetForegroundColour((119,118,114))
            self.AlturaFinal.SetForegroundColour((119,118,114))
            self.PCreal.SetForegroundColour((119,118,114))
            self.PCalvo.SetForegroundColour((119,118,114))
            self.SigmaReal.SetForegroundColour((119,118,114))
            self.SigmaAlvo.SetForegroundColour((119,118,114))
            self.AlturaMM.SetForegroundColour((119,118,114))
            self.DiametroMM.SetForegroundColour((119,118,114))
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

            self.h9_sizer.Add(texto13, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h9_sizer.AddStretchSpacer(1)
            self.h9_sizer.Add(self.AlturaFinal, 5, wx.CENTER)

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

            self.v_sizer.Add(self.gDP, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.condic, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.dp, 1, wx.EXPAND | wx.ALL, 5)

            self.v1_sizer.Add(staticboxSizer3, 15, wx.EXPAND | wx.ALL)
            self.v1_sizer.AddStretchSpacer(1)
            self.v1_sizer.Add(staticboxSizer4, 20, wx.EXPAND | wx.ALL)

            self.v2_sizer.Add(staticboxSizer5, 15, wx.EXPAND | wx.ALL)
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
            self.Bind(wx.EVT_TIMER, self.TimeInterval, self.timer)
            self.Bind(wx.EVT_CHECKBOX, self.onCheck, self.ensaioAuto)
            self._ciclo = 0  #condicao dos ciclos inicia com zero
            self.erro = False  #indica se há erros na execução
            self.Automatico = True #inicia  com o ensaio Automatico sendo true
            self.ensaioAuto.SetValue(True)

    #--------------------------------------------------
        '''Função CheckBox'''
        def onCheck(self, event):
            print '\nBottomPanel - onCheck'
            global Automatico
            if  self.ensaioAuto.GetValue() == False:
                self.Automatico = False
            else:
                self.Automatico = True

    #--------------------------------------------------
        '''Função responsável em realizar a CONEXÃO'''
        def LTESTE(self, event):
            print '\nBottomPanel - LTESTE'
            threadConection = ConexaoThread.ConexaoThread()
            dlg = My.MyProgressDialog(2)
            dlg.ShowModal()
            cond = threadConection.ret()
            if cond[0] == 'connectado':
                menssagError = wx.MessageDialog(self, 'CONECTADO!', 'EDP', wx.OK|wx.ICON_AUTH_NEEDED)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                con.modeConectDNIT134() #acessa o ensaio da 134 no arduino
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
                    global DefResiliente
                    global DefPermanente
                    global pc
                    global pg
                    global REFERENCIA1
                    global REFERENCIA2
                    global REFERENCIA_MEDIA
                    global ntglp
                    global freq
                    con.modeI()  #inicia o modo de impressão de dados
                    condition = True
                    conditionEnsaio = False
                    cnt = 0
                    cont = 0
                    cont1 = 0
                    amplitudeMax = 0
                    amplitudeMax2 = 0
                    patamarAnterior = 0
                    patamar = 0
                    DefResiliente = 0
                    DefPermanente = 0
                    pc = 0
                    pg = 0
                    GolpeAnterior = -1
                    self.leituraZerob1 = 0
                    self.leituraZerob2 = 0
                    x_counter = 0
                    valores = [0,0,0,0,0,0,0,0,0,0]
                    while True:
                        while condition == True:
                            valores = con.ColetaI(valores)
                            if cont1 >= 20: #mede a frequencia da impressão de dados na tela
                                self.y1mm.Clear()
                                self.y2mm.Clear()
                                self.y1V.Clear()
                                self.y2V.Clear()
                                self.PCreal.Clear()
                                self.SigmaReal.Clear()
                                self.AlturaFinal.Clear()
                                self.valorLeitura0 = valores[1] #usado apenas no LZERO
                                self.valorLeitura1 = valores[2] #usado apenas no LZERO
                                self.y1mm.AppendText(str(round((valores[1]-self.leituraZerob1), 4)))
                                self.y2mm.AppendText(str(round((valores[2]-self.leituraZerob2), 4)))
                                self.y1V.AppendText(str(round((valores[3]), 2)))
                                self.y2V.AppendText(str(round((valores[4]), 2)))
                                self.PCreal.AppendText(str(round(abs((valores[5])), 3)))
                                self.SigmaReal.AppendText(str(round(abs(valores[6]-valores[5]), 3)))
                                if self.leituraZerob1 == 0:
                                    self.AlturaFinal.AppendText(str(round(H, 3)))
                                else:
                                    self.AlturaFinal.AppendText(str(round(H-ymedio, 3)))
                                if cont1 == 20:
                                    cont1 = 0
                            cont1 = cont1 + 1

                            ntglp = valores[9] #numero total de golpes
                            y1 = valores[1]-self.leituraZerob1
                            y2 = valores[2]-self.leituraZerob2  #alterar essa linha quando usar os 2 sensores
                            ymedio = (y1 + y2)/2 + H0 #A média + H0 que é o ponto de referência inicial

                            # Dados para a parte GRÁFICA #
                            if conditionEnsaio == True and valores[8] >= 0:
                                X = np.append(X, valores[0])
                                Y = np.append(Y, ymedio)
                                x_counter = len(X)
                                if x_counter >= 500: #antes era 1500
                                    X = np.delete(X, 0, 0)
                                    Y = np.delete(Y, 0, 0)

                                # Dados do dp #
                                if Fase == 'DP' and Pausa == False:
                                    #PEGA OS VALORES DE REFERENCIA
                                    if valores[0] == 0.01:
                                        REFERENCIA1 = y1+H0
                                        REFERENCIA2 = y2+H0
                                        REFERENCIA_MEDIA = ymedio
                                    if valores[0] > 0.2 and valores[0] < 0.5:
                                        REFERENCIA1 = (REFERENCIA1 + (y1+H0))/2
                                        REFERENCIA2 = (REFERENCIA2 + (y2+H0))/2
                                        REFERENCIA_MEDIA = (REFERENCIA_MEDIA + ymedio)/2

                                    #condicao de erro para o ensaio
                                    if int(valores[7]) == 1:
                                        print "ERRO NO ENSAIO"

                                    #PRESSÕES DO ENSAIO
                                    pc = (pc + valores[5])/2
                                    pg = (pg + (valores[6]-valores[5]))/2

                                    D = valores[0] - int(valores[0])
                                    #REFERENTE AOS DADOS DE DEFORMAÇÃO PERMANENTE FREQ 1
                                    if freq == '1':
                                        if D == 0.01:
                                            patamar = ymedio
                                            amplitudeMax = ymedio
                                        if D < 0.2:
                                            if ymedio > amplitudeMax:
                                                amplitudeMax = ymedio
                                        if D > 0.2 and D < 0.9:
                                            patamar = (patamar + ymedio)/2
                                        if D > 0.9:
                                            DefResiliente  = amplitudeMax - patamar
                                            DefPermanente = patamar
                                            patamarAnterior = patamar
                                        #print D, DefResiliente, DefPermanente, REFERENCIA_MEDIA

                                    #REFERENTE AOS DADOS DE DEFORMAÇÃO PERMANENTE FREQ 2
                                    if freq == '2':
                                        if D == 0.01:
                                            patamar = ymedio
                                            amplitudeMax = ymedio
                                            amplitudeMax2 = ymedio
                                        if D < 0.2:
                                            if ymedio > amplitudeMax:
                                                amplitudeMax = ymedio
                                        if D > 0.2 and D < 0.5:
                                            patamar = (patamar + ymedio)/2
                                        if D > 0.5 and D < 0.65:
                                            if ymedio > amplitudeMax2:
                                                amplitudeMax2 = ymedio
                                            DefResiliente  = amplitudeMax - patamar
                                            DefPermanente = patamar
                                        if D > 0.6 and D < 0.9:
                                            patamar = (patamar + ymedio)/2
                                        if D > 0.9:
                                            DefResiliente  = amplitudeMax2 - patamar
                                            DefPermanente = patamar
                                        #print D, DefResiliente, DefPermanente, REFERENCIA_MEDIA
                                if int(valores[8]) != GolpeAnterior:
                                    GolpeAnterior = int(valores[8])
                                    self.GolpeAtual.Clear()
                                    self.GolpeAtual.AppendText(str(int(valores[8])))

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
            print '\nBottomPanel - LZERO'
            self.freq.Enable()
            self.condic.Enable()
            self.dp.Enable()
            self.LTeste.Disable()
            self.leituraZerob1 = float(self.valorLeitura0)
            self.leituraZerob2 = float(self.valorLeitura1)
            print self.leituraZerob1
            print self.leituraZerob2

    #--------------------------------------------------
        '''Função responsável em mostrar o gráfico da deformação permanente'''
        def GDP(self, event):
            print '\nBottomPanel - GDP'

    #--------------------------------------------------
        '''Função responsável em realizar o CONDICIONAMENTO'''
        def CONDIC(self, event):
            print '\nBottomPanel - CONDIC'
            global condition
            global Fase
            global REFERENCIA1
            global REFERENCIA2
            global REFERENCIA_MEDIA
            global modeADM
            Fase = 'CONDICIONAMENTO'
            self.erro = False

            self.LZero.Disable()
            self.freq.Disable()
            self.dp.Disable()
            self.condic.Disable()
            self.PCalvo.Clear()
            self.SigmaAlvo.Clear()
            self.Ciclo.Clear()
            self.NGolpes.Clear()
            self.GolpeAtual.Clear()
            self.PCalvo.AppendText(str(VETOR_COND[0][0])+'0')
            self.SigmaAlvo.AppendText(str(VETOR_COND[0][1]-VETOR_COND[0][0])+'0')
            self.NGolpes.AppendText(str(glpCOND))
            self.Ciclo.AppendText('1')
            self.GolpeAtual.AppendText(str(0))

            info = "EDP 179/2018IE"
            titulo = "Preparação da câmara triaxial."
            message1 = "Verifique se está tudo certo!"
            message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
            dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
            if dlg.ShowModal() == wx.ID_OK:
                if self.Automatico == False:
                    self.graph.fim_inicio.SetLabel('INICIO')
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    self.graph.fim_inicio.Enable()

                if self.Automatico == True:
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                    wx.PostEvent(self.graph.fim_inicio, evt)

    #--------------------------------------------------
        '''Função responsável em realizar a DEFORMAÇÃO PERMANENTE'''
        def DP(self, event):
            print '\nBottomPanel - DP'
            global condition
            global Fase
            global REFERENCIA1
            global REFERENCIA2
            global REFERENCIA_MEDIA
            self.erro = False
            ciclo = 1

            self.LZero.Disable()
            self.freq.Disable()
            self.dp.Disable()
            self.condic.Disable()
            self.PCalvo.Clear()
            self.SigmaAlvo.Clear()
            self.Ciclo.Clear()
            self.NGolpes.Clear()
            self.GolpeAtual.Clear()
            self.PCalvo.AppendText(str(VETOR_DP[0][0])+'0')
            self.SigmaAlvo.AppendText(str(VETOR_DP[0][1]-VETOR_DP[0][0])+'0')
            self.NGolpes.AppendText(str(glpDP))
            self.Ciclo.AppendText('1')
            self.GolpeAtual.AppendText(str(0))

            if Fase == '':
                info = "EDP 179/2018ME"
                titulo = "Preparação da câmara triaxial."
                message1 = "Verifique se está tudo certo!"
                message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                if dlg.ShowModal() == wx.ID_OK:
                    Fase = 'DP'
                    if self._ciclo >= 0 and self._ciclo < ciclo and self.Automatico == False:
                        self.graph.fim_inicio.SetLabel('INICIO')
                        self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                        self.graph.fim_inicio.Enable()

                    if self._ciclo >= 0 and self._ciclo < ciclo and self.Automatico == True:
                        self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                        wx.PostEvent(self.graph.fim_inicio, evt)

                    if self._ciclo >= ciclo and self.erro == False:
                        self.dp.Disable()
                        self.pressao_zero(VETOR_DP[0][0], VETOR_DP[0][1])
                        self._ciclo = 0
                        dlg3 = dialogoDinamico(3, "EDP 179/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatórios de extração são gerados na tela inicial.", "FIM!", "", None)
                        dlg3.ShowModal()
            else:
                Fase = 'DP'
                if self._ciclo >= 0 and self._ciclo < ciclo and self.Automatico == False:
                    self.graph.fim_inicio.SetLabel('INICIO')
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    self.graph.fim_inicio.Enable()

                if self._ciclo >= 0 and self._ciclo < ciclo and self.Automatico == True:
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                    wx.PostEvent(self.graph.fim_inicio, evt)

                if self._ciclo >= ciclo and self.erro == False:
                    self.dp.Disable()
                    self.pressao_zero(VETOR_DP[0][0], VETOR_DP[0][1])
                    self._ciclo = 0
                    dlg3 = dialogoDinamico(3, "EDP 179/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatórios de extração são gerados na tela inicial.", "FIM!", "", None)
                    dlg3.ShowModal()

    #--------------------------------------------------
        '''Função responsável em zerar a pressão do sistema'''
        def pressao_zero(self, p1Sen ,p2Sen):
            print '\nBottomPanel - pressao_zero'
            global condition
            condition = False
            threadConection = DinamicaThread.DinamicaThreadTwoZero(0.005, p2Sen) #0.005 é o menor valor de pressão admissível para valvula dinamica
            dlgC1 = My.MyProgressDialog(4)
            dlgC1.ShowModal()
            time.sleep(1)
            #threadConection = MotorThread.MotorThreadZero(0.030)  #0.030 é o menor valor de pressão admissível para SI do motor de passos
            threadConection = DinamicaThread.DinamicaThreadOneZero(0.005, p1Sen) #0.005 é o menor valor de pressão admissível para valvula dinamica
            dlg2 = My.MyProgressDialog(4)
            dlg2.ShowModal()
            condition = True

    #--------------------------------------------------
        '''Função responsável pela plotagem'''
        def TimeInterval(self, event):
            print '\nBottomPanel - TimeInterval'
            global mult
            mult += 1
            self.graph.draw()


'''Tela Realização do Ensaio'''
class TelaRealizacaoEnsaioDNIT179(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, parent = None, title = 'EDP - DNIT 179/2018IE - Tela_Ensaio_Beta', size = (1000,750), style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

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
            info = "EDP 179/2018IE"
            titulo = "Ajuste o Zero dos LVDTs"
            message1 = "Com o valor entre:"
            message2 = "2.5 e 3.0 Volts"
            message3 = "realizando a L. TESTE"
            dlg = dialogoDinamico(1, info, titulo, message1, message2, message3, None)
            dlg.ShowModal()

if __name__ == "__main__":
	app = wx.App()
	frame = TelaRealizacaoEnsaioDNIT179(None)
	frame.ShowModal()
	app.MainLoop()
