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

'''plt.style.use('ggplot')'''
frequencias = ['1', '2', '3', '4']

'''Variáveis Globais'''
global leituraZerob1 #leitura zero do sensor 1
global leituraZerob2 #leitura zero do sensor 2
global H  #Altura do corpo de prova em milímetros
global H0 #Altura de referência do medididor de deslocamento
global X  #valores X do gráfico
global Y  #valores Y do gráfico
global xz1
global yz1
global yt1
global yz2
global yt2
global pc1
global pg1
global REFERENCIA1 #referencia de ponto de partida para o sensor 1
global REFERENCIA2 #referencia de ponto de partida para o sensor 2
global Ti #valor temporal
global Fase #valor para identificar se esta no CONDICIONAMENTO ou no MR
global Automatico #idica se o ensaio será automático ou não
global Pausa #indica se o ensaio foi pausado
global mult  #Multiplo de 5 que ajuda a arrumar o gráfico em 5 em 5

H0 = 0.01
H = 200
mult = 0
Pausa = False
idt = 'DNIT134-03-'  #identificador do ensaio no banco de dados
subleito = False    #recebe valor de True ou False
X = np.array([])
Y = np.array([])
xz1 = []
yz1 = []
yt1 = []
yz2 = []
yt2 = []
pc1 = []
pg1 = []
Fase = ''

VETOR_COND = [[0.070,0.140],
              [0.070,0.280],
              [0.105,0.420]]

