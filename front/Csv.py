# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import bancodedados
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
        frame = self.basic_gui()

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
          ensaio = list[0]
          status = list[1]
          tipo = list[2]
          cp = list[3]
          rodovia = list[4]
          origem = list[5]
          trecho = list[6]
          estkm = list[7]
          operador = list[8]
          datadacoleta = list[9]
          datainicio = list[10]
          datafim = list[11]
          amostra = list[12]
          diametro = list[13]
          altura = list[14]
          obs = list[15]
          freq = list[16]
          if int(amostra) == 0:
              valoramostra = 'Deformada'
          else:
              valoramostra = 'Indeformada'
          with wx.FileDialog(self, name, wildcard="CSV files(*.csv)|*.csv*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
               if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

               pathname = fileDialog.GetPath()

               try:
                    with open(fileDialog.GetPath() + '.csv', 'wb') as file:
                         editor = csv.writer(file, delimiter=';')
                         editor.writerow(['EDP -', 'ENSAIOS', 'DINAMICOS', 'PARA', 'PAVIMENTACAO'])
                         editor.writerow(['Identificador:', idt])
                         editor.writerow(['Inicio do ensaio:', datainicio])
                         editor.writerow(['Fim do ensaio:', datafim])
                         editor.writerow(['Coleta da amostra:', datadacoleta])
                         editor.writerow(['N do CP:', cp])
                         editor.writerow(['Rodovia:', rodovia])
                         editor.writerow(['Origem:', origem])
                         editor.writerow(['Trecho:', trecho])
                         editor.writerow(['est/km:', estkm])
                         editor.writerow(['Observacao:', obs])
                         editor.writerow(['Operador:', operador])
                         editor.writerow(['Tipo da amostra:', valoramostra,])
                         editor.writerow(['Diametro [mm]:', format(diametro).replace('.',',')])
                         editor.writerow(['Altura [mm]:', format(altura).replace('.',',')])
                         editor.writerow(['Frequencia do ensaio:', str(freq)+'Hz'])
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
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_134(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA CALCULADO AINDA!\n\n Seu arquivo .CSV ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createCSV("Export CSV - "+idt)

    #--------------------------------------------------
     def createCSV(self, name):
          idt = self.idt
          list = self.list

          '''Obter dados do banco'''
          list = bancodedados.dados_iniciais_(idt)
          ensaio = list[0]
          status = list[1]
          tipo = list[2]
          cp = list[3]
          rodovia = list[4]
          origem = list[5]
          trecho = list[6]
          estkm = list[7]
          operador = list[8]
          datdacoleta = list[9]
          datainicio = list[10]
          datafim = list[11]
          amostra = list[12]
          diametro = list[13]
          altura = list[14]
          obs = list[15]
          freq = list[16]

          with wx.FileDialog(self, name, wildcard="CSV files(*.csv)|*.csv*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
               if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

               pathname = fileDialog.GetPath()

               try:
                    with open(fileDialog.GetPath() + '.csv', 'wb') as file:
                         editor = csv.writer(file)
                         i = 0
                         while i < len(list):
                              editor.writerows([list[i]])
                              i+=1

               except IOError:
                    wx.LogError("O arquivo não pôde ser salvo em '%s'." % pathname)
