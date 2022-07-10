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
frequencias = ['1']

#########################################################################
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
                self._self.bottom.SigmaAlvo.Clear()
                self._self.bottom.fase.Clear()
                self.AVANCA = True

                print '\nAVANCA.FASE.MR='+str(self._fase+1)+'\n'
                self._self.bottom.SigmaAlvo.AppendText("%.3f" % VETOR_MR[self._fase][0])
                self._self.bottom.fase.AppendText(str(self._fase+1))

                if(self._fase < 5):
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

            condition = False
            if self._fase > 0:
                if VETOR_MR[self._fase][0] != VETOR_MR[self._fase - 1][0] and self.AVANCA == False:
                    threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_MR[self._fase][0], VETOR_MR[self._fase-1][0])
                    dlgC1 = My.MyProgressDialog(3)
                    dlgC1.ShowModal()
                    self.DINAMICA2_ANTERIOR = VETOR_MR[self._fase][0]
                    time.sleep(1)

                if self.AVANCA == True:
                    threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_MR[self._fase][0], self.DINAMICA2_ANTERIOR)
                    dlgC1 = My.MyProgressDialog(3)
                    dlgC1.ShowModal()
                    self.DINAMICA2_ANTERIOR = VETOR_MR[self._fase][0]
                    time.sleep(.5)
                    self.AVANCA = False
            else:
                threadConection = DinamicaThread.DinamicaThreadTwo(VETOR_MR[self._fase][0], 0)
                dlgC1 = My.MyProgressDialog(3)
                dlgC1.ShowModal()
                time.sleep(.5)

            if threadConection.ret() == False:
                dlgC3 = dialogoDinamico(3, "EDP DNIT181/2018ME", "MÓDULO DE RESILIÊNCIA", "Ocorreu algum problema com o ajuste da pressão!", "Verifique o motor de passos!", "", None)
                dlgC3.ShowModal()
                self._self.bottom.erro = True
                if self._fase == 0:
                    self._self.bottom.mr.Enable()

            time.sleep(.5)
            if self._self.bottom.Automatico == False:
                condition = True
                dlg3 = dialogoDinamico(3, "EDP DNIT181/2018ME", "MÓDULO DE RESILIÊNCIA", "Tudo pronto!", "Aperte INICIO.", "", None)
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
                global X
                global Y
                global mult
                global ntglp
                global H
                global REFERENCIA_MEDIA

                while True:
                    try:
                        valorGolpe = int(self._self.bottom.GolpeAtual.GetValue())
                        alturaFinalCP = float(self._self.bottom.AlturaFinal.GetValue())
                        if valorGolpe == int(ntglp-1):
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
            global mult

            '''Diálogo se deseja realmente finalizar o Ensaio'''
            dlg = wx.MessageDialog(None, 'Deseja realmente finalizar o MR?', 'EDP', wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
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
                self.Close(True)


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

            self.mr = wx.Button(self, -1, 'M. R.')
            self.Bind(wx.EVT_BUTTON, self.MR, self.mr)
            self.LTeste = wx.Button(self, -1, "L. TESTE", size = wx.DefaultSize)
            self.Bind(wx.EVT_BUTTON, self.LTESTE, self.LTeste)
            self.LZero = wx.Button(self, -1, "L. ZERO", size = wx.DefaultSize)
            self.Bind(wx.EVT_BUTTON, self.LZERO, self.LZero)

            self.mr.Disable()
            self.LZero.Disable()

            self.mr.SetFont(FontTitle1)
            self.LTeste.SetFont(FontTitle1)
            self.LZero.SetFont(FontTitle1)

            texto1 = wx.StaticText(self, label = "EIXO Y", style = wx.ALIGN_CENTRE)
            texto4 = wx.StaticText(self, label = "σ1 - Tensão vertical (MPa)", style = wx.ALIGN_CENTRE)
            texto5 = wx.StaticText(self, label = "Y1 (V)", style = wx.ALIGN_CENTER)
            texto6 = wx.StaticText(self, label = "Y2 (V)", style = wx.ALIGN_CENTER)
            texto7 = wx.StaticText(self, label = "Y1 (mm)", style = wx.ALIGN_CENTER)
            texto8 = wx.StaticText(self, label = "Y2 (mm)", style = wx.ALIGN_CENTER)
            texto13 = wx.StaticText(self, label = "Altura Final (mm)", style = wx.ALIGN_LEFT)
            texto15 = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
            texto17 = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
            texto18 = wx.StaticText(self, label = "Altura (mm)", style = wx.ALIGN_LEFT)
            texto19 = wx.StaticText(self, label = "Diâmetro (mm)", style = wx.ALIGN_LEFT)
            texto21 = wx.StaticText(self, label = "FASE", style = wx.ALIGN_CENTER)
            texto22 = wx.StaticText(self, label = "Nº de CICLOs", style = wx.ALIGN_CENTER)
            texto23 = wx.StaticText(self, label = "Freq. (Hz)", style = wx.ALIGN_CENTER)
            texto24 = wx.StaticText(self, label = "CICLO Atual", style = wx.ALIGN_CENTER)

            texto1.SetFont(FontTitle)
            texto4.SetFont(FontTitle)
            texto5.SetFont(Fonttext)
            texto6.SetFont(Fonttext)
            texto7.SetFont(Fonttext)
            texto8.SetFont(Fonttext)
            texto13.SetFont(FontTitle)
            texto15.SetFont(Fonttext)
            texto17.SetFont(Fonttext)
            texto18.SetFont(Fonttext)
            texto19.SetFont(Fonttext)
            texto21.SetFont(FontTitle)
            texto22.SetFont(Fonttext)
            texto23.SetFont(Fonttext)
            texto24.SetFont(Fonttext)

            texto1.SetBackgroundColour(wx.Colour(215,215,215))
            texto4.SetBackgroundColour(wx.Colour(215,215,215))
            texto5.SetBackgroundColour(wx.Colour(215,215,215))
            texto6.SetBackgroundColour(wx.Colour(215,215,215))
            texto7.SetBackgroundColour(wx.Colour(215,215,215))
            texto8.SetBackgroundColour(wx.Colour(215,215,215))
            texto13.SetBackgroundColour(wx.Colour(215,215,215))
            texto15.SetBackgroundColour(wx.Colour(215,215,215))
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
            self.SigmaReal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.SigmaAlvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.AlturaMM = wx.TextCtrl(self, -1, str(H), size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.DiametroMM = wx.TextCtrl(self, -1, str(Diam), size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.fase = wx.TextCtrl(self, -1, '1', size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.NGolpes = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.GolpeAtual = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTRE)
            self.freq = wx.ComboBox(self, -1, frequencias[0], choices = frequencias, size = (50, 35), style = wx.CB_READONLY)
            self.ensaioAuto = wx.CheckBox(self, -1, 'Ensaio automático', (20,0), (260,-1), style = wx.ALIGN_LEFT)

            self.y1V.Disable()
            self.y2V.Disable()
            self.y1mm.Disable()
            self.y2mm.Disable()
            self.AlturaFinal.Disable()
            self.SigmaReal.Disable()
            self.SigmaAlvo.Disable()
            self.AlturaMM.Disable()
            self.DiametroMM.Disable()
            self.fase.Disable()
            self.NGolpes.Disable()
            self.GolpeAtual.Disable()
            self.freq.Disable()

            self.y1V.SetFont(Fonttext)
            self.y2V.SetFont(Fonttext)
            self.y1mm.SetFont(Fonttext)
            self.y2mm.SetFont(Fonttext)
            self.AlturaFinal.SetFont(Fonttext)
            self.SigmaReal.SetFont(Fonttext)
            self.SigmaAlvo.SetFont(Fonttext)
            self.AlturaMM.SetFont(Fonttext)
            self.DiametroMM.SetFont(Fonttext)
            self.fase.SetFont(Fonttext)
            self.NGolpes.SetFont(Fonttext)
            self.GolpeAtual.SetFont(Fonttext)
            self.freq.SetFont(Fonttext)

            self.y1V.SetForegroundColour((119,118,114))
            self.y2V.SetForegroundColour((119,118,114))
            self.y1mm.SetForegroundColour((119,118,114))
            self.y2mm.SetForegroundColour((119,118,114))
            self.AlturaFinal.SetForegroundColour((119,118,114))
            self.SigmaReal.SetForegroundColour((119,118,114))
            self.SigmaAlvo.SetForegroundColour((119,118,114))
            self.AlturaMM.SetForegroundColour((119,118,114))
            self.DiametroMM.SetForegroundColour((119,118,114))
            self.fase.SetForegroundColour((119,118,114))
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

            self.v_sizer.Add(self.mr, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.AddStretchSpacer(3)

            self.v1_sizer.Add(staticboxSizer4, 20, wx.EXPAND | wx.ALL)
            self.v1_sizer.AddStretchSpacer(18)

            self.v2_sizer.Add(staticboxSizer5, 15, wx.EXPAND | wx.ALL)
            self.v2_sizer.AddStretchSpacer(1)
            self.v2_sizer.Add(staticboxSizer6, 20, wx.EXPAND | wx.ALL)

            self.h1_sizer.Add(staticboxSizer1, 1, wx.EXPAND | wx.ALL, 3)
            self.h1_sizer.Add(self.v2_sizer, 1, wx.EXPAND | wx.ALL, 3)
            self.h1_sizer.Add(self.v1_sizer, 1, wx.EXPAND | wx.ALL, 3)

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
            self.Automatico = True #inicia com o ensaio Automatico sendo true
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
                        global Ti
                        global Pausa
                        global X
                        global Y
                        global H
                        global pg1
                        global yyy
                        global REFERENCIA1
                        global REFERENCIA2
                        global REFERENCIA_MEDIA
                        global ntglp
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
                                    self.SigmaReal.Clear()
                                    self.AlturaFinal.Clear()
                                    self.valorLeitura0 = valores[1] #usado apenas no LZERO
                                    self.valorLeitura1 = valores[2] #usado apenas no LZERO
                                    self.y1mm.AppendText(str(round(abs(valores[1]-self.leituraZerob1), 4)))
                                    self.y2mm.AppendText(str(round(abs(valores[2]-self.leituraZerob2), 4)))
                                    self.y1V.AppendText(str(round((valores[3]), 2)))
                                    self.y2V.AppendText(str(round((valores[4]), 2)))
                                    self.SigmaReal.AppendText(str(round(abs(valores[6]), 3)))
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
                                if conditionEnsaio == True and valores[0] > 0:
                                    X = np.append(X, valores[0])
                                    Y = np.append(Y, ymedio)
                                    x_counter = len(X)
                                    if x_counter >= 1000: #antes era 1500
                                        X = np.delete(X, 0, 0)
                                        Y = np.delete(Y, 0, 0)

                                    # Dados do MR #
                                    if Pausa == False:
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
                                        if valores[0] > 30 and valores[0] < 30.2:
                                            if valores[0] == 30.01:
                                                amplitudeMaxAnterior = ymedio
                                                mediaMovel = ymedio
                                            if ymedio > amplitudeMaxAnterior:
                                                amplitudeMaxAnterior = ymedio
                                        if valores[0] > 30.2 and valores[0] < 31:
                                            mediaMovel = (mediaMovel+ymedio)/2
                                            defResilienteAnterior = amplitudeMaxAnterior - mediaMovel

                                        # Condição da analise de discrepância #
                                        if valores[0] > 40:
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

                                        if int(valores[0]) > 40 and int(valores[0]) <= int(valores[9]):
                                            pg1.append(valores[6])

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
                menssagError = wx.MessageDialog(self, 'ERRO AO EXECUTAR L. TESTE', 'EDP', wx.OK|wx.ICON_EXCLAMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()

    #--------------------------------------------------
        '''Função responsável pela leitura zero'''
        def LZERO(self, event):
            print '\nBottomPanel - LZERO'
            self.freq.Enable()
            self.mr.Enable()
            self.LTeste.Disable()
            self.leituraZerob1 = float(self.valorLeitura0)
            self.leituraZerob2 = float(self.valorLeitura1)
            print self.leituraZerob1
            print self.leituraZerob2

    #--------------------------------------------------
        '''Função responsável em realizar o MODULO RESILIENTE'''
        def MR(self, event):
            print '\nBottomPanel - MR'
            global condition
            global pg1
            global yyy
            global REFERENCIA1
            global REFERENCIA2
            global REFERENCIA_MEDIA
            global idt
            global DISCREP
            global glpMR
            self.erro = False
            fase = 5

            if self._fase < fase:
                print '\nFASE.MR='+str(self._fase+1)+'\n'

            if self._fase > 0:
                try:
                    dr = sum(yyy)/len(yyy)
                    pg = sum(pg1)/len(pg1)
                    bancodedados.saveDNIT181(idt, str(self._fase), pg, dr, REFERENCIA_MEDIA)
                except:
                    dlg = dialogoDinamico(3, "EDP 134/2018ME", "SALVAMENTO", "Ocorreu algum problema com o salvamento dos dados!", "O Ensaio precisarar ser finalizado!", "", None)
                    dlg.ShowModal()
                yyy = []
                pg1 = []

            if self._fase < fase:
                self.LZero.Disable()
                self.freq.Disable()
                self.mr.Disable()
                self.SigmaAlvo.Clear()
                self.fase.Clear()
                self.NGolpes.Clear()
                self.GolpeAtual.Clear()
                self.SigmaAlvo.AppendText("%.3f" % VETOR_MR[self._fase][0])
                self.NGolpes.AppendText(str(glpMR))
                self.fase.AppendText(str(self._fase+1))
                self.GolpeAtual.AppendText(str(0))

            if self._fase == 0:
                info = "EDP 181/2018ME"
                titulo = "Preparação da câmara triaxial."
                message1 = "Verifique se está tudo certo!"
                message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                if dlg.ShowModal() == wx.ID_OK:
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
                    self.pressao_zero(VETOR_MR[self._fase-1][0])
                    self._fase = 0
                    bancodedados.data_final_Update_idt(idt)
                    dlg3 = dialogoDinamico(3, "EDP DNIT181/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatório de extração são gerados na tela inicial.", "FIM!", "", None)
                    if dlg3.ShowModal() == wx.ID_OK:
                        time.sleep(.3)
                        con.modeStoped()
                        time.sleep(.3)
                        con.modeB()
                        time.sleep(.3)
                        con.modeD()
                        self.Close(True)

    #--------------------------------------------------
        '''Função responsável em zerar a pressão do sistema'''
        def pressao_zero(self, p2Sen):
            print '\nBottomPanel - pressao_zero'
            global condition
            condition = False
            threadConection = DinamicaThread.DinamicaThreadTwoZero(0.005, p2Sen) #0.005 é o menor valor de pressão admissível para valvula dinamica
            dlgC1 = My.MyProgressDialog(4)
            dlgC1.ShowModal()
            condition = True

    #--------------------------------------------------
        '''Função responsável pela plotagem'''
        def TimeInterval(self, event):
            print '\nBottomPanel - TimeInterval'
            global mult
            mult += 1
            self.graph.draw()


'''Tela Realização do Ensaio'''
class TelaRealizacaoEnsaioDNIT181(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, identificador, diametro, altura, *args, **kwargs):
            wx.Frame.__init__(self, parent = None, title = 'EDP - DNIT 181/2018ME - Tela Ensaio', size = (1000,750), style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Variáveis Globais'''
            global idt #identificador do ensaio
            global leituraZerob1 #leitura zero do sensor 1
            global leituraZerob2 #leitura zero do sensor 2
            global H  #Altura do corpo de prova em milímetros
            global Diam  #Diametro do corpo de prova em milímetros
            global H0 #Altura de referência do medididor de deslocamento
            global X  #valores X do gráfico
            global Y  #valores Y do gráfico
            global pg1  #pressao do golpe
            global yyy  #valores de deformação
            global REFERENCIA1 #referencia de ponto de partida para o sensor 1
            global REFERENCIA2 #referencia de ponto de partida para o sensor 2
            global REFERENCIA_MEDIA #referencia de ponto de partidada MÉDIA
            global Ti #valor temporal
            global Automatico #idica se o ensaio será automático ou não
            global Pausa #indica se o ensaio foi pausado
            global mult  #Multiplo de 5 que ajuda a arrumar o gráfico em 5 em 5
            global glpMR #quantidade de golpes do MR
            global ntglp #quantidade total de golpes disponíveis
            global DISCREP #valor da discrepância
            global VETOR_COND #Vetor com os pares de pressões do CONDICIONAMENTO
            global VETOR_MR #Vetor com os pares de pressões do MR

            '''Banco de dados'''
            config = bancodedados.CONFIG_181()
            VETOR_MR = bancodedados.QD_181()

            idt = identificador
            H = altura
            Diam = diametro
            glpMR = config[0]
            DISCREP = 1+float(config[1])/100
            H0 = 0.0000001
            mult = 0
            Pausa = False
            X = np.array([])
            Y = np.array([])
            pg1 = []
            yyy = []

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

            self.Centre()
            self.Show()
            self.Maximize(True)

            '''Dialogo Inicial'''
            info = "EDP 181/2018ME"
            titulo = "Ajuste o Zero dos LVDTs"
            message1 = "Com o valor entre:"
            message2 = "2.5 e 3.0 Volts"
            message3 = "realizando a L. TESTE"
            dlg = dialogoDinamico(1, info, titulo, message1, message2, message3, None)
            dlg.ShowModal()