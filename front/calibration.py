# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import bancodedados

'''Tela Calibração'''
class Cal(wx.Frame):
        #--------------------------------------------------
        def __init__(self, *args, **kwargs):
                wx.Frame.__init__(self, None, -1, 'EDP - Curva de Calibração', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

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

                # adicione as páginas ao caderno com o rótulo para mostrar na guia
                nb.AddPage(page01, "DNIT 134")
                nb.AddPage(page02, "DNIT 135")

                sizer = wx.BoxSizer()
                sizer.Add(nb, 1, wx.EXPAND)
                panel.SetSizer(sizer)
                self.SetSize((360,520))
                self.Centre()
                self.Show()

class Page01(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page01, self).__init__(parent)
                self.id = id

                '''Dados do bancodedados'''
                self.lista = bancodedados.LVDT_134()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                title0 = wx.StaticText(self, -1, "SENSOR DE DESLOCAMENTO 1", (20,20), (-1,-1), wx.ALIGN_CENTER)
                title0.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,40), (-1,-1), wx.ALIGN_RIGHT)
                textoi0 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,65), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt0 = wx.TextCtrl(self, -1, self.lista[0], (200,63), (120,-1), wx.TE_LEFT)
                self.ilvdt0.Disable()
                textoA0 = wx.StaticText(self, -1, "A =", (20,95), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt0 = wx.TextCtrl(self, -1, "%.12f" % self.lista[1], (40,93), (120,-1), wx.TE_LEFT)
                self.alvdt0.Disable()
                textoB0 = wx.StaticText(self, -1, "B =", (178,95), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt0 = wx.TextCtrl(self, -1, "%.12f" % self.lista[2], (200,93), (120,-1), wx.TE_LEFT)
                self.blvdt0.Disable()

                title1 = wx.StaticText(self, -1, "SENSOR DE DESLOCAMENTO 2", (20,220), (-1,-1), wx.ALIGN_CENTER)
                title1.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,240), (-1,-1), wx.ALIGN_RIGHT)
                textoi1 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,265), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt1 = wx.TextCtrl(self, -1, self.lista[3], (200,263), (120,-1), wx.TE_LEFT)
                self.ilvdt1.Disable()
                textoA1 = wx.StaticText(self, -1, "A =", (20,295), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt1 = wx.TextCtrl(self, -1, "%.12f" % self.lista[4], (40,293), (120,-1), wx.TE_LEFT)
                self.alvdt1.Disable()
                textoB1 = wx.StaticText(self, -1, "B =", (178,295), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt1 = wx.TextCtrl(self, -1, "%.12f" % self.lista[5], (200,293), (120,-1), wx.TE_LEFT)
                self.blvdt1.Disable()

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
                AA0 = format(AA0).replace(',','.')
                BB0 = format(BB0).replace(',','.')
                AA1 = format(AA1).replace(',','.')
                BB1 = format(BB1).replace(',','.')
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
                        bancodedados.update_dados_LVDT_134(II0, AA0, BB0, II1, AA1, BB1)
                        self.editar1.Enable()
                        self.Salvar1.Disable()
                        self.ilvdt0.Disable()
                        self.alvdt0.Disable()
                        self.blvdt0.Disable()
                        self.ilvdt1.Disable()
                        self.alvdt1.Disable()
                        self.blvdt1.Disable()
                        self.Update()
                        self.Refresh()

class Page02(wx.Panel):
        #--------------------------------------------------
        def __init__(self, parent, id):
                super(Page02, self).__init__(parent)
                self.id = id

                '''Dados do bancodedados'''
                self.lista = bancodedados.LVDT_135()

                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                title0 = wx.StaticText(self, -1, "SENSOR DE DESLOCAMENTO 3", (20,20), (-1,-1), wx.ALIGN_CENTER)
                title0.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,40), (-1,-1), wx.ALIGN_RIGHT)
                textoi0 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,65), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt0 = wx.TextCtrl(self, -1, self.lista[0], (200,63), (120,-1), wx.TE_LEFT)
                self.ilvdt0.Disable()
                textoA0 = wx.StaticText(self, -1, "A =", (20,95), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt0 = wx.TextCtrl(self, -1, "%.12f" % self.lista[1], (40,93), (120,-1), wx.TE_LEFT)
                self.alvdt0.Disable()
                textoB0 = wx.StaticText(self, -1, "B =", (178,95), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt0 = wx.TextCtrl(self, -1, "%.12f" % self.lista[2], (200,93), (120,-1), wx.TE_LEFT)
                self.blvdt0.Disable()

                title1 = wx.StaticText(self, -1, "SENSOR DE DESLOCAMENTO 4", (20,220), (-1,-1), wx.ALIGN_CENTER)
                title1.SetFont(FontTitle)
                texto1 = wx.StaticText(self, -1, "Curva do tipo Ax + B", (20,240), (-1,-1), wx.ALIGN_RIGHT)
                textoi1 = wx.StaticText(self, -1, "IDENTIFICADOR =", (100,265), (-1,-1), wx.ALIGN_RIGHT)
                self.ilvdt1 = wx.TextCtrl(self, -1, self.lista[3], (200,263), (120,-1), wx.TE_LEFT)
                self.ilvdt1.Disable()
                textoA1 = wx.StaticText(self, -1, "A =", (20,295), (-1,-1), wx.ALIGN_RIGHT)
                self.alvdt1 = wx.TextCtrl(self, -1, "%.12f" % self.lista[4], (40,293), (120,-1), wx.TE_LEFT)
                self.alvdt1.Disable()
                textoB1 = wx.StaticText(self, -1, "B =", (178,295), (-1,-1), wx.ALIGN_RIGHT)
                self.blvdt1 = wx.TextCtrl(self, -1, "%.12f" % self.lista[5], (200,293), (120,-1), wx.TE_LEFT)
                self.blvdt1.Disable()

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
                AA0 = format(AA0).replace(',','.')
                BB0 = format(BB0).replace(',','.')
                AA1 = format(AA1).replace(',','.')
                BB1 = format(BB1).replace(',','.')
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
                        bancodedados.update_dados_LVDT_135(II0, AA0, BB0, II1, AA1, BB1)
                        self.editar2.Enable()
                        self.Salvar2.Disable()
                        self.ilvdt0.Disable()
                        self.alvdt0.Disable()
                        self.blvdt0.Disable()
                        self.ilvdt1.Disable()
                        self.alvdt1.Disable()
                        self.blvdt1.Disable()
                        self.Update()
                        self.Refresh()
