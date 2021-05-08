import wx
from wx.lib.wordwrap import wordwrap

class gui(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self,None, id, title, style=wx.DEFAULT_FRAME_STYLE)
        panel1 = wx.Panel(self, -1)
        panel1.SetBackgroundColour('#fffaaa')
        menuBar = wx.MenuBar()
        file = wx.Menu()
        file.Append(101, '&About1', 'About1')
        file.Append(102, '&About2', 'About2')
        menuBar.Append(file, '&File')
        self.SetMenuBar(menuBar)
        wx.EVT_MENU(self, 101, self.onAbout)# Event for the About1 menu
        wx.EVT_MENU(self, 102, self.onAboutDlg)# Event for the About2 menu

    def onAbout(self, event):
        message = 'This fantastic app was developed using wxPython.\nwxPython is c00l :)'
        dlg = wx.MessageDialog(self, message, 'My APP', wx.OK|wx.ICON_INFORMATION)
        aboutPanel = wx.TextCtrl(dlg, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        aboutPanel.WriteText('Experimentation is the part of our life.\n')
        dlg.ShowModal()
        dlg.Destroy()

    def onAboutDlg(self, event):
        self.panel = wx.Panel(self, -1)
        info = wx.AboutDialogInfo()
        info.Name = "My About Box"
        info.Version = "0.1"
        info.Copyright = "(C) 2014 xxx"
        info.Description = wordwrap(
        "This is an example application that shows the problem "
        "that I am facing :)",
        350, wx.ClientDC(self.panel))
        info.WebSite = ("http://stackoverflow.com/users/2382792/pss", "My Home Page")
        info.Developers = ["PSS"]
        info.License = wordwrap("Driving license and a AK-47 too :P ", 500,wx.ClientDC(self.panel))
        #    Uncomment the following line to get the error!
        #aboutPanel = wx.TextCtrl(info, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        #aboutPanel.WriteText('Experimentation is the part of our life.\n')
        wx.AboutBox(info)


if __name__ == '__main__':
    app = wx.App()
    frame = gui(parent=None, id=-1, title="My-App")
    frame.Show()
    app.MainLoop()
