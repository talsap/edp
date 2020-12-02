# -*- coding: utf-8 -*-
#!/usr/bin/env python
import wx
class Mywin(wx.Frame):
   def __init__(self, parent, title):
      super(Mywin, self).__init__(parent, title = title,size = (300,200))

      panel = wx.Panel(self)
      v_sizer = wx.BoxSizer(wx.VERTICAL)
      h_sizer = wx.BoxSizer(wx.HORIZONTAL)
      self.label = wx.StaticText(panel,label = "Your choice:" ,style = wx.ALIGN_CENTRE)
      v_sizer.Add(self.label, 0 ,wx.ALIGN_CENTER_HORIZONTAL |wx.ALL, 20)
      texto1 = wx.StaticText(panel,label = "NORMAS",style = wx.ALIGN_CENTRE)

      h_sizer.Add(texto1,0,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
      languages = ['C', 'C++', 'Python', 'Java', 'Perl']
      self.combo = wx.ComboBox(panel, choices = languages, style = wx.EXPAND)

      h_sizer.Add(self.combo,1,wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
      v_sizer.Add(h_sizer,1,wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)

      v_sizer.AddStretchSpacer()
      self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo)

      panel.SetSizer(v_sizer)
      self.Centre()
      self.Show()

   def OnCombo(self, event):
      self.label.SetLabel("You selected"+self.combo.GetValue()+" from Combobox")

app = wx.App()
Mywin(None,  'ComboBox and Choice demo')
app.MainLoop()
