# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import bancodedadosCAB
import bancodedados
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

#--------------------------------------------------
def pm(mm):
    return mm/0.352777

'''Class Export PDF'''
class Pdf134(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - PDF')
        self.idt = idt
        self.a = bancodedadosCAB.idEscolha()
        frame = self.basic_gui()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_134_pdf(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo PDF ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createPDF("EDP PDF - "+idt)

    #--------------------------------------------------
     def createPDF(self, name):
     	idt = self.idt
        lista = self.list

     	'''Obtendo os dados do banco'''
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

        '''Obter dados do banco'''
        list = bancodedados.dados_iniciais_(idt)
        ensaio = list[0].encode('utf-8','ignore')
        status = list[1].encode('utf-8','ignore')
        tipo = list[2].encode('utf-8','ignore')
        cp = list[3].encode('utf-8','ignore')
        rodovia = list[4].encode('utf-8','ignore')
        origem = list[5].encode('utf-8','ignore')
        trecho = list[6].encode('utf-8','ignore')
        estkm = list[7].encode('utf-8','ignore')
        operador = list[8].encode('utf-8','ignore')
        datadacoleta = list[9].encode('utf-8','ignore')
        datainicio = list[10].encode('utf-8','ignore')
        datafim = list[11].encode('utf-8','ignore')
        amostra = list[12].encode('utf-8','ignore')
        diametro = list[13]
        altura = list[14]
        obs = list[15].encode('utf-8','ignore')
        freq = list[16]
        if int(amostra) == 0:
            valoramostra = 'Deformada'
        else:
            valoramostra = 'Indeformada'

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

                #CABEÇALHO
                try:
                    cnv.drawImage(logo, pm(15), pm(252), width = 95, height = 95)
                except:
                    pass
                cnv.setFont("Helvetica-Bold", 16)
                cnv.drawCentredString(pm(125), pm(280.5), fantasia)
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(125), pm(274), instituicao)
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(pm(125), pm(269), rua+', '+numero+', '+bairro)
                cnv.drawCentredString(pm(125), pm(264), cep+', '+cidade+', '+uf)
                cnv.drawCentredString(pm(125), pm(259), complemento)
                cnv.drawCentredString(pm(125), pm(254), cpfcnpj+', '+fone+', '+email)

                #TABLE
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(100), pm(240), 'MÓDULO DE RESILIÊNCIA - SOLO')
                cnv.setFont("Helvetica", 11)
                cnv.drawRightString(pm(80), pm(230), 'Identificador:')
                cnv.drawRightString(pm(80), pm(225), 'Início do ensaio:')
                cnv.drawRightString(pm(80), pm(220), 'Fim do ensaio:')
                cnv.drawRightString(pm(80), pm(215), 'Coleta da amostra:')
                cnv.drawRightString(pm(80), pm(210), 'Nº do CP:')
                cnv.drawRightString(pm(80), pm(205), 'Rodovia:')
                cnv.drawRightString(pm(80), pm(200), 'Origem:')
                cnv.drawRightString(pm(80), pm(195), 'Trecho:')
                cnv.drawRightString(pm(80), pm(190), 'est/km:')
                cnv.drawRightString(pm(80), pm(185), 'Operador:')
                cnv.drawRightString(pm(80), pm(180), 'Observação:')
                cnv.drawRightString(pm(80), pm(175), 'Tipo da amostra:')
                cnv.drawRightString(pm(80), pm(170), 'Diâmetro [mm]:')
                cnv.drawRightString(pm(80), pm(165), 'Altura [mm]:')
                cnv.drawRightString(pm(80), pm(160), 'Frequência do ensaio [Hz]:')

                cnv.drawString(pm(82), pm(230), idt)
                cnv.drawString(pm(82), pm(225), datainicio)
                cnv.drawString(pm(82), pm(220), datafim)
                cnv.drawString(pm(82), pm(215), datadacoleta)
                cnv.drawString(pm(82), pm(210), cp)
                cnv.drawString(pm(82), pm(205), rodovia)
                cnv.drawString(pm(82), pm(200), origem)
                cnv.drawString(pm(82), pm(195), trecho)
                cnv.drawString(pm(82), pm(190), estkm)
                cnv.drawString(pm(82), pm(185), operador)
                cnv.drawString(pm(82), pm(180), obs)
                cnv.drawString(pm(82), pm(175), valoramostra)
                cnv.drawString(pm(82), pm(170), str(diametro))
                cnv.drawString(pm(82), pm(165), str(altura))
                cnv.drawString(pm(82), pm(160), str(freq))

                #TABLE
                t=Table(lista)
                t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

                t.wrapOn(cnv, 720, 576)
                t.drawOn(cnv, pm(45), pm(-6*len(lista)+144))
                cnv.save()
                self.Destroy()

            except:
                wx.LogError("O arquivo nao pode ser salvo em '%s'." % pathname)
                dlg = wx.MessageDialog(None, 'Erro ao criar PDF', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
                self.Destroy()
                return
