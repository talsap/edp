# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import time
import threading
import matplotlib
import numpy as np
import bancodedados
import bdConfiguration
import back.connection as con
import matplotlib.pyplot as plt
import back.MyProgressDialog as My
import back.SaveThread as SaveThread
import back.MotorThread as MotorThread
import back.DinamicaThread as DinamicaThread
import back.ConexaoThread as ConexaoThread
import back.HexForRGB as HexRGB
import bdPreferences
from drawnow import *
from front.quadrotensoes import quadro
from front.dialogoDinamico import dialogoDinamico
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

'''Frequencias para o ensaio'''
frequencias = ['1']

#########################################################################
'''Painel Superior'''
class TopPanel(wx.Panel):
        def __init__(self, parent, _self):
            wx.Panel.__init__(self, parent = parent)
            global colorLineGrafic
            
            colors = bdPreferences.ListColors()
            colorCard = colors[0]
            colorTextCtrl = colors[1]
            colorBackground = colors[2]
            colorLineGrafic = colors[3]
            colorBackgroundGrafic = colors[4]

            self._self = _self
            self.SetBackgroundColour(colorBackground)

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
            rect.set_facecolor(colorBackgroundGrafic)

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
            self.DINAMICA2_ANTERIOR = 0
            self.DINAMICA1_ANTERIOR = 0
            self.AVANCA = False

    #--------------------------------------------------
        '''Função AVANCA'''
        def AVANCA(self, event):
            print '\nTopPanel - AVANCA'
            global Fase
            global X
            global Y
            global mult

            '''Diálogo se deseja realmente avancar um FASE'''
            dlg = wx.MessageDialog(None, 'Deseja realmente avancar um FASE?', 'EDP', wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
            result = dlg.ShowModal()

            if result == wx.ID_YES:
                dlg.Destroy()
                con.modeFIM()
                self.fim_inicio.Enable()
                self.avanca.Enable()
                self.continua.Disable()
                self.fim_inicio.Disable()
                self.fim_inicio.SetLabel('INICIO')
                self._self.bottom.GolpeAtual.Clear()
                self._self.bottom.GolpeAtual.AppendText(str(0))

                self._fase = self._self.bottom._fase + 1
                self._self.bottom._fase = self._fase

                self._self.bottom.timer.Stop()
                X = np.array([])
                Y = np.array([])
                mult = 0
                self.draww()
                self._self.bottom.PCalvo.Clear()
                self._self.bottom.SigmaAlvo.Clear()
                self._self.bottom.fase.Clear()
                self.AVANCA = True

                if Fase == 'CONDICIONAMENTO':
                    print '\nAVANCA.FASE.COND='+str(self._fase+1)+'\n'
                    self._self.bottom.PCalvo.AppendText("%.3f" % VETOR_COND[self._fase][0])
                    self._self.bottom.SigmaAlvo.AppendText("%.3f" % (VETOR_COND[self._fase][1]-VETOR_COND[self._fase][0]))
                    self._self.bottom.fase.AppendText(str(self._fase+1))

                    if(self._fase < 2):
                        self.avanca.Enable()
                    else:
                        self.avanca.Disable()

                if Fase == 'MR':
                    print '\nAVANCA.FASE.MR='+str(self._fase+1)+'\n'
                    self._self.bottom.PCalvo.AppendText("%.3f" % VETOR_MR[self._fase][0])
                    self._self.bottom.SigmaAlvo.AppendText("%.3f" % (VETOR_MR[self._fase][1]-VETOR_MR[self._fase][0]))
                    self._self.bottom.fase.AppendText(str(self._fase+1))

                    if(self._fase < 17):
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
            self._fase = self._self.bottom._fase
            #time.sleep(1)

            if Fase == 'CONDICIONAMENTO':
                condition = False
                if self._fase > 0:
                    if VETOR_COND[self._fase][1] != VETOR_COND[self._fase - 1][1] and self.AVANCA == False:
                        threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_COND[self._fase][1], VETOR_COND[self._fase-1][1])
                        dlgC1 = My.MyProgressDialog(3)
                        dlgC1.ShowModal()
                        self.DINAMICA2_ANTERIOR = VETOR_COND[self._fase][1]
                        self.DINAMICA1_ANTERIOR = VETOR_COND[self._fase][0]
                        time.sleep(1)

                    if VETOR_COND[self._fase][0] != VETOR_COND[self._fase - 1][0]:
                        #threadConection = MotorThread.MotorThread(VETOR_COND[self._fase][0])
                        threadConection = DinamicaThread.DinamicaThreadOne(VETOR_COND[self._fase][0], self.DINAMICA1_ANTERIOR)
                        dlgC2 = My.MyProgressDialog(3)
                        dlgC2.ShowModal()

                    if self.AVANCA == True:
                        threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_COND[self._fase][1], self.DINAMICA2_ANTERIOR)
                        dlgC1 = My.MyProgressDialog(3)
                        dlgC1.ShowModal()
                        self.DINAMICA2_ANTERIOR = VETOR_COND[self._fase][1]
                        time.sleep(.5)
                        if VETOR_COND[self._fase][0] != self.DINAMICA1_ANTERIOR:
                            threadConection = DinamicaThread.DinamicaThreadOne(VETOR_COND[self._fase][0], self.DINAMICA1_ANTERIOR)
                            dlgC2 = My.MyProgressDialog(3)
                            dlgC2.ShowModal()
                            self.DINAMICA1_ANTERIOR = VETOR_COND[self._fase][0]
                        self.AVANCA = False
                else:
                    threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_COND[self._fase][1], 0)
                    dlgC1 = My.MyProgressDialog(3)
                    dlgC1.ShowModal()
                    time.sleep(.5)
                    #threadConection = MotorThread.MotorThread(VETOR_COND[self._fase][0])
                    threadConection = DinamicaThread.DinamicaThreadOne(VETOR_COND[self._fase][0], 0)
                    dlgC2 = My.MyProgressDialog(3)
                    dlgC2.ShowModal()

                if threadConection.ret() == False:
                    dlgC3 = dialogoDinamico(3, "EDP 134/2018ME", "CONDICIONAMENTO", "Ocorreu algum problema com o ajuste da pressão!", "Verifique o motor de passos!", "", None)
                    dlgC3.ShowModal()
                    self._self.bottom.erro = True
                    if self._fase == 0:
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
                if self._fase > 0:
                    if VETOR_MR[self._fase][1] != VETOR_MR[self._fase - 1][1] and self.AVANCA == False:
                        threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_MR[self._fase][1], VETOR_MR[self._fase-1][1])
                        dlgC1 = My.MyProgressDialog(3)
                        dlgC1.ShowModal()
                        self.DINAMICA2_ANTERIOR = VETOR_MR[self._fase][1]
                        time.sleep(1)

                    if VETOR_MR[self._fase][0] != VETOR_MR[self._fase - 1][0] and self.AVANCA == False:
                        #threadConection = MotorThread.MotorThread(VETOR_MR[self._fase][0])
                        threadConection = DinamicaThread.DinamicaThreadOne(VETOR_MR[self._fase][0], self.DINAMICA1_ANTERIOR)
                        dlgC2 = My.MyProgressDialog(3)
                        dlgC2.ShowModal()

                    if self.AVANCA == True:
                        threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_MR[self._fase][1], self.DINAMICA2_ANTERIOR)
                        dlgC1 = My.MyProgressDialog(3)
                        dlgC1.ShowModal()
                        self.DINAMICA2_ANTERIOR = VETOR_MR[self._fase][1]
                        time.sleep(.5)
                        if VETOR_MR[self._fase][0] != self.DINAMICA1_ANTERIOR:
                            threadConection = DinamicaThread.DinamicaThreadOne(VETOR_MR[self._fase][0], self.DINAMICA1_ANTERIOR)
                            dlgC2 = My.MyProgressDialog(3)
                            dlgC2.ShowModal()
                            self.DINAMICA1_ANTERIOR = VETOR_MR[self._fase][0]
                        self.AVANCA = False
                else:
                    threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_MR[self._fase][1], 0)
                    dlgC1 = My.MyProgressDialog(3)
                    dlgC1.ShowModal()
                    time.sleep(.5)
                    #threadConection = MotorThread.MotorThread(VETOR_MR[self._fase][0])
                    threadConection = DinamicaThread.DinamicaThreadOne(VETOR_MR[self._fase][0], 0)
                    dlgC2 = My.MyProgressDialog(3)
                    dlgC2.ShowModal()

                if threadConection.ret() == False:
                    dlgC3 = dialogoDinamico(3, "EDP DNIT134/2018ME", "MÓDULO DE RESILIÊNCIA", "Ocorreu algum problema com o ajuste da pressão!", "Verifique o motor de passos!", "", None)
                    dlgC3.ShowModal()
                    self._self.bottom.erro = True
                    if self._fase == 0:
                        self._self.bottom.mr.Enable()
                time.sleep(.5)

                if self._self.bottom.Automatico == False:
                    condition = True
                    dlg3 = dialogoDinamico(3, "EDP DNIT134/2018ME", "MÓDULO DE RESILIÊNCIA", "Tudo pronto!", "Aperte INICIO.", "", None)
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
            time.sleep(2)
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
                global glpCOND
                global ntglp
                global H
                global DPmaxACUM
                global REFERENCIA_MEDIA

                if Fase == 'CONDICIONAMENTO':
                    while True:
                        try:
                            valorGolpe = int(self._self.bottom.GolpeAtual.GetValue())
                            if valorGolpe == int(glpCOND):
                                time.sleep(4)
                                con.modeI()
                                self.pausa.Disable()
                                self._fase = self._self.bottom._fase + 1
                                self._self.bottom._fase = self._fase
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
                            alturaFinalCP = float(self._self.bottom.AlturaFinal.GetValue())
                            if valorGolpe == int(ntglp-1) or (H - REFERENCIA_MEDIA) < DPmaxACUM or alturaFinalCP < (DPmaxACUM-5):
                                time.sleep(4)
                                con.modeI()
                                self.pausa.Disable()
                                self._fase = self._self.bottom._fase + 1
                                self._self.bottom._fase = self._fase
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
                con.modeFIM()
                self.avanca.Disable()
                self.continua.Disable()

                conditionEnsaio = False
                self._self.bottom.timer.Stop()
                X = np.array([])
                Y = np.array([])
                mult = 0
                self.draww()

                if Fase == 'CONDICIONAMENTO':
                    self._self.bottom._fase = 0
                    self._self.bottom.mr.Enable()
                    self.fim_inicio.SetLabel('INICIO')
                    self.Bind(wx.EVT_BUTTON, self.INICIO, self.fim_inicio)
                    self._self.bottom.pressao_zero(VETOR_COND[self._fase][0], VETOR_COND[self._fase][1])
                    con.modeI()

                if Fase == 'MR':
                    con.modeI()
                    self._self.bottom.pressao_zero(VETOR_MR[self._fase][0], VETOR_MR[self._fase][1])
                    con.modeI()
                    bancodedados.data_final_Update_idt(idt)
                    dlg3 = dialogoDinamico(3, "EDP 134/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatório podem ser gerados na tela inicial.", "FIM!", "", None)
                    if dlg3.ShowModal() == wx.ID_OK:
                        time.sleep(.3)
                        con.modeStoped()
                        time.sleep(.3)
                        con.modeB()
                        time.sleep(.3)
                        con.modeD()
                        condition = False
                        time.sleep(.3)
                        self._self.Close(True)
                        self._self.Destroy()

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
            global colorLineGrafic
            self.axes.clear()
            self.axes.set_xlim(mult*5-5, mult*5)
            self.axes.set_xlabel("TEMPO (seg)")
            self.axes.set_ylabel("DESLOCAMENTO (mm)")
            self.axes.plot(X, Y, colorLineGrafic)
            self.canvas.draw()

