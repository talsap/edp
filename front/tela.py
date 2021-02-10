# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import bancodedados
import wx.lib.agw.hyperlink as hl
import wx.lib.mixins.listctrl as listmix
from wx.lib.agw import ultimatelistctrl as ULC
from TelaNovo import TelaNovo
from cabecalhos import Cab
from Pdf import Pdf
'''from Editar import Editar'''
'''from Csv import Csv'''

'''lista = [[1, ['DNIT134/2018ME - C.P. N XXX', '16:25:19  19/07/2019', '17:51:58  19/07/2019']], [2, ['DNIT134/2018ME - C.P. N XXX', '07:32:26  29/07/2019', '17:51:58  19/07/2019']], [3, ['DNIT134/2018ME - C.P. N XXX', '12:14:48  29/07/2019', '17:51:58  19/07/2019']], [4, ['DNIT134/2018ME - C.P. N XXX', '16:55:57  30/07/2019', '17:51:58  19/07/2019']], [5, ['DNIT134/2018ME - C.P. N XXX', '16:55:57  30/07/2019', '17:51:58  19/07/2019']], [6, ['DNIT134/2018ME - C.P. N XXX', '16:55:57  30/07/2019', '17:51:58  19/07/2019']], [7, ['DNIT134/2018ME - C.P. N XXX', '16:55:57  30/07/2019', '17:51:58  19/07/2019']], [8, ['DNIT134/2018ME - C.P. N XXX', '16:55:57  30/07/2019', '17:51:58  19/07/2019']], [9, ['DNIT134/2018ME - C.P. N XXX', '16:55:57  30/07/2019', '17:51:58  19/07/2019']], [10, ['DNIT134/2018ME - C.P. N XXX', '16:55:57  30/07/2019', '17:51:58  19/07/2019']], [11, ['DNIT134/2018ME - C.P. N XXX', '16:55:57  30/07/2019', '17:51:58  19/07/2019']]]'''

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
     def __init__(self, *args, **kwargs):
         super(Tela, self).__init__(title = 'EDP - Beta', name = 'Facade', style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION, *args, **kwargs)
         frame = self.basic_gui()

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
         arquivoMenu.AppendSeparator()
         exitMenuItem = arquivoMenu.Append(wx.NewId(), 'Sair\tCtrl+S','Sair')
         ajudaMenuItem = ajudaMenu.Append(wx.NewId(),'Ajuda\tCtrl+A','Ajuda')
         self.Bind(wx.EVT_MENU, self.NovoEnsaio, novoEnsaioMenuItem)
         self.Bind(wx.EVT_MENU, self.Cabecalhos, cabecalhosMenuitem)
         self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
         self.Bind(wx.EVT_MENU, self.ajudaGUI, ajudaMenuItem)
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
             self.list_ctrl.InsertColumn(0, 'IDENTIFICADOR', wx.LIST_FORMAT_CENTRE, width=170)
             self.list_ctrl.InsertColumn(1, 'INICIO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=115)
             self.list_ctrl.InsertColumn(2, 'TERMINO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=135)
             self.list_ctrl.InsertColumn(3, 'EDT', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(4, 'PDF', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(5, 'CSV', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(6, 'DEL', wx.LIST_FORMAT_CENTRE, width=40)
         else:
             self.list_ctrl.InsertColumn(0, 'IDENTIFICADOR', wx.LIST_FORMAT_CENTRE, width=180)
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
         print str(id)+'EDI'

    #--------------------------------------------------
     def Pdf(self, event):
         id = event.GetId()
         id = id - 8000
         print str(id)+'PDF'
         dialogo = Pdf(id).ShowModal()

    #--------------------------------------------------
     def exportCSV(self, event):
         id = event.GetId()
         id = id - 16000
         print str(id)+'CSV'

    #--------------------------------------------------
     def Deletar(self, event):
         id = event.GetId()
         id = id - 24000
         print str(id)+'DEL'

         '''Diálogo se deseja realmente excluir o Ensaio'''
         dlg = wx.MessageDialog(None, 'Deseja mesmo excluir esse Ensaio?', 'EAU', wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
         result = dlg.ShowModal()

         if result == wx.ID_YES:
             bancodedados.delete(id)
             dlg.Destroy()

             self.list_ctrl.DeleteAllItems()
             '''lista = bancodedados.ListaVisualizacao()'''
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
     def ajudaGUI(self, event):
          '''Dialogo ajuda'''
          message1 = ('Software EDP - Ensaios Dinâmicos para Pavimentação\n\n')
          message2 = ('Este software foi desenvolvido para facilitar a realização dos ensaios que determina o módulo de resiliência, o módulo dinâmico e a resistência a deformação permanente, tanto para solos quanto para misturas asfálticas de acordo com as normas do DNIT:\n\nDNIT 134/2018-ME       DNIT 135/2018-ME        DNIT 179/2018-IE\nDNIT 184/2018-ME       DNIT 416/2019-ME\n\nDúvidas em relação ao software, entrar em contato através do\ne-mail: ')
          message3 = ('tarcisiosapucaia27@gmail.com')
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
          self.Close(True)
