def szukaj(tab,x): #szukanie wartości x w tablicy tab
    if len(tab) == 0:
        return len()
    i = 0
    while i<len(tab):
        if tab[i]==x:
            break
        else:
            i=i+1
    return i


tab1 = [1,2,"Henio",3,-6,44,'C',1,0,-3]
print(f'tabela 1: {tab1}, rozmiar: {len(tab1)}')
print(f'szukam 3: {szukaj(tab1,3) != len(tab1)}')
print(f'szukam 99: {szukaj(tab1,99) != len(tab1)}')

tab2 = ['A','L','A','M','A','K','O','T','A']

print(f'tabela 2: {tab2}, rozmiar: {len(tab1)}')
print(f'szukam 3: {szukaj(tab2,3) != len(tab2)}')
print(f'szukam 99: {szukaj(tab2,99) != len(tab2)}')
print(f'szukam A: {szukaj(tab2,"A") != len(tab2)}')
