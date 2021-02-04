# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import bancodedadosCAB
import wx.lib.sized_controls as sc
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from wx.lib.pdfviewer import pdfViewer

'''Tela de Preview do Cabeçalho do PDF'''
class Preview(sc.SizedFrame):
    #--------------------------------------------------
        def __init__(self, parent, id, *args, **kwargs):
            super(Preview, self).__init__(parent, id, 'Pré-Visualização', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION, **kwargs)

            self.id = id

            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

            '''Configurações do Size'''
            self.SetSize((650,400))

            paneCont = self.GetContentsPane()

            try:
                self.viewer = pdfViewer(paneCont, wx.NewId(), (10,10), (600,400), wx.HSCROLL | wx.VSCROLL | wx.SUNKEN_BORDER)
                self.viewer.UsePrintDirect = ``False``
                self.viewer.SetSizerProps(expand=True, proportion=1)
                self.viewer.LoadFile(r'logo\\CAB.pdf')

                '''Inicialize o panel'''
                self.Centre()
                self.Show()
            except:
                '''Dialogo para informar que algum problema fez com que nao seja possivel previzualizae'''
                dlg = wx.MessageDialog(None, 'Algum problema fez com que o Preview não seja mostrado.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
