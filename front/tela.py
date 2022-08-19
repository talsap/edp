# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import banco.bancodedados as bancodedados
import banco.bdPreferences as bdPreferences
import wx.lib.agw.hyperlink as hl
import wx.lib.mixins.listctrl as listmix
import back.HexForRGB as HexRGB
from wx.lib.agw import ultimatelistctrl as ULC
from TelaNovo import TelaNovo
from cabecalhos import Cab
from calibration import Cal
from configuration import Config
from conection import Conn
from preferencias import Pref
from Pdf import *
from Csv import *
from Editar import *

global version

'''Classe da Lista editável'''
class EditableListCtrl(ULC.UltimateListCtrl, listmix.ListCtrlAutoWidthMixin):
    #--------------------------------------------------
        def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
            ULC.UltimateListCtrl.__init__(self, parent, ID, pos, size, agwStyle = ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT | ULC.ULC_HRULES | ULC.ULC_VRULES | ULC.ULC_NO_HIGHLIGHT)

        def UpdateListCtrl(self):
            self.DeleteAllItems()
            lista = bancodedados.ListaVisualizacao()
            index = 0

            for key, row in lista:
                   pos = self.InsertStringItem(index, row[0])
                   self.SetStringItem(index, 1, row[1])
                   self.SetStringItem(index, 2, row[2])
                   buttonEDT = wx.Button(self, id = key, label="")
                   buttonPDF = wx.Button(self, id = 8000+key, label="")
                   buttonCSV = wx.Button(self, id = 16000+key, label="")
                   buttonDEL = wx.Button(self, id = 24000+key, label="")
                   buttonEDT.SetBitmap(wx.Bitmap(r'icons\icons-editar-arquivo-24px.png'))
                   buttonPDF.SetBitmap(wx.Bitmap(r'icons\icons-exportar-pdf-24px.png'))
                   buttonCSV.SetBitmap(wx.Bitmap(r'icons\icons-exportar-csv-24px.png'))
                   buttonDEL.SetBitmap(wx.Bitmap(r'icons\icons-lixo-24px.png'))
                   self.SetItemWindow(pos, col=3, wnd=buttonEDT, expand=True)
                   self.SetItemWindow(pos, col=4, wnd=buttonPDF, expand=True)
                   self.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
                   self.SetItemWindow(pos, col=5, wnd=buttonDEL, expand=True)
                   self.SetItemData(index, key)
                   index += 1

            if len(lista) >=11:
               self.SetColumnWidth(0, width=170)
               self.SetColumnWidth(1, width=115)
               self.SetColumnWidth(2, width=135)
               self.SetColumnWidth(3, width=40)
               self.SetColumnWidth(4, width=40)
               self.SetColumnWidth(5, width=40)
               self.SetColumnWidth(6, width=40)
            else:
               self.SetColumnWidth(0, width=180)
               self.SetColumnWidth(1, width=120)
               self.SetColumnWidth(2, width=135)
               self.SetColumnWidth(3, width=40)
               self.SetColumnWidth(4, width=40)
               self.SetColumnWidth(5, width=40)
               self.SetColumnWidth(6, width=40)