VETOR_MR =  [[0.023,0.040], 
             [0.020,0.060],
             [0.020,0.080],
             [0.035,0.070],
             [0.035,0.105],
             [0.035,0.140],
             [0.050,0.100],
             [0.050,0.150],
             [0.050,0.200],
             [0.070,0.140],
             [0.070,0.210],
             [0.070,0.280],
             [0.105,0.210],
             [0.105,0.315],
             [0.105,0.420],
             [0.140,0.280],
             [0.140,0.420],
             [0.140,0.560]]

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
            self.Bind(wx.EVT_BUTTON, self.AVANCA, self.avanca)
            self.pausa = wx.Button(self, -1, 'PAUSA')
            self.Bind(wx.EVT_BUTTON, self.PAUSA, self.pausa)
            self.continua = wx.Button(self, -1, 'CONTINUA')
            self.Bind(wx.EVT_BUTTON, self.CONTINUA, self.continua)
            self.fim_inicio = wx.Button(self, -1, 'INICIO')
            self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)

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
            self.DINAMICA_ANTERIOR = 0
            self.AVANCA = False

    #--------------------------------------------------
        '''Função AVANCA'''
        def AVANCA(self, event):
            print '\nTopPanel - AVANCA'
            global Fase
            global X
            global Y
            global mult

            '''Diálogo se deseja realmente avancar um ciclo'''
            dlg = wx.MessageDialog(None, 'Deseja realmente avancar um CICLO?', 'EDP', wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
            result = dlg.ShowModal()

            if result == wx.ID_YES:
                dlg.Destroy()
                con.modeF()
                self.fim_inicio.Enable()
                self.avanca.Enable()
                self.continua.Disable()
                self.fim_inicio.Disable()
                self.fim_inicio.SetLabel('INICIO')
                self._self.bottom.GolpeAtual.Clear()
                self._self.bottom.GolpeAtual.AppendText(str(0))

                self._ciclo = self._self.bottom._ciclo + 1
                self._self.bottom._ciclo = self._ciclo

                self._self.bottom.timer.Stop()
                X = np.array([])
                Y = np.array([])
                mult = 0
                self.draww()
                self._self.bottom.PCalvo.Clear()
                self._self.bottom.SigmaAlvo.Clear()
                self._self.bottom.Ciclo.Clear()
                self.AVANCA = True

                if Fase == 'CONDICIONAMENTO':
                    print '\nAVANCA.CICLO.COND='+str(self._ciclo+1)+'\n'
                    self._self.bottom.PCalvo.AppendText(str(VETOR_COND[self._ciclo][0]))
                    self._self.bottom.SigmaAlvo.AppendText(str(VETOR_COND[self._ciclo][1]-VETOR_COND[self._ciclo][0]))
                    self._self.bottom.Ciclo.AppendText(str(self._ciclo+1))

                    if(self._ciclo < 2):
                        self.avanca.Enable()
                    else:
                        self.avanca.Disable()

                if Fase == 'MR':
                    print '\nAVANCA.CICLO.MR='+str(self._ciclo+1)+'\n'
                    self._self.bottom.PCalvo.AppendText(str(VETOR_MR[self._ciclo][0]))
                    self._self.bottom.SigmaAlvo.AppendText(str(VETOR_MR[self._ciclo][1]-VETOR_MR[self._ciclo][0]))
                    self._self.bottom.Ciclo.AppendText(str(self._ciclo+1))

                    if(self._ciclo < 17):
                        self.avanca.Enable()
                    else:
                        self.avanca.Disable()

                self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)
                self.fim_inicio.Enable()

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
            if Fase == 'CONDICIONAMENTO' and subleito == False:
                self.avanca.Enable()
            if Fase == 'MR':
                self.avanca.Enable()

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
            self._self.bottom.timer.Start(int('5000'))
            self.pausa.Enable()
            self.fim_inicio.Disable()
            self.continua.Disable()
            self.avanca.Disable()

    #--------------------------------------------------
        '''Função INICIO'''
        def INICIO(self, event):
            print '\nTopPanel - INICIO'
            global Fase
            global condition
            global conditionEnsaio
            self.fim_inicio.Disable()
            self.avanca.Disable()
            self._ciclo = self._self.bottom._ciclo
            #time.sleep(1)

            if Fase == 'CONDICIONAMENTO':
                condition = False
                if self._ciclo > 0:
                    if VETOR_COND[self._ciclo][1] != VETOR_COND[self._ciclo - 1][1] and self.AVANCA == False:
                        threadConection = DinamicaThread.DinamicaThread(VETOR_COND[self._ciclo][1], VETOR_COND[self._ciclo-1][1])
                        dlgC1 = My.MyProgressDialog(3)
                        dlgC1.ShowModal()
                        self.DINAMICA_ANTERIOR = VETOR_COND[self._ciclo][1]
                        time.sleep(1)

                    if self.AVANCA == True:
                        threadConection = DinamicaThread.DinamicaThread(VETOR_COND[self._ciclo][1], self.DINAMICA_ANTERIOR)
                        dlgC1 = My.MyProgressDialog(3)
                        dlgC1.ShowModal()
                        self.DINAMICA_ANTERIOR = VETOR_COND[self._ciclo][1]
                        self.AVANCA = False
                        time.sleep(1)
                else:
                    threadConection = DinamicaThread.DinamicaThread(VETOR_COND[self._ciclo][1], 0)
                    dlgC1 = My.MyProgressDialog(3)
                    dlgC1.ShowModal()
                    time.sleep(1)

                if self._ciclo > 0:
                    if VETOR_COND[self._ciclo][0] != VETOR_COND[self._ciclo - 1][0]:
                        threadConection = MotorThread.MotorThread(VETOR_COND[self._ciclo][0])
                        dlgC2 = My.MyProgressDialog(3)
                        dlgC2.ShowModal()
                else:
                    threadConection = MotorThread.MotorThread(VETOR_COND[self._ciclo][0])
                    dlgC2 = My.MyProgressDialog(3)
                    dlgC2.ShowModal()

                if threadConection.ret() == False:
                    dlgC3 = dialogoDinamico(3, "EDP 134/2018ME", "CONDICIONAMENTO", "Ocorreu algum problema com o ajuste da pressão!", "Verifique o motor de passos!", "", None)
                    dlgC3.ShowModal()
                    self._self.bottom.erro = True
                    if self._ciclo == 0:
                        self._self.bottom.mr.Enable()
                        self._self.bottom.condic.Enable()
                time.sleep(.5)

                if self._self.bottom.Automatico == False:
                    condition = True
                    dlg3 = dialogoDinamico(3, "EDP 134/2018ME", "CONDICIONAMENTO", "Tudo pronto!", "Aperte INICIO.", "", None)
                    dlg3.ShowModal()
                    time.sleep(1)

            if Fase == 'MR':
                condition = False
                if self._ciclo > 0:
                    if VETOR_MR[self._ciclo][1] != VETOR_MR[self._ciclo - 1][1] and self.AVANCA == False:
                        threadConection = DinamicaThread.DinamicaThread(VETOR_MR[self._ciclo][1], VETOR_MR[self._ciclo-1][1])
                        dlgC1 = My.MyProgressDialog(3)
                        dlgC1.ShowModal()
                        self.DINAMICA_ANTERIOR = VETOR_MR[self._ciclo][1]
                        time.sleep(1)

                    if self.AVANCA == True:
                        threadConection = DinamicaThread.DinamicaThread(VETOR_MR[self._ciclo][1], self.DINAMICA_ANTERIOR)
                        dlgC1 = My.MyProgressDialog(3)
                        dlgC1.ShowModal()
                        self.DINAMICA_ANTERIOR = VETOR_MR[self._ciclo][1]
                        self.AVANCA = False
                        time.sleep(1)
                else:
                    threadConection = DinamicaThread.DinamicaThread(VETOR_MR[self._ciclo][1], 0)
                    dlgC1 = My.MyProgressDialog(3)
                    dlgC1.ShowModal()
                    time.sleep(1)

                if self._ciclo > 0:
                    if VETOR_MR[self._ciclo][0] != VETOR_MR[self._ciclo - 1][0]:
                        threadConection = MotorThread.MotorThread(VETOR_MR[self._ciclo][0])
                        dlgC2 = My.MyProgressDialog(3)
                        dlgC2.ShowModal()
                else:
                    threadConection = MotorThread.MotorThread(VETOR_MR[self._ciclo][0])
                    dlgC2 = My.MyProgressDialog(3)
                    dlgC2.ShowModal()

                if threadConection.ret() == False:
                    dlgC3 = dialogoDinamico(3, "EDP 134/2018ME", "MÓDULO DE RESILIÊNCIA", "Ocorreu algum problema com o ajuste da pressão!", "Verifique o motor de passos!", "", None)
                    dlgC3.ShowModal()
                    self._self.bottom.erro = True
                    if self._ciclo == 0:
                        self._self.bottom.mr.Enable()
                time.sleep(.5)

                if self._self.bottom.Automatico == False:
                    condition = True
                    dlg3 = dialogoDinamico(3, "EDP 134/2018ME", "MÓDULO DE RESILIÊNCIA", "Tudo pronto!", "Aperte INICIO.", "", None)
                    dlg3.ShowModal()
                    time.sleep(1)

            condition = False
            con.modeStoped()
            gl = self._self.bottom.NGolpes.GetValue()
            freq = self._self.bottom.freq.GetValue()
            con.modeG()
            time.sleep(0.5)
            con.modeGOLPES(int(gl), int(freq))
            condition = True
            conditionEnsaio = True
            time.sleep(4)
            self._self.bottom.timer.Start(int('5000'))
            self.pausa.Enable()
            self.fim_inicio.SetLabel('FIM')
            self.Bind(wx.EVT_BUTTON, self.FIM, self.fim_inicio)

            #--------------------------------------------------
            def worker1(self):
                global condition
                global conditionEnsaio
                global Fase
                global X
                global Y
                global mult

                if Fase == 'CONDICIONAMENTO':
                    while True:
                        try:
                            valorGolpe = int(self._self.bottom.GolpeAtual.GetValue())
                            if valorGolpe == 500:
                                time.sleep(4)
                                con.modeI()
                                self.pausa.Disable()
                                self._ciclo = self._self.bottom._ciclo + 1
                                self._self.bottom._ciclo = self._ciclo
                                conditionEnsaio = False
                                valorGolpe = 0
                                self._self.bottom.timer.Stop()
                                X = np.array([])
                                Y = np.array([])
                                mult = 0
                                self.draww()
                                self.pausa.Disable()
                                evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self._self.bottom.condic.GetId())
                                wx.PostEvent(self._self.bottom.condic, evt)
                                break
                        except:
                            pass

                if Fase == 'MR':
                    while True:
                        try:
                            valorGolpe = int(self._self.bottom.GolpeAtual.GetValue())
                            if valorGolpe == 10:
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
                                evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self._self.bottom.mr.GetId())
                                wx.PostEvent(self._self.bottom.mr, evt)
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
                con.modeF()
                self.avanca.Disable()
                self.continua.Disable()

                conditionEnsaio = False
                self._self.bottom.timer.Stop()
                X = np.array([])
                Y = np.array([])
                mult = 0
                self.draww()

            if Fase == 'CONDICIONAMENTO':
                self._self.bottom._ciclo = 0
                self._self.bottom.mr.Enable()
                self.fim_inicio.SetLabel('INICIO')
                self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)
                self._self.bottom.pressao_zero(VETOR_COND[self._ciclo][1])
                con.modeI()

            if Fase == 'MR':
                con.modeI()
                self._self.bottom.pressao_zero(VETOR_MR[self._ciclo][1])
                dlg3 = dialogoDinamico(3, "EDP 134/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatório de extração são gerados na tela inicial.", "FIM!", "", None)
                dlg3.ShowModal()

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
            self.axes.set_xlim(mult*5-5, mult*5)
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

            self.qTensoes = wx.Button(self, -1, 'Q. Tensões')
            self.Bind(wx.EVT_BUTTON, self.QT, self.qTensoes)
            self.condic = wx.Button(self, -1, 'CONDIC.')
            self.Bind(wx.EVT_BUTTON, self.CONDIC, self.condic)
            self.mr = wx.Button(self, -1, 'M. R.')
            self.Bind(wx.EVT_BUTTON, self.MR, self.mr)
            self.LTeste = wx.Button(self, -1, "L. TESTE", size = wx.DefaultSize)
            self.Bind(wx.EVT_BUTTON, self.LTESTE, self.LTeste)
            self.LZero = wx.Button(self, -1, "L. ZERO", size = wx.DefaultSize)
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

            texto1 = wx.StaticText(self, label = "EIXO Y", style = wx.ALIGN_CENTRE)
            #texto2 = wx.StaticText(self, label = "EIXO Y (mm)", style = wx.ALIGN_CENTRE)
            texto3 = wx.StaticText(self, label = "σ3 - Tensão confinante (MPa)", style = wx.ALIGN_CENTRE)
            texto4 = wx.StaticText(self, label = "σd - Tensão desvio (MPa)", style = wx.ALIGN_CENTRE)
            texto5 = wx.StaticText(self, label = "Y1 (V)", style = wx.ALIGN_CENTER)
            texto6 = wx.StaticText(self, label = "Y2 (V)", style = wx.ALIGN_CENTER)
            texto7 = wx.StaticText(self, label = "Y1 (mm)", style = wx.ALIGN_CENTER)
            texto8 = wx.StaticText(self, label = "Y2 (mm)", style = wx.ALIGN_CENTER)
            #texto9 = wx.StaticText(self, label = "Def. Elástica", style = wx.ALIGN_CENTER)
            #texto10 = wx.StaticText(self, label = "Def. Plástica", style = wx.ALIGN_CENTER)
            #texto11 = wx.StaticText(self, label = "Def. P. Cond.", style = wx.ALIGN_CENTER)
            #texto12 = wx.StaticText(self, label = "Def. P. Acum.", style = wx.ALIGN_CENTER)
            texto13 = wx.StaticText(self, label = "Altura Final (mm)", style = wx.ALIGN_LEFT)
            texto14 = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
            texto15 = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
            texto16 = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
            texto17 = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
            texto18 = wx.StaticText(self, label = "Altura (mm)", style = wx.ALIGN_LEFT)
            texto19 = wx.StaticText(self, label = "Diâmetro (mm)", style = wx.ALIGN_LEFT)
            #texto20 = wx.StaticText(self, label = "Def. Crítica (mm)", style = wx.ALIGN_LEFT)
            texto21 = wx.StaticText(self, label = "CICLO", style = wx.ALIGN_CENTER)
            texto22 = wx.StaticText(self, label = "Nº de Golpes", style = wx.ALIGN_CENTER)
            texto23 = wx.StaticText(self, label = "Freq. (Hz)", style = wx.ALIGN_CENTER)
            texto24 = wx.StaticText(self, label = "Golpe Atual", style = wx.ALIGN_CENTER)

            texto1.SetFont(FontTitle)
            #texto2.SetFont(FontTitle)
            texto3.SetFont(FontTitle)
            texto4.SetFont(FontTitle)
            texto5.SetFont(Fonttext)
            texto6.SetFont(Fonttext)
            texto7.SetFont(Fonttext)
            texto8.SetFont(Fonttext)
            #texto9.SetFont(Fonttext)
            #texto10.SetFont(Fonttext)
            #texto11.SetFont(Fonttext)
            #texto12.SetFont(Fonttext)
            texto13.SetFont(FontTitle)
            texto14.SetFont(Fonttext)
            texto15.SetFont(Fonttext)
            texto16.SetFont(Fonttext)
            texto17.SetFont(Fonttext)
            texto18.SetFont(Fonttext)
            texto19.SetFont(Fonttext)
            #texto20.SetFont(FontTitle)
            texto21.SetFont(FontTitle)
            texto22.SetFont(Fonttext)
            texto23.SetFont(Fonttext)
            texto24.SetFont(Fonttext)

            texto1.SetBackgroundColour(wx.Colour(215,215,215))
            #texto2.SetBackgroundColour(wx.Colour(215,215,215))
            texto3.SetBackgroundColour(wx.Colour(215,215,215))
            texto4.SetBackgroundColour(wx.Colour(215,215,215))
            texto5.SetBackgroundColour(wx.Colour(215,215,215))
            texto6.SetBackgroundColour(wx.Colour(215,215,215))
            texto7.SetBackgroundColour(wx.Colour(215,215,215))
            texto8.SetBackgroundColour(wx.Colour(215,215,215))
            #texto9.SetBackgroundColour(wx.Colour(215,215,215))
            #texto10.SetBackgroundColour(wx.Colour(215,215,215))
            #texto11.SetBackgroundColour(wx.Colour(215,215,215))
            #texto12.SetBackgroundColour(wx.Colour(215,215,215))
            texto13.SetBackgroundColour(wx.Colour(215,215,215))
            texto14.SetBackgroundColour(wx.Colour(215,215,215))
            texto15.SetBackgroundColour(wx.Colour(215,215,215))
            texto16.SetBackgroundColour(wx.Colour(215,215,215))
            texto17.SetBackgroundColour(wx.Colour(215,215,215))
            texto18.SetBackgroundColour(wx.Colour(215,215,215))
            texto19.SetBackgroundColour(wx.Colour(215,215,215))
            #texto20.SetBackgroundColour(wx.Colour(215,215,215))
            texto21.SetBackgroundColour(wx.Colour(215,215,215))
            texto22.SetBackgroundColour(wx.Colour(215,215,215))
            texto23.SetBackgroundColour(wx.Colour(215,215,215))
            texto24.SetBackgroundColour(wx.Colour(215,215,215))

            self.y1V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y2V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y1mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.y2mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            #self.defElastica = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            #self.defPlastica = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            #self.defPCond = wx.TextCtrl(self, -1, '', size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            #self.defPAcum = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.AlturaFinal = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.PCreal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.PCalvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.SigmaReal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.SigmaAlvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.AlturaMM = wx.TextCtrl(self, -1, '200,00', size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.DiametroMM = wx.TextCtrl(self, -1, '100,0', size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            #self.DefCritica = wx.TextCtrl(self, -1, wx.EmptyString, size = (80, 41.5), style = wx.TE_READONLY | wx.TE_CENTER)
            self.Ciclo = wx.TextCtrl(self, -1, '1', size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.NGolpes = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.GolpeAtual = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTRE)
            self.freq = wx.ComboBox(self, -1, frequencias[0], choices = frequencias, size = (50, 35), style = wx.CB_READONLY)
            self.ensaioAuto = wx.CheckBox(self, -1, 'Ensaio automático', (20,0), (260,-1), style = wx.ALIGN_LEFT)

            self.y1V.Disable()
            self.y2V.Disable()
            self.y1mm.Disable()
            self.y2mm.Disable()
            #self.defElastica.Disable()
            #self.defPlastica.Disable()
            #self.defPCond.Disable()
            #self.defPAcum.Disable()
            self.AlturaFinal.Disable()
            self.PCreal.Disable()
            self.PCalvo.Disable()
            self.SigmaReal.Disable()
            self.SigmaAlvo.Disable()
            self.AlturaMM.Disable()
            self.DiametroMM.Disable()
            #self.DefCritica.Disable()
            self.Ciclo.Disable()
            self.NGolpes.Disable()
            self.GolpeAtual.Disable()
            self.freq.Disable()

            self.y1V.SetFont(Fonttext)
            self.y2V.SetFont(Fonttext)
            self.y1mm.SetFont(Fonttext)
            self.y2mm.SetFont(Fonttext)
            #self.defElastica.SetFont(Fonttext)
            #self.defPlastica.SetFont(Fonttext)
            #self.defPCond.SetFont(Fonttext)
            #self.defPAcum.SetFont(Fonttext)
            self.AlturaFinal.SetFont(Fonttext)
            self.PCreal.SetFont(Fonttext)
            self.PCalvo.SetFont(Fonttext)
            self.SigmaReal.SetFont(Fonttext)
            self.SigmaAlvo.SetFont(Fonttext)
            self.AlturaMM.SetFont(Fonttext)
            self.DiametroMM.SetFont(Fonttext)
            #self.DefCritica.SetFont(Fonttext)
            self.Ciclo.SetFont(Fonttext)
            self.NGolpes.SetFont(Fonttext)
            self.GolpeAtual.SetFont(Fonttext)
            self.freq.SetFont(Fonttext)

            self.y1V.SetForegroundColour((119,118,114))
            self.y2V.SetForegroundColour((119,118,114))
            self.y1mm.SetForegroundColour((119,118,114))
            self.y2mm.SetForegroundColour((119,118,114))
            #self.defElastica.SetForegroundColour((119,118,114))
            #self.defPlastica.SetForegroundColour((119,118,114))
            #self.defPCond.SetForegroundColour((119,118,114))
            #self.defPAcum.SetForegroundColour((119,118,114))
            self.AlturaFinal.SetForegroundColour((119,118,114))
            self.PCreal.SetForegroundColour((119,118,114))
            self.PCalvo.SetForegroundColour((119,118,114))
            self.SigmaReal.SetForegroundColour((119,118,114))
            self.SigmaAlvo.SetForegroundColour((119,118,114))
            self.AlturaMM.SetForegroundColour((119,118,114))
            self.DiametroMM.SetForegroundColour((119,118,114))
            #self.DefCritica.SetForegroundColour((119,118,114))
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
            #self.v15_sizer = wx.BoxSizer(wx.VERTICAL)
            #self.h13_sizer = wx.BoxSizer(wx.HORIZONTAL)
            #self.h14_sizer = wx.BoxSizer(wx.HORIZONTAL)
            #self.h15_sizer = wx.BoxSizer(wx.HORIZONTAL)
            #self.h16_sizer = wx.BoxSizer(wx.HORIZONTAL)
            #self.h17_sizer = wx.BoxSizer(wx.HORIZONTAL)
            #self.h18_sizer = wx.BoxSizer(wx.HORIZONTAL)

            #self.h13_sizer.Add(texto13, 7, wx.ALIGN_CENTER_VERTICAL)
            #self.h13_sizer.AddStretchSpacer(1)
            #self.h13_sizer.Add(self.AlturaFinal, 5, wx.CENTER)

            #self.h14_sizer.Add(texto12, 7, wx.ALIGN_CENTER_VERTICAL)
            #self.h14_sizer.AddStretchSpacer(1)
            #self.h14_sizer.Add(self.defPAcum, 5, wx.CENTER)

            #self.h15_sizer.Add(texto11, 7, wx.ALIGN_CENTER_VERTICAL)
            #self.h15_sizer.AddStretchSpacer(1)
            #self.h15_sizer.Add(self.defPCond, 5, wx.CENTER)

            #self.h16_sizer.Add(texto10, 7, wx.ALIGN_CENTER_VERTICAL)
            #self.h16_sizer.AddStretchSpacer(1)
            #self.h16_sizer.Add(self.defPlastica, 5, wx.CENTER)

            #self.h17_sizer.Add(texto9, 7, wx.ALIGN_CENTER_VERTICAL)
            #self.h17_sizer.AddStretchSpacer(1)
            #self.h17_sizer.Add(self.defElastica, 5, wx.CENTER)

            #self.v15_sizer.Add(texto2, 3, wx.ALL | wx.EXPAND  | wx.CENTER)
            #self.v15_sizer.Add(self.h17_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            #self.v15_sizer.AddStretchSpacer(1)
            #self.v15_sizer.Add(self.h16_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            #self.v15_sizer.AddStretchSpacer(1)
            #self.v15_sizer.Add(self.h15_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            #self.v15_sizer.AddStretchSpacer(1)
            #self.v15_sizer.Add(self.h14_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            #self.v15_sizer.AddStretchSpacer(1)
            #self.v15_sizer.Add(self.h13_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)

            #self.h18_sizer.Add(self.v15_sizer, 1, wx.CENTER)
            #staticboxSizer2.Add(self.h18_sizer, 0, wx.ALL | wx.EXPAND  | wx.CENTER, 10)

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
            #self.h1_sizer.Add(staticboxSizer2, 1, wx.EXPAND | wx.ALL, 3)
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
        '''Função responsável em realizar a CONECÇÃO'''
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
                    global xz1
                    global yz1
                    global yt1
                    global yz2
                    global yt2
                    global pc1
                    global pg1
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
                    x_counter = 0
                    valores = [0,0,0,0,0,0,0,0,0]
                    while True:
                        while condition == True:
                            valores = con.ColetaI(valores)
                            if cont1 >= 10:
                                self.y1mm.Clear()
                                self.y2mm.Clear()
                                self.y1V.Clear()
                                self.y2V.Clear()
                                self.PCreal.Clear()
                                self.SigmaReal.Clear()
                                self.valorLeitura0 = valores[1]
                                self.valorLeitura1 = valores[2]
                                self.y1mm.AppendText(str(round((valores[1]-self.leituraZerob1), 4)))
                                self.y2mm.AppendText(str(round((valores[2]-self.leituraZerob2), 4)))
                                self.y1V.AppendText(str(round((valores[3]), 2)))
                                self.y2V.AppendText(str(round((valores[4]), 2)))
                                self.PCreal.AppendText(str(round((valores[5]), 3)))
                                self.SigmaReal.AppendText(str(round(valores[6]-valores[5], 3)))
                                if cont1 == 10:
                                    cont1 = 0
                            cont1 = cont1 + 1

                            y1 = valores[1]-self.leituraZerob1
                            y2 = valores[2]-self.leituraZerob2  #alterar essa linha quando usar os 2 sensores
                            ymedio = (y1 + y2)/2 + H0 #A média + H0 que é o ponto de referência inicial

                            #print ymedio
                            '''if conditionEnsaio == True:'''
                            if conditionEnsaio == True and valores[0] > 0:
                                X = np.append(X, valores[0])
                                Y = np.append(Y, ymedio)
                                x_counter = len(X)
                                if x_counter >= 1000: #antes era 1500
                                    X = np.delete(X, 0, 0)
                                    Y = np.delete(Y, 0, 0)
                                if Fase == 'CONDICIONAMENTO' and Pausa == False:
                                    if valores[0] == 0.01:
                                        REFERENCIA1 = y1+H0
                                        REFERENCIA2 = y2+H0
                                if Fase == 'MR' and Pausa == False:
                                    if valores[0] == 0.01:
                                        REFERENCIA1 = y1+H0
                                        REFERENCIA2 = y2+H0
                                        '''discrepancia = 5'''

                                    '''if valores[0] > 4 and valores[0] < 4.2:
                                        if valores[0] == 4.01:
                                            amplitudeMax4 = ymedio
                                        if ymedio > amplitudeMax4:
                                            amplitudeMax4 = ymedio
                                            intervaloSup1 = amplitudeMax4 + 0.05*amplitudeMax4
                                            intervaloInf1 = amplidudeMax4 - 0.05*amplitudeMax4

                                    if valores[0] > 5 and valores[0] < 5.2:
                                        if valores[0] == 5.01:
                                            amplitudeMax5 = ymedio
                                        if ymedio > amplitudeMax5:
                                            amplitudeMax5 = ymedio
                                            intervaloSup2 = amplitudeMax5 + 0.05*amplitudeMax5
                                            intervaloInf2 = amplidudeMax5 - 0.05*amplitudeMax5'''

                                    if int(valores[0]) > 4 and int(valores[0]) <= 10:
                                        xz1.append(valores[0])
                                        yz1.append(y1+H0)
                                        yz2.append(y2+H0)
                                        pc1.append(valores[5])
                                        pg1.append(valores[6]-valores[5])
                                        yt1.append(valores[3])
                                        yt2.append(valores[4])

                                if cont >= 8:
                                    self.AlturaFinal.Clear()
                                    self.AlturaFinal.AppendText(str(round(H-(ymedio-REFERENCIA1/2-REFERENCIA2/2), 2)))
                                '''if cont >= 8:
                                    self.defElastica.Clear()
                                    self.defPlastica.Clear()
                                    self.defPAcum.Clear()
                                    self.AlturaFinal.Clear()
                                    self.DefCritica.Clear()
                                    self.defElastica.AppendText(str(round((valores[8]), 3)))
                                    self.defPlastica.AppendText(str(round((valores[9]), 3)))
                                    self.defPAcum.AppendText(str(round((valores[10]), 3)))
                                    self.AlturaFinal.AppendText(str(round(H-(valores[0]-self.leituraZerob1), 2)))
                                    self.DefCritica.AppendText(str(round((valores[10]), 3)))
                                    if cont == 10:
                                        cont = 0
                                cont += 1'''

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

    #--------------------------------------------------
        '''Função responsável em mostrar o quadro dinâmico de tensões'''
        def QT(self, event):
            print '\nBottomPanel - QT'
            dlg = quadro().ShowModal()

    #--------------------------------------------------
        '''Função responsável em realizar o CONDICIONAMENTO'''
        def CONDIC(self, event):
            print '\nBottomPanel - CONDIC'
            global condition
            global Fase
            global xz1
            global yz1
            global yt1
            global yz2
            global yt2
            global pc1
            global pg1
            global REFERENCIA1
            global REFERENCIA2
            Fase = 'CONDICIONAMENTO'
            self.erro = False

            if subleito == True:
                ciclo = 1
            else:
                ciclo = 3

            if self._ciclo < ciclo:
                print '\nCICLO.COND='+str(self._ciclo+1)+'\n'

            if self._ciclo > 0 and subleito == True:
                bancodedados.saveReferencia(idt+"COND-"+str(self._ciclo), REFERENCIA1, REFERENCIA2)

            if self._ciclo < ciclo:
                self.LZero.Disable()
                self.freq.Disable()
                self.mr.Disable()
                self.condic.Disable()
                self.PCalvo.Clear()
                self.SigmaAlvo.Clear()
                self.Ciclo.Clear()
                self.NGolpes.Clear()
                self.GolpeAtual.Clear()
                self.PCalvo.AppendText(str(VETOR_COND[self._ciclo][0])+'0')
                self.SigmaAlvo.AppendText(str(VETOR_COND[self._ciclo][1]-VETOR_COND[self._ciclo][0])+'0')
                self.NGolpes.AppendText(str(500))
                self.Ciclo.AppendText('C-'+str(self._ciclo+1))
                self.GolpeAtual.AppendText(str(0))

            if self._ciclo == 0:
                info = "EDP 134/2018ME"
                titulo = "Preparação da câmara triaxial."
                message1 = "Verifique se está tudo certo!"
                message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                dlg.ShowModal()

            if self._ciclo == 0:
                self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                self.graph.fim_inicio.Enable()
                if subleito == False:
                    self.graph.avanca.Enable()

            if self._ciclo > 0 and self._ciclo < ciclo and self.Automatico == False:
                self.graph.fim_inicio.SetLabel('INICIO')
                self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                self.graph.fim_inicio.Enable()
                self.graph.avanca.Enable()

            if self._ciclo > 0 and self._ciclo < ciclo and self.Automatico == True:
                self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                wx.PostEvent(self.graph.fim_inicio, evt)

            if self._ciclo >= ciclo and self.Automatico == False and self.erro == False:
                self._ciclo = 0
                self.mr.Enable()
                self.condic.Disable()
                self.graph.fim_inicio.SetLabel('INICIO')
                #self.pressao_zero()

            if self._ciclo >= ciclo and self.Automatico == True and self.erro == False:
                self._ciclo = 0
                self.condic.Disable()
                self.graph.fim_inicio.SetLabel('INICIO')
                evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.mr.GetId())
                wx.PostEvent(self.mr, evt)

    #--------------------------------------------------
        '''Função responsável em realizar o MODULO RESILIENTE'''
        def MR(self, event):
            print '\nBottomPanel - MR'
            global condition
            global Fase
            global xz1
            global yz1
            global yt1
            global yz2
            global yt2
            global pc1
            global pg1
            global REFERENCIA1
            global REFERENCIA2
            Fase = 'MR'
            self.erro = False

            if subleito == True:
                ciclo = 12
            else:
                ciclo = 18

            if self._ciclo < ciclo:
                print '\nCICLO.MR='+str(self._ciclo+1)+'\n'

            if self._ciclo > 0:
                threadConection = SaveThread.SaveThread(idt+"MR-"+str(self._ciclo), xz1, yz1, yt1, yz2, yt2, pc1, pg1, REFERENCIA1, REFERENCIA2)
                dlgC2 = My.MyProgressDialog(len(xz1)-2)
                dlgC2.ShowModal()
                xz1 = []
                yz1 = []
                yt1 = []
                yz2 = []
                yt2 = []
                pc1 = []
                pg1 = []

            if self._ciclo < ciclo:
                self.LZero.Disable()
                self.freq.Disable()
                self.mr.Disable()
                self.condic.Disable()
                self.PCalvo.Clear()
                self.SigmaAlvo.Clear()
                self.Ciclo.Clear()
                self.NGolpes.Clear()
                self.GolpeAtual.Clear()
                self.PCalvo.AppendText(str(VETOR_MR[self._ciclo][0])+'0')
                self.SigmaAlvo.AppendText(str(VETOR_MR[self._ciclo][1]-VETOR_MR[self._ciclo][0])+'0')
                self.NGolpes.AppendText(str(10))
                self.Ciclo.AppendText('MR-'+str(self._ciclo+1))
                self.GolpeAtual.AppendText(str(0))

            if self._ciclo == 0 and self.Automatico == False:
                info = "EDP 134/2018ME"
                titulo = "Preparação da câmara triaxial."
                message1 = "Verifique se está tudo certo!"
                message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                dlg.ShowModal()

            if self._ciclo == 0:
                self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                self.graph.fim_inicio.Enable()
                self.graph.avanca.Enable()

            if self._ciclo >= 0 and self._ciclo < ciclo and self.Automatico == False:
                self.graph.fim_inicio.SetLabel('INICIO')
                self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                self.graph.fim_inicio.Enable()
                self.graph.avanca.Enable()

            if self._ciclo >= 0 and self._ciclo < ciclo and self.Automatico == True:
                self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                wx.PostEvent(self.graph.fim_inicio, evt)

            if self._ciclo >= ciclo and self.erro == False:
                self.mr.Disable()
                self.pressao_zero(VETOR_MR[self._ciclo-1][1])
                self._ciclo = 0
                dlg3 = dialogoDinamico(3, "EDP 134/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatório de extração são gerados na tela inicial.", "FIM!", "", None)
                dlg3.ShowModal()

    #--------------------------------------------------
        '''Função responsável em zera a pressão do sistema'''
        def pressao_zero(self, p2Sen):
            print '\nBottomPanel - pressao_zero'
            global condition
            condition = False
            threadConection = DinamicaThread.DinamicaThreadZero(0.005, p2Sen) #0.005 é o menor valor de pressão admissível para valvula dinamica
            dlgC1 = My.MyProgressDialog(4)
            dlgC1.ShowModal()
            time.sleep(1)
            threadConection = MotorThread.MotorThreadZero(0.030)  #0.030 é o menor valor de pressão admissível para SI do motor de passos
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
class TelaRealizacaoEnsaioDNIT134(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, parent = None, title = 'EDP - DNIT 134/2018ME - Tela_Ensaio_Beta', size = (1000,750), style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

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
            info = "EDP 134/2018ME"
            titulo = "Ajuste o Zero dos LVDTs"
            message1 = "Com o valor entre:"
            message2 = "2.5 e 3.0 Volts"
            message3 = "realizando a L. TESTE"
            dlg = dialogoDinamico(1, info, titulo, message1, message2, message3, None)
            dlg.ShowModal()

if __name__ == "__main__":
	app = wx.App()
	frame = TelaRealizacaoEnsaioDNIT134(None)
	frame.ShowModal()
	app.MainLoop()