# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import bancodedados

'''Tela Calibração'''
class Cal(wx.Frame):
        #--------------------------------------------------
        def __init__(self, *args, **kwargs):
                wx.Frame.__init__(self, None, -1, 'EDP - Calibração', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

                '''Iserção do IconeLogo'''
                try:
                    ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                    self.SetIcon(ico)
                except:
                    pass

                '''Configurações do Size'''
                self.SetSize((360,520))
                v_sizer = wx.BoxSizer(wx.VERTICAL)
                v1_sizer = wx.BoxSizer(wx.VERTICAL)
                v2_sizer = wx.BoxSizer(wx.VERTICAL)
                h_sizer = wx.BoxSizer(wx.HORIZONTAL)
                h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
                h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
                panel = wx.Panel(self)

                '''Dados do bancodedados'''
                lista = bancodedados.LVDT()

                '''Utilitários da Tela'''
                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

                title0 = wx.StaticText(panel, label = "LVDT 0", style = wx.ALIGN_CENTRE)
                title0.SetFont(FontTitle)
                texto1 = wx.StaticText(panel, label = "Curva do tipo Ax + B", style = wx.ALIGN_RIGHT)

                textoA0 = wx.StaticText(panel, label = "A =", style = wx.ALIGN_RIGHT)
                self.alvdt0 = wx.TextCtrl(panel, -1, "%.5f" % lista[0], style = wx.TE_LEFT)
                self.alvdt0.Disable()
                textoB0 = wx.StaticText(panel, label = "B =", style = wx.ALIGN_RIGHT)
                self.blvdt0 = wx.TextCtrl(panel, -1, "%.5f" % lista[1], style = wx.TE_LEFT)
                self.blvdt0.Disable()

                title1 = wx.StaticText(panel, label = "LVDT 1", style = wx.ALIGN_CENTRE)
                title1.SetFont(FontTitle)
                texto2 = wx.StaticText(panel, label = "Curva do tipo Ax + B", style = wx.ALIGN_RIGHT)

                textoA1 = wx.StaticText(panel, label = "A =", style = wx.ALIGN_RIGHT)
                self.alvdt1 = wx.TextCtrl(panel, -1, "%.5f" % lista[2], style = wx.TE_LEFT)
                self.alvdt1.Disable()
                textoB1 = wx.StaticText(panel, label = "B =", style = wx.ALIGN_RIGHT)
                self.blvdt1 = wx.TextCtrl(panel, -1, "%.5f" % lista[3], style = wx.TE_LEFT)
                self.blvdt1.Disable()

                self.editar = wx.Button(panel, -1, 'Editar')
                self.Salvar = wx.Button(panel, -1, 'Salvar')
                self.Bind(wx.EVT_BUTTON, self.Editar, self.editar)
                self.Bind(wx.EVT_BUTTON, self.Salva, self.Salvar)
                self.Salvar.Disable()

                '''Organização dos Sizes'''
                h1_sizer.Add(textoA0, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
                h1_sizer.Add(self.alvdt0, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
                h1_sizer.Add(textoB0, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
                h1_sizer.Add(self.blvdt0, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

                h2_sizer.Add(textoA1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
                h2_sizer.Add(self.alvdt1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
                h2_sizer.Add(textoB1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
                h2_sizer.Add(self.blvdt1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

                v1_sizer.Add(title0)
                v1_sizer.Add(texto1, 1)
                v1_sizer.Add(h1_sizer, 1)
                v1_sizer.AddStretchSpacer(2)

                v2_sizer.Add(title1)
                v2_sizer.Add(texto2, 1)
                v2_sizer.Add(h2_sizer, 1)
                v2_sizer.AddStretchSpacer(2)

                v_sizer.Add(v1_sizer, 4, wx.EXPAND | wx.ALL, 12)
                v_sizer.Add(v2_sizer, 4, wx.EXPAND | wx.ALL, 12)
                h_sizer.Add(self.editar, 10, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
                h_sizer.Add(self.Salvar, 10, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
                v_sizer.Add(h_sizer, 1, wx.EXPAND | wx.ALL, 12)

                panel.SetSizer(v_sizer)
                self.Centre()
                self.Show()

        #--------------------------------------------------
        def Editar(self, event):
            '''Edita...'''
            self.editar.Disable()
            self.Salvar.Enable()
            self.alvdt0.Enable()
            self.blvdt0.Enable()
            self.alvdt1.Enable()
            self.blvdt1.Enable()

        #--------------------------------------------------
        def Salva(self, event):
            '''Salva...'''
            AA0 = self.alvdt0.GetValue()
            BB0 = self.blvdt0.GetValue()
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
                '''Diálogo para Forçar preenchimento do Identificador'''
                dlg = wx.MessageDialog(None, 'É necessário que os campos estejam todos preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()

            else:
                if(condicional>0):
                    bancodedados.update_dados_LVDT(AA0, BB0, AA1, BB1)
                    self.editar.Enable()
                    self.Salvar.Disable()
                    self.alvdt0.Disable()
                    self.blvdt0.Disable()
                    self.alvdt1.Disable()
                    self.blvdt1.Disable()
