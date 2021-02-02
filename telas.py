# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import bancodedadosCAB
from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel

'''Tela de Preview do Cabeçalho do PDF'''
class Preview(wx.Frame):
    #--------------------------------------------------
        def __init__(self, id, *args, **kwargs):
            wx.Frame.__init__(self, None, -1, 'Pré-Visualização', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            self.id = id

            '''Iserção do IconeLogo'''
            ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)

            '''Configurações do Size'''
            self.SetSize((650,400))

            self.Bind(wx.EVT_PAINT, self.OnPaint)
            self.Centre()
            self.Show()

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
            '''dc.DrawRectangle(23, 30, 600, 350)'''
            self.viewer = pdfViewer(self, wx.NewId(), 600, 350, wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
            self.viewer.UsePrintDirect = ``False``
            self.viewer.SetSizerProps(expand=True, proportion=1)

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


if __name__ == "__main__":
		app = wx.App()
		frame = Preview(1)
		frame.Show()
		app.MainLoop()
