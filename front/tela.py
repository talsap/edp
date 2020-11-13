# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
'''import bancodedados'''
import wx.lib.mixins.listctrl as listmix
from wx.lib.agw import ultimatelistctrl as ULC
'''from novo import TelaNovo'''
'''from capsulas import Cap'''
'''from Editar import Editar'''
'''from Csv import Csv'''

'''Classe da Lista editável'''
class EditableListCtrl(ULC.UltimateListCtrl, listmix.ListCtrlAutoWidthMixin):
    #--------------------------------------------------
        def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
            ULC.UltimateListCtrl.__init__(self, parent, ID, pos, size, agwStyle = ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT | ULC.ULC_HRULES | ULC.ULC_VRULES | ULC.ULC_NO_HIGHLIGHT)

        def UpdateListCtrl(self):
            self.DeleteAllItems()
            '''lista = bancodedados.ListaVisualizacao()'''
            index = 0

            for key, row in lista:
                   pos = self.InsertStringItem(index, row[0])
                   self.SetStringItem(index, 1, row[1])
                   self.SetStringItem(index, 2, row[2])
                   self.SetStringItem(index, 3, row[3])
                   buttonEDT = wx.Button(self, id = key, label="")
                   buttonGRF = wx.Button(self, id = 4000+key, label="")
                   buttonPDF = wx.Button(self, id = 10000+key, label="")
                   buttonCSV = wx.Button(self, id = 15000+key, label="")
                   buttonDEL = wx.Button(self, id = 20000+key, label="")
                   buttonEDT.SetBitmap(wx.Bitmap('icons\icons-editar-arquivo-24px.png'))
                   buttonGRF.SetBitmap(wx.Bitmap('icons\icons-grafico-24px.png'))
                   buttonPDF.SetBitmap(wx.Bitmap('icons\icons-exportar-pdf-24px.png'))
                   buttonCSV.SetBitmap(wx.Bitmap('icons\icons-exportar-csv-24px.png'))
                   buttonDEL.SetBitmap(wx.Bitmap('icons\icons-lixo-24px.png'))
                   self.SetItemWindow(pos, col=4, wnd=buttonEDT, expand=True)
                   self.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
                   self.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
                   self.SetItemData(index, key)
                   index += 1

            if len(lista) >=8:
               self.SetColumnWidth(0, width=115)
               self.SetColumnWidth(1, width=115)
               self.SetColumnWidth(2, width=135)
               self.SetColumnWidth(3, width=70)
               self.SetColumnWidth(4, width=40)
               self.SetColumnWidth(5, width=40)
               self.SetColumnWidth(6, width=40)
            else:
               self.SetColumnWidth(0, width=125)
               self.SetColumnWidth(1, width=120)
               self.SetColumnWidth(2, width=135)
               self.SetColumnWidth(3, width=70)
               self.SetColumnWidth(4, width=40)
               self.SetColumnWidth(5, width=40)
               self.SetColumnWidth(6, width=40)

