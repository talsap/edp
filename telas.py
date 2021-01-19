# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import wx.adv
'''from TelaRealizacaoEnsaioDNIT134 import TelaRealizacaoEnsaioDNIT134'''

'''Tela Selecão de Ensaio'''
class TelaNovoEnsaioDNIT134(wx.Frame):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, None, -1, 'EDP - CABEÇALHO', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Iserção do IconeLogo'''
            ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)

            '''Configurações do Size'''
            self.SetSize((650,400))
            sizer = wx.BoxSizer(wx.VERTICAL)
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            v1_sizer = wx.BoxSizer(wx.VERTICAL)
            v2_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h4_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h6_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h7_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h8_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.panel = wx.Panel(self)

            logo = wx.Button(self.panel, -1, 'Logo')
            previsualizar = wx.Button(self.panel, -1, 'Pré-Visualizar')
            previsualizar.SetForegroundColour((119,118,114))

            v1_sizer.AddStretchSpacer(10)
            v1_sizer.Add(logo, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
            v1_sizer.AddStretchSpacer(1)
            v1_sizer.Add(previsualizar, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
            v1_sizer.AddStretchSpacer(10)

            texto1 = wx.StaticText(self.panel, label = "Identificador", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(texto1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.Identificador = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h2_sizer.Add(self.Identificador, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            h2_sizer.AddStretchSpacer(9)

            texto2 = wx.StaticText(self.panel, label = "Empresa/Instituição", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(texto2, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.empresa = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h3_sizer.Add(self.empresa, 5, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto3 = wx.StaticText(self.panel, label = "Fantasia", style = wx.ALIGN_RIGHT)
            h3_sizer.AddStretchSpacer(1)
            h3_sizer.Add(texto3, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.fantasia = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h3_sizer.Add(self.fantasia, 6, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            texto4 = wx.StaticText(self.panel, label = "CPF/CNPJ", style = wx.ALIGN_RIGHT)
            h4_sizer.Add(texto4, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cpfcnpj = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h4_sizer.Add(self.cpfcnpj, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto5 = wx.StaticText(self.panel, label = "E-mail", style = wx.ALIGN_RIGHT)
            h4_sizer.AddStretchSpacer(1)
            h4_sizer.Add(texto5, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.email = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h4_sizer.Add(self.email, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            texto6 = wx.StaticText(self.panel, label = "Fone", style = wx.ALIGN_RIGHT)
            h5_sizer.Add(texto6, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.fone = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h5_sizer.Add(self.fone, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto7 = wx.StaticText(self.panel, label = "UF", style = wx.ALIGN_RIGHT)
            h5_sizer.AddStretchSpacer(1)
            h5_sizer.Add(texto7, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.uf = wx.TextCtrl(self.panel, -1, '', size=(25,23), style = wx.TE_RIGHT)
            h5_sizer.Add(self.uf, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            h5_sizer.AddStretchSpacer(1)
            texto8 = wx.StaticText(self.panel, label = "Cidade", style = wx.ALIGN_RIGHT)
            h5_sizer.Add(texto8, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cidade = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h5_sizer.Add(self.cidade, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            texto9 = wx.StaticText(self.panel, label = "Bairro", style = wx.ALIGN_RIGHT)
            h6_sizer.Add(texto9, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.bairro = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h6_sizer.Add(self.bairro, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto10 = wx.StaticText(self.panel, label = "Rua", style = wx.ALIGN_RIGHT)
            h6_sizer.AddStretchSpacer(1)
            h6_sizer.Add(texto10, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.rua = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h6_sizer.Add(self.rua, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            h6_sizer.AddStretchSpacer(1)
            texto11 = wx.StaticText(self.panel, label = "Nº", style = wx.ALIGN_RIGHT)
            h6_sizer.Add(texto11, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.numero = wx.TextCtrl(self.panel, -1, '', size=(25,23), style = wx.TE_RIGHT)
            h6_sizer.Add(self.numero, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            texto12 = wx.StaticText(self.panel, label = "CEP", style = wx.ALIGN_RIGHT)
            h7_sizer.Add(texto12, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cep = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h7_sizer.Add(self.cep, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto13 = wx.StaticText(self.panel, label = "Complemento", style = wx.ALIGN_RIGHT)
            h7_sizer.AddStretchSpacer(1)
            h7_sizer.Add(texto13, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.complemento = wx.TextCtrl(self.panel, -1, '', style = wx.TE_RIGHT)
            h7_sizer.Add(self.complemento, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v2_sizer.AddStretchSpacer(1)
            v2_sizer.Add(h2_sizer, 1)
            v2_sizer.AddStretchSpacer(1)
            v2_sizer.Add(h3_sizer, 1)
            v2_sizer.AddStretchSpacer(1)
            v2_sizer.Add(h4_sizer, 1)
            v2_sizer.AddStretchSpacer(1)
            v2_sizer.Add(h5_sizer, 1)
            v2_sizer.AddStretchSpacer(1)
            v2_sizer.Add(h6_sizer, 1)
            v2_sizer.AddStretchSpacer(1)
            v2_sizer.Add(h7_sizer, 1)
            v2_sizer.AddStretchSpacer(8)

            h_sizer.Add(v1_sizer, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            h_sizer.Add(v2_sizer, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

            salvar = wx.Button(self.panel, -1, 'Salvar')
            sair = wx.Button(self.panel, -1, 'Sair')

            h1_sizer.AddStretchSpacer(5)
            h1_sizer.Add(salvar, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            h1_sizer.Add(sair, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            h1_sizer.AddStretchSpacer(5)

            v_sizer.Add(h_sizer, 2)
            v_sizer.Add(h1_sizer, 0)
            sizer.Add(v_sizer, 0,  wx.EXPAND | wx.ALL, 15)

            self.Bind(wx.EVT_PAINT, self.OnPaint)

            self.panel.SetSizer(sizer)
            self.Centre()
            self.Show()
    #--------------------------------------------------
        def OnPaint(self, event):
            dc = wx.ClientDC(self.panel)

            dc.SetPen(wx.Pen('#4c4c4c', 1, wx.SOLID))
            dc.DrawRectangle(20, 30, 90, 90)

    #--------------------------------------------------
        def Prosseguir(self, event):
            self.Close(True)
            frame = TelaRealizacaoEnsaioDNIT134()



if __name__ == "__main__":
		app = wx.App()
		frame = TelaNovoEnsaioDNIT134()
		frame.Show()
		app.MainLoop()
