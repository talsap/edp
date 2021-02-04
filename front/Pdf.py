# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import bancodedadosCAB
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

'''Class Export PDF'''
class Pdf(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, id, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - PDF')
        self.id = id
        frame = self.basic_gui()

    #--------------------------------------------------
     def basic_gui(self):
        id = self.id
        self.a = bancodedadosCAB.idEscolha()
        self.createPDF("EDP - PDF")

    #--------------------------------------------------
     def createPDF(self, name):
     	id = self.id

     	'''Obtendo os dados do banco'''
        print name
        listaCAB = bancodedadosCAB.ListaDadosCab(self.a)
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

        '''Criando arquivo PDF'''
        with wx.FileDialog(self, name, wildcard="PDF files(*.pdf)|*.pdf*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()

            try:
                if re.search('\\.pdf\\b', pathname, re.IGNORECASE):
                    diretorio = pathname
                else:
                    diretorio = pathname+".pdf"

                cnv = canvas.Canvas(diretorio, pagesize=A4)
                try:
                    cnv.drawImage(logo, 15/0.352777, 252/0.352777, width = 95, height = 95)
                except:
                    pass

                cnv.setFont("Helvetica-Bold", 16)
                cnv.drawCentredString(125/0.352777, 280.5/0.352777, fantasia)
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(125/0.352777, 274/0.352777, instituicao)
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(125/0.352777, 269/0.352777, rua+', '+numero+', '+bairro)
                cnv.drawCentredString((125)/0.352777, 264/0.352777, cep+', '+cidade+', '+uf)
                cnv.drawCentredString((125)/0.352777, 259/0.352777, complemento)
                cnv.drawCentredString((125)/0.352777, 254/0.352777, cpfcnpj+', '+fone+', '+email)
                cnv.save()

            except:
                wx.LogError("O arquivo nao pode ser salvo em '%s'." % pathname)
                dlg = wx.MessageDialog(None, 'Erro ao criar PDF', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
                return
