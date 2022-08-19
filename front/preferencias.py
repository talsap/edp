# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import banco.bdPreferences as bdPreferences
import back.HexForRGB as HexRGB
global linesGraficc

linesGraficc = ['b', 'b-', 'b--','b-.','b:', 'b.', 'b,',
         'g', 'g-', 'g--','g-.','g:', 'g.', 'g,',
         'r', 'r-', 'r--','r-.','r:', 'r.', 'r,',
         'c', 'c-', 'c--','c-.','c:', 'c.', 'c,',
         'm', 'm-', 'm--','m-.','m:', 'm.', 'm,',
         'y', 'y-', 'y--','y-.','y:', 'y.', 'y,',
         'k', 'k-', 'k--','k-.','k:', 'k.', 'k,',
         'w', 'w-', 'w--','w-.','w:', 'w.', 'w,'
]

'''Tela Preferencias'''
class Pref(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
                wx.Dialog.__init__(self, None, -1, 'EDP - Preferências', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

                v_sizer = wx.BoxSizer(wx.VERTICAL)
                h_sizer = wx.BoxSizer(wx.HORIZONTAL)
                h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
                panel = wx.Panel(self)

                colors = bdPreferences.ListColors()
                colorBackground = colors[2]

                self.SetBackgroundColour(colorBackground)

                '''Iserção do IconeLogo'''
                try:
                    ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                    self.SetIcon(ico)
                except:
                    pass
                
                FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
                title0 = wx.StaticText(self, -1, "PREFERÊNCIAS", (20,20), (-1,-1), wx.ALIGN_CENTER)
                title0.SetFont(FontTitle)
                texto0 = wx.StaticText(self, -1, "COR BACKGROUND =", (20,65), (-1,-1), wx.ALIGN_RIGHT)
                self.background = wx.TextCtrl(self, -1, colors[2], (200,63), (120,-1), wx.TE_LEFT)
                self.background.Disable()
                texto1 = wx.StaticText(self, -1, "COR BACKGROUND TEXTCTRL =", (20,105), (-1,-1), wx.ALIGN_RIGHT)
                self.textCtrl = wx.TextCtrl(self, -1, colors[1], (200,103), (120,-1), wx.TE_LEFT)
                self.textCtrl .Disable()
                texto2 = wx.StaticText(self, -1, "COR BACKGROUND GRAFIC =", (20,145), (-1,-1), wx.ALIGN_RIGHT)
                self.backgroundG= wx.TextCtrl(self, -1, colors[4], (200,143), (120,-1), wx.TE_LEFT)
                self.backgroundG.Disable()
                texto3 = wx.StaticText(self, -1, "COR LINE GRAFIC =", (20,185), (-1,-1), wx.ALIGN_RIGHT)
                self.LineG= wx.TextCtrl(self, -1, colors[3], (200,183), (120,-1), wx.TE_LEFT)
                self.LineG.Disable()
                texto4 = wx.StaticText(self, -1, "COR DOS CARDS =", (20,225), (-1,-1), wx.ALIGN_RIGHT)
                self.cards= wx.TextCtrl(self, -1, colors[0], (200,223), (120,-1), wx.TE_LEFT)
                self.cards.Disable()

                self.editar1 = wx.Button(self, -1, 'Editar', (30,400), (-1,-1))
                self.Salvar1 = wx.Button(self, -1, 'Salvar', (230,400), (-1,-1))
                self.Bind(wx.EVT_BUTTON, self.Editar1, self.editar1)
                self.Bind(wx.EVT_BUTTON, self.Salva1, self.Salvar1)
                self.Bind(wx.EVT_CLOSE, self.onExit)
                self.Salvar1.Disable()

                '''Configurações do Size'''
                self.SetSize((360,520))

                panel.SetSizer(v_sizer)
                self.Centre()
                self.Show()

        #--------------------------------------------------
        def Editar1(self, event):
                '''Edita...'''
                self.editar1.Disable()
                self.Salvar1.Enable()
                self.background.Enable()
                self.textCtrl.Enable()
                self.backgroundG.Enable()
                self.LineG.Enable()
                self.cards.Enable()
                self.Update()
                self.Refresh()

        #--------------------------------------------------
        def Salva1(self, event):
                '''Diálogo se deseja alterar as cores'''
                dlg = wx.MessageDialog(None, 'Deseja mesmo alterar as cores?', 'EDP', wx.ICON_EXCLAMATION | wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
                result = dlg.ShowModal()

                if result == wx.ID_YES:
                    '''Salva...'''
                    color3 = self.background.GetValue()
                    color2 = self.textCtrl.GetValue()
                    color5 = self.backgroundG.GetValue()
                    color4 = self.LineG.GetValue()
                    color1 = self.cards.GetValue()

                    condicional = 0

                    try:
                        color1RGB = HexRGB.RGB(color1)
                        color2RGB = HexRGB.RGB(color2)
                        color3RGB = HexRGB.RGB(color3)
                        color5RGB = HexRGB.RGB(color5)
                        if color4 not in linesGraficc:
                            color4 = 'r-'
                            self.LineG.Clear()
                            self.LineG.AppendText(color4)
                        print color1RGB, color2RGB, color3RGB, color4, color5RGB
                        condicional = 1

                    except ValueError:
                        print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                        menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                        aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                        menssagError.ShowModal()
                        menssagError.Destroy()
                        condicional = -1

                    if color1 == '' or color2 == '' or color3 == '' or color4 == '' or color5 == '':
                        '''Diálogo para Forçar preenchimento dos valores'''
                        dlg = wx.MessageDialog(None, 'É necessário que alguns campos estejam preenchidos.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                        result = dlg.ShowModal()

                    else:
                        if(condicional>=1):
                            bdPreferences.colors_update(color1, color2, color3, color4, color5)
                            self.editar1.Enable()
                            self.Salvar1.Disable()
                            self.background.Disable()
                            self.textCtrl.Disable()
                            self.backgroundG.Disable()
                            self.LineG.Disable()
                            self.cards.Disable()
                            self.Update()
                            self.Refresh()
                else:
                    colors = bdPreferences.ListColors()
                    self.background.Clear()
                    self.textCtrl.Clear()
                    self.backgroundG.Clear()
                    self.LineG.Clear()
                    self.cards.Clear()
                    self.background.AppendText(colors[2])
                    self.textCtrl.AppendText(colors[1])
                    self.backgroundG.AppendText(colors[4])
                    self.LineG.AppendText(colors[3])
                    self.cards.AppendText(colors[0])
                    self.editar1.Enable()
                    self.Salvar1.Disable()
                    self.background.Disable()
                    self.textCtrl.Disable()
                    self.backgroundG.Disable()
                    self.LineG.Disable()
                    self.cards.Disable()
                    self.Update()
                    self.Refresh()

        #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()
