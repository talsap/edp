# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import bancodedadosCAB
import wx.lib.sized_controls as sc
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from wx.lib.pdfviewer import pdfViewer

'''Tela de Preview do Cabeçalho do PDF'''
class Preview(sc.SizedFrame):
    #--------------------------------------------------
        def __init__(self, parent, id, *args, **kwargs):
            super(Preview, self).__init__(parent, id, 'Pré-Visualização', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION, **kwargs)

            self.id = id

            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

            '''Configurações do Size'''
            self.SetSize((650,400))


            '''cnv = canvas.Canvas('logo', pagesize=A4)'''

            paneCont = self.GetContentsPane()

            self.viewer = pdfViewer(paneCont, wx.NewId(), (10,10), (600,400), wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
            self.viewer.UsePrintDirect = ``False``
            self.viewer.SetSizerProps(expand=True, proportion=1)
            self.viewer.LoadFile(r'logo\\A.pdf')

            '''Inicialize o panel'''
            self.Centre()
            self.Show()



            '''self.Bind(wx.EVT_PAINT, self.OnPaint)'''
    #--------------------------------------------------
        def OnPaint(self, event):
            id = self.id
            id = bancodedadosCAB.idEscolha() #apagar depois

            '''Opcao de Adicionar Logo'''
            dc = wx.ClientDC(self)

            '''Obtendo os dados do banco'''
            listaCAB = bancodedadosCAB.ListaDadosCab(id)
            instituicao = listaCAB[1].encode('utf-8','ignore')
            fantasia = listaCAB[2].encode('utf-8','ignore')
            cpfcnpj = listaCAB[3].encode('utf-8','ignore')
            email = listaCAB[4].encode('utf-8','ignore')
            fone = listaCAB[5].encode('utf-8','ignore')
            uf = listaCAB[6].encode('utf-8','ignore')
            cidade = listaCAB[7].encode('utf-8','ignore')
            bairro = listaCAB[8].encode('utf-8','ignore')
            rua = listaCAB[9].encode('utf-8','ignore')
            numero = listaCAB[10].encode('utf-8','ignore')
            complemento = listaCAB[11].encode('utf-8','ignore')
            cep = listaCAB[12].encode('utf-8','ignore')
            logo = listaCAB[13].encode('utf-8','ignore')

            dc.SetPen(wx.Pen('#4c4c4c', 1, wx.SOLID))
            dc.DrawRectangle(23, 30, 600, 350)

            '''fantasia.SetFont()'''
            dc.DrawText(fantasia, 40,40)

            '''try:
                dc.drawImage(logo, 15/0.352777, 252/0.352777, width = 95, height = 95)
            except:
                pass'''

            '''dc.setFont("Helvetica-Bold", 16)'''
            '''dc.drawCentredString(357, 300, fantasia)'''
            '''dc.setFont("Helvetica-Bold", 14)
            dc.drawCentredString(125/0.352777, 274/0.352777, instituicao)
            dc.setFont("Helvetica", 11)
            dc.drawCentredString(125/0.352777, 269/0.352777, rua+', '+numero+', '+bairro)
            dc.drawCentredString((125)/0.352777, 264/0.352777, cep+', '+cidade+', '+uf)
            dc.drawCentredString((125)/0.352777, 259/0.352777, complemento)
            dc.drawCentredString((125)/0.352777, 254/0.352777, cpfcnpj+', '+fone+', '+email)'''
