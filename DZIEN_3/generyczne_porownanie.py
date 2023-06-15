def porownaj_imiona(obj,pImie):
    if obj.imie == pImie:
        return True
    else:
        return False
    
def porownaj_wiek(obj,pWiek):
    if obj.wiek == pWiek:
        return True
    else:
        return False
    
class Element: #pewien rekord danych
    def __init__(self,pImie,pWiek):
        self.pImie = pImie
        self.pWiek = pWiek
        
# if type(obj) != Element:
#     print("Nieprawidłowy obiekt...")
#     return False
        
def szukaj(tab,x,porownywarka):
    if len(tab)==0:
        return len()
    i=0
    while i<len(tab):
        if porownywarka(tab[i],x):
            break
        else:
            i=i+1
    return i

