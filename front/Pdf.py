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
from reportlab.platypus import Table, TableStyle, Paragraph

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
        lvdt = bancodedados.S1S2()
        ensaio = list[0].encode('utf-8','ignore')
        status = list[1].encode('utf-8','ignore')
        tipo = list[2].encode('utf-8','ignore')
        naturazaDaAmostra = list[3].encode('utf-8','ignore')
        teorUmidade = list[4].encode('utf-8','ignore')
        pesoEspecifico = list[5].encode('utf-8','ignore')
        umidadeOtima = list[6].encode('utf-8','ignore')
        energiaCompactacao = list[7].encode('utf-8','ignore')
        grauCompactacao = list[8].encode('utf-8','ignore')
        datadacoleta = list[9].encode('utf-8','ignore')
        datainicio = list[10].encode('utf-8','ignore')
        datafim = list[11].encode('utf-8','ignore')
        amostra = list[12].encode('utf-8','ignore')
        diametro = list[13]
        altura = list[14]
        obs = list[15].encode('utf-8','ignore')
        freq = list[16]
        pressaoConf = list[17].encode('utf-8','ignore')
        pressaoDesvio = list[18].encode('utf-8','ignore')
        tipoEstabilizante = list[19].encode('utf-8','ignore')
        pesoEstabilizante = list[20].encode('utf-8','ignore')
        tempoCura = list[21].encode('utf-8','ignore')
        tecnico = list[22].encode('utf-8','ignore')
        formacao = list[23].encode('utf-8','ignore')

        if int(amostra) == 0:
            valoramostra = 'Deformada'
        else:
            valoramostra = 'Indeformada'
        try:
            desvioUmidade = str(float(teorUmidade)-float(umidadeOtima))
        except:
            desvioUmidade = ''

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
                cnv.setTitle(idt)

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

                #CORPO
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(110), pm(242), 'Relatório de Ensaio de Módulo de Resiliência')
                cnv.setFont("Helvetica", 11)
                cnv.drawRightString(pm(110), pm(235), 'Identificação:')
                cnv.drawRightString(pm(110), pm(230), 'Norma de referência:')
                cnv.drawRightString(pm(110), pm(225), 'Coleta da amostra:')
                cnv.drawRightString(pm(110), pm(220), 'Início do ensaio')
                cnv.drawRightString(pm(110), pm(215), 'Fim do ensaio:')
                cnv.drawRightString(pm(110), pm(210), 'Identificação e natureza da amostra:')
                cnv.drawRightString(pm(110), pm(205), 'Tipo de amostra:')
                cnv.drawRightString(pm(110), pm(200), 'Energia de compactação:')
                cnv.drawRightString(pm(110), pm(195), 'Tamanho do Corpo de Prova [mm]:')
                cnv.drawRightString(pm(110), pm(190), 'Teor de umidade do Corpo de Prova [%]:')
                cnv.drawRightString(pm(110), pm(185), 'Peso específico seco do Corpo de Prova [kN/m³]:')
                cnv.drawRightString(pm(110), pm(180), 'Grau de compactação do Corpo de Prova [%]:')
                cnv.drawRightString(pm(110), pm(175), 'Desvio de umidade [%]:')
                cnv.drawRightString(pm(110), pm(170), 'Frequência do ensaio [Hz]:')
                cnv.drawRightString(pm(110), pm(165), 'Curso do LVDT empregado [mm]')

                cnv.drawString(pm(112), pm(235), idt)
                cnv.drawString(pm(112), pm(230), 'DNIT 134/2018-ME')
                cnv.drawString(pm(112), pm(225), datadacoleta)
                cnv.drawString(pm(112), pm(220), datainicio)
                cnv.drawString(pm(112), pm(215), datafim)
                cnv.drawString(pm(112), pm(210), naturazaDaAmostra)
                cnv.drawString(pm(112), pm(205), valoramostra)
                cnv.drawString(pm(112), pm(200), energiaCompactacao)
                cnv.drawString(pm(112), pm(195), str(diametro)+' x '+str(altura))
                cnv.drawString(pm(112), pm(190), teorUmidade)
                cnv.drawString(pm(112), pm(185), pesoEspecifico)
                cnv.drawString(pm(112), pm(180), grauCompactacao)
                cnv.drawString(pm(112), pm(175), desvioUmidade)
                cnv.drawString(pm(112), pm(170), str(freq))
                cnv.drawString(pm(112), pm(165), str(lvdt[3]))

                #RODAPÉ
                o = Paragraph('OBS.: '+obs)
                o.wrapOn(cnv, 250, 50)
                o.drawOn(cnv, pm(32), pm(10))
                cnv.line(pm(130),pm(18),pm(195),pm(18))
                cnv.drawString(pm(130), pm(14), 'R. T.: '+tecnico)
                cnv.drawString(pm(130), pm(10), formacao) 

                #TABLE
                t=Table(lista)
                t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

                t.wrapOn(cnv, 720, 576)
                t.drawOn(cnv, pm(48), pm((19-len(lista))*6.35+25))
                print len(lista)

                cnv.save()
                self.Destroy()

            except:
                wx.LogError("O arquivo nao pode ser salvo em '%s'." % pathname)
                dlg = wx.MessageDialog(None, 'Erro ao criar PDF', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
                self.Destroy()
                return

'''Class Export PDF'''
class Pdf179(wx.Dialog):
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
        lvdt = bancodedados.S1S2()
        ensaio = list[0].encode('utf-8','ignore')
        status = list[1].encode('utf-8','ignore')
        tipo = list[2].encode('utf-8','ignore')
        naturazaDaAmostra = list[3].encode('utf-8','ignore')
        teorUmidade = list[4].encode('utf-8','ignore')
        pesoEspecifico = list[5].encode('utf-8','ignore')
        umidadeOtima = list[6].encode('utf-8','ignore')
        energiaCompactacao = list[7].encode('utf-8','ignore')
        grauCompactacao = list[8].encode('utf-8','ignore')
        datadacoleta = list[9].encode('utf-8','ignore')
        datainicio = list[10].encode('utf-8','ignore')
        datafim = list[11].encode('utf-8','ignore')
        amostra = list[12].encode('utf-8','ignore')
        diametro = list[13]
        altura = list[14]
        obs = list[15].encode('utf-8','ignore')
        freq = list[16]
        pressaoConf = list[17].encode('utf-8','ignore')
        pressaoDesvio = list[18].encode('utf-8','ignore')
        tipoEstabilizante = list[19].encode('utf-8','ignore')
        pesoEstabilizante = list[20].encode('utf-8','ignore')
        tempoCura = list[21].encode('utf-8','ignore')
        tecnico = list[22].encode('utf-8','ignore')
        formacao = list[23].encode('utf-8','ignore')

        if int(amostra) == 0:
            valoramostra = 'Deformada'
        else:
            valoramostra = 'Indeformada'
        try:
            desvioUmidade = str(float(teorUmidade)-float(umidadeOtima))
        except:
            desvioUmidade = ''

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
                cnv.setTitle(idt)

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

                #CORPO
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(105), pm(240), 'MÓDULO DE RESILIÊNCIA - SOLO')
                cnv.setFont("Helvetica", 11)
                cnv.drawRightString(pm(110), pm(230), 'Identificação:')
                cnv.drawRightString(pm(110), pm(225), 'Norma de referência:')
                cnv.drawRightString(pm(110), pm(220), 'Coleta da amostra:')
                cnv.drawRightString(pm(110), pm(215), 'Início do ensaio')
                cnv.drawRightString(pm(110), pm(210), 'Fim do ensaio:')
                cnv.drawRightString(pm(110), pm(205), 'Identificação e natureza da amostra:')
                cnv.drawRightString(pm(110), pm(200), 'Tipo de amostra:')
                cnv.drawRightString(pm(110), pm(195), 'Energia de compactação:')
                cnv.drawRightString(pm(110), pm(190), 'Tamanho do Corpo de Prova (mm):')
                cnv.drawRightString(pm(110), pm(185), 'Teor de umidade do Corpo de Prova (%):')
                cnv.drawRightString(pm(110), pm(180), 'Peso específico seco do Corpo de Prova (kN/m³):')
                cnv.drawRightString(pm(110), pm(175), 'Grau de compactação do Corpo de Prova (%):')
                cnv.drawRightString(pm(110), pm(170), 'Desvio de umidade (%):')
                cnv.drawRightString(pm(110), pm(165), 'Frequência do ensaio [Hz]:')
                cnv.drawRightString(pm(110), pm(160), 'Curso do LVDT empregado (mm)')

                cnv.drawString(pm(112), pm(230), idt)
                cnv.drawString(pm(112), pm(225), 'DNIT 134/2018-ME')
                cnv.drawString(pm(112), pm(220), datadacoleta)
                cnv.drawString(pm(112), pm(215), datainicio)
                cnv.drawString(pm(112), pm(210), datafim)
                cnv.drawString(pm(112), pm(205), naturazaDaAmostra)
                cnv.drawString(pm(112), pm(200), valoramostra)
                cnv.drawString(pm(112), pm(195), energiaCompactacao)
                cnv.drawString(pm(112), pm(190), str(diametro)+' x '+str(altura))
                cnv.drawString(pm(112), pm(185), teorUmidade)
                cnv.drawString(pm(112), pm(180), pesoEspecifico)
                cnv.drawString(pm(112), pm(175), grauCompactacao)
                cnv.drawString(pm(112), pm(170), desvioUmidade)
                cnv.drawString(pm(112), pm(165), str(freq))
                cnv.drawString(pm(112), pm(160), str(lvdt[3]))

                #TABLE
                t=Table(lista)
                t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                t.wrapOn(cnv, 720, 576)
                t.drawOn(cnv, pm(48), pm((19-len(lista))*6.35+15))
                

                #RODAPÉ
                o = Paragraph('OBS.: '+obs)
                o.wrapOn(cnv, 250, 50)
                o.drawOn(cnv, pm(32), pm(10))
                cnv.line(pm(130),pm(18),pm(195),pm(18))
                cnv.drawString(pm(130), pm(14), 'R. T.: '+tecnico)
                cnv.drawString(pm(130), pm(10), formacao) 

                cnv.save()
                self.Destroy()

            except:
                wx.LogError("O arquivo nao pode ser salvo em '%s'." % pathname)
                dlg = wx.MessageDialog(None, 'Erro ao criar PDF', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
                self.Destroy()
                return