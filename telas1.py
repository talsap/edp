import wx
import wx.lib.sized_controls as sc

from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel

class PDFViewer(sc.SizedFrame):
    def __init__(self, parent, **kwds):
        super(PDFViewer, self).__init__(parent, **kwds)

        paneCont = self.GetContentsPane()
        self.buttonpanel = pdfButtonPanel(paneCont, wx.NewId(),
                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.buttonpanel.SetSizerProps(expand=True)
        self.viewer = pdfViewer(paneCont, wx.NewId(), wx.DefaultPosition,
                                wx.DefaultSize,
                                wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
        self.viewer.UsePrintDirect = ``False``
        self.viewer.SetSizerProps(expand=True, proportion=1)

        # introduce buttonpanel and viewer to each other
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel


if __name__ == '__main__':
    import wx.lib.mixins.inspection as WIT
    app = WIT.InspectableApp(redirect=False)


    pdfV = PDFViewer(None, size=(800, 600))
    pdfV.viewer.UsePrintDirect = ``False``
    pdfV.viewer.LoadFile(r'a path to a .pdf file')
    pdfV.Show()

    app.MainLoop()
