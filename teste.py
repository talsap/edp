# -*- coding: utf-8 -*-
#!/usr/bin/env python
import wx
import wx.lib.agw.hyperlink as hl

class Example(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        textS = wx.StaticText(panel, label='Plain')
        textS.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Arial'))
        lnk = hl.HyperLinkCtrl(panel, -1, "wxPython Main Page",
                                  URL="http://www.wxpython.org/")
        textE = wx.StaticText(panel, label='Text')
        textE.SetFont(wx.Font(12, wx.SWISS, wx.ITALIC, wx.NORMAL, False, 'Courier'))
        self.SetSize((500, 150))
        sizer.Add(textS, 0, wx.ALL, 5 )
        sizer.Add(lnk, 0, wx.ALL, 5 )
        sizer.Add(textE, 0, wx.ALL, 5 )
        lnk.EnableRollover(True)
        lnk.SetToolTip(wx.ToolTip("Hello World!"))
        lnk.UpdateLink()
        self.SetSizer(sizer)
        self.Centre()
        self.Show(True)

if __name__ == '__main__':
    ex = wx.App()
    Example(None, 'A Hyperlink')
    ex.MainLoop()