'''Painel Inferior'''
class BottomPanel(wx.Panel):
        def __init__(self, parent, top):
            wx.Panel.__init__(self, parent = parent)

            colors = bdPreferences.ListColors()
            colorCard = colors[0]
            colorTextCtrl = colors[1]
            colorBackground = colors[2]
            colorLineGrafic = colors[3]
            colorBackgroundGrafic = colors[4]

            colorStaticBox = HexRGB.RGB(colorCard)
            colorTextBackground = HexRGB.RGB(colorCard)
            colorTextCtrl = HexRGB.RGB(colorTextCtrl)

            self.graph = top

            self.SetBackgroundColour(colorBackground)         

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

            staticbox1.SetBackgroundColour(colorStaticBox)
            staticbox2.SetBackgroundColour(colorStaticBox)
            staticbox3.SetBackgroundColour(colorStaticBox)
            staticbox4.SetBackgroundColour(colorStaticBox)
            staticbox5.SetBackgroundColour(colorStaticBox)
            staticbox6.SetBackgroundColour(colorStaticBox)

            self.qTensoes = wx.Button(self, -1, 'Q. Tensões')
            self.Bind(wx.EVT_BUTTON, self.QT, self.qTensoes)
            self.condic = wx.Button(self, -1, 'CONDIC.')
            self.Bind(wx.EVT_BUTTON, self.CONDIC, self.condic)
            self.mr = wx.Button(self, -1, 'M. R.')
            self.Bind(wx.EVT_BUTTON, self.MR, self.mr)
            self.LTeste = wx.Button(self, -1, "CONECTAR", size = wx.DefaultSize)
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
            texto21 = wx.StaticText(self, label = "FASE", style = wx.ALIGN_CENTER)
            texto22 = wx.StaticText(self, label = "Nº de CICLOs", style = wx.ALIGN_CENTER)
            texto23 = wx.StaticText(self, label = "Freq. (Hz)", style = wx.ALIGN_CENTER)
            texto24 = wx.StaticText(self, label = "CICLO Atual", style = wx.ALIGN_CENTER)

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

            texto1.SetBackgroundColour(colorTextBackground )
            #texto2.SetBackgroundColour(colorTextBackground )
            texto3.SetBackgroundColour(colorTextBackground )
            texto4.SetBackgroundColour(colorTextBackground )
            texto5.SetBackgroundColour(colorTextBackground )
            texto6.SetBackgroundColour(colorTextBackground )
            texto7.SetBackgroundColour(colorTextBackground )
            texto8.SetBackgroundColour(colorTextBackground )
            #texto9.SetBackgroundColour(colorTextBackground )
            #texto10.SetBackgroundColour(colorTextBackground )
            #texto11.SetBackgroundColour(colorTextBackground )
            #texto12.SetBackgroundColour(colorTextBackground )
            texto13.SetBackgroundColour(colorTextBackground )
            texto14.SetBackgroundColour(colorTextBackground )
            texto15.SetBackgroundColour(colorTextBackground )
            texto16.SetBackgroundColour(colorTextBackground )
            texto17.SetBackgroundColour(colorTextBackground )
            texto18.SetBackgroundColour(colorTextBackground )
            texto19.SetBackgroundColour(colorTextBackground )
            #texto20.SetBackgroundColour(colorTextBackground )
            texto21.SetBackgroundColour(colorTextBackground )
            texto22.SetBackgroundColour(colorTextBackground )
            texto23.SetBackgroundColour(colorTextBackground )
            texto24.SetBackgroundColour(colorTextBackground )

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
            self.AlturaMM = wx.TextCtrl(self, -1, str(H), size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.DiametroMM = wx.TextCtrl(self, -1, str(Diam), size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            #self.DefCritica = wx.TextCtrl(self, -1, wx.EmptyString, size = (80, 41.5), style = wx.TE_READONLY | wx.TE_CENTER)
            self.fase = wx.TextCtrl(self, -1, '1', size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTER)
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
            self.fase.Disable()
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
            self.fase.SetFont(Fonttext)
            self.NGolpes.SetFont(Fonttext)
            self.GolpeAtual.SetFont(Fonttext)
            self.freq.SetFont(Fonttext)

            self.y1V.SetForegroundColour(colorTextCtrl)
            self.y2V.SetForegroundColour(colorTextCtrl)
            self.y1mm.SetForegroundColour(colorTextCtrl)
            self.y2mm.SetForegroundColour(colorTextCtrl)
            #self.defElastica.SetForegroundColour(colorTextCtrl)
            #self.defPlastica.SetForegroundColour(colorTextCtrl)
            #self.defPCond.SetForegroundColour(colorTextCtrl)
            #self.defPAcum.SetForegroundColour(colorTextCtrl)
            self.AlturaFinal.SetForegroundColour(colorTextCtrl)
            self.PCreal.SetForegroundColour(colorTextCtrl)
            self.PCalvo.SetForegroundColour(colorTextCtrl)
            self.SigmaReal.SetForegroundColour(colorTextCtrl)
            self.SigmaAlvo.SetForegroundColour(colorTextCtrl)
            self.AlturaMM.SetForegroundColour(colorTextCtrl)
            self.DiametroMM.SetForegroundColour(colorTextCtrl)
            #self.DefCritica.SetForegroundColour(colorTextCtrl)
            self.fase.SetForegroundColour(colorTextCtrl)
            self.NGolpes.SetForegroundColour(colorTextCtrl)
            self.GolpeAtual.SetForegroundColour(colorTextCtrl)

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
            self.v6_sizer.Add(self.fase, 2, wx.ALL | wx.CENTER, 5)

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
            self._fase = 0  #condicao dos fases inicia com zero
            self.erro = False  #indica se há erros na execução
            self.Automatico = True  #inicia  com o ensaio Automatico sendo true
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
            global DISCREP

            try:
                threadConection = ConexaoThread.ConexaoThread(DISCREP)
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
                        global yyy
                        global REFERENCIA1
                        global REFERENCIA2
                        global REFERENCIA_MEDIA
                        global ntglp
                        global modeADM
                        con.modeI()  #inicia o modo de impressão de dados
                        condition = True
                        conditionEnsaio = False
                        cnt = 0
                        cont = 0
                        cont1 = 0
                        amplitudeMax = 0
                        amplitudeMaxAnterior = 0
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
                                    self.y1mm.AppendText(str(round(abs(valores[1]-self.leituraZerob1), 4)))
                                    self.y2mm.AppendText(str(round(abs(valores[2]-self.leituraZerob2), 4)))
                                    self.y1V.AppendText(str(round((valores[3]), 2)))
                                    self.y2V.AppendText(str(round((valores[4]), 2)))
                                    self.PCreal.AppendText(str(round(abs((valores[5])), 3)))
                                    self.SigmaReal.AppendText(str(round(abs(valores[6]-valores[5]), 3)))
                                    if self.leituraZerob1 == 0:
                                        self.AlturaFinal.AppendText(str(round(H, 3)))
                                    else:
                                        self.AlturaFinal.AppendText(str(round(H-abs(ymedio), 3)))
                                    if cont1 == 20:
                                        cont1 = 0
                                cont1 = cont1 + 1

                                ntglp = valores[9] #numero total de golpes
                                y1 = valores[1]-self.leituraZerob1
                                y2 = valores[2]-self.leituraZerob2  #alterar essa linha quando usar os 2 sensores
                                ymedio = (y1 + y2)/2 + H0 #A média + H0 que é o ponto de referência inicial

                                # Dados para a parte GRÁFICA #
                                if conditionEnsaio == True and valores[0] > 0:
                                    X = np.append(X, valores[0])
                                    Y = np.append(Y, ymedio)
                                    x_counter = len(X)
                                    if x_counter >= 1000: #antes era 1500
                                        X = np.delete(X, 0, 0)
                                        Y = np.delete(Y, 0, 0)

                                    # Dados do CONDICIONAMENTO #
                                    if Fase == 'CONDICIONAMENTO' and Pausa == False:
                                        if valores[0] < 5:
                                            REFERENCIA_MEDIA = ymedio
                                        if valores[0] == (ntglp - 1):
                                            REFERENCIA1 = y1+H0
                                            REFERENCIA2 = y2+H0
                                            REFERENCIA_MEDIA = ymedio
                                        if valores[0] > (ntglp - 0.80) and valores[0] < (ntglp - 0.1):
                                            REFERENCIA1 = (REFERENCIA1 + (y1+H0))/2
                                            REFERENCIA2 = (REFERENCIA2 + (y2+H0))/2
                                            REFERENCIA_MEDIA = (REFERENCIA_MEDIA + ymedio)/2

                                    # Dados do MR #
                                    if Fase == 'MR' and Pausa == False:
                                        #condicao de erro para o ensaio
                                        if int(valores[7]) == 1:
                                            print "ERRO NO ENSAIO"

                                        #PEGA OS VALORES DE REFERENCIA
                                        if valores[0] == 0.01:
                                            REFERENCIA1 = y1+H0
                                            REFERENCIA2 = y2+H0
                                            REFERENCIA_MEDIA = ymedio
                                        if valores[0] > 0.2 and valores[0] < 0.9:
                                            REFERENCIA1 = (REFERENCIA1 + (y1+H0))/2
                                            REFERENCIA2 = (REFERENCIA2 + (y2+H0))/2
                                            REFERENCIA_MEDIA = (REFERENCIA_MEDIA + ymedio)/2

                                        # DefResiliente incial de compararação (para condicao de discrepância)
                                        if valores[0] > 4 and valores[0] < 4.2:
                                            if valores[0] == 4.01:
                                                amplitudeMaxAnterior = ymedio
                                                mediaMovel = ymedio
                                            if ymedio > amplitudeMaxAnterior:
                                                amplitudeMaxAnterior = ymedio
                                        if valores[0] > 4.2 and valores[0] < 5:
                                            mediaMovel = (mediaMovel+ymedio)/2
                                            defResilienteAnterior = amplitudeMaxAnterior - mediaMovel

                                        # Condição da analise de discrepância #
                                        if valores[0] > 5:
                                            valoreS = valores[0] - int(valores[0])
                                            if valoreS > 0 and valoreS < 0.2:
                                                if valoreS == 0.01:
                                                    amplitudeMax = ymedio
                                                    mediaMovel = ymedio
                                                if ymedio > amplitudeMax:
                                                    amplitudeMax = ymedio

                                            if valoreS > 0.2 and valoreS < 0.90:
                                                mediaMovel = (mediaMovel+ymedio)/2
                                                defResiliente = amplitudeMax - mediaMovel

                                            if valoreS > 0.98:
                                                if defResiliente > defResilienteAnterior:
                                                    if defResiliente/defResilienteAnterior < DISCREP:
                                                        print defResiliente, defResilienteAnterior
                                                        if len(yyy) < 5:
                                                            yyy.append(defResiliente)
                                                if defResiliente < defResilienteAnterior:
                                                    if defResilienteAnterior/defResiliente < DISCREP:
                                                        print defResiliente, defResilienteAnterior
                                                        if len(yyy) < 5:
                                                            yyy.append(defResiliente)
                                                defResilienteAnterior = defResiliente

                                        if int(valores[0]) > 4 and int(valores[0]) <= int(valores[9]):
                                            if modeADM == True:
                                                xz1.append(valores[0])
                                                yz1.append(y1+H0)
                                                yz2.append(y2+H0)
                                                yt1.append(valores[3])
                                                yt2.append(valores[4])
                                            else:
                                                pc1.append(valores[5])
                                                pg1.append(valores[6]-valores[5])

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
            except:
                menssagError = wx.MessageDialog(self, 'ERRO AO EXECUTAR O CONECTAR', 'EDP', wx.OK|wx.ICON_EXCLAMATION)
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
            global REFERENCIA_MEDIA
            global idt
            global modeADM
            global DISCREP
            global glpCOND
            Fase = 'CONDICIONAMENTO'
            self.erro = False

            if subleito == True:
                fase = 1
            else:
                fase = 3

            if self._fase < fase:
                print '\nFASE.COND='+str(self._fase+1)+'\n'

            if self._fase > 0:
                if modeADM == True:
                    bancodedados.saveReferenciaADM(idt, str(self._fase), REFERENCIA1, REFERENCIA2)
                else:
                    print REFERENCIA_MEDIA
                    bancodedados.saveReferencia(idt, str(self._fase), REFERENCIA_MEDIA)

            if self._fase < fase:
                self.LZero.Disable()
                self.freq.Disable()
                self.mr.Disable()
                self.condic.Disable()
                self.PCalvo.Clear()
                self.SigmaAlvo.Clear()
                self.fase.Clear()
                self.NGolpes.Clear()
                self.GolpeAtual.Clear()
                self.PCalvo.AppendText("%.3f" % VETOR_COND[self._fase][0])
                self.SigmaAlvo.AppendText("%.3f" % (VETOR_COND[self._fase][1]-VETOR_COND[self._fase][0]))
                self.NGolpes.AppendText(str(glpCOND))
                self.fase.AppendText(str(self._fase+1))
                self.GolpeAtual.AppendText(str(0))

            if self._fase == 0:
                info = "EDP 134/2018ME"
                titulo = "Preparação da câmara triaxial."
                message1 = "Verifique se está tudo certo!"
                message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                if dlg.ShowModal() == wx.ID_OK:
                    freq = self.freq.GetValue()
                    bancodedados.Update_freq(idt, int(freq))
                    bancodedados.data_inicio_Update_idt(idt)
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    self.graph.fim_inicio.Enable()
                    if subleito == False:
                        self.graph.avanca.Enable()
                    if self.Automatico == True:
                        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                        wx.PostEvent(self.graph.fim_inicio, evt)

            else:
                if self._fase > 0 and self._fase < fase and self.Automatico == False:
                    self.graph.fim_inicio.SetLabel('INICIO')
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    self.graph.fim_inicio.Enable()
                    self.graph.avanca.Enable()

                if self._fase > 0 and self._fase < fase and self.Automatico == True:
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                    wx.PostEvent(self.graph.fim_inicio, evt)

                if self._fase >= fase and self.Automatico == False and self.erro == False:
                    self._fase = 0
                    self.mr.Enable()
                    self.condic.Disable()
                    self.graph.fim_inicio.SetLabel('INICIO')

                if self._fase >= fase and self.Automatico == True and self.erro == False:
                    self._fase = 0
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
            global yyy
            global REFERENCIA1
            global REFERENCIA2
            global REFERENCIA_MEDIA
            global idt
            global modeADM
            global DISCREP
            global glpCOND
            global glpMR
            self.erro = False

            if subleito == True:
                fase = 12
            else:
                fase = 18

            if self._fase < fase:
                print '\nFASE.MR='+str(self._fase+1)+'\n'

            if self._fase > 0:
                if modeADM == True:
                    threadConection = SaveThread.SaveThreadADM(idt, str(self._fase), xz1, yz1, yt1, yz2, yt2, pc1, pg1, REFERENCIA1, REFERENCIA2)
                    dlgC2 = My.MyProgressDialog(len(xz1)-2)
                    dlgC2.ShowModal()
                    xz1 = []
                    yz1 = []
                    yt1 = []
                    yz2 = []
                    yt2 = []
                    pc1 = []
                    pg1 = []
                else:
                    try:
                        dr = sum(yyy)/len(yyy)
                        pc = sum(pc1)/len(pc1)
                        pg = sum(pg1)/len(pg1)
                    except:
                        dlg = dialogoDinamico(3, "EDP 134/2018ME", "SALVAMENTO", "Ocorreu algum problema com o salvamento dos dados!", "O Ensaio precisarar ser finalizado!", "", None)
                        dlg.ShowModal()
                    bancodedados.saveDNIT134(idt, str(self._fase), pc, pg, dr, REFERENCIA_MEDIA)
                    yyy = []
                    pc1 = []
                    pg1 = []

            if self._fase < fase:
                self.LZero.Disable()
                self.freq.Disable()
                self.mr.Disable()
                self.condic.Disable()
                self.PCalvo.Clear()
                self.SigmaAlvo.Clear()
                self.fase.Clear()
                self.NGolpes.Clear()
                self.GolpeAtual.Clear()
                self.PCalvo.AppendText("%.3f" % VETOR_MR[self._fase][0])
                self.SigmaAlvo.AppendText("%.3f" % (VETOR_MR[self._fase][1]-VETOR_MR[self._fase][0]))
                self.NGolpes.AppendText(str(glpMR))
                self.fase.AppendText(str(self._fase+1))
                self.GolpeAtual.AppendText(str(0))

            if Fase == '':
                info = "EDP 134/2018ME"
                titulo = "Preparação da câmara triaxial."
                message1 = "Verifique se está tudo certo!"
                message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                if dlg.ShowModal() == wx.ID_OK:
                    Fase = 'MR'
                    if self._fase == 0:
                        freq = self.freq.GetValue()
                        bancodedados.Update_freq(idt, int(freq))
                        bancodedados.data_inicio_Update_idt(idt)

                    if self._fase >= 0 and self._fase < fase and self.Automatico == False:
                        self.graph.fim_inicio.SetLabel('INICIO')
                        self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                        self.graph.fim_inicio.Enable()
                        self.graph.avanca.Enable()

                    if self._fase >= 0 and self._fase < fase and self.Automatico == True:
                        self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                        wx.PostEvent(self.graph.fim_inicio, evt)

            else:
                Fase = 'MR'
                if self._fase >= 0 and self._fase < fase and self.Automatico == False:
                    self.graph.fim_inicio.SetLabel('INICIO')
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    self.graph.fim_inicio.Enable()
                    self.graph.avanca.Enable()

                if self._fase >= 0 and self._fase < fase and self.Automatico == True:
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                    wx.PostEvent(self.graph.fim_inicio, evt)

                if self._fase >= fase and self.erro == False:
                    self.mr.Disable()
                    self.pressao_zero(VETOR_MR[self._fase-1][0], VETOR_MR[self._fase-1][1])
                    self._fase = 0
                    bancodedados.data_final_Update_idt(idt)
                    dlg3 = dialogoDinamico(3, "EDP DNIT134/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatório de extração são gerados na tela inicial.", "FIM!", "", None)
                    if dlg3.ShowModal() == wx.ID_OK:
                        time.sleep(.3)
                        con.modeStoped()
                        time.sleep(.3)
                        con.modeB()
                        time.sleep(.3)
                        con.modeD()
                        self.Close(True)

    #--------------------------------------------------
        '''Função responsável em zera a pressão do sistema'''
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
class TelaRealizacaoEnsaioDNIT134(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, identificador, tipo, diametro, altura, *args, **kwargs):
            wx.Dialog.__init__(self, parent = None, title = 'EDP - Ensaios Dinâmicos para Pavimentação - DNIT 134/2018ME - Tela Ensaio', size = (1000,750), style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Variáveis Globais'''
            global idt #identificador do ensaio
            global leituraZerob1 #leitura zero do sensor 1
            global leituraZerob2 #leitura zero do sensor 2
            global H  #Altura do corpo de prova em milímetros
            global Diam  #Diametro do corpo de prova em milímetros
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
            global yyy
            global REFERENCIA1 #referencia de ponto de partida para o sensor 1
            global REFERENCIA2 #referencia de ponto de partida para o sensor 2
            global REFERENCIA_MEDIA #referencia de ponto de partidada MÉDIA
            global Ti #valor temporal
            global Fase #valor para identificar se esta no CONDICIONAMENTO ou no MR
            global Automatico #idica se o ensaio será automático ou não
            global Pausa #indica se o ensaio foi pausado
            global mult  #Multiplo de 5 que ajuda a arrumar o gráfico em 5 em 5
            global glpCOND #quantidade de golpes do CONDICIONAMENTO
            global glpMR #quantidade de golpes do MR
            global ntglp #quantidade total de golpes disponíveis
            global modeADM #modo Administrador de salvar dados (apenas para dbug)
            global DISCREP #valor da discrepância
            global subleito #recebe valor de True ou False
            global DPmaxACUM #Altura mínima que o corpo de prova deve atingir
            global VETOR_COND #Vetor com os pares de pressões do CONDICIONAMENTO
            global VETOR_MR #Vetor com os pares de pressões do MR

            '''Banco de dados'''
            pressoes = bdConfiguration.QD_134_MOD()
            config = bdConfiguration.CONFIG_134()

            idt = identificador
            subleito = tipo
            H = altura
            Diam = diametro
            glpCOND = config[0]
            glpMR = config[1]
            modeADM = False
            DISCREP = 1+float(config[2])/100
            DPmaxACUM = float(H) - float(H)*float(config[2])/100
            H0 = 0.0000001
            mult = 0
            Pausa = False
            X = np.array([])
            Y = np.array([])
            xz1 = []
            yz1 = []
            yt1 = []
            yz2 = []
            yt2 = []
            pc1 = []
            pg1 = []
            yyy = []
            Fase = ''
            VETOR_COND = pressoes[0]
            VETOR_MR = pressoes[1]

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
            message3 = "realizando a CONEXAO"
            dlg = dialogoDinamico(1, info, titulo, message1, message2, message3, None)
            dlg.ShowModal()
