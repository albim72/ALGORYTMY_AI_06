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
        self.imie = pImie
        self.wiek = pWiek

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


tab = [Element("Jan",24),Element("Eliza",34),Element("Maria",40),Element("Tymek",60)]
print(f"Szukam imię=Maria: {szukaj(tab,'Maria',porownaj_imiona)!=len(tab)}")
print(f"Szukam imię=Dorota: {szukaj(tab,'Dorota',porownaj_imiona)!=len(tab)}")

print(f"Szukam wiek=102: {szukaj(tab,102,porownaj_wiek)!=len(tab)}")
print(f"Szukam wiek=34: {szukaj(tab,34,porownaj_wiek)!=len(tab)}")


