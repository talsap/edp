# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import bancodedadosCAB
import math
import os
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

pi = math.pi

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
     def mp(point):
        return point/0.352777

    #--------------------------------------------------
     def createPDF(self, name):
     	id = self.id

     	'''Obtendo os dados do banco'''
        print name
        listaCAB = bancodedadosCAB.ListaDadosCab(self.a)
        instituicao = listaCAB[1].encode('ascii','ignore')
        fantasia = listaCAB[2].encode('ascii','ignore')
        cpfcnpj = listaCAB[3].encode('ascii','ignore')
        email = listaCAB[4].encode('ascii','ignore')
        fone = listaCAB[5].encode('ascii','ignore')
        uf = listaCAB[6].encode('ascii','ignore')
        cidade = listaCAB[7].encode('ascii','ignore')
        bairro = listaCAB[8].encode('ascii','ignore')
        rua = listaCAB[9].encode('ascii','ignore')
        numero = listaCAB[10].encode('ascii','ignore')
        complemento = listaCAB[11].encode('ascii','ignore')
        cep = listaCAB[12].encode('ascii','ignore')
        logo = listaCAB[13].encode('ascii','ignore')

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
                    cnv.drawImage(logo, 30/0.352777, 254/0.352777, width = 90, height = 90)
                except:
                    pass

                cnv.setFont("Helvetica-Bold", 24)
                cnv.drawString(100/0.352777, 277/0.352777, instituicao)
                cnv.save()

            except:
                wx.LogError("O arquivo nao pode ser salvo em '%s'." % pathname)
                dlg = wx.MessageDialog(None, 'Erro ao criar PDF', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
                return


if __name__ == "__main__":
		app = wx.App()
		frame = Pdf(1)
		frame.Show()
		app.MainLoop()
