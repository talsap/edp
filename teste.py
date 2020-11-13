# -*- coding: utf-8 -*-
import wx

class SampleApp(wx.App):
    def OnInit(self):
        self.init_frame()
        return True

    def init_frame(self):
        self.frm_main = wx.Frame(None)
        self.sizer = wx.BoxSizer()
        self.frm_main.SetSizer(self.sizer)
        self.txt_title = wx.TextCtrl(self.frm_main)
        self.sizer.Add(self.txt_title, 1, wx.ALIGN_CENTER_VERTICAL)
        self.btn_submit = wx.Button(self.frm_main)
        self.btn_submit.SetLabel("Submit")
        self.sizer.Add(self.btn_submit, 0, wx.ALIGN_CENTER_VERTICAL)
        self.frm_main.SetTitle("sample_2_2")
        self.frm_main.SetSize((400, 200))
        self.frm_main.Show()

if __name__ == "__main__":
    app = SampleApp(False)
    app.MainLoop()
