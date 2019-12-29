import random

bludiste = []

def template(): #0 = zed, 1 = zaklad, 2 = volno
    bludiste.append([0 for _ in range(21)])
    bludiste.append([0]+[2 for _ in range(19)]+[0])
    for _ in range(9):
        bludiste.append([0,2]+[ x for _ in range(9) for x in (1,2)]+[0])
        bludiste.append([0]+[2 for _ in range(19)]+[0])
    bludiste.append([0 for _ in range(21)])

def tisk_bludiste():
    for radek in bludiste:
        for prvek in radek:
            if prvek == 0: print('X', end="")
            else: print('.', end="")
        print()
        
def tisk_seznam():
    for sez in bludiste:
        print(sez)

def uloz_bludiste(num):
    f = open(f"levels/level{num}.txt","wt")
    for radek in bludiste:
        for prvek in radek:    
            f.write(f"{prvek}")
        f.write("\n")
    f.close()
     
def kolik_zakladu():
    pocet_zakladu = 0
    for radek in bludiste:
        for prvek in radek:
            if prvek == 1:
                pocet_zakladu +=1
            else: pass
    return pocet_zakladu

def vyber_nahodne_zaklad():
    poc_zakladu = 0
    poc_radku = 0
    index = random.randint(1,kolik_zakladu())
    #print(index)
    for radek in bludiste:
        poc_prvku = 0
        while poc_prvku !=21:
            if radek[poc_prvku] == 1:
                poc_zakladu += 1
                if poc_zakladu == index:
                    return (poc_radku, poc_prvku)
            poc_prvku += 1
        poc_radku += 1
        
def postav_zed():
    souradnice = vyber_nahodne_zaklad()
    y, x = souradnice[0], souradnice[1]
    volba = random.randint(1,4) #1 = nahoru, 2 = dolu, 3 = vlevo, 4 = vpravo
    if volba == 1: #nahoru
        while bludiste[y][x] != 0:
            bludiste[y][x] = 0
            y -= 1
    elif volba == 2: #dolu
        while bludiste[y][x] != 0:
            bludiste[y][x] = 0
            y += 1
    elif volba == 3: #vlevo
        while bludiste[y][x] != 0:
            bludiste[y][x] = 0
            x -= 1
    else:            #vpravo
        while bludiste[y][x] != 0:
            bludiste[y][x] = 0
            x += 1

def postav_bludiste():
    template()
    while kolik_zakladu() != 0:
        postav_zed()
            
postav_bludiste()
cislo_levelu = input("Cislo levelu ktery se pregeneruje (1-5):")
uloz_bludiste(cislo_levelu)