'''Tela Inicial'''
class Tela(wx.Frame):
    #------------------------------------------------------
     def __init__(self, *args, **kwargs):
         super(Tela, self).__init__(title = 'EDP - Beta', name = 'Facade', style = wx.MAXIMIZE_BOX |wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION, *args, **kwargs)
         frame = self.basic_gui()

     def basic_gui(self):
         v_sizer = wx.BoxSizer(wx.VERTICAL)
         h_sizer = wx.BoxSizer(wx.HORIZONTAL)
         self.panel = wx.Panel(self)

         '''Iserção do IconeLogo'''
         ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
         self.SetIcon(ico)

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
         novoCabecalhoMenuiItem = arquivoMenu.Append(wx.NewId(), 'Novo Cabeçalho', 'Novo Cabeçalho')
         cabecalhosMenuitem = arquivoMenu.Append(wx.NewId(), 'Cabeçalhos', 'Cabeçalhos')
         arquivoMenu.AppendSeparator()
         exitMenuItem = arquivoMenu.Append(wx.NewId(), 'Sair\tCtrl+S','Sair')
         ajudaMenuItem = ajudaMenu.Append(wx.NewId(),'Ajuda\tCtrl+A','Ajuda')
         self.Bind(wx.EVT_MENU, self.NovoEnsaio, novoEnsaioMenuItem)
         self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
         self.Bind(wx.EVT_MENU, self.ajudaGUI, ajudaMenuItem)
         self.SetMenuBar(menuBar)

         '''Botao Novo Ensaio'''
         self.button = wx.Button(self.panel, -1, '', size=(48,48))
         self.button.SetBitmap(wx.Bitmap('icons\icons-adicionar-48px.png'))
         self.Bind(wx.EVT_BUTTON, self.NovoEnsaio, self.button)
         v_sizer.AddStretchSpacer(5)
         v_sizer.Add(self.button, 0, wx.ALIGN_CENTER_HORIZONTAL)
         v_sizer.AddStretchSpacer(5)
         self.panel.SetSizerAndFit(v_sizer)

         '''lista = bancodedados.ListaVisualizacao()'''

         '''Lista dos Ensaios'''
         self.list_ctrl = EditableListCtrl(self.panel, size=(600,0))
         h_sizer.AddStretchSpacer(5)
         h_sizer.Add(self.list_ctrl, 0, wx.EXPAND)
         h_sizer.AddStretchSpacer(5)
         v_sizer.Add(h_sizer, 35, wx.ALIGN_CENTER_HORIZONTAL)
         v_sizer.AddStretchSpacer(1)
         self.panel.SetSizerAndFit(v_sizer)

         '''if len(lista) >=8:
             self.list_ctrl.InsertColumn(0, 'IDENTIFICADOR', wx.LIST_FORMAT_CENTRE, width=115)
             self.list_ctrl.InsertColumn(1, 'INICIO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=115)
             self.list_ctrl.InsertColumn(2, 'TERMINO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=135)
             self.list_ctrl.InsertColumn(3, 'ESTAGIOS', wx.LIST_FORMAT_CENTRE, width=70)
             self.list_ctrl.InsertColumn(4, 'EDT', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(7, 'CSV', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(8, 'DEL', wx.LIST_FORMAT_CENTRE, width=40)
         else:
             self.list_ctrl.InsertColumn(0, 'IDENTIFICADOR', wx.LIST_FORMAT_CENTRE, width=125)
             self.list_ctrl.InsertColumn(1, 'INICIO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=120)
             self.list_ctrl.InsertColumn(2, 'TERMINO DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=135)
             self.list_ctrl.InsertColumn(3, 'ESTAGIOS', wx.LIST_FORMAT_CENTRE, width=70)
             self.list_ctrl.InsertColumn(4, 'EDT', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(7, 'CSV', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(8, 'DEL', wx.LIST_FORMAT_CENTRE, width=40)

         index = 0

         for key, row in lista:
             pos = self.list_ctrl.InsertStringItem(index, row[0])
             self.list_ctrl.SetStringItem(index, 1, row[1])
             self.list_ctrl.SetStringItem(index, 2, row[2])
             self.list_ctrl.SetStringItem(index, 3, row[3])
             buttonEDT = wx.Button(self.list_ctrl, id = key, label="")
             buttonGRF = wx.Button(self.list_ctrl, id = 4000+key, label="")
             buttonPDF = wx.Button(self.list_ctrl, id = 10000+key, label="")
             buttonCSV = wx.Button(self.list_ctrl, id = 15000+key, label="")
             buttonDEL = wx.Button(self.list_ctrl, id = 20000+key, label="")
             buttonEDT.SetBitmap(wx.Bitmap('icons\icons-editar-arquivo-24px.png'))
             buttonGRF.SetBitmap(wx.Bitmap('icons\icons-grafico-24px.png'))
             buttonPDF.SetBitmap(wx.Bitmap('icons\icons-exportar-pdf-24px.png'))
             buttonCSV.SetBitmap(wx.Bitmap('icons\icons-exportar-csv-24px.png'))
             buttonDEL.SetBitmap(wx.Bitmap('icons\icons-lixo-24px.png'))
             self.list_ctrl.SetItemWindow(pos, col=4, wnd=buttonEDT, expand=True)
             self.list_ctrl.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
             self.list_ctrl.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
             self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
             self.Bind(wx.EVT_BUTTON, self.exportCSV, buttonCSV)
             self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
             self.list_ctrl.SetItemData(index, key)
             index += 1

         self.Bind(wx.EVT_LIST_COL_DRAGGING, self.ColumAdapter, self.list_ctrl)
         self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.ColumAdapter2, self.list_ctrl)
         self.Bind(wx.EVT_LIST_COL_CLICK, self.ColumAdapter3, self.list_ctrl)
         self.vBox = wx.BoxSizer(wx.VERTICAL)
         self.vBox.Add ((-1, 140))
         self.vBox.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 20)
         self.SetSizer(self.vBox)'''

    #--------------------------------------------------
     def Editar(self, event):
         id = event.GetId()
         dialogo = Editar(id)
         resultado = dialogo.ShowModal()
         self.list_ctrl.UpdateListCtrl()

    #--------------------------------------------------
     def exportCSV(self, event):
         id = event.GetId()
         id = id - 15000
         dialogo = Csv(id)

    #--------------------------------------------------
     def Deletar(self, event):
         id = event.GetId()
         id = id - 20000

         '''Diálogo se deseja realmente excluir o Ensaio'''
         dlg = wx.MessageDialog(None, 'Deseja mesmo excluir esse Ensaio?', 'EAU', wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
         result = dlg.ShowModal()

         if result == wx.ID_YES:
             bancodedados.delete(id)
             dlg.Destroy()

             self.list_ctrl.DeleteAllItems()
             lista = bancodedados.ListaVisualizacao()
             index = 0

             for key, row in lista:
                    pos = self.list_ctrl.InsertStringItem(index, row[0])
                    self.list_ctrl.SetStringItem(index, 1, row[1])
                    self.list_ctrl.SetStringItem(index, 2, row[2])
                    self.list_ctrl.SetStringItem(index, 3, row[3])
                    buttonEDT = wx.Button(self.list_ctrl, id = key, label="")
                    buttonGRF = wx.Button(self.list_ctrl, id = 4000+key, label="")
                    buttonPDF = wx.Button(self.list_ctrl, id = 10000+key, label="")
                    buttonCSV = wx.Button(self.list_ctrl, id = 15000+key, label="")
                    buttonDEL = wx.Button(self.list_ctrl, id = 20000+key, label="")
                    buttonEDT.SetBitmap(wx.Bitmap('icons\icons-editar-arquivo-24px.png'))
                    buttonGRF.SetBitmap(wx.Bitmap('icons\icons-grafico-24px.png'))
                    buttonPDF.SetBitmap(wx.Bitmap('icons\icons-exportar-pdf-24px.png'))
                    buttonCSV.SetBitmap(wx.Bitmap('icons\icons-exportar-csv-24px.png'))
                    buttonDEL.SetBitmap(wx.Bitmap('icons\icons-lixo-24px.png'))
                    self.list_ctrl.SetItemWindow(pos, col=4, wnd=buttonEDT, expand=True)
                    self.list_ctrl.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
                    self.list_ctrl.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
                    self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
                    self.Bind(wx.EVT_BUTTON, self.exportCSV, buttonCSV)
                    self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
                    self.list_ctrl.SetItemData(index, key)
                    index += 1

             if len(lista) >=8:
                self.list_ctrl.SetColumnWidth(0, width=115)
                self.list_ctrl.SetColumnWidth(1, width=115)
                self.list_ctrl.SetColumnWidth(2, width=135)
                self.list_ctrl.SetColumnWidth(3, width=70)
                self.list_ctrl.SetColumnWidth(4, width=40)
                self.list_ctrl.SetColumnWidth(5, width=40)
                self.list_ctrl.SetColumnWidth(6, width=40)
             else:
                self.list_ctrl.SetColumnWidth(0, width=125)
                self.list_ctrl.SetColumnWidth(1, width=120)
                self.list_ctrl.SetColumnWidth(2, width=135)
                self.list_ctrl.SetColumnWidth(3, width=70)
                self.list_ctrl.SetColumnWidth(4, width=40)
                self.list_ctrl.SetColumnWidth(5, width=40)
                self.list_ctrl.SetColumnWidth(6, width=40)
         else:
             dlg.Destroy()

    #--------------------------------------------------
     def NovoEnsaio(self, event):
         quant = bancodedados.quant_ensaios_deletados()
         valor_Logico = bancodedados.ler_quant_ensaios() - 1 - quant
         frame = TelaNovo()
         resultado = frame.ShowModal()

         lista = bancodedados.ListaVisualizacao()
         index = bancodedados.ler_quant_ensaios() - 1 - quant

         '''For apenas para definir os key's'''
         for key, row in lista:
             pass

         if valor_Logico == index:
             pass

         else:
             pos = self.list_ctrl.InsertStringItem(index, lista[index][1][0])
             self.list_ctrl.SetStringItem(index, 1, lista[index][1][1])
             self.list_ctrl.SetStringItem(index, 2, lista[index][1][2])
             self.list_ctrl.SetStringItem(index, 3, lista[index][1][3])
             buttonEDT = wx.Button(self.list_ctrl, id = key, label="")
             buttonGRF = wx.Button(self.list_ctrl, id = 4000+key, label="")
             buttonPDF = wx.Button(self.list_ctrl, id = 10000+key, label="")
             buttonCSV = wx.Button(self.list_ctrl, id = 15000+key, label="")
             buttonDEL = wx.Button(self.list_ctrl, id = 20000+key, label="")
             buttonEDT.SetBitmap(wx.Bitmap('icons\icons-editar-arquivo-24px.png'))
             buttonGRF.SetBitmap(wx.Bitmap('icons\icons-grafico-24px.png'))
             buttonPDF.SetBitmap(wx.Bitmap('icons\icons-exportar-pdf-24px.png'))
             buttonCSV.SetBitmap(wx.Bitmap('icons\icons-exportar-csv-24px.png'))
             buttonDEL.SetBitmap(wx.Bitmap('icons\icons-lixo-24px.png'))
             self.list_ctrl.SetItemWindow(pos, col=4, wnd=buttonEDT, expand=True)
             self.list_ctrl.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
             self.list_ctrl.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
             self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
             self.Bind(wx.EVT_BUTTON, self.exportCSV, buttonCSV)
             self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
             self.list_ctrl.SetItemData(index, key)
             self.list_ctrl.Update()
             valor_Logico = valor_Logico + 1

         lista = bancodedados.ListaVisualizacao()
         if len(lista) >=8:
            self.list_ctrl.SetColumnWidth(0, width=115)
            self.list_ctrl.SetColumnWidth(1, width=115)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=70)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)
         else:
            self.list_ctrl.SetColumnWidth(0, width=125)
            self.list_ctrl.SetColumnWidth(1, width=120)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=70)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def CapCadastradas(self, event):
         '''Abri tela com as Capsulas Cadastradas no bancodedados'''
         frame = Cap()
         resultado = frame.ShowModal()

    #--------------------------------------------------
     def ajudaGUI(self, event):
          '''Dialogo ajuda'''
          message1 = ('Software EAU - Ensaio de Adensamento Unidimensional\n\n')
          message2 = ('Esse software foi desenvolvido para facilitar o método de ensaio da antiga MB-3336, hoje conhecida pela NBR 12007 - SOLO - ENSAIO DE ADENSAMENTO UNIDIMENSIONAL pela ABNT - Associacão Brasileira de Normas Técnicas. Esta norma prescreve o método de determinação das propriedades de adensamento do solo, caracterizadas pela velocidade e magnitude das deformacões, quando o solo é lateralmente confinado e carregado de forma axial.')
          dlg = wx.MessageDialog(self, message1 + message2, 'EAU', wx.OK|wx.ICON_INFORMATION)
          aboutPanel = wx.TextCtrl(dlg, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
          dlg.ShowModal()
          dlg.Destroy()

    #--------------------------------------------------
     def ColumAdapter(self, event):
         lista = bancodedados.ListaVisualizacao()
         '''Ajusta os tamanhos das colunas ao arrastar'''
         if len(lista) >=8:
            self.list_ctrl.SetColumnWidth(0, width=115)
            self.list_ctrl.SetColumnWidth(1, width=115)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=70)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)
         else:
            self.list_ctrl.SetColumnWidth(0, width=125)
            self.list_ctrl.SetColumnWidth(1, width=120)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=70)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def ColumAdapter2(self, event):
         lista = bancodedados.ListaVisualizacao()
         '''Ajusta os tamanhos das colunas ao clicar com botão esquerdo sobre a coluna'''
         if len(lista) >=8:
            self.list_ctrl.SetColumnWidth(0, width=115)
            self.list_ctrl.SetColumnWidth(1, width=115)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=70)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)
         else:
            self.list_ctrl.SetColumnWidth(0, width=125)
            self.list_ctrl.SetColumnWidth(1, width=120)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=70)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def ColumAdapter3(self, event):
         lista = bancodedados.ListaVisualizacao()
         '''Ajusta os tamanhos das colunas ao clicar com o botão direito sobre a coluna'''
         if len(lista) >=8:
            self.list_ctrl.SetColumnWidth(0, width=115)
            self.list_ctrl.SetColumnWidth(1, width=115)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=70)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)
         else:
            self.list_ctrl.SetColumnWidth(0, width=125)
            self.list_ctrl.SetColumnWidth(1, width=120)
            self.list_ctrl.SetColumnWidth(2, width=135)
            self.list_ctrl.SetColumnWidth(3, width=70)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def onExit(self, event):
          '''Opcao Sair'''
          self.Close(True)
