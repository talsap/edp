# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import wx.adv
from TelaRealizacaoEnsaioDNIT134 import TelaRealizacaoEnsaioDNIT134

'''Tela Selecão de Ensaio'''
class TelaNovoEnsaioDNIT134(wx.Frame):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, None, -1, 'EDP - DNIT 134/2018ME', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Iserção do IconeLogo'''
            ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)

            '''Configurações do Size'''
            self.SetSize((500,410))
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
            panel = wx.Panel(self)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            title = wx.StaticText(panel, label = "Dados do Ensaio", style = wx.ALIGN_CENTRE)
            title.SetFont(FontTitle)
            '''title.SetBackgroundColour("green")'''
            v_sizer.Add(title, 1, wx.EXPAND | wx.ALL)

            texto1 = wx.StaticText(panel, label = "Identificador", style = wx.ALIGN_RIGHT)
            h_sizer.Add(texto1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.Identificador = wx.TextCtrl(panel, -1, 'DNIT 134/2018', style = wx.TE_RIGHT)
            h_sizer.Add(self.Identificador, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto2 = wx.StaticText(panel, label = "C.P. Nº", style = wx.ALIGN_RIGHT)
            h_sizer.Add(texto2, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cp = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h_sizer.Add(self.cp, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h_sizer, 1, wx.EXPAND | wx.ALL)

            texto3 = wx.StaticText(panel, label = "Rodovia", style = wx.ALIGN_RIGHT)
            h1_sizer.Add(texto3, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.rodovia = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h1_sizer.Add(self.rodovia, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto4 = wx.StaticText(panel, label = "Origem", style = wx.ALIGN_RIGHT)
            h1_sizer.Add(texto4, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.origem = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h1_sizer.Add(self.origem, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h1_sizer, 1, wx.EXPAND | wx.ALL)

            texto5 = wx.StaticText(panel, label = "Trecho", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(texto5, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.trecho = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h2_sizer.Add(self.trecho, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto6 = wx.StaticText(panel, label = "Est/km", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(texto6, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.est = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h2_sizer.Add(self.est, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h2_sizer, 1, wx.EXPAND | wx.ALL)

            texto7 = wx.StaticText(panel, label = "Operador", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(texto7, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.operador = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h3_sizer.Add(self.operador, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto8 = wx.StaticText(panel, label = "Interesse", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(texto8, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.interesse = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h3_sizer.Add(self.interesse, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h3_sizer, 1, wx.EXPAND | wx.ALL)

            texto9 = wx.StaticText(panel, label = "Data", style = wx.ALIGN_RIGHT)
            h4_sizer.Add(texto9, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.date = wx.adv.DatePickerCtrl(panel, id = wx.ID_ANY, dt = wx.DefaultDateTime, size = wx.DefaultSize, style = wx.adv.DP_SHOWCENTURY | wx.adv.DP_DROPDOWN , validator = wx.DefaultValidator, name = "datectrl")
            h4_sizer.Add(self.date, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h4_sizer, 1, wx.EXPAND | wx.ALL)
            texto10 = wx.StaticText(panel, label = "Diâmetro C.P. (mm)", style = wx.ALIGN_RIGHT)
            h5_sizer.Add(texto10, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.diametro = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h5_sizer.Add(self.diametro, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h5_sizer, 1, wx.EXPAND | wx.ALL)
            texto11 = wx.StaticText(panel, label = "Altura C.P. (mm)", style = wx.ALIGN_RIGHT)
            h6_sizer.Add(texto11, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.altura = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h6_sizer.Add(self.altura, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h6_sizer, 1, wx.EXPAND | wx.ALL)

            staticbox = wx.StaticBox(panel, -1, '')
            staticboxSizer = wx.StaticBoxSizer(staticbox, wx.VERTICAL)
            texto12 = wx.StaticText(panel, label = "Amostra", style = wx.ALIGN_RIGHT)
            tipoAmostras = ['Deformada', 'Indeformada']
            self.amostra = wx.RadioBox(panel, label = '', choices = tipoAmostras, majorDimension = 1, style = wx.RA_SPECIFY_COLS)
            v2_sizer.Add(texto12, 0, wx.ALL|wx.CENTER)
            v2_sizer.Add(self.amostra, 0, wx.ALL|wx.CENTER)
            staticboxSizer.Add(v2_sizer, 0, wx.ALL|wx.CENTER)

            h7_sizer.AddStretchSpacer(2)
            h7_sizer.Add(staticboxSizer, 3, wx.EXPAND | wx.ALL, 1)
            h7_sizer.AddStretchSpacer(1)
            h7_sizer.Add(v1_sizer, 3, wx.EXPAND | wx.ALL)

            v_sizer.Add(h7_sizer, 3, wx.EXPAND | wx.ALL)

            texto13 = wx.StaticText(panel, label = "Energia", style = wx.ALIGN_RIGHT)
            h8_sizer.Add(texto13, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.energia = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h8_sizer.Add(self.energia, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto14 = wx.StaticText(panel, label = "Dist.Ap.(mm)", style = wx.ALIGN_RIGHT)
            h8_sizer.Add(texto14, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
            self.distAp = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h8_sizer.Add(self.distAp, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h8_sizer, 1, wx.EXPAND | wx.ALL)

            texto15 = wx.StaticText(panel, label = "Observações", style = wx.ALIGN_RIGHT)
            h9_sizer.Add(texto15, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.obs = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            h9_sizer.Add(self.obs, 5, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h9_sizer, 1, wx.EXPAND | wx.ALL)
            '''v_sizer.AddStretchSpacer(1)'''

            continuar = wx.Button(panel, -1, 'Continuar')
            continuar.Bind(wx.EVT_BUTTON, self.Prosseguir)
            v_sizer.Add(continuar, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            sizer.Add(v_sizer, 0,  wx.EXPAND | wx.ALL, 15)

            panel.SetSizer(sizer)
            self.Centre()
            self.Show()

    #--------------------------------------------------
        def Prosseguir(self, event):
            self.Close(True)
            frame = TelaRealizacaoEnsaioDNIT134()
