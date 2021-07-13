# -*- coding: utf-8 -*-

import bancodedados

global X1
global X2
global X3
global X4

X1 = []
Y1 = []
X2 = []
Y2 = []
X3 = []
Y3 = []
X4 = []
Y4 = []

def save(x, y):
    global X1
    global X2
    global X3
    global X4
    a1 = False
    if len(X1) == 0 and a1 == False:
        X1 = x
        Y1 = y
        a1 = True

    if len(X1) > 0 and a1 == False:
        X2 = x
        Y2 = y
        a1 = True

    if len(X1) > 0 and len(X2) > 0 and a1 == False:
        X3 = x
        Y3 = y
        a1 = True

    if len(X1) > 0 and len(X2) > 0 and len(X3) > 0 and a1 == False:
        X4 = x
        Y4 = y
        a1 = True

    if len(X1) > 0 and len(X2) > 0 and len(X3) > 0 and len(X4) > 0:
        print 'ERRO_VETORES_TODOS_CHEIOS'

def salvamento(idt, pc, pg):
    global X1
    global X2
    global X3
    global X4
    
    while len(X1) > 0 or len(X2) > 0 or len(X3) > 0 or len(X4) > 0:
        if len(X1) > 0:
            bancodedados.save(idt, X1, Y1, pc, pg)
            X1 = []
            Y1 = []

        if len(X2) > 0:
            bancodedados.save(idt, X2, Y2, pc, pg)
            X2 = []
            Y2 = []

        if len(X3) > 0:
            bancodedados.save(idt, X3, Y3, pc, pg)
            X3 = []
            Y3 = []

        if len(X4) > 0:
            bancodedados.save(idt, X4, Y4, pc, pg)
            X4 = []
            Y4 = []
