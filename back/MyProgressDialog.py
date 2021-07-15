# -*- coding: utf-8 -*-
import wx
from pubsub import pub

########################################################################
'''MyProgressDialog'''
class MyProgressDialog(wx.Dialog):
    #-------------------------------------------------------------------
    def __init__(self, k):
        """Construtor"""
        wx.Dialog.__init__(self, None, -1, size=(600,15), style=0)
        self.Centre()
        self.k = k
        self.count = 0
        self.progress = wx.Gauge(self, range = self.k)
        self.texto = wx.StaticText(self, label = wx.EmptyString, style = wx.ALIGN_CENTRE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.progress, 0, wx.EXPAND)
        sizer1.AddStretchSpacer(1)
        sizer1.Add(self.texto, 2, wx.ALIGN_CENTER)
        sizer1.AddStretchSpacer(1)
        sizer1.Add(sizer, 8, wx.ALIGN_CENTER)
        self.SetSizer(sizer1)
        # create a pubsub receiver
        pub.subscribe(self.updateProgress, "update")

    #-------------------------------------------------------------------
    def updateProgress(self, msg):
        self.count += 1
        if self.count < self.k:
            self.texto.SetLabel(msg)
        if self.count >= self.k:
            self.Destroy()
        self.progress.SetValue(self.count)
