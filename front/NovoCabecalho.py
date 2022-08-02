# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import shutil
import bancodedadosCAB
from front.previsualizar import PDFViewer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

'''Tela Novo Cabeçalho'''
class NovoCabecalho(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'EDP - Novo Cabeçalho', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

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
            h10_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.panel = wx.Panel(self)

            self.logo = wx.Button(self.panel, -1, 'Logo')
            self.previsualizar = wx.Button(self.panel, -1, 'Pré-Visualizar')
            self.previsualizar.Disable()
            self.Bind(wx.EVT_BUTTON, self.OnOpen, self.logo)

            v1_sizer.AddStretchSpacer(10)
            v1_sizer.Add(self.logo, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
            v1_sizer.AddStretchSpacer(1)
            v1_sizer.Add(self.previsualizar, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL)
            v1_sizer.AddStretchSpacer(10)

            texto1 = wx.StaticText(self.panel, label = "Identificador", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(texto1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.Identificador = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h2_sizer.Add(self.Identificador, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            h2_sizer.AddStretchSpacer(9)

            texto2 = wx.StaticText(self.panel, label = "Empresa/Instituição", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(texto2, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.empresa = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h3_sizer.Add(self.empresa, 5, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            '''h3_sizer.AddStretchSpacer(1)'''
            texto3 = wx.StaticText(self.panel, label = "Fantasia", style = wx.ALIGN_RIGHT)
            h10_sizer.Add(texto3, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.fantasia = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h10_sizer.Add(self.fantasia, 6, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            texto4 = wx.StaticText(self.panel, label = "CPF/CNPJ", style = wx.ALIGN_RIGHT)
            h4_sizer.Add(texto4, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cpfcnpj = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h4_sizer.Add(self.cpfcnpj, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto5 = wx.StaticText(self.panel, label = "E-mail", style = wx.ALIGN_RIGHT)
            h4_sizer.AddStretchSpacer(1)
            h4_sizer.Add(texto5, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.email = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h4_sizer.Add(self.email, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            texto6 = wx.StaticText(self.panel, label = "Fone", style = wx.ALIGN_RIGHT)
            h5_sizer.Add(texto6, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.fone = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h5_sizer.Add(self.fone, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto7 = wx.StaticText(self.panel, label = "UF", style = wx.ALIGN_RIGHT)
            h5_sizer.AddStretchSpacer(1)
            h5_sizer.Add(texto7, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.uf = wx.TextCtrl(self.panel, -1, '', size=(25,23), style = wx.TE_LEFT)
            h5_sizer.Add(self.uf, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            h5_sizer.AddStretchSpacer(1)
            texto8 = wx.StaticText(self.panel, label = "Cidade", style = wx.ALIGN_RIGHT)
            h5_sizer.Add(texto8, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cidade = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h5_sizer.Add(self.cidade, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            texto9 = wx.StaticText(self.panel, label = "Bairro", style = wx.ALIGN_RIGHT)
            h6_sizer.Add(texto9, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.bairro = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h6_sizer.Add(self.bairro, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto10 = wx.StaticText(self.panel, label = "Rua", style = wx.ALIGN_RIGHT)
            h6_sizer.AddStretchSpacer(1)
            h6_sizer.Add(texto10, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.rua = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h6_sizer.Add(self.rua, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            h6_sizer.AddStretchSpacer(1)
            texto11 = wx.StaticText(self.panel, label = "Nº", style = wx.ALIGN_RIGHT)
            h6_sizer.Add(texto11, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.numero = wx.TextCtrl(self.panel, -1, '', size=(25,23), style = wx.TE_LEFT)
            h6_sizer.Add(self.numero, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            texto12 = wx.StaticText(self.panel, label = "CEP", style = wx.ALIGN_RIGHT)
            h7_sizer.Add(texto12, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cep = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h7_sizer.Add(self.cep, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            texto13 = wx.StaticText(self.panel, label = "Complemento", style = wx.ALIGN_RIGHT)
            h7_sizer.AddStretchSpacer(1)
            h7_sizer.Add(texto13, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.complemento = wx.TextCtrl(self.panel, -1, '', style = wx.TE_LEFT)
            h7_sizer.Add(self.complemento, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v2_sizer.AddStretchSpacer(1)
            v2_sizer.Add(h2_sizer, 1)
            v2_sizer.AddStretchSpacer(1)
            v2_sizer.Add(h10_sizer, 1)
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

            self.salvar = wx.Button(self.panel, -1, 'Salvar')
            sair = wx.Button(self.panel, -1, 'Sair')
            self.Bind(wx.EVT_BUTTON, self.salvarDados, self.salvar)
            self.Bind(wx.EVT_BUTTON, self.onExit, sair)

            h1_sizer.AddStretchSpacer(5)
            h1_sizer.Add(self.salvar, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            h1_sizer.Add(sair, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            h1_sizer.AddStretchSpacer(5)

            v_sizer.Add(h_sizer, 2)
            v_sizer.Add(h1_sizer, 0)
            sizer.Add(v_sizer, 0,  wx.EXPAND | wx.ALL, 15)

            self.Bind(wx.EVT_PAINT, self.OnPaint)
            self.directory = ''

            self.panel.SetSizer(sizer)
            self.Centre()
            self.Show()
    #--------------------------------------------------
        def OnPaint(self, event):
            '''Opcao Logo Dimensão'''
            self.dc = wx.ClientDC(self.panel)

            self.dc.SetPen(wx.Pen('#4c4c4c', 1, wx.SOLID))
            png = wx.Image(r'logo\default.png', wx.BITMAP_TYPE_PNG)
            bmp = png.Scale(90, 90, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
            self.dc.DrawRectangle(20, 30, 90, 90)
            self.dc.DrawBitmap(bmp, 20, 30, useMask=False)

    #--------------------------------------------------
        def PreviewPDF(self, event):
            '''Opcao ver Preview do Cabeçalho do PDF'''
            pdfV = PDFViewer(None, size=(800, 600))
            pdfV.viewer.UsePrintDirect = ``False``
            pdfV.viewer.LoadFile(os.path.abspath('logo\CAB.pdf'))
            pdfV.Show()

    #--------------------------------------------------
        def salvarDados(self, event):
            '''Opcao Salvar dados Cabeçalho'''
            a = self.Identificador.GetValue()
            b = self.empresa.GetValue()
            c = self.fantasia.GetValue()
            d = self.cpfcnpj.GetValue()
            e = self.email.GetValue()
            f = self.fone.GetValue()
            g = self.uf.GetValue()
            h = self.cidade.GetValue()
            i = self.bairro.GetValue()
            j = self.rua.GetValue()
            k = self.numero.GetValue()
            l = self.cep.GetValue()
            m = self.complemento.GetValue()
            n = self.directory

            if  a == '' or c == '':
                '''Diálogo para Forçar preenchimento do Identificador e do nome Fantasia'''
                dlg = wx.MessageDialog(None, 'É necessário que no mínimo o Identificador e o nome Fantasia seja preenchido.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()

            else:
                cond = bancodedadosCAB.data_identificadores()
                if a in cond:
                    '''Diálogo para informar que já existe um Cabeçalho com esse identificador'''
                    dlg = wx.MessageDialog(None, 'Já existe um Cabeçalho com esse identificador.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()
                else:
                    print 'Salvando dados...'
                    bancodedadosCAB.data_save_dados(a, b, c, d, e, f, g, h, i, j, k, l, m, n)
                    idd = bancodedadosCAB.identificador_id(a)
                    bancodedadosCAB.updateEscolha(idd)

                    '''criando cabeçalho pra vizualização'''
                    try:
                        cnv = canvas.Canvas(r'logo\\CAB.pdf', pagesize=A4)
                    except:
                        print 'error ao criar CAB.pdf'

                    try:
                        cnv.drawImage(n, 15/0.352777, 252/0.352777, width = 95, height = 95)
                    except:
                        pass

                    cnv.setFont("Helvetica-Bold", 16)
                    cnv.drawCentredString(125/0.352777, 280.5/0.352777, c)
                    cnv.setFont("Helvetica-Bold", 14)
                    cnv.drawCentredString(125/0.352777, 274/0.352777, b)
                    cnv.setFont("Helvetica", 11)
                    cnv.drawCentredString(125/0.352777, 269/0.352777, j+', '+k+', '+i)
                    cnv.drawCentredString((125)/0.352777, 264/0.352777, l+', '+h+', '+g)
                    cnv.drawCentredString((125)/0.352777, 259/0.352777, m)
                    cnv.drawCentredString((125)/0.352777, 254/0.352777, d+', '+f+', '+e)
                    cnv.save()

                    self.previsualizar.Enable()
                    self.Bind(wx.EVT_BUTTON, self.PreviewPDF, self.previsualizar)
                    self.panel.Update()
                    myobject = event.GetEventObject()
                    myobject.Disable()
                    try:
                        self.AbrirLogo.Disable()
                    except:
                        self.logo.Disable()
                        self.logo.Update()

    #--------------------------------------------------
        def OnOpen(self, event):
            '''Opcao abrir imagen logo'''

            with wx.FileDialog(self, "Adicione uma imagem como logo", wildcard="Image files (*.png;*.jpeg;*.jpg;*.bmp;*.ico)|*.png;*.jpeg;*.jpg;*.bmp;*.ico", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_OK:
                    nameDirectory = fileDialog.GetPath()
                    try:
                        shutil.copy(nameDirectory, r'logo')
                    except:
                        pass
                    nameArquivo = fileDialog.GetFilename()
                    nameArquivo = nameArquivo.encode('ascii', 'ignore')
                    self.directory = 'logo\\'+ nameArquivo
                    imageLogo = wx.Image(self.directory, wx.BITMAP_TYPE_ANY)
                    bmp = imageLogo.Scale(90, 90, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                    self.dc.Clear()
                    self.dc.DrawRectangle(20, 30, 90, 90)
                    self.dc.DrawBitmap(bmp, 20, 30, useMask=True)
                    self.AbrirLogo = event.GetEventObject()
                    return

    #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Close(True)
