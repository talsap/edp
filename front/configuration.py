# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import bancodedados
from quadrotensoes import *

'''Tela de Configurações'''
class Config(wx.Frame):
        #--------------------------------------------------
        def __init__(self, *args, **kwargs):
                wx.Frame.__init__(self, None, -1, 'EDP - Configuração dos Ensaios', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

                '''Iserção do IconeLogo'''
                try:
                    ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                    self.SetIcon(ico)
                except:
                    pass

                # Aqui criamos um painel e um Notebook representado as guias
                panel = wx.Panel(self)
                nb = wx.Notebook(panel)

                # crie as janelas da página como filhas do Notebook
                page01 = Page01(nb, id)
                page02 = Page02(nb, id)
                page03 = Page03(nb, id)

                # adicione as páginas ao caderno com o rótulo para mostrar na guia
                nb.AddPage(page01, "DNIT 134")
                nb.AddPage(page02, "DNIT 179")
                nb.AddPage(page03, "DNIT 181")

                sizer = wx.BoxSizer()
                sizer.Add(nb, 1, wx.EXPAND)
                panel.SetSizer(sizer)
                self.SetSize((360,300))
                self.Centre()
                self.Show()

class Page01(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page01, self).__init__(parent)
                self.id = id

                '''Dados do bancodedados'''
                self.lista = bancodedados.CONFIG_134()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                texto0 = wx.StaticText(self, -1, "Quantidade de ciclos do CONDIC. =", (52,25), (-1,-1), wx.ALIGN_LEFT)
                self.CicloCOND = wx.SpinCtrl(self, -1, str(self.lista[0]), (245,23), (80,-1), wx.TE_CENTRE)
                self.CicloCOND.SetMin(10)
                self.CicloCOND.SetMax(1000)
                self.CicloCOND.SetValue(str(self.lista[0]))
                self.CicloCOND.Disable()
                texto1 = wx.StaticText(self, -1, "Quantidade mínima de ciclos do M. R. =", (29,55), (-1,-1), wx.ALIGN_RIGHT)
                self.CicloMR = wx.SpinCtrl(self, -1, str(self.lista[1]), (245,53), (80,-1), wx.TE_CENTRE)
                self.CicloMR.SetMin(10)
                self.CicloMR.SetMax(200)
                self.CicloMR.SetValue(str(self.lista[1]))
                self.CicloMR.Disable()
                texto2 = wx.StaticText(self, -1, "erro máximo entre as leituras [%] =", (57,85), (-1,-1), wx.ALIGN_RIGHT)
                self.erro = wx.SpinCtrl(self, -1, str(self.lista[2]), (245,83), (80,-1), wx.TE_CENTRE)
                self.erro.SetMin(5)
                self.erro.SetMax(100)
                self.erro.SetValue(str(self.lista[2]))
                self.erro.Disable()
                texto2 = wx.StaticText(self, -1, "D. P. acumulada em [%] da altura do CP =", (20,115), (-1,-1), wx.ALIGN_RIGHT)
                self.DPacum = wx.SpinCtrl(self, -1, str(self.lista[3]), (245,113), (80,-1), wx.TE_CENTRE)
                self.DPacum.SetMin(5)
                self.DPacum.SetMax(8)
                self.DPacum.SetValue(str(self.lista[3]))
                self.DPacum.Disable()

                self.QTensoes = wx.Button(self, -1, 'Q. TENSÕES', (238,145), (-1,40))
                self.Bind(wx.EVT_BUTTON, self.QT, self.QTensoes)

                self.editar1 = wx.Button(self, -1, 'Editar', (60,200), (-1,-1))
                self.Salvar1 = wx.Button(self, -1, 'Salvar', (200,200), (-1,-1))
                self.Bind(wx.EVT_BUTTON, self.Editar1, self.editar1)
                self.Bind(wx.EVT_BUTTON, self.Salva1, self.Salvar1)
                self.Salvar1.Disable()

        #--------------------------------------------------
        def QT(self, event):
            print '\nQT1'
            dlg = quadroEditavelDNIT134().ShowModal()

        #--------------------------------------------------
        def Editar1(self, event):
                '''Edita...'''
                self.editar1.Disable()
                self.CicloCOND.Enable()
                self.CicloMR.Enable()
                self.erro.Enable()
                self.DPacum.Enable()
                self.Salvar1.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva1(self, event):
                '''Salva...'''
                CICLOCOND = self.CicloCOND.GetValue()
                CICLOMR = self.CicloMR.GetValue()
                ERRO = self.erro.GetValue()
                DP_ACUM = self.DPacum.GetValue()
                CICLOCOND = format(CICLOCOND).replace(',','.')
                CICLOMR = format(CICLOMR).replace(',','.')
                ERRO = format(ERRO).replace(',','.')
                DP_ACUM = format(DP_ACUM).replace(',','.')

                try:
                    CICLOCOND = float(CICLOCOND)
                    CICLOMR = float(CICLOMR)
                    ERRO = float(ERRO)
                    DP_ACUM = float(DP_ACUM)
                    CICLOCOND = int(CICLOCOND)
                    CICLOMR = int(CICLOMR)
                    ERRO = int(ERRO)
                    DP_ACUM = int(DP_ACUM)
                    condicional = 1

                except ValueError:
                    print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                    menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    condicional = -1

                if CICLOCOND == '' or CICLOMR == '' or ERRO == '' or DP_ACUM == '':
                    '''Diálogo para Forçar preenchimento dos valores'''
                    dlg = wx.MessageDialog(None, 'É necessário que alguns campos estejam preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

                else:
                    if(condicional>0):
                        bancodedados.update_dados_CONFIG_134(CICLOCOND, CICLOMR, ERRO, DP_ACUM)
                        self.editar1.Enable()
                        self.Salvar1.Disable()
                        self.CicloCOND.Disable()
                        self.CicloMR.Disable()
                        self.erro.Disable()
                        self.DPacum.Disable()
                        self.Update()
                        self.Refresh()

class Page02(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page02, self).__init__(parent)
                self.id = id

                '''Dados do bancodedados'''
                self.lista = bancodedados.CONFIG_179()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                texto0 = wx.StaticText(self, -1, "Quantidade de ciclos do CONDIC. =", (52,25), (-1,-1), wx.ALIGN_LEFT)
                self.CicloCOND = wx.SpinCtrl(self, -1, str(self.lista[0]), (245,23), (80,-1), wx.TE_CENTRE)
                self.CicloCOND.SetMin(10)
                self.CicloCOND.SetMax(1000)
                self.CicloCOND.SetValue(str(self.lista[0]))
                self.CicloCOND.Disable()
                texto1 = wx.StaticText(self, -1, "Quantidade de ciclos do D. P. =", (76,55), (-1,-1), wx.ALIGN_RIGHT)
                self.CicloDP = wx.SpinCtrl(self, -1, str(self.lista[1]), (245,53), (80,-1), wx.TE_CENTRE)
                self.CicloDP.SetMin(1000)
                self.CicloDP.SetMax(500000)
                self.CicloDP.SetValue(str(self.lista[1]))
                self.CicloDP.Disable()

                self.QTensoes = wx.Button(self, -1, 'Q. TENSÕES', (238,85), (-1,40))
                self.Bind(wx.EVT_BUTTON, self.QT, self.QTensoes)

                self.editar2 = wx.Button(self, -1, 'Editar', (60,200), (-1,-1))
                self.Salvar2 = wx.Button(self, -1, 'Salvar', (200,200), (-1,-1))
                self.Bind(wx.EVT_BUTTON, self.Editar2, self.editar2)
                self.Bind(wx.EVT_BUTTON, self.Salva2, self.Salvar2)
                self.Salvar2.Disable()

        #--------------------------------------------------
        def QT(self, event):
            print '\nQT2'
            dlg = quadroEditavelDNIT179().ShowModal()

        #--------------------------------------------------
        def Editar2(self, event):
                '''Edita...'''
                self.editar2.Disable()
                self.CicloCOND.Enable()
                self.CicloDP.Enable()
                self.Salvar2.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva2(self, event):
                '''Salva...'''
                CICLOCOND = self.CicloCOND.GetValue()
                CICLODP = self.CicloDP.GetValue()
                CICLOCOND = format(CICLOCOND).replace(',','.')
                CICLODP = format(CICLODP).replace(',','.')

                try:
                    CICLOCOND = float(CICLOCOND)
                    CICLODP = float(CICLODP)
                    CICLOCOND = int(CICLOCOND)
                    CICLODP = int(CICLODP)
                    condicional = 1

                except ValueError:
                    print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                    menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    condicional = -1

                if CICLOCOND == '' or CICLODP == '':
                    '''Diálogo para Forçar preenchimento dos valores'''
                    dlg = wx.MessageDialog(None, 'É necessário que alguns campos estejam preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

                else:
                    if(condicional>0):
                        bancodedados.update_dados_CONFIG_179(CICLOCOND, CICLODP)
                        self.editar2.Enable()
                        self.Salvar2.Disable()
                        self.CicloCOND.Disable()
                        self.CicloDP.Disable()
                        self.Update()
                        self.Refresh()

class Page03(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page03, self).__init__(parent)
                self.id = id

                '''Dados do bancodedados'''
                self.lista = bancodedados.CONFIG_181()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                texto0 = wx.StaticText(self, -1, "Quantidade de ciclos do M. R. =", (73,25), (-1,-1), wx.ALIGN_LEFT)
                self.CicloMR = wx.SpinCtrl(self, -1, str(self.lista[0]), (245,23), (80,-1), wx.TE_CENTRE)
                self.CicloMR.SetMin(10)
                self.CicloMR.SetMax(200)
                self.CicloMR.SetValue(str(self.lista[0]))
                self.CicloMR.Disable()
                texto2 = wx.StaticText(self, -1, "erro máximo entre as leituras [%] =", (57,55), (-1,-1), wx.ALIGN_RIGHT)
                self.erro = wx.SpinCtrl(self, -1, str(self.lista[1]), (245,53), (80,-1), wx.TE_CENTRE)
                self.erro.SetMin(5)
                self.erro.SetMax(100)
                self.erro.SetValue(str(self.lista[1]))
                self.erro.Disable()

                self.QTensoes = wx.Button(self, -1, 'Q. TENSÕES', (238,85), (-1,40))
                self.Bind(wx.EVT_BUTTON, self.QT, self.QTensoes)

                self.editar3 = wx.Button(self, -1, 'Editar', (60,200), (-1,-1))
                self.Salvar3 = wx.Button(self, -1, 'Salvar', (200,200), (-1,-1))
                self.Bind(wx.EVT_BUTTON, self.Editar3, self.editar3)
                self.Bind(wx.EVT_BUTTON, self.Salva3, self.Salvar3)
                self.Salvar3.Disable()

        #--------------------------------------------------
        def QT(self, event):
            print '\nQT3'
            dlg = quadroEditavelDNIT181().ShowModal()

        #--------------------------------------------------
        def Editar3(self, event):
                '''Edita...'''
                self.editar3.Disable()
                self.CicloMR.Enable()
                self.erro.Enable()
                self.Salvar3.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva3(self, event):
                '''Salva...'''
                CICLOMR = self.CicloMR.GetValue()
                ERRO = self.erro.GetValue()
                CICLOMR = format(CICLOMR).replace(',','.')
                ERRO = format(ERRO).replace(',','.')

                try:
                    CICLOMR = float(CICLOMR)
                    ERRO = float(ERRO)
                    CICLOMR = int(CICLOMR)
                    ERRO = int(ERRO)
                    condicional = 1

                except ValueError:
                    print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                    menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    condicional = -1

                if CICLOMR == '' or ERRO == '':
                    '''Diálogo para Forçar preenchimento dos valores'''
                    dlg = wx.MessageDialog(None, 'É necessário que alguns campos estejam preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

                else:
                    if(condicional>0):
                        bancodedados.update_dados_CONFIG_181(CICLOMR, ERRO)
                        self.editar3.Enable()
                        self.Salvar3.Disable()
                        self.CicloMR.Disable()
                        self.erro.Disable()
                        self.Update()
                        self.Refresh()