'''Tela Inicial'''
class Tela(wx.Frame):
    #------------------------------------------------------
     def __init__(self, version, *args, **kwargs):
         super(Tela, self).__init__(parent = None, title = 'EDP - Ensaios Dinâmicos para Pavimentação - V.'+version, name = 'Facade', style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION, *args, **kwargs)
         frame = self.basic_gui()
         self.version = version
         
         colors = bdPreferences.ListColors()
         colorBackground = colors[2]

         self.SetBackgroundColour(colorBackground)

     def basic_gui(self):
         v_sizer = wx.BoxSizer(wx.VERTICAL)
         h_sizer = wx.BoxSizer(wx.HORIZONTAL)
         panel = wx.Panel(self)
        
         '''Iserção do IconeLogo'''
         try:
             ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
             self.SetIcon(ico)
         except:
             pass

         '''Configurações do Size'''
         self.SetSize((630,500))
         self.Centre()
         self.Show()

         '''StatusBar'''
         self.CreateStatusBar()
         self.SetStatusText('Ensaios Dinâmicos para Pavimentação')
         
         '''MenuBarra'''
         arquivoMenu = wx.Menu()
         configuracoesMenu = wx.Menu()
         ajudaMenu = wx.Menu()
         menuBar = wx.MenuBar()
         menuBar.Append(arquivoMenu, '&Arquivo')
         menuBar.Append(configuracoesMenu, '&Configurações')
         menuBar.Append(ajudaMenu, '&Ajuda')

         novoEnsaioMenuItem = arquivoMenu.Append(wx.NewId(),'Novo Ensaio\tCtrl+N', 'Novo Ensaio')
         arquivoMenu.AppendSeparator()
         cabecalhosMenuitem = arquivoMenu.Append(wx.NewId(), 'Cabeçalhos', 'Cabeçalhos')
         preferenciasMenuitem = arquivoMenu.Append(wx.NewId(), 'Preferências', 'Preferências')
         arquivoMenu.AppendSeparator()
         exitMenuItem = arquivoMenu.Append(wx.NewId(), 'Sair\tCtrl+S','Sair')
         calibrateLVDTitem = configuracoesMenu.Append(wx.NewId(), 'Coeficientes de Calibração \tCtrl+T', 'Coeficientes de Calibração')
         configurationEnsaio = configuracoesMenu.Append(wx.NewId(), 'Configurações dos Ensaios \tCtrl+I', 'Configurações dos Ensaios')
         configurationConection = configuracoesMenu.Append(wx.NewId(), 'Testar Conexão \tCtrl+Y', 'Testar Conexão')
         ajudaMenuItem = ajudaMenu.Append(wx.NewId(),'Ajuda\tCtrl+A','Ajuda')
         self.Bind(wx.EVT_MENU, self.NovoEnsaio, novoEnsaioMenuItem)
         self.Bind(wx.EVT_MENU, self.Cabecalhos, cabecalhosMenuitem)
         self.Bind(wx.EVT_MENU, self.Preferencias, preferenciasMenuitem)
         self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
         self.Bind(wx.EVT_MENU, self.calibrate, calibrateLVDTitem)
         self.Bind(wx.EVT_MENU, self.config, configurationEnsaio)
         self.Bind(wx.EVT_MENU, self.conection, configurationConection)
         self.Bind(wx.EVT_MENU, self.ajudaGUI, ajudaMenuItem)
         self.Bind(wx.EVT_CLOSE, self.onExit)
         self.SetMenuBar(menuBar)

         '''Botao Novo Ensaio'''
         self.button = wx.Button(panel, -1, '', size=(48,48))
         self.button.SetBitmap(wx.Bitmap(r'icons\icons-adicionar-48px.png'))
         self.Bind(wx.EVT_BUTTON, self.NovoEnsaio, self.button)
         v_sizer.AddStretchSpacer(5)
         v_sizer.Add(self.button, 0, wx.ALIGN_CENTER_HORIZONTAL)
         v_sizer.AddStretchSpacer(4)
         panel.SetSizerAndFit(v_sizer)

         lista = bancodedados.ListaVisualizacao()

         '''Lista dos Ensaios'''
         self.list_ctrl = EditableListCtrl(panel, size=(600,0))
         h_sizer.AddStretchSpacer(5)
         h_sizer.Add(self.list_ctrl, 0, wx.EXPAND)
         h_sizer.AddStretchSpacer(5)
         v_sizer.Add(h_sizer, 40, wx.ALIGN_CENTER_HORIZONTAL)
         v_sizer.AddStretchSpacer(1)
         panel.SetSizerAndFit(v_sizer)

         if len(lista) >=11:
             self.list_ctrl.InsertColumn(0, 'IDENTIFICAÇÃO', wx.LIST_FORMAT_CENTRE, width=170)
             self.list_ctrl.InsertColumn(1, 'INICIO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=115)
             self.list_ctrl.InsertColumn(2, 'TERMINO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=135)
             self.list_ctrl.InsertColumn(3, 'EDT', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(4, 'PDF', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(5, 'CSV', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(6, 'DEL', wx.LIST_FORMAT_CENTRE, width=40)
         else:
             self.list_ctrl.InsertColumn(0, 'IDENTIFICAÇÃO', wx.LIST_FORMAT_CENTRE, width=180)
             self.list_ctrl.InsertColumn(1, 'INICIO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=120)
             self.list_ctrl.InsertColumn(2, 'TERMINO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=135)
             self.list_ctrl.InsertColumn(3, 'EDT', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(4, 'PDF', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(5, 'CSV', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(6, 'DEL', wx.LIST_FORMAT_CENTRE, width=40)

         index = 0

         for key, row in lista:
             pos = self.list_ctrl.InsertStringItem(index, row[0])
             self.list_ctrl.SetStringItem(index, 1, row[1])
             self.list_ctrl.SetStringItem(index, 2, row[2])
             buttonEDT = wx.Button(self.list_ctrl, id = key, label="")
             buttonPDF = wx.Button(self.list_ctrl, id = 8000+key, label="")
             buttonCSV = wx.Button(self.list_ctrl, id = 16000+key, label="")
             buttonDEL = wx.Button(self.list_ctrl, id = 24000+key, label="")
             buttonEDT.SetBitmap(wx.Bitmap(r'icons\icons-editar-arquivo-24px.png'))
             buttonPDF.SetBitmap(wx.Bitmap(r'icons\icons-exportar-pdf-24px.png'))
             buttonCSV.SetBitmap(wx.Bitmap(r'icons\icons-exportar-csv-24px.png'))
             buttonDEL.SetBitmap(wx.Bitmap(r'icons\icons-lixo-24px.png'))
             self.list_ctrl.SetItemWindow(pos, col=3, wnd=buttonEDT, expand=True)
             self.list_ctrl.SetItemWindow(pos, col=4, wnd=buttonPDF, expand=True)
             self.list_ctrl.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
             self.list_ctrl.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
             self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
             self.Bind(wx.EVT_BUTTON, self.Pdf, buttonPDF)
             self.Bind(wx.EVT_BUTTON, self.exportCSV, buttonCSV)
             self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
             self.list_ctrl.SetItemData(index, key)
             index += 1

         self.Bind(wx.EVT_LIST_COL_DRAGGING, self.ColumAdapter, self.list_ctrl)
         self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.ColumAdapter2, self.list_ctrl)
         self.Bind(wx.EVT_LIST_COL_CLICK, self.ColumAdapter3, self.list_ctrl)

    #--------------------------------------------------
     def Editar(self, event):
         id = event.GetId()
         list = bancodedados.qual_identificador(id)
         if list[0] == "134":
             dialogo = EditarDNIT134(list[1])
         if list[0] == "179":
             dialogo = EditarDNIT179(list[1])
         if list[0] == "181":
             dialogo = EditarDNIT181(list[1])

    #--------------------------------------------------
     def Pdf(self, event):
         id = event.GetId()
         id = id - 8000
         list = bancodedados.qual_identificador(id)
         if list[0] == "134":
             dialogo = Pdf134(list[1])
         if list[0] == "179":
             dialogo = Pdf179(list[1])
         if list[0] == "181":
             dialogo = Pdf181(list[1])
    #--------------------------------------------------
     def exportCSV(self, event):
         id = event.GetId()
         id = id - 16000
         list = bancodedados.qual_identificador(id)
         if list[0] == "134":
             dialogo = Csv134(list[1])
         if list[0] == "179":
             dialogo = Csv179(list[1])
         if list[0] == "181":
             dialogo = Csv181(list[1])

    #--------------------------------------------------
     def Deletar(self, event):
         id = event.GetId()
         id = id - 24000
         list = bancodedados.qual_identificador(id)
         print list[1]
         print id

         '''Diálogo se deseja realmente excluir o Ensaio'''
         dlg = wx.MessageDialog(None, 'Deseja mesmo excluir esse Ensaio?', 'EDP', wx.ICON_EXCLAMATION | wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
         result = dlg.ShowModal()

         if result == wx.ID_YES:
             bancodedados.delete(list[1])
             dlg.Destroy()

             self.list_ctrl.DeleteAllItems()
             lista = bancodedados.ListaVisualizacao()
             index = 0

             for key, row in lista:
                    pos = self.list_ctrl.InsertStringItem(index, row[0])
                    self.list_ctrl.SetStringItem(index, 1, row[1])
                    self.list_ctrl.SetStringItem(index, 2, row[2])
                    buttonEDT = wx.Button(self.list_ctrl, id = key, label="")
                    buttonPDF = wx.Button(self.list_ctrl, id = 8000+key, label="")
                    buttonCSV = wx.Button(self.list_ctrl, id = 16000+key, label="")
                    buttonDEL = wx.Button(self.list_ctrl, id = 24000+key, label="")
                    buttonEDT.SetBitmap(wx.Bitmap(r'icons\icons-editar-arquivo-24px.png'))
                    buttonPDF.SetBitmap(wx.Bitmap(r'icons\icons-exportar-pdf-24px.png'))
                    buttonCSV.SetBitmap(wx.Bitmap(r'icons\icons-exportar-csv-24px.png'))
                    buttonDEL.SetBitmap(wx.Bitmap(r'icons\icons-lixo-24px.png'))
                    self.list_ctrl.SetItemWindow(pos, col=3, wnd=buttonEDT, expand=True)
                    self.list_ctrl.SetItemWindow(pos, col=4, wnd=buttonPDF, expand=True)
                    self.list_ctrl.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
                    self.list_ctrl.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
                    self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
                    self.Bind(wx.EVT_BUTTON, self.Pdf, buttonPDF)
                    self.Bind(wx.EVT_BUTTON, self.exportCSV, buttonCSV)
                    self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
                    self.list_ctrl.SetItemData(index, key)
                    index += 1

             if len(lista) >=11:
                self.list_ctrl.SetColumnWidth(0, width=170)
                self.list_ctrl.SetColumnWidth(1, width=115)
                self.list_ctrl.SetColumnWidth(2, width=135)
                self.list_ctrl.SetColumnWidth(3, width=40)
                self.list_ctrl.SetColumnWidth(4, width=40)
                self.list_ctrl.SetColumnWidth(5, width=40)
                self.list_ctrl.SetColumnWidth(6, width=40)
             else:
                self.list_ctrl.SetColumnWidth(0, width=180)
                self.list_ctrl.SetColumnWidth(1, width=120)
                self.list_ctrl.SetColumnWidth(2, width=135)
                self.list_ctrl.SetColumnWidth(3, width=40)
                self.list_ctrl.SetColumnWidth(4, width=40)
                self.list_ctrl.SetColumnWidth(5, width=40)
                self.list_ctrl.SetColumnWidth(6, width=40)
         else:
             dlg.Destroy()

    #--------------------------------------------------
     def NovoEnsaio(self, event):
         '''quant = bancodedados.quant_ensaios_deletados()'''
         '''valor_Logico = bancodedados.ler_quant_ensaios() - 1 - quant'''
         dialogo = TelaNovo().ShowModal()

         self.list_ctrl.DeleteAllItems()
         lista = bancodedados.ListaVisualizacao()
         index = 0

         for key, row in lista:
                pos = self.list_ctrl.InsertStringItem(index, row[0])
                self.list_ctrl.SetStringItem(index, 1, row[1])
                self.list_ctrl.SetStringItem(index, 2, row[2])
                buttonEDT = wx.Button(self.list_ctrl, id = key, label="")
                buttonPDF = wx.Button(self.list_ctrl, id = 8000+key, label="")
                buttonCSV = wx.Button(self.list_ctrl, id = 16000+key, label="")
                buttonDEL = wx.Button(self.list_ctrl, id = 24000+key, label="")
                buttonEDT.SetBitmap(wx.Bitmap(r'icons\icons-editar-arquivo-24px.png'))
                buttonPDF.SetBitmap(wx.Bitmap(r'icons\icons-exportar-pdf-24px.png'))
                buttonCSV.SetBitmap(wx.Bitmap(r'icons\icons-exportar-csv-24px.png'))
                buttonDEL.SetBitmap(wx.Bitmap(r'icons\icons-lixo-24px.png'))
                self.list_ctrl.SetItemWindow(pos, col=3, wnd=buttonEDT, expand=True)
                self.list_ctrl.SetItemWindow(pos, col=4, wnd=buttonPDF, expand=True)
                self.list_ctrl.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
                self.list_ctrl.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
                self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
                self.Bind(wx.EVT_BUTTON, self.Pdf, buttonPDF)
                self.Bind(wx.EVT_BUTTON, self.exportCSV, buttonCSV)
                self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
                self.list_ctrl.SetItemData(index, key)
                index += 1

         if len(lista) >=11:
            self.list_ctrl.SetColumnWidth(0, width=170)
            self.list_ctrl.SetColumnWidth(1, width=115)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=40)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)
         else:
            self.list_ctrl.SetColumnWidth(0, width=180)
            self.list_ctrl.SetColumnWidth(1, width=120)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=40)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def Cabecalhos(self, event):
         '''Abri tela com os Cabeçalhos cadastrados'''
         frame = Cab()
    
    #--------------------------------------------------
     def Preferencias(self, event):
         '''Abri tela com as preferências'''
         frame = Pref()

    #--------------------------------------------------
     def ajudaGUI(self, event):
          '''Dialogo ajuda'''
          message1 = ('Software EDP - Ensaios Dinâmicos para Pavimentação - versão %s\n\n' % self.version)
          message2 = ('Este software foi desenvolvido para facilitar a realização de alguns ensaios dinâmicos que estão previstos nas seguintes normas brasileira segundo o DNIT:\n\nDNIT 134/2018-ME           DNIT 179/2018-IE           DNIT 181/2018-ME       \n\nDúvidas em relação ao software, entrar em contato através do\ne-mail: ')
          message3 = ('tarcisiosapucaia@hotmail.com')
          dlg = wx.MessageDialog(self, message1 + message2 + message3, 'EDP', wx.OK|wx.ICON_INFORMATION)
          aboutPanel = wx.TextCtrl(dlg, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
          dlg.ShowModal()
          dlg.Destroy()

    #--------------------------------------------------
     def ColumAdapter(self, event):
         '''lista = bancodedados.ListaVisualizacao()'''
         '''Ajusta os tamanhos das colunas ao arrastar'''
         if len(lista) >=11:
            self.list_ctrl.SetColumnWidth(0, width=170)
            self.list_ctrl.SetColumnWidth(1, width=115)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=40)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)
         else:
            self.list_ctrl.SetColumnWidth(0, width=180)
            self.list_ctrl.SetColumnWidth(1, width=120)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=40)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def ColumAdapter2(self, event):
         '''lista = bancodedados.ListaVisualizacao()'''
         '''Ajusta os tamanhos das colunas ao clicar com botão esquerdo sobre a coluna'''
         if len(lista) >=11:
            self.list_ctrl.SetColumnWidth(0, width=170)
            self.list_ctrl.SetColumnWidth(1, width=115)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=40)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)
         else:
            self.list_ctrl.SetColumnWidth(0, width=180)
            self.list_ctrl.SetColumnWidth(1, width=120)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=40)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def ColumAdapter3(self, event):
         '''lista = bancodedados.ListaVisualizacao()'''
         '''Ajusta os tamanhos das colunas ao clicar com o botão direito sobre a coluna'''
         if len(lista) >=11:
            self.list_ctrl.SetColumnWidth(0, width=170)
            self.list_ctrl.SetColumnWidth(1, width=115)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=40)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)
         else:
            self.list_ctrl.SetColumnWidth(0, width=180)
            self.list_ctrl.SetColumnWidth(1, width=120)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=40)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def onExit(self, event):
          '''Opcao Sair'''
          self.Destroy()
          
    #--------------------------------------------------
     def calibrate(self, event):
          '''Opcao Calibração'''
          frame = Cal()

    #--------------------------------------------------
     def config(self, event):
         '''Opcao de Configuração'''
         frame = Config()
    
    #--------------------------------------------------
     def conection(self, event):
         '''Opcao de conexao'''
         frame = Conn()

