# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import banco.bancodedadosCAB as bancodedadosCAB
import banco.bancodedados as bancodedados
import banco.bdPreferences as bdPreferences
import banco.bdConfiguration as bdConfiguration
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
        lvdt = bdConfiguration.S1S2()
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
                x = -2
                cnv.drawRightString(pm(110), pm(235+x), 'Identificação:')
                cnv.drawRightString(pm(110), pm(230+x), 'Norma de referência:')
                cnv.drawRightString(pm(110), pm(225+x), 'Coleta da amostra:')
                cnv.drawRightString(pm(110), pm(220+x), 'Início do ensaio:')
                cnv.drawRightString(pm(110), pm(215+x), 'Fim do ensaio:')
                cnv.drawRightString(pm(110), pm(210+x), 'Identificação e natureza da amostra:')
                cnv.drawRightString(pm(110), pm(205+x), 'Tipo de amostra:')
                cnv.drawRightString(pm(110), pm(200+x), 'Energia de compactação:')
                cnv.drawRightString(pm(110), pm(195+x), 'Tamanho do Corpo de Prova [mm]:')
                cnv.drawRightString(pm(110), pm(190+x), 'Teor de umidade do Corpo de Prova [%]:')
                cnv.drawRightString(pm(110), pm(185+x), 'Peso específico seco do Corpo de Prova [kN/m³]:')
                cnv.drawRightString(pm(110), pm(180+x), 'Grau de compactação do Corpo de Prova [%]:')
                cnv.drawRightString(pm(110), pm(175+x), 'Desvio de umidade [%]:')
                cnv.drawRightString(pm(110), pm(170+x), 'Frequência do ensaio [Hz]:')
                cnv.drawRightString(pm(110), pm(165+x), 'Curso do LVDT empregado [mm]:')

                cnv.drawString(pm(112), pm(235+x), idt)
                cnv.drawString(pm(112), pm(230+x), 'DNIT 134/2018-ME')
                cnv.drawString(pm(112), pm(225+x), datadacoleta)
                cnv.drawString(pm(112), pm(220+x), datainicio)
                cnv.drawString(pm(112), pm(215+x), datafim)
                cnv.drawString(pm(112), pm(210+x), naturazaDaAmostra)
                cnv.drawString(pm(112), pm(205+x), valoramostra)
                cnv.drawString(pm(112), pm(200+x), energiaCompactacao)
                cnv.drawString(pm(112), pm(195+x), str(format(diametro).replace('.',','))+' x '+str(format(altura).replace('.',',')))
                cnv.drawString(pm(112), pm(190+x), teorUmidade)
                cnv.drawString(pm(112), pm(185+x), pesoEspecifico)
                cnv.drawString(pm(112), pm(180+x), grauCompactacao)
                cnv.drawString(pm(112), pm(175+x), desvioUmidade)
                cnv.drawString(pm(112), pm(170+x), str(freq))
                cnv.drawString(pm(112), pm(165+x), str(int(lvdt[3])))

                #TABLE
                t=Table(lista)
                t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

                t.wrapOn(cnv, 720, 576)
                t.drawOn(cnv, pm(48), pm((19-len(lista))*6.35+25))
                
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

        self.list = bancodedados.dados_da_coleta_179_pdf(idt)

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
        lvdt = bdConfiguration.S1S2()
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
        try:
            pressaoConf = str(float(pressaoConf)*1000)
        except:
            pressaoConf = ''
        try:
            pressaoDesvio = str(float(pressaoDesvio)*1000)
        except:
            pressaoDesvio = ''

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
                cnv.drawCentredString(pm(110), pm(242), 'Relatório de Ensaio de Deformação Permanente')
                cnv.setFont("Helvetica", 11)
                x = -2
                cnv.drawRightString(pm(110), pm(235+x), 'Identificação:')
                cnv.drawRightString(pm(110), pm(230+x), 'Norma de referência:')
                cnv.drawRightString(pm(110), pm(225+x), 'Coleta da amostra:')
                cnv.drawRightString(pm(110), pm(220+x), 'Início do ensaio:')
                cnv.drawRightString(pm(110), pm(215+x), 'Fim do ensaio:')
                cnv.drawRightString(pm(110), pm(210+x), 'Identificação e natureza da amostra:')
                cnv.drawRightString(pm(110), pm(205+x), 'Tipo de amostra:')
                cnv.drawRightString(pm(110), pm(200+x), 'Energia de compactação:')
                cnv.drawRightString(pm(110), pm(195+x), 'Tamanho do Corpo de Prova [mm]:')
                cnv.drawRightString(pm(110), pm(190+x), 'Teor de umidade do Corpo de Prova [%]:')
                cnv.drawRightString(pm(110), pm(185+x), 'Peso específico seco do Corpo de Prova [kN/m³]:')
                cnv.drawRightString(pm(110), pm(180+x), 'Grau de compactação do Corpo de Prova [%]:')
                cnv.drawRightString(pm(110), pm(175+x), 'Desvio de umidade [%]:')
                cnv.drawRightString(pm(110), pm(170+x), 'Frequência do ensaio [Hz]:')
                cnv.drawRightString(pm(110), pm(165+x), 'Curso do LVDT empregado [mm]:')
                cnv.drawRightString(pm(110), pm(160+x), 'σ3 [kPa]:')
                cnv.drawRightString(pm(110), pm(155+x), 'σd [kPa]:')
                cnv.drawRightString(pm(90), pm(158+x), 'Estado de tensões do ensaio:')

                cnv.drawString(pm(112), pm(235+x), idt)
                cnv.drawString(pm(112), pm(230+x), 'DNIT 179/2018-IE')
                cnv.drawString(pm(112), pm(225+x), datadacoleta)
                cnv.drawString(pm(112), pm(220+x), datainicio)
                cnv.drawString(pm(112), pm(215+x), datafim)
                cnv.drawString(pm(112), pm(210+x), naturazaDaAmostra)
                cnv.drawString(pm(112), pm(205+x), valoramostra)
                cnv.drawString(pm(112), pm(200+x), energiaCompactacao)
                cnv.drawString(pm(112), pm(195+x), str(format(diametro).replace('.',','))+' x '+str(format(altura).replace('.',',')))
                cnv.drawString(pm(112), pm(190+x), teorUmidade)
                cnv.drawString(pm(112), pm(185+x), pesoEspecifico)
                cnv.drawString(pm(112), pm(180+x), grauCompactacao)
                cnv.drawString(pm(112), pm(175+x), desvioUmidade)
                cnv.drawString(pm(112), pm(170+x), str(freq))
                cnv.drawString(pm(112), pm(165+x), str(int(lvdt[3])))
                cnv.drawString(pm(112), pm(160+x), format(pressaoConf).replace('.',','))
                cnv.drawString(pm(112), pm(155+x), format(pressaoDesvio).replace('.',','))

                if len(lista) <=17:
                    #TABLE1
                    t=Table(lista[0:17])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((17-len(lista[0:17]))*6.35+25))
                
                if len(lista) >17 and len(lista) <=54:
                    #TABLE1
                    t=Table(lista[0:17])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((17-len(lista[0:17]))*6.35+25))
                    cnv.showPage()

                    #TABLEPAGE2
                    t=Table([lista[0]]+lista[17:54])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[17:54]))*6.35+25))
                
                if len(lista) >54 and len(lista) <=91:
                    #TABLE1
                    t=Table(lista[0:17])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((17-len(lista[0:17]))*6.35+25))
                    cnv.showPage()

                    #TABLEPAGE2
                    t=Table([lista[0]]+lista[17:54])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[17:54]))*6.35+25))
                    cnv.showPage()

                    #TABLEPAGE3
                    t=Table([lista[0]]+lista[54:91])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[54:91]))*6.35+25))

                if len(lista) >91 and len(lista) <=128:
                    #TABLE1
                    t=Table(lista[0:17])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((17-len(lista[0:17]))*6.35+25))
                    cnv.showPage()

                    #TABLEPAGE2
                    t=Table([lista[0]]+lista[17:54])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[17:54]))*6.35+25))
                    cnv.showPage()

                    #TABLEPAGE3
                    t=Table([lista[0]]+lista[54:91])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[54:91]))*6.35+25))
                    cnv.showPage()

                    #TABLEPAGE4
                    t=Table([lista[0]]+lista[91:128])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[91:128]))*6.35+25))

                if len(lista) >128 and len(lista) <=165:
                    #TABLE1
                    t=Table(lista[0:17])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((17-len(lista[0:17]))*6.35+25))
                    cnv.showPage()

                    #TABLEPAGE2
                    t=Table([lista[0]]+lista[17:54])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[17:54]))*6.35+25))
                    cnv.showPage()

                    #TABLEPAGE3
                    t=Table([lista[0]]+lista[54:91])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[54:91]))*6.35+25))
                    cnv.showPage()

                    #TABLEPAGE4
                    t=Table([lista[0]]+lista[91:128])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[91:128]))*6.35+25))
                    cnv.showPage()

                    #TABLEPAGE5
                    t=Table([lista[0]]+lista[128:165])
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                    
                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[128:165]))*6.35+25))

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

