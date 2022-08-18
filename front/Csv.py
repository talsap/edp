# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import banco.bancodedados as bancodedados
import banco.bdConfiguration as bdConfiguration
import unicodecsv
import csv
import math

pi = math.pi

'''Class Export CSV134'''
class Csv134(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - CSV')
        self.idt = idt
        self.Bind(wx.EVT_CLOSE, self.onExit)
        frame = self.basic_gui()

     #--------------------------------------------------
     def onExit(self, event):
          '''Opcao Sair'''
          self.Destroy()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_134(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo .CSV ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createCSV("EDP CSV - "+idt)

    #--------------------------------------------------
     def createCSV(self, name):
          idt = self.idt
          lista = self.list

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
               desvioUmidade = float(teorUmidade)-float(umidadeOtima)
          except:
               desvioUmidade = ''

          with wx.FileDialog(self, name, wildcard="CSV files(*.csv)|*.csv*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
               if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

               pathname = fileDialog.GetPath()

               try:
                    with open(fileDialog.GetPath() + '.csv', 'wb') as csvfile:
                         editor = unicodecsv.writer(csvfile, delimiter=';', encoding='utf-8')
                         editor.writerow(['EDP -', 'ENSAIOS', 'DINAMICOS', 'PARA', 'PAVIMENTACAO'])
                         editor.writerow(['Identificacao:', idt])
                         editor.writerow(['Norma de referencia:', 'DNIT 134/2018-ME'])
                         editor.writerow(['Coleta da amostra:', datadacoleta])
                         editor.writerow(['Inicio do ensaio:', datainicio])
                         editor.writerow(['Fim do ensaio:', datafim])
                         editor.writerow(['Natureza da amostra:', naturazaDaAmostra])
                         editor.writerow(['Tipo da amostra:', valoramostra])
                         editor.writerow(['Energia de compactacao:', energiaCompactacao])
                         editor.writerow(['Diametro [mm]:', format(diametro).replace('.',',')])
                         editor.writerow(['Altura [mm]:', format(altura).replace('.',',')])
                         editor.writerow(['Teor de umidade do Corpo de Prova [%]:', teorUmidade])
                         editor.writerow(['Peso especifico seco do Corpo de Prova [kN/m3]:', pesoEspecifico])
                         editor.writerow(['Grau de compactacao do Corpo de Prova [%]:', grauCompactacao])
                         editor.writerow(['Desvio de umidade [%]:', desvioUmidade])
                         editor.writerow(['Frequencia do ensaio [Hz]:', freq])
                         editor.writerow(['Curso do LVDT empregado [mm]:', int(lvdt[3])])                         
                         editor.writerow(['','','',''])
                         i = 0
                         while i < len(lista):
                              editor.writerow(lista[i])
                              i+=1

               except IOError:
                    wx.LogError("O arquivo não pôde ser salvo em '%s'." % pathname)

'''Class Export CSV179'''
class Csv179(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - CSV')
        self.idt = idt
        frame = self.basic_gui()

     #--------------------------------------------------
     def onExit(self, event):
          '''Opcao Sair'''
          self.Destroy()
          
    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_179(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo .CSV ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createCSV("EDP CSV - "+idt)

    #--------------------------------------------------
     def createCSV(self, name):
          idt = self.idt
          lista = self.list

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
               desvioUmidade = float(teorUmidade)-float(umidadeOtima)
          except:
               desvioUmidade = ''
          try:
               pressaoConf = float(pressaoConf)*1000
          except:
               pressaoConf = ''
          try:
               pressaoDesvio = float(pressaoDesvio)*1000
          except:
               pressaoDesvio = ''

          with wx.FileDialog(self, name, wildcard="CSV files(*.csv)|*.csv*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
               if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

               pathname = fileDialog.GetPath()

               try:
                    with open(fileDialog.GetPath() + '.csv', 'wb') as csvfile:
                         editor = unicodecsv.writer(csvfile, delimiter=';', encoding='utf-8')
                         editor.writerow(['EDP -', 'ENSAIOS', 'DINAMICOS', 'PARA', 'PAVIMENTACAO'])
                         editor.writerow(['Identificacao:', idt])
                         editor.writerow(['Norma de referencia:', 'DNIT 134/2018-ME'])
                         editor.writerow(['Coleta da amostra:', datadacoleta])
                         editor.writerow(['Inicio do ensaio:', datainicio])
                         editor.writerow(['Fim do ensaio:', datafim])
                         editor.writerow(['Natureza da amostra:', naturazaDaAmostra])
                         editor.writerow(['Tipo da amostra:', valoramostra,])
                         editor.writerow(['Energia de compactacao:', energiaCompactacao])
                         editor.writerow(['Diametro [mm]:', format(diametro).replace('.',',')])
                         editor.writerow(['Altura [mm]:', format(altura).replace('.',',')])
                         editor.writerow(['Teor de umidade do Corpo de Prova [%]:', teorUmidade])
                         editor.writerow(['Peso especifico seco do Corpo de Prova [kN/m3]:', pesoEspecifico])
                         editor.writerow(['Grau de compactacao do Corpo de Prova [%]:', grauCompactacao])
                         editor.writerow(['Desvio de umidade [%]:', desvioUmidade])
                         editor.writerow(['Frequencia do ensaio [Hz]:', freq])
                         editor.writerow(['Curso do LVDT empregado [mm]:', int(lvdt[3])])
                         editor.writerow(['Sigma3 [kPa]:', format(pressaoConf).replace('.',',')])    
                         editor.writerow(['Sigmad [kPa]:', format(pressaoDesvio).replace('.',',')])                      
                         editor.writerow(['','','',''])
                         i = 0
                         while i < len(lista):
                              editor.writerow(lista[i])
                              i+=1

               except IOError:
                    wx.LogError("O arquivo não pôde ser salvo em '%s'." % pathname)

'''Class Export CSV181'''
class Csv181(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - CSV')
        self.idt = idt
        frame = self.basic_gui()

     #--------------------------------------------------
     def onExit(self, event):
          '''Opcao Sair'''
          self.Destroy()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_181(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo .CSV ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createCSV("EDP CSV - "+idt)

    #--------------------------------------------------
     def createCSV(self, name):
          idt = self.idt
          lista = self.list

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
               desvioUmidade = float(teorUmidade)-float(umidadeOtima)
          except:
               desvioUmidade = ''

          with wx.FileDialog(self, name, wildcard="CSV files(*.csv)|*.csv*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
               if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

               pathname = fileDialog.GetPath()

               try:
                    with open(fileDialog.GetPath() + '.csv', 'wb') as csvfile:
                         editor = unicodecsv.writer(csvfile, delimiter=';', encoding='utf-8')
                         editor.writerow(['EDP -', 'ENSAIOS', 'DINAMICOS', 'PARA', 'PAVIMENTACAO'])
                         editor.writerow(['Identificacao:', idt])
                         editor.writerow(['Norma de referencia:', 'DNIT 134/2018-ME'])
                         editor.writerow(['Coleta da amostra:', datadacoleta])
                         editor.writerow(['Inicio do ensaio:', datainicio])
                         editor.writerow(['Fim do ensaio:', datafim])
                         editor.writerow(['Natureza da amostra:', naturazaDaAmostra])
                         editor.writerow(['Tipo de estabilizante quimico:', tipoEstabilizante])
                         editor.writerow(['Tempo de cura [dias]:', tempoCura])
                         editor.writerow(['Peso do estabilizante quimico [%]:', pesoEstabilizante])
                         editor.writerow(['Energia de compactacao:', energiaCompactacao])
                         editor.writerow(['Diametro [mm]:', format(diametro).replace('.',',')])
                         editor.writerow(['Altura [mm]:', format(altura).replace('.',',')])
                         editor.writerow(['Teor de umidade do Corpo de Prova [%]:', teorUmidade])
                         editor.writerow(['Peso especifico seco do Corpo de Prova [kN/m3]:', pesoEspecifico])
                         editor.writerow(['Grau de compactacao do Corpo de Prova [%]:', grauCompactacao])
                         editor.writerow(['Desvio de umidade [%]:', desvioUmidade])
                         editor.writerow(['Frequencia do ensaio [Hz]:', freq])
                         editor.writerow(['Curso do LVDT empregado [mm]:', int(lvdt[3])])                         
                         editor.writerow(['','','',''])
                         i = 0
                         while i < len(lista):
                              editor.writerow(lista[i])
                              i+=1

               except IOError:
                    wx.LogError("O arquivo não pôde ser salvo em '%s'." % pathname)

