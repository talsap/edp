#!/usr/bin/env python
import wx

class Mywin(wx.Frame):

    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(500, 300))
        self.tips = ["","Rectangle 1","Rectangle 2"]
        self.rect = []
        self.InitUI()

    def InitUI(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour('RED'))
        self.Centre()
        self.Show(True)

        menuBar = wx.MenuBar()
        RectangleButton = wx.Menu()
        self.status = self.CreateStatusBar()
        self.status.SetFieldsCount(number=2)
        Item1 = RectangleButton.Append(wx.ID_ANY, 'Rectangle 1')
        Item2 = RectangleButton.Append(wx.ID_ANY, 'Rectangle 2')

        menuBar.Append(RectangleButton, 'Rectangles')

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.DrawRect1, Item1)
        self.Bind(wx.EVT_MENU, self.DrawRect2, Item2)
        self.panel.Bind(wx.EVT_MOTION, self.MouseMovement)


    def DrawRect1(self, e):
        self.panel.SetBackgroundColour(wx.Colour('BLUE'))
        self.Update()
        self.dc = wx.ClientDC(self.panel)
        self.dc.SetBrush(wx.Brush(wx.Colour('white')))
        self.dc.DrawRectangle(10, 20, 100, 200)
        #Note the position of the DC
        self.rect = [x for x in self.dc.BoundingBox]
        #Append the id
        self.rect.append(1)

    def DrawRect2(self, e):
        self.panel.SetBackgroundColour(wx.Colour('GREEN'))
        self.Update()
        self.dc = wx.ClientDC(self.panel)
        self.dc.SetBrush(wx.Brush(wx.Colour('white')))
        self.dc.DrawRectangle(20, 20, 50, 50)
        self.rect = [x for x in self.dc.BoundingBox]
        self.rect.append(2)

    def MouseMovement(self, event):
        x,y = event.GetPosition()
        self.panel.SetToolTip('')
        self.status.SetStatusText('', 1)
        if self.rect:
            if x >= self.rect[0] and x <= self.rect[2] and y >= self.rect[1] and y <= self.rect[3]:
                self.panel.SetToolTip(self.tips[self.rect[4]])
                self.status.SetStatusText("Hovering over "+self.tips[self.rect[4]], 1)
                win = Popup(self,self.rect[4],self.tips[self.rect[4]])
                pos = self.GetScreenPosition()
                win.Position(pos,(-1,-1))
                win.Popup()

class Popup(wx.PopupTransientWindow):

    def __init__(self, parent, id, id_text):
        wx.PopupTransientWindow.__init__(self, parent)
        panel = wx.Panel(self)
        panel.SetBackgroundColour("gold")

        text = wx.StaticText(panel, -1,
                          "This is a wx.PopupTransientWindow\n"
                          "Click mouse outside of it\n\n"
                          "Id of widget is "+str(id)+"\n"
                          "You are hovering over "+id_text)
        # add other widgets here if required
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALL, 5)
        panel.SetSizer(sizer)
        sizer.Fit(panel)
        sizer.Fit(self)
        self.Layout()



myApp = wx.App()
Mywin(None,'Drawing demo')
myApp.MainLoop()
