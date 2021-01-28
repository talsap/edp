# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
'''import bancodedados'''
import unicodecsv
import csv
import math

pi = math.pi

'''Class Export CSV'''
class Csv(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, id, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EAU - CSV')
        self.id = id
        frame = self.basic_gui()

    #--------------------------------------------------
     def basic_gui(self):
        id = self.id
        '''massaEspGra = bancodedados.massaEspecificaGraos(id)
        massaS = bancodedados.mSeca(id)
        b = bancodedados.ListStatursEstagio(id)'''

        massaEspGra = 10
        massaS = 10
        b = 10
        condition = 0
        c = 1

        if c in b:
            condition = 0

        try:
            '''grauSatInicial = bancodedados.grauSaturacaoInicial(id)
            indiceVaziosInicial = bancodedados.indiceVaziosInicial(id)
            alturaSolidos = bancodedados.AlturaSolidos(id)'''

            grauSatInicial = 10
            indiceVaziosInicial = 10
            alturaSolidos = 10
            condition = 1
        except:
            condition = 0

        if massaEspGra == '' or massaS[0] == '' or massaS[1] == '' or massaS[2] == '' or massaEspGra == 0  or massaS[0] == 0 or massaS[1] == 0 or massaS[2] == 0 or condition == 0:
            menssagError = wx.MessageDialog(self, 'NADA CALCULADO AINDA!\n\n Seu arquivo .CSV ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EAU', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createCSV("teste")

    #--------------------------------------------------
     def createCSV(self, name):
     	id = self.id

     	'''Obter dados do banco'''
        try:
            pass
        except Exception as e:
            raise

        a = bancodedados.ListaDadosInicias(id)

     	dataInicio = a[0]
     	dataFim = bancodedados.DataFinalDoEnsaio(id)
     	nomeDoEnsaio = a[12]
     	local = a[9]
     	operador = a[10]
     	profundidadeColeta = a[11]
     	diametroAnel = a[2]
     	alturaAnel = a[3]
        alturaCP = a[6]
     	volumeAnel = (pi/4)*a[2]**2
     	massaAnel = a[4]
     	massaSoloInicial = a[5] - a[4]
     	massaEspGrao = a[7]
     	teorUmidadeInicial = bancodedados.teorUmidadeInicial(id)
     	grauSatInicial = bancodedados.grauSaturacaoInicial(id)
     	indiceVaziosInicial = bancodedados.indiceVaziosInicial(id)
     	alturaSolidos = bancodedados.AlturaSolidos(id)
        P = bancodedados.P_Aplicadas(id)
        IndiceVaziosFinal = bancodedados.e_finalEstagio(id)
        Estagios = bancodedados.ComboEstagios(id)
        quant = len(Estagios)
        Tabela = []
        i = 1
        
        while i<quant:
            Tabela.append(bancodedados.TabelaEstagio(id, i))
            i = i+1

        with wx.FileDialog(self, name, wildcard="CSV files(*.csv)|*.csv*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()

            try:
                with open(fileDialog.GetPath() + '.csv', 'w') as file:
				editor = csv.writer(file)
				editor.writerow(['EAU - Ensaio de Adensamento Unidimensional','','',''])
				editor.writerow(['Data Inicial do Ensaio','','',dataInicio])
				editor.writerow(['Data Final do Ensaio','','',dataFim])
				editor.writerow(['Local','','',local])
				editor.writerow(['Operador','','',operador])
				editor.writerow(['Profundidade da coleta (m)','','',profundidadeColeta])
				editor.writerow(['','','',''])
				editor.writerow(['Diametro do Anel (mm)','','',diametroAnel])
				editor.writerow(['Altura do Anel (mm)','','',alturaAnel])
				editor.writerow(['Volume do Anel (mm3)','','',volumeAnel])
				editor.writerow(['Massa do anel (g)','','', massaAnel])
				editor.writerow(['Massa do Solo Inicial (g)','','',massaSoloInicial])
				editor.writerow(['Massa Especifica dos Graos (g/cm3)','','',massaEspGrao])
				editor.writerow(['Teor de Umidade Inicial','','',teorUmidadeInicial])
				editor.writerow(['Grau Saturacao Inicial','','',grauSatInicial])
				editor.writerow(['Indice de Vazios Inicial','','',indiceVaziosInicial])
				editor.writerow(['Altura dos Solidos (cm)','','',alturaSolidos])
                editor.writerows(Tabela)

            except IOError:
            	wx.LogError("O arquivo não pôde ser salvo em '%s'." % pathname)
