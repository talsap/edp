# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import wx.adv
import banco.bancodedados as bancodedados
import banco.bdConfiguration as bdConfiguration
from TelaRealizacaoEnsaioDNIT179 import TelaRealizacaoEnsaioDNIT179
import back.HexForRGB as HexRGB
import banco.bdPreferences as bdPreferences

'''Tela Selecão de Ensaio'''
class TelaNovoEnsaioDNIT179(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'EDP - Ensaios Dinâmicos para Pavimentação - DNIT 179/2018IE', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
            self.Bind(wx.EVT_CLOSE, self.onExit)
            
            colors = bdPreferences.ListColors()
            colorBackground = colors[2]

            self.SetBackgroundColour(colorBackground)
            
            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

            '''Configurações do Size'''
            self.SetSize((600,410))
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
            h10_sizer = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            title = wx.StaticText(panel, label = "Dados do Ensaio", style = wx.ALIGN_CENTRE)
            title.SetFont(FontTitle)
            v_sizer.Add(title, 1, wx.EXPAND | wx.ALL)

            texto1 = wx.StaticText(panel, label = "Identificação", style = wx.ALIGN_RIGHT)
            h_sizer.Add(texto1, 96, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.Identificador = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            self.Identificador.SetMaxLength(15)
            h_sizer.Add(self.Identificador, 32, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto2 = wx.StaticText(panel, label = "Pares de Tensão (MPa)", style = wx.ALIGN_RIGHT)
            h_sizer.Add(texto2, 83, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.Pares = wx.ComboBox(panel, choices = bdConfiguration.Pares_Tensoes(), style = wx.ALL | wx.CB_READONLY)
            self.Pares.SetSelection(0)
            h_sizer.Add(self.Pares, 60, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h_sizer, 1, wx.EXPAND | wx.ALL)

            texto16 = wx.StaticText(panel, label = "Responsável Técnico", style = wx.ALIGN_RIGHT)
            h10_sizer.Add(texto16, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.responsavel = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            self.responsavel.SetMaxLength(30)
            h10_sizer.Add(self.responsavel, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto17 = wx.StaticText(panel, label = "Formação/CREA", style = wx.ALIGN_RIGHT)
            h10_sizer.Add(texto17, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.formacao = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            self.formacao.SetMaxLength(30)
            h10_sizer.Add(self.formacao, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h10_sizer, 1, wx.EXPAND | wx.ALL)

            texto3 = wx.StaticText(panel, label = "Natureza da Amostra", style = wx.ALIGN_RIGHT)
            h1_sizer.Add(texto3, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cp = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            self.cp.SetMaxLength(30)
            h1_sizer.Add(self.cp, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto4 = wx.StaticText(panel, label = "Teor de Umidade (%)", style = wx.ALIGN_RIGHT)
            h1_sizer.Add(texto4, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.teordeumidade = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            self.teordeumidade.SetMaxLength(5)
            h1_sizer.Add(self.teordeumidade, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h1_sizer, 1, wx.EXPAND | wx.ALL)

            texto5 = wx.StaticText(panel, label = "Peso específico seco (kN/m³)", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(texto5, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.pesoespecifico = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            self.pesoespecifico.SetMaxLength(5)
            h2_sizer.Add(self.pesoespecifico, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto6 = wx.StaticText(panel, label = "Umidade Ótima (%)", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(texto6, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.umidadeotima = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            self.umidadeotima.SetMaxLength(5)
            h2_sizer.Add(self.umidadeotima, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h2_sizer, 1, wx.EXPAND | wx.ALL)

            texto7 = wx.StaticText(panel, label = "Energia de compactação", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(texto7, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.energiacompactacao = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            self.energiacompactacao.SetMaxLength(30)
            h3_sizer.Add(self.energiacompactacao, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto8 = wx.StaticText(panel, label = "Grau de compactação (%)", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(texto8, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.graucompactacao = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            self.graucompactacao.SetMaxLength(5)
            h3_sizer.Add(self.graucompactacao, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h3_sizer, 1, wx.EXPAND | wx.ALL)

            texto9 = wx.StaticText(panel, label = "Data da coleta ou recebimento", style = wx.ALIGN_RIGHT)
            h4_sizer.Add(texto9, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.date = wx.adv.DatePickerCtrl(panel, id = wx.ID_ANY, dt = wx.DefaultDateTime, size = wx.DefaultSize, style = wx.adv.DP_SHOWCENTURY | wx.adv.DP_DROPDOWN , validator = wx.DefaultValidator, name = "datectrl")
            h4_sizer.Add(self.date, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h4_sizer, 1, wx.EXPAND | wx.ALL)
            texto10 = wx.StaticText(panel, label = "Diâmetro C.P. (mm)", style = wx.ALIGN_RIGHT)
            h5_sizer.Add(texto10, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.diametro = wx.TextCtrl(panel, -1, '100', style = wx.TE_RIGHT | wx.TE_READONLY)
            h5_sizer.Add(self.diametro, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h5_sizer, 1, wx.EXPAND | wx.ALL)
            texto11 = wx.StaticText(panel, label = "Altura C.P. (mm)", style = wx.ALIGN_RIGHT)
            h6_sizer.Add(texto11, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.altura = wx.TextCtrl(panel, -1, '200', style = wx.TE_RIGHT | wx.TE_READONLY)
            h6_sizer.Add(self.altura, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h6_sizer, 1, wx.EXPAND | wx.ALL)

            staticbox = wx.StaticBox(panel, -1, '')
            staticboxSizer = wx.StaticBoxSizer(staticbox, wx.VERTICAL)
            texto12 = wx.StaticText(panel, label = "Tipo da Amostra", style = wx.ALIGN_RIGHT)
            tipoAmostras = ['Deformada', 'Indeformada']
            self.amostra = wx.RadioBox(panel, label = '', choices = tipoAmostras, majorDimension = 1, style = wx.RA_SPECIFY_COLS)
            self.amostra.Bind(wx.EVT_RADIOBOX, self.RadioBoxEvent)
            v2_sizer.Add(texto12, 0, wx.ALL|wx.CENTER)
            v2_sizer.Add(self.amostra, 0, wx.ALL|wx.CENTER)
            staticboxSizer.Add(v2_sizer, 0, wx.ALL|wx.CENTER)

            h7_sizer.AddStretchSpacer(2)
            h7_sizer.Add(staticboxSizer, 1, wx.EXPAND | wx.ALL, 1)
            h7_sizer.AddStretchSpacer(1)
            h7_sizer.Add(v1_sizer, 5, wx.EXPAND | wx.ALL)

            v_sizer.Add(h7_sizer, 3, wx.EXPAND | wx.ALL)

            texto15 = wx.StaticText(panel, label = "Observações", style = wx.ALIGN_RIGHT)
            h9_sizer.Add(texto15, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.obs = wx.TextCtrl(panel, -1, '', style = wx.TE_RIGHT)
            self.obs.SetMaxLength(120)
            h9_sizer.Add(self.obs, 5, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h9_sizer, 1, wx.EXPAND | wx.ALL)

            continuar = wx.Button(panel, -1, 'Continuar')
            continuar.Bind(wx.EVT_BUTTON, self.Prosseguir)
            v_sizer.Add(continuar, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            sizer.Add(v_sizer, 1,  wx.EXPAND | wx.ALL, 15)

            panel.SetSizer(sizer)
            self.Centre()
            self.Show()

    #--------------------------------------------------
        def RadioBoxEvent(self, event):
            amostra = self.amostra.GetSelection()
            if amostra == 1:
                self.diametro.Clear()
                self.altura.Clear()
                self.diametro.SetEditable(True)
                self.altura.SetEditable(True)
            if amostra == 0:
                self.diametro.Clear()
                self.altura.Clear()
                self.diametro.AppendText("100")
                self.altura.AppendText("200")
                self.diametro.SetEditable(False)
                self.altura.SetEditable(False)

    #--------------------------------------------------
        def Prosseguir(self, event):
            identificador = self.Identificador.GetValue()
            tipo = self.Pares.GetSelection()
            cp = self.cp.GetValue()
            tecnico = self.responsavel.GetValue()
            formacao = self.formacao.GetValue()
            teordeumidade = self.teordeumidade.GetValue()
            pesoespecifico = self.pesoespecifico.GetValue()
            umidadeotima = self.umidadeotima.GetValue()
            energiacompactacao = self.energiacompactacao.GetValue()
            graucompactacao = self.graucompactacao.GetValue()
            data = self.date.GetValue()
            amostra = self.amostra.GetSelection()
            diametro = self.diametro.GetValue()
            diametro = format(diametro).replace(',','.')
            diametro = format(diametro).replace('-','')
            altura = self.altura.GetValue()
            altura = format(altura).replace(',','.')
            altura = format(altura).replace('-','')
            obs = self.obs.GetValue()
            condicional = 1

            try:
                diametro = float(diametro)
                altura = float(altura)

            except ValueError:
                print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                diametro = -1
                condicional = -1

            if identificador == '' and condicional>0:
                '''Diálogo para Forçar preenchimento da Identificacao'''
                dlg = wx.MessageDialog(None, 'É necessário que no mínimo a Indentificação seja preenchida.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
            else:
                cond = bancodedados.data_identificadores()
                if identificador in cond:
                    '''Diálogo para informar que já existe um Ensaio com esse identificação'''
                    dlg = wx.MessageDialog(None, 'Já existe um Ensaio com essa Identificação.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()
                else:
                    if diametro!='' and altura!='' and diametro>=95 and diametro<=155 and altura>=190 and altura<=310:
                        if diametro>0 and altura>0:
                            '''Salva os dados iniciais de um ensaio'''
                            bancodedados.data_save_dados_179(identificador, tipo, cp, teordeumidade, pesoespecifico, umidadeotima, energiacompactacao, graucompactacao, data, amostra, diametro, altura, obs, tecnico, formacao)
                            self.Close(True)
                            frame = TelaRealizacaoEnsaioDNIT179(identificador, tipo, diametro, altura).ShowModal()
                    else:
                        '''Diálogo para informar que os campos diametro e altura estão vazios ou não estão na faixa adequada.'''
                        if condicional>0:
                            dlg = wx.MessageDialog(None, 'Os valores de diametro e de altura devem ser preenchidos corretamente.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                            result = dlg.ShowModal()
        
        #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()