'''Class Export PDF'''
class Pdf181(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - PDF')
        self.idt = idt
        self.a = bancodedadosCAB.idEscolha()
        frame = self.basic_gui()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_181_pdf(idt)

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
        lvdt = bdConfiguration.S1S2()
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
                x = -2
                cnv.drawRightString(pm(110), pm(235+x), 'Identificação:')
                cnv.drawRightString(pm(110), pm(230+x), 'Norma de referência:')
                cnv.drawRightString(pm(110), pm(225+x), 'Coleta da amostra:')
                cnv.drawRightString(pm(110), pm(220+x), 'Início do ensaio:')
                cnv.drawRightString(pm(110), pm(215+x), 'Fim do ensaio:')
                cnv.drawRightString(pm(110), pm(210+x), 'Identificação e natureza da amostra:')
                cnv.drawRightString(pm(110), pm(205+x), 'Tipo de estabilizante químico:')
                cnv.drawRightString(pm(110), pm(200+x), 'Tempo de cura [dias]:')
                cnv.drawRightString(pm(110), pm(195+x), 'Peso do estabilizante químico [%]:')
                cnv.drawRightString(pm(110), pm(190+x), 'Energia de compactação:')
                cnv.drawRightString(pm(110), pm(185+x), 'Tamanho do Corpo de Prova [mm]:')
                cnv.drawRightString(pm(110), pm(180+x), 'Teor de umidade do Corpo de Prova [%]:')
                cnv.drawRightString(pm(110), pm(175+x), 'Peso específico seco do Corpo de Prova [kN/m³]:')
                cnv.drawRightString(pm(110), pm(170+x), 'Grau de compactação do Corpo de Prova [%]:')
                cnv.drawRightString(pm(110), pm(165+x), 'Desvio de umidade [%]:')
                cnv.drawRightString(pm(110), pm(160+x), 'Frequência do ensaio [Hz]:')
                cnv.drawRightString(pm(110), pm(155+x), 'Curso do LVDT empregado [mm]:')

                cnv.drawString(pm(112), pm(235+x), idt)
                cnv.drawString(pm(112), pm(230+x), 'DNIT 181/2018-ME')
                cnv.drawString(pm(112), pm(225+x), datadacoleta)
                cnv.drawString(pm(112), pm(220+x), datainicio)
                cnv.drawString(pm(112), pm(215+x), datafim)
                cnv.drawString(pm(112), pm(210+x), naturazaDaAmostra)
                cnv.drawString(pm(112), pm(205+x), tipoEstabilizante)
                cnv.drawString(pm(112), pm(200+x), tempoCura)
                cnv.drawString(pm(112), pm(195+x), pesoEstabilizante)
                cnv.drawString(pm(112), pm(190+x), energiaCompactacao)
                cnv.drawString(pm(112), pm(185+x), str(format(diametro).replace('.',','))+' x '+str(format(altura).replace('.',',')))
                cnv.drawString(pm(112), pm(180+x), teorUmidade)
                cnv.drawString(pm(112), pm(175+x), pesoEspecifico)
                cnv.drawString(pm(112), pm(170+x), grauCompactacao)
                cnv.drawString(pm(112), pm(165+x), desvioUmidade)
                cnv.drawString(pm(112), pm(160+x), str(freq))
                cnv.drawString(pm(112), pm(155+x), str(int(lvdt[3])))

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
                t.drawOn(cnv, pm(60), pm((17-len(lista))*6.35+25))

                cnv.save()
                self.Destroy()

            except:
                wx.LogError("O arquivo nao pode ser salvo em '%s'." % pathname)
                dlg = wx.MessageDialog(None, 'Erro ao criar PDF', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
                self.Destroy()
                return