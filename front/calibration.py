# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import banco.bdConfiguration as bdConfiguration
import banco.bdPreferences as bdPreferences
import back.HexForRGB as HexRGB

'''Tela Calibração'''
class Cal(wx.Dialog):
        #--------------------------------------------------
        def __init__(self, *args, **kwargs):
                wx.Dialog.__init__(self, None, -1, 'EDP - Coeficientes de Calibração', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

                colors = bdPreferences.ListColors()
                colorBackground = colors[2]

                self.SetBackgroundColour(colorBackground)
                
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
                page04 = Page04(nb, id)
                #page05 = Page05(nb, id)
                page06 = Page06(nb, id)

                # adicione as páginas ao caderno com o rótulo para mostrar na guia
                nb.AddPage(page01, "S1-S2")
                nb.AddPage(page02, "S3-S4")
                nb.AddPage(page03, "DIN-1")
                nb.AddPage(page04, "DIN-2")
                #nb.AddPage(page05, "MOTOR")
                nb.AddPage(page06, "CIL-P")

                sizer = wx.BoxSizer()
                sizer.Add(nb, 1, wx.EXPAND)
                panel.SetSizer(sizer)
                self.Bind(wx.EVT_CLOSE, self.onExit)
                self.SetSize((360,520))
                self.Centre()
                self.Show()

        #--------------------------------------------------
        def onExit(self, event):
                '''Opcao Sair'''
                self.Destroy()

class Page01(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page01, self).__init__(parent)
                self.id = id
                
                colors = bdPreferences.ListColors()
                colorBackground = colors[2]

                self.SetBackgroundColour(colorBackground)

                '''Dados do bancodedados'''
                self.lista = bdConfiguration.S1S2()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                title0 = wx.StaticText(self, -1, "SENSOR DE DESLOCAMENTO 1", (20,20), (-1,-1), wx.ALIGN_CENTER)
                title0.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,40), (-1,-1), wx.ALIGN_RIGHT)
                textoi0 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,65), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt0 = wx.TextCtrl(self, -1, self.lista[0], (200,63), (120,-1), wx.TE_LEFT)
                self.ilvdt0.Disable()
                textoA0 = wx.StaticText(self, -1, "A =", (20,95), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt0 = wx.TextCtrl(self, -1, "%.4f" % self.lista[1], (40,93), (120,-1), wx.TE_LEFT)
                self.alvdt0.Disable()
                textoB0 = wx.StaticText(self, -1, "B =", (178,95), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt0 = wx.TextCtrl(self, -1, "%.4f" % self.lista[2], (200,93), (120,-1), wx.TE_LEFT)
                self.blvdt0.Disable()
                textoC0 = wx.StaticText(self, -1, "Cursor LVDT empregado (mm) =", (20,126), (-1,-1), wx.ALIGN_RIGHT)
                self.c0 = wx.TextCtrl(self, -1, "%.0f" % self.lista[3], (200,123), (120,-1), wx.TE_LEFT)
                self.c0.Disable()

                title1 = wx.StaticText(self, -1, "SENSOR DE DESLOCAMENTO 2", (20,220), (-1,-1), wx.ALIGN_CENTER)
                title1.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,240), (-1,-1), wx.ALIGN_RIGHT)
                textoi1 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,265), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt1 = wx.TextCtrl(self, -1, self.lista[4], (200,263), (120,-1), wx.TE_LEFT)
                self.ilvdt1.Disable()
                textoA1 = wx.StaticText(self, -1, "A =", (20,295), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt1 = wx.TextCtrl(self, -1, "%.4f" % self.lista[5], (40,293), (120,-1), wx.TE_LEFT)
                self.alvdt1.Disable()
                textoB1 = wx.StaticText(self, -1, "B =", (178,295), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt1 = wx.TextCtrl(self, -1, "%.4f" % self.lista[6], (200,293), (120,-1), wx.TE_LEFT)
                self.blvdt1.Disable()
                textoC1 = wx.StaticText(self, -1, "Cursor LVDT empregado (mm) =", (20,326), (-1,-1), wx.ALIGN_RIGHT)
                self.c1 = wx.TextCtrl(self, -1, "%.0f" % self.lista[7], (200,323), (120,-1), wx.TE_LEFT)
                self.c1.Disable()

                self.editar1 = wx.Button(self, -1, 'Editar', (60,400), (-1,-1))
                self.Salvar1 = wx.Button(self, -1, 'Salvar', (200,400), (-1,-1))
                self.Bind(wx.EVT_BUTTON, self.Editar1, self.editar1)
                self.Bind(wx.EVT_BUTTON, self.Salva1, self.Salvar1)
                self.Salvar1.Disable()

        #--------------------------------------------------
        def Editar1(self, event):
                '''Edita...'''
                self.editar1.Disable()
                self.Salvar1.Enable()
                self.ilvdt0.Enable()
                self.alvdt0.Enable()
                self.blvdt0.Enable()
                self.ilvdt1.Enable()
                self.alvdt1.Enable()
                self.blvdt1.Enable()
                self.c0.Enable()
                self.c1.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva1(self, event):
                '''Salva...'''
                II0 = self.ilvdt0.GetValue()
                AA0 = self.alvdt0.GetValue()
                BB0 = self.blvdt0.GetValue()
                II1 = self.ilvdt1.GetValue()
                AA1 = self.alvdt1.GetValue()
                BB1 = self.blvdt1.GetValue()
                CC0 = self.c0.GetValue()
                CC1 = self.c1.GetValue()
                AA0 = format(AA0).replace(',','.')
                BB0 = format(BB0).replace(',','.')
                AA1 = format(AA1).replace(',','.')
                BB1 = format(BB1).replace(',','.')
                CC0 = format(CC0).replace(',','.')
                CC1 = format(CC1).replace(',','.')

                condicional = 0

                try:
                    AA0 = float(AA0)
                    BB0 = float(BB1)
                    AA1 = float(AA1)
                    BB1 = float(BB1)
                    CC0 = float(CC0)
                    CC1 = float(CC1)
                    condicional = 1

                except ValueError:
                    print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                    menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    condicional = -1

                if AA0 == '' or BB0 == '' or AA1 == '' or BB1 == '' or CC0 == '' or CC1 == '':
                    '''Diálogo para Forçar preenchimento dos valores'''
                    dlg = wx.MessageDialog(None, 'É necessário que alguns campos estejam preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

                else:
                    if(condicional>0):
                        bdConfiguration.update_dados_S1S2(II0, AA0, BB0, CC0, II1, AA1, BB1, CC1)
                        self.editar1.Enable()
                        self.Salvar1.Disable()
                        self.ilvdt0.Disable()
                        self.alvdt0.Disable()
                        self.blvdt0.Disable()
                        self.ilvdt1.Disable()
                        self.alvdt1.Disable()
                        self.blvdt1.Disable()
                        self.c0.Disable()
                        self.c1.Disable()
                        self.Update()
                        self.Refresh()

class Page02(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page02, self).__init__(parent)
                self.id = id
                
                colors = bdPreferences.ListColors()
                colorBackground = colors[2]

                self.SetBackgroundColour(colorBackground)
                
                '''Dados do bancodedados'''
                self.lista = bdConfiguration.S3S4()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                title0 = wx.StaticText(self, -1, "SENSOR DE DESLOCAMENTO 3", (20,20), (-1,-1), wx.ALIGN_CENTER)
                title0.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,40), (-1,-1), wx.ALIGN_RIGHT)
                textoi0 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,65), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt0 = wx.TextCtrl(self, -1, self.lista[0], (200,63), (120,-1), wx.TE_LEFT)
                self.ilvdt0.Disable()
                textoA0 = wx.StaticText(self, -1, "A =", (20,95), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt0 = wx.TextCtrl(self, -1, "%.4f" % self.lista[1], (40,93), (120,-1), wx.TE_LEFT)
                self.alvdt0.Disable()
                textoB0 = wx.StaticText(self, -1, "B =", (178,95), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt0 = wx.TextCtrl(self, -1, "%.4f" % self.lista[2], (200,93), (120,-1), wx.TE_LEFT)
                self.blvdt0.Disable()
                textoC0 = wx.StaticText(self, -1, "Cursor LVDT empregado (mm) =", (20,126), (-1,-1), wx.ALIGN_RIGHT)
                self.c0 = wx.TextCtrl(self, -1, "%.0f" % self.lista[3], (200,123), (120,-1), wx.TE_LEFT)
                self.c0.Disable()

                title1 = wx.StaticText(self, -1, "SENSOR DE DESLOCAMENTO 4", (20,220), (-1,-1), wx.ALIGN_CENTER)
                title1.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,240), (-1,-1), wx.ALIGN_RIGHT)
                textoi1 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,265), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt1 = wx.TextCtrl(self, -1, self.lista[4], (200,263), (120,-1), wx.TE_LEFT)
                self.ilvdt1.Disable()
                textoA1 = wx.StaticText(self, -1, "A =", (20,295), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt1 = wx.TextCtrl(self, -1, "%.4f" % self.lista[5], (40,293), (120,-1), wx.TE_LEFT)
                self.alvdt1.Disable()
                textoB1 = wx.StaticText(self, -1, "B =", (178,295), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt1 = wx.TextCtrl(self, -1, "%.4f" % self.lista[6], (200,293), (120,-1), wx.TE_LEFT)
                self.blvdt1.Disable()
                textoC1 = wx.StaticText(self, -1, "Cursor LVDT empregado (mm) =", (20,326), (-1,-1), wx.ALIGN_RIGHT)
                self.c1 = wx.TextCtrl(self, -1, "%.0f" % self.lista[7], (200,323), (120,-1), wx.TE_LEFT)
                self.c1.Disable()

                self.editar2 = wx.Button(self, -1, 'Editar', (60,400), (-1,-1))
                self.Salvar2 = wx.Button(self, -1, 'Salvar', (200,400), (-1,-1))
                self.Bind(wx.EVT_BUTTON, self.Editar2, self.editar2)
                self.Bind(wx.EVT_BUTTON, self.Salva2, self.Salvar2)
                self.Salvar2.Disable()

        #--------------------------------------------------
        def Editar2(self, event):
                '''Edita...'''
                self.editar2.Disable()
                self.Salvar2.Enable()
                self.ilvdt0.Enable()
                self.alvdt0.Enable()
                self.blvdt0.Enable()
                self.ilvdt1.Enable()
                self.alvdt1.Enable()
                self.blvdt1.Enable()
                self.c0.Enable()
                self.c1.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva2(self, event):
                '''Salva...'''
                II0 = self.ilvdt0.GetValue()
                AA0 = self.alvdt0.GetValue()
                BB0 = self.blvdt0.GetValue()
                II1 = self.ilvdt1.GetValue()
                AA1 = self.alvdt1.GetValue()
                BB1 = self.blvdt1.GetValue()
                CC0 = self.c0.GetValue()
                CC1 = self.c1.GetValue()
                AA0 = format(AA0).replace(',','.')
                BB0 = format(BB0).replace(',','.')
                AA1 = format(AA1).replace(',','.')
                BB1 = format(BB1).replace(',','.')
                CC0 = format(CC0).replace(',','.')
                CC1 = format(CC1).replace(',','.')

                condicional = 0

                try:
                    AA0 = float(AA0)
                    BB0 = float(BB1)
                    AA1 = float(AA1)
                    BB1 = float(BB1)
                    CC0 = float(CC0)
                    CC1 = float(CC1)
                    condicional = 1

                except ValueError:
                    print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                    menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    condicional = -1

                if AA0 == '' or BB0 == '' or AA1 == '' or BB1 == '' or CC0 == '' or CC1 == '':
                    '''Diálogo para Forçar preenchimento dos valores'''
                    dlg = wx.MessageDialog(None, 'É necessário que alguns campos estejam preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

                else:
                    if(condicional>0):
                        bdConfiguration.update_dados_S3S4(II0, AA0, BB0, CC0, II1, AA1, BB1, CC1)
                        self.editar2.Enable()
                        self.Salvar2.Disable()
                        self.ilvdt0.Disable()
                        self.alvdt0.Disable()
                        self.blvdt0.Disable()
                        self.ilvdt1.Disable()
                        self.alvdt1.Disable()
                        self.blvdt1.Disable()
                        self.c0.Disable()
                        self.c1.Disable()
                        self.Update()
                        self.Refresh()

class Page03(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page03, self).__init__(parent)
                self.id = id
                
                colors = bdPreferences.ListColors()
                colorBackground = colors[2]

                self.SetBackgroundColour(colorBackground)
                
                '''Dados do bancodedados'''
                self.lista = bdConfiguration.DadosD1()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                title0 = wx.StaticText(self, -1, "(INPUT)", (20,20), (-1,-1), wx.ALIGN_CENTER)
                title0.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,40), (-1,-1), wx.ALIGN_RIGHT)
                textoi0 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,65), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt0 = wx.TextCtrl(self, -1, self.lista[0], (200,63), (120,-1), wx.TE_LEFT)
                self.ilvdt0.Disable()
                textoA0 = wx.StaticText(self, -1, "A =", (20,95), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt0 = wx.TextCtrl(self, -1, "%.4f" % self.lista[1], (40,93), (120,-1), wx.TE_LEFT)
                self.alvdt0.Disable()
                textoB0 = wx.StaticText(self, -1, "B =", (178,95), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt0 = wx.TextCtrl(self, -1, "%.4f" % self.lista[2], (200,93), (120,-1), wx.TE_LEFT)
                self.blvdt0.Disable()
                textoC0 = wx.StaticText(self, -1, "Descrição =", (133,126), (-1,-1), wx.ALIGN_LEFT)
                self.c0 = wx.TextCtrl(self, -1, self.lista[3], (200,123), (120,-1), wx.TE_LEFT)
                self.c0.Disable()

                title1 = wx.StaticText(self, -1, "(OUTPUT)", (20,220), (-1,-1), wx.ALIGN_CENTER)
                title1.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,240), (-1,-1), wx.ALIGN_RIGHT)
                textoi1 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,265), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt1 = wx.TextCtrl(self, -1, self.lista[4], (200,263), (120,-1), wx.TE_LEFT)
                self.ilvdt1.Disable()
                textoA1 = wx.StaticText(self, -1, "A =", (20,295), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt1 = wx.TextCtrl(self, -1, "%.4f" % self.lista[5], (40,293), (120,-1), wx.TE_LEFT)
                self.alvdt1.Disable()
                textoB1 = wx.StaticText(self, -1, "B =", (178,295), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt1 = wx.TextCtrl(self, -1, "%.4f" % self.lista[6], (200,293), (120,-1), wx.TE_LEFT)
                self.blvdt1.Disable()
                textoC1 = wx.StaticText(self, -1, "Descrição =", (133,326), (-1,-1), wx.ALIGN_RIGHT)
                self.c1 = wx.TextCtrl(self, -1, self.lista[7], (200,323), (120,-1), wx.TE_LEFT)
                self.c1.Disable()

                self.editar2 = wx.Button(self, -1, 'Editar', (60,400), (-1,-1))
                self.Salvar2 = wx.Button(self, -1, 'Salvar', (200,400), (-1,-1))
                self.Bind(wx.EVT_BUTTON, self.Editar2, self.editar2)
                self.Bind(wx.EVT_BUTTON, self.Salva2, self.Salvar2)
                self.Salvar2.Disable()

        #--------------------------------------------------
        def Editar2(self, event):
                '''Edita...'''
                self.editar2.Disable()
                self.Salvar2.Enable()
                self.ilvdt0.Enable()
                self.alvdt0.Enable()
                self.blvdt0.Enable()
                self.ilvdt1.Enable()
                self.alvdt1.Enable()
                self.blvdt1.Enable()
                self.c0.Enable()
                self.c1.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva2(self, event):
                '''Salva...'''
                II0 = self.ilvdt0.GetValue()
                AA0 = self.alvdt0.GetValue()
                BB0 = self.blvdt0.GetValue()
                II1 = self.ilvdt1.GetValue()
                AA1 = self.alvdt1.GetValue()
                BB1 = self.blvdt1.GetValue()
                CC0 = self.c0.GetValue()
                CC1 = self.c1.GetValue()
                AA0 = format(AA0).replace(',','.')
                BB0 = format(BB0).replace(',','.')
                AA1 = format(AA1).replace(',','.')
                BB1 = format(BB1).replace(',','.')
                CC0 = format(CC0).replace(',','.')
                CC1 = format(CC1).replace(',','.')

                condicional = 0

                try:
                    AA0 = float(AA0)
                    BB0 = float(BB1)
                    AA1 = float(AA1)
                    BB1 = float(BB1)
                    condicional = 1

                except ValueError:
                    print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                    menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    condicional = -1

                if AA0 == '' or BB0 == '' or AA1 == '' or BB1 == '':
                    '''Diálogo para Forçar preenchimento dos valores'''
                    dlg = wx.MessageDialog(None, 'É necessário que alguns campos estejam preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

                else:
                    if(condicional>0):
                        bdConfiguration.update_dados_D1(II0, AA0, BB0, CC0, II1, AA1, BB1, CC1)
                        self.editar2.Enable()
                        self.Salvar2.Disable()
                        self.ilvdt0.Disable()
                        self.alvdt0.Disable()
                        self.blvdt0.Disable()
                        self.ilvdt1.Disable()
                        self.alvdt1.Disable()
                        self.blvdt1.Disable()
                        self.c0.Disable()
                        self.c1.Disable()
                        self.Update()
                        self.Refresh()

class Page04(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page04, self).__init__(parent)
                self.id = id
                
                colors = bdPreferences.ListColors()
                colorBackground = colors[2]

                self.SetBackgroundColour(colorBackground)
                
                '''Dados do bancodedados'''
                self.lista = bdConfiguration.DadosD2()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                title0 = wx.StaticText(self, -1, "(INPUT)", (20,20), (-1,-1), wx.ALIGN_CENTER)
                title0.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,40), (-1,-1), wx.ALIGN_RIGHT)
                textoi0 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,65), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt0 = wx.TextCtrl(self, -1, self.lista[0], (200,63), (120,-1), wx.TE_LEFT)
                self.ilvdt0.Disable()
                textoA0 = wx.StaticText(self, -1, "A =", (20,95), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt0 = wx.TextCtrl(self, -1, "%.4f" % self.lista[1], (40,93), (120,-1), wx.TE_LEFT)
                self.alvdt0.Disable()
                textoB0 = wx.StaticText(self, -1, "B =", (178,95), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt0 = wx.TextCtrl(self, -1, "%.4f" % self.lista[2], (200,93), (120,-1), wx.TE_LEFT)
                self.blvdt0.Disable()
                textoC0 = wx.StaticText(self, -1, "Descrição =", (133,126), (-1,-1), wx.ALIGN_RIGHT)
                self.c0 = wx.TextCtrl(self, -1, self.lista[3], (200,123), (120,-1), wx.TE_LEFT)
                self.c0.Disable()

                title1 = wx.StaticText(self, -1, "(OUTPUT)", (20,220), (-1,-1), wx.ALIGN_CENTER)
                title1.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,240), (-1,-1), wx.ALIGN_RIGHT)
                textoi1 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,265), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt1 = wx.TextCtrl(self, -1, self.lista[4], (200,263), (120,-1), wx.TE_LEFT)
                self.ilvdt1.Disable()
                textoA1 = wx.StaticText(self, -1, "A =", (20,295), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt1 = wx.TextCtrl(self, -1, "%.4f" % self.lista[5], (40,293), (120,-1), wx.TE_LEFT)
                self.alvdt1.Disable()
                textoB1 = wx.StaticText(self, -1, "B =", (178,295), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt1 = wx.TextCtrl(self, -1, "%.4f" % self.lista[6], (200,293), (120,-1), wx.TE_LEFT)
                self.blvdt1.Disable()
                textoC1 = wx.StaticText(self, -1, "Descrição =", (133,326), (-1,-1), wx.ALIGN_RIGHT)
                self.c1 = wx.TextCtrl(self, -1, self.lista[7], (200,323), (120,-1), wx.TE_LEFT)
                self.c1.Disable()

                self.editar2 = wx.Button(self, -1, 'Editar', (60,400), (-1,-1))
                self.Salvar2 = wx.Button(self, -1, 'Salvar', (200,400), (-1,-1))
                self.Bind(wx.EVT_BUTTON, self.Editar2, self.editar2)
                self.Bind(wx.EVT_BUTTON, self.Salva2, self.Salvar2)
                self.Salvar2.Disable()

        #--------------------------------------------------
        def Editar2(self, event):
                '''Edita...'''
                self.editar2.Disable()
                self.Salvar2.Enable()
                self.ilvdt0.Enable()
                self.alvdt0.Enable()
                self.blvdt0.Enable()
                self.ilvdt1.Enable()
                self.alvdt1.Enable()
                self.blvdt1.Enable()
                self.c0.Enable()
                self.c1.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva2(self, event):
                '''Salva...'''
                II0 = self.ilvdt0.GetValue()
                AA0 = self.alvdt0.GetValue()
                BB0 = self.blvdt0.GetValue()
                II1 = self.ilvdt1.GetValue()
                AA1 = self.alvdt1.GetValue()
                BB1 = self.blvdt1.GetValue()
                CC0 = self.c0.GetValue()
                CC1 = self.c1.GetValue()
                AA0 = format(AA0).replace(',','.')
                BB0 = format(BB0).replace(',','.')
                AA1 = format(AA1).replace(',','.')
                BB1 = format(BB1).replace(',','.')
                CC0 = format(CC0).replace(',','.')
                CC1 = format(CC1).replace(',','.')

                condicional = 0

                try:
                    AA0 = float(AA0)
                    BB0 = float(BB1)
                    AA1 = float(AA1)
                    BB1 = float(BB1)
                    condicional = 1

                except ValueError:
                    print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                    menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    condicional = -1

                if AA0 == '' or BB0 == '' or AA1 == '' or BB1 == '':
                    '''Diálogo para Forçar preenchimento dos valores'''
                    dlg = wx.MessageDialog(None, 'É necessário que alguns campos estejam preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

                else:
                    if(condicional>0):
                        bdConfiguration.update_dados_D2(II0, AA0, BB0, CC0, II1, AA1, BB1, CC1)
                        self.editar2.Enable()
                        self.Salvar2.Disable()
                        self.ilvdt0.Disable()
                        self.alvdt0.Disable()
                        self.blvdt0.Disable()
                        self.ilvdt1.Disable()
                        self.alvdt1.Disable()
                        self.blvdt1.Disable()
                        self.c0.Disable()
                        self.c1.Disable()
                        self.Update()
                        self.Refresh()

class Page05(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page05, self).__init__(parent)
                self.id = id
                
                colors = bdPreferences.ListColors()
                colorBackground = colors[2]

                self.SetBackgroundColour(colorBackground)
                
                '''Dados do bancodedados'''
                self.lista = bdConfiguration.DadosMT()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                title0 = wx.StaticText(self, -1, "MOTOR DE PASSOS", (20,20), (-1,-1), wx.ALIGN_CENTER)
                title0.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,40), (-1,-1), wx.ALIGN_RIGHT)
                textoi0 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,65), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt0 = wx.TextCtrl(self, -1, self.lista[0], (200,63), (120,-1), wx.TE_LEFT)
                self.ilvdt0.Disable()
                textoA0 = wx.StaticText(self, -1, "A =", (20,95), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt0 = wx.TextCtrl(self, -1, "%.4f" % self.lista[1], (40,93), (120,-1), wx.TE_LEFT)
                self.alvdt0.Disable()
                textoB0 = wx.StaticText(self, -1, "B =", (178,95), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt0 = wx.TextCtrl(self, -1, "%.4f" % self.lista[2], (200,93), (120,-1), wx.TE_LEFT)
                self.blvdt0.Disable()
                textoC0 = wx.StaticText(self, -1, "Descrição =", (20,126), (-1,-1), wx.ALIGN_RIGHT)
                self.c0 = wx.TextCtrl(self, -1, self.lista[3], (200,123), (120,-1), wx.TE_LEFT)
                self.c0.Disable()

                self.editar2 = wx.Button(self, -1, 'Editar', (60,400), (-1,-1))
                self.Salvar2 = wx.Button(self, -1, 'Salvar', (200,400), (-1,-1))
                self.Bind(wx.EVT_BUTTON, self.Editar2, self.editar2)
                self.Bind(wx.EVT_BUTTON, self.Salva2, self.Salvar2)
                self.Salvar2.Disable()

        #--------------------------------------------------
        def Editar2(self, event):
                '''Edita...'''
                self.editar2.Disable()
                self.Salvar2.Enable()
                self.ilvdt0.Enable()
                self.alvdt0.Enable()
                self.blvdt0.Enable()
                self.c0.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva2(self, event):
                '''Salva...'''
                II0 = self.ilvdt0.GetValue()
                AA0 = self.alvdt0.GetValue()
                BB0 = self.blvdt0.GetValue()
                CC0 = self.c0.GetValue()
                AA0 = format(AA0).replace(',','.')
                BB0 = format(BB0).replace(',','.')
                CC0 = format(CC0).replace(',','.')

                condicional = 0

                try:
                    AA0 = float(AA0)
                    BB0 = float(BB1)
                    condicional = 1

                except ValueError:
                    print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                    menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    condicional = -1

                if AA0 == '' or BB0 == '':
                    '''Diálogo para Forçar preenchimento dos valores'''
                    dlg = wx.MessageDialog(None, 'É necessário que alguns campos estejam preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

                else:
                    if(condicional>0):
                        bdConfiguration.update_dados_D2(II0, AA0, BB0, CC0)
                        self.editar2.Enable()
                        self.Salvar2.Disable()
                        self.ilvdt0.Disable()
                        self.alvdt0.Disable()
                        self.blvdt0.Disable()
                        self.c0.Disable()
                        self.Update()
                        self.Refresh()

class Page06(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page06, self).__init__(parent)
                self.id = id
                
                colors = bdPreferences.ListColors()
                colorBackground = colors[2]

                self.SetBackgroundColour(colorBackground)
                
                '''Dados do bancodedados'''
                A1 = bdConfiguration.DadosCL()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                title0 = wx.StaticText(self, -1, "CILINDRO PNEUMÁTICO", (20,20), (-1,-1), wx.ALIGN_CENTER)
                title0.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Área interna do cilindro em (mm)²", (20,40), (-1,-1), wx.ALIGN_RIGHT)
                textoA1 = wx.StaticText(self, -1, "A1 =", (20,75), (-1,-1), wx.ALIGN_RIGHT)
                self.A1= wx.TextCtrl(self, -1, "%.6f" % A1, (47,73), (120,-1), wx.TE_LEFT)
                self.A1.Disable()

                self.editar2 = wx.Button(self, -1, 'Editar', (60,400), (-1,-1))
                self.Salvar2 = wx.Button(self, -1, 'Salvar', (200,400), (-1,-1))
                self.Bind(wx.EVT_BUTTON, self.Editar2, self.editar2)
                self.Bind(wx.EVT_BUTTON, self.Salva2, self.Salvar2)
                self.Salvar2.Disable()

        #--------------------------------------------------
        def Editar2(self, event):
                '''Edita...'''
                self.editar2.Disable()
                self.Salvar2.Enable()
                self.A1.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva2(self, event):
                '''Salva...'''
                AA1 = self.A1.GetValue()
                AA1 = format(AA1).replace(',','.')

                condicional = 0

                try:
                    AA1 = float(AA1)
                    condicional = 1

                except ValueError:
                    print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                    menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    condicional = -1

                if AA1 == '':
                    '''Diálogo para Forçar preenchimento dos valores'''
                    dlg = wx.MessageDialog(None, 'É necessário que alguns campos estejam preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

                else:
                    if(condicional>0):
                        bdConfiguration.update_dados_CL(AA1)
                        self.editar2.Enable()
                        self.Salvar2.Disable()
                        self.A1.Disable()
                        self.Update()
                        self.Refresh()