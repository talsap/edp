# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
'''import bancodedados'''
'''from novoensaio import TelaNovoEnsaio'''

'''Tela Selecão de Ensaio'''
class TelaNovo(wx.Frame):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, None, -1, 'EDP - Beta', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Iserção do IconeLogo'''
            ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)

            '''Configurações do Size'''
            self.SetSize((450,200))
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self)

            self.FontTitle =wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            self.title = wx.StaticText(panel, label = "ENSAIOS DINÂMICOS" ,style = wx.ALIGN_CENTRE)
            self.title.SetFont(self.FontTitle)
            v_sizer.Add(self.title, 0 ,wx.ALIGN_CENTER_HORIZONTAL |wx.ALL, 20)
            texto1 = wx.StaticText(panel,label = "NORMAS",style = wx.ALIGN_CENTRE)

            h_sizer.Add(texto1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
            languages = ['C', 'C++', 'Python', 'Java', 'Perl']
            self.combo = wx.ComboBox(panel, choices = languages, style = wx.EXPAND)

            h_sizer.Add(self.combo,1,wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)
            h_sizer.AddStretchSpacer(40)
            v_sizer.Add(h_sizer,1,wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)

            v_sizer.AddStretchSpacer()
            '''self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo)'''

            panel.SetSizer(v_sizer)
            self.Centre()
            self.Show()


    #--------------------------------------------------
        def Prosseguir(self, event):
            a = self.date.GetValue()
            b = self.localColeta.GetValue()
            c = self.operador.GetValue()
            d = self.profundidade.GetValue()
            d = format(d).replace(',','.')
            d = format(d).replace('-','')
            e = self.identificador.GetValue()

    #--------------------------------------------------
            try:
                if d!= '':
                    d = float(d)

            except ValueError:
                print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada', 'EAU', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                d = -1

    #--------------------------------------------------
            self.identificadorCadastrados = bancodedados.ler_IDE()

            if d<0 or d>=0 or d == '':
                if e in self.identificadorCadastrados:
                    print('Ja existe esse identificador')
                    menssagError = wx.MessageDialog(self, 'Já existe um ensaio com esse identificador', 'EAU', wx.OK|wx.ICON_INFORMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                else:
                    self.Close(True)
                    con = TelaNovoEnsaio(a, b, c, d, e)
                    resultado = con.ShowModal()

            else:
                print('Algum dos campos esta digitado errado')
