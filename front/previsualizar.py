# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import wx.lib.sized_controls as sc
from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel

'''Tela de Preview do Cabeçalho do PDF'''
class PDFViewer(sc.SizedFrame):
    def __init__(self, parent, **kwds):
        super(PDFViewer, self).__init__(parent, **kwds)
        '''Iserção do IconeLogo'''
        try:
            ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)
        except:
            pass

        paneCont = self.GetContentsPane()
        self.viewer = pdfViewer(paneCont, wx.NewId(), wx.DefaultPosition, wx.DefaultSize, wx.CLOSE_BOX | wx.VSCROLL)
        self.viewer.UsePrintDirect = ``False``
        self.viewer.SetSizerProps(expand=True, proportion=-1)
