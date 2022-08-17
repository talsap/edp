#CONVERTE CORES

'''converte de rgb para hexadecimal'''
def Hex(R, G, B):
    return '#%02x%02x%02x' % (R, G, B)

'''converte de hexadecimal para rgb'''
def RGB(Hex):
    hex = Hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
