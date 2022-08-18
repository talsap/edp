# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import time
import threading
import back.connection as con
import back.ConexaoThread as ConexaoThread
import back.MyProgressDialog as My
import back.HexForRGB as HexRGB
import banco.bdPreferences as bdPreferences

'''Tela de Configurações'''
class Conn(wx.Dialog):
        #--------------------------------------------------
        def __init__(self, *args, **kwargs):
                wx.Dialog.__init__(self, None, -1, 'EDP - Conexão', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

                colors = bdPreferences.ListColors()
                colorCard = colors[0]
                colorTextCtrl = colors[1]
                colorBackground = colors[2]
                colorLineGrafic = colors[3]
                colorBackgroundGrafic = colors[4]

                colorStaticBox = HexRGB.RGB(colorCard)
                colorTextBackground = HexRGB.RGB(colorCard)
                colorTextCtrl = HexRGB.RGB(colorTextCtrl)

                self.SetBackgroundColour(colorBackground)
                
                '''Iserção do IconeLogo'''
                try:
                    ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                    self.SetIcon(ico)
                except:
                    pass

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
                FontTitle1 = wx.Font(-1, wx.SWISS, wx.NORMAL, wx.BOLD)
                Fonttext = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

                staticbox1 = wx.StaticBox(self, -1, '')

                staticboxSizer1 = wx.StaticBoxSizer(staticbox1, wx.VERTICAL)
                staticbox1.SetBackgroundColour(colorStaticBox)

                self.LTeste = wx.Button(self, -1, "CONECTAR", size = wx.DefaultSize)
                self.Bind(wx.EVT_BUTTON, self.LTESTE, self.LTeste)
                self.Bind(wx.EVT_CLOSE, self.onExit)
                self.LTeste.SetFont(FontTitle1)

                texto1 = wx.StaticText(self, label = "TESTAR CONEXÃO", style = wx.ALIGN_CENTRE)
                texto5 = wx.StaticText(self, label = "Y1 (V)", style = wx.ALIGN_CENTER)
                texto6 = wx.StaticText(self, label = "Y2 (V)", style = wx.ALIGN_CENTER)
                texto7 = wx.StaticText(self, label = "Y1 (mm)", style = wx.ALIGN_CENTER)
                texto8 = wx.StaticText(self, label = "Y2 (mm)", style = wx.ALIGN_CENTER)

                texto1.SetFont(FontTitle)
                texto5.SetFont(Fonttext)
                texto6.SetFont(Fonttext)
                texto7.SetFont(Fonttext)
                texto8.SetFont(Fonttext)

                texto1.SetBackgroundColour(colorTextBackground)
                texto5.SetBackgroundColour(colorTextBackground)
                texto6.SetBackgroundColour(colorTextBackground)
                texto7.SetBackgroundColour(colorTextBackground)
                texto8.SetBackgroundColour(colorTextBackground)

                self.y1V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
                self.y2V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
                self.y1mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
                self.y2mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)

                self.y1V.Disable()
                self.y2V.Disable()
                self.y1mm.Disable()
                self.y2mm.Disable()

                self.y1V.SetFont(Fonttext)
                self.y2V.SetFont(Fonttext)
                self.y1mm.SetFont(Fonttext)
                self.y2mm.SetFont(Fonttext)

                self.y1V.SetForegroundColour(colorTextCtrl)
                self.y2V.SetForegroundColour(colorTextCtrl)
                self.y1mm.SetForegroundColour(colorTextCtrl)
                self.y2mm.SetForegroundColour(colorTextCtrl)

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

                self.h21_sizer.AddStretchSpacer(1)
                self.h21_sizer.Add(self.LTeste, 8, wx.ALL)
                self.h21_sizer.AddStretchSpacer(1)

                self.v20_sizer.Add(self.h20_sizer, 3, wx.CENTER)
                self.v20_sizer.AddStretchSpacer(1)
                self.v20_sizer.Add(self.h19_sizer, 3, wx.CENTER)
                self.v20_sizer.AddStretchSpacer(2)
                self.v20_sizer.Add(self.h21_sizer, 2, wx.CENTER)

                self.v21_sizer.Add(texto1, 1, wx.CENTER)
                self.v21_sizer.Add(self.v20_sizer, 7, wx.CENTER)

                self.h22_sizer.Add(self.v21_sizer, 1, wx.CENTER)
                staticboxSizer1.Add(self.h22_sizer, 0,  wx.ALL | wx.EXPAND  | wx.CENTER, 10)

                self.sizer = wx.BoxSizer(wx.VERTICAL)
                self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h1_sizer = wx.BoxSizer(wx.HORIZONTAL)

                self.h1_sizer.Add(staticboxSizer1, 1, wx.EXPAND | wx.ALL, 3)

                self.h_sizer.Add(self.h1_sizer, 12, wx.EXPAND | wx.ALL, 5)
                #self.h_sizer.AddStretchSpacer(4)

                self.sizer.Add(self.h_sizer, 0,  wx.EXPAND | wx.ALL, 10)
                self.SetSizer(self.sizer)

                self.SetSize((360,300))
                self.Centre()
                self.Show()
        
        #--------------------------------------------------
        '''Função responsável em realizar a CONEXÃO'''
        def LTESTE(self, event):
            print '\nBottomPanel - LTESTE'

            threadConection = ConexaoThread.ConexaoThread(1.05) #1.05 é o valor defautl para a DISCREP
            cond = threadConection.ret()
            if cond[0] == 'connectado':
                menssagError = wx.MessageDialog(self, 'CONECTADO!', 'EDP', wx.OK|wx.ICON_AUTH_NEEDED)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                con.modeConectDNIT134() #acessa o ensaio da 134 no arduino

                #--------------------------------------------------
                def worker(self):
                    con.modeI()  #inicia o modo de impressão de dados
                    global condition
                    condition = True
                    cont1 = 0
                    valores = [0,0,0,0,0,0,0,0,0,0]
                    while condition == True:
                        valores = con.ColetaI(valores)
                        if cont1 >= 20: #mede a frequencia da impressão de dados na tela
                            self.y1mm.Clear()
                            self.y2mm.Clear()
                            self.y1V.Clear()
                            self.y2V.Clear()
                            self.y1mm.AppendText(str(round(abs(valores[1]), 4)))
                            self.y2mm.AppendText(str(round(abs(valores[2]), 4)))
                            self.y1V.AppendText(str(round((valores[3]), 2)))
                            self.y2V.AppendText(str(round((valores[4]), 2)))
                            if cont1 == 20:
                                cont1 = 0
                        cont1 = cont1 + 1

                #--------------------------------------------------
                self.t = threading.Thread(target=worker, args=(self,))
                if self.t.is_alive():
                    self.t.run()
                    print "RUN"
                else:
                    self.t.start()
                    print "START"
                self.LTeste.SetLabel('DESCONECTAR')
                self.Bind(wx.EVT_BUTTON, self.Desconect, self.LTeste)

            else:
                menssagError = wx.MessageDialog(self, 'Não é possível manter uma conexão serial!', 'EDP', wx.OK|wx.ICON_EXCLAMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
        
        #--------------------------------------------------
        '''Função responsável em realizar a DESCONEXÃO'''
        def Desconect(self, event):
            global condition
            condition = False
            self.y1mm.Clear()
            self.y2mm.Clear()
            self.y1V.Clear()
            self.y2V.Clear()            
            time.sleep(.3)
            con.modeStoped()
            time.sleep(.3)
            con.modeB()
            time.sleep(.3)
            con.modeD()
            self.t.join()
            self.LTeste.SetLabel('CONECTAR')
            self.Bind(wx.EVT_BUTTON, self.LTESTE, self.LTeste)
        
        #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            print 'sair'
            self.Destroy()