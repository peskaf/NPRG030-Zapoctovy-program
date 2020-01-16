'''
Generování a procházení bludiště
Filip Peška, I. ročník
zimní semestr 2019/20
Programování 1 [NPRG030]
'''

import pygame, os
from pygame.locals import *
import utils #soubor vlastnich funkci ve stejnem adresari
pygame.init()

#Generovani bludiste_________________________________________________________________________________________________________________________Generovani bludiste_begin
def gen_maze(): #funkce generovani bludiste
    global finished
    bludiste = []
    utils.postav_bludiste(bludiste)
    utils.uloz_bludiste_random(bludiste)
    finished = False #nastavi, ze nahodne vygenerovane bludiste (jedine pro to se tato fce pouziva) nebylo jeste dokonceno
            
#Generovani bludiste_________________________________________________________________________________________________________________________Generovani bludiste_end

#Game________________________________________________________________________________________________________________________________________Game_begin
    
strana = 25 #strana jednoho ctverecku
kde_y = 30 #slozka souradnice prvniho ctverecku
kde_x = 40 #slozka souradnice prvniho ctverecku
vel = 5 #rychlost (zmena), (delitelne 5)
clock = pygame.time.Clock()
win=pygame.display.set_mode((800, 600))
pygame.display.set_caption("MazeGame")
level = 0 #cislo levelu ktery hrac vybral

class player():
    global strana, kde_x, kde_y
    def __init__(this): #hrac se objevi v levem hornim rohu bludiste
        this.px = strana+kde_x
        this.py = strana+kde_y
        pygame.draw.rect(win, (78, 255, 0), (this.px,this.py,strana,strana))
        pygame.display.update()
    def move(this,zmenax,zmenay): #kontroluje validitu tahu (zda neni na dalsi pozici zakazana/vitezna barva)
        if win.get_at((this.px+zmenax, this.py+zmenay)) == (212,123,21) or win.get_at((this.px+zmenax+strana-1, this.py+zmenay)) == (212,123,21) or win.get_at((this.px+zmenax+strana-1, this.py+zmenay+strana-1)) == (212,123,21) or win.get_at((this.px+zmenax, this.py+zmenay+strana-1)) == (212,123,21):    #hranice
            pass
        elif win.get_at((this.px+zmenax, this.py+zmenay)) == (255,0,0) or win.get_at((this.px+zmenax+strana-1, this.py+zmenay)) == (255,0,0) or win.get_at((this.px+zmenax+strana-1, this.py+zmenay+strana-1)) == (255,0,0) or win.get_at((this.px+zmenax, this.py+zmenay+strana-1)) == (255,0,0):  #cil
            global finished
            finished = True
        else:               #pokud je tah validni, prekresli hrace na dane souradnice
            pygame.draw.rect(win, (0, 0, 0), (this.px,this.py,strana,strana))
            this.px += zmenax
            this.py += zmenay
            pygame.draw.rect(win, (78, 255, 0), (this.px,this.py,strana,strana))
            pygame.display.update()
               
def build(co): #vykresli bludiste vybraneho levelu ze souboru (build("level1.txt") postavi level 1,...)
    f = open(co, 'rt')
    kde_y = 30
    win.fill((0,0,0))
    for radek in f:
        kde_x = 40
        for znak in radek:
            if znak == "0":
                pygame.draw.rect(win,(212,123,21),(kde_x,kde_y,strana,strana))
            else: pass
            kde_x += strana
        kde_y += strana
    pygame.draw.rect(win, (255, 0, 0), (515,530,strana,strana)) #cil (cerveny ctverec)
    font_timer = pygame.font.Font("font/built_titling_bd.otf", 35) #timer napis
    text_timer_label = font_timer.render('Time elapsed:',True,(255,255,255)) #timer napis
    win.blit(text_timer_label, (575,25)) #timer napis
    pygame.display.update()
    f.close()

def scores(): #vykresli personal bests z jednotlivych levelu (ty jsou ulozeny v souborech)
    
    def reset(): #resetuje PBs
        for j in [1,2,3,4,5]:
            sc = open(f"scores/level{j}_sc.txt", "wt") #otevreni souboru
            sc.write("90.00")
            sc.close()
        pygame.display.update()

    def write_it(): #napise na obrazovku nejlepsi casy
        
        font_guide = pygame.font.Font("font/built_titling_bd.otf", 25) #font instrukce k navratu do menu
        font_sco = pygame.font.Font("font/built_titling_bd.otf", 50)  #font jednotlivych skore
        shift = -150 #odsazeni jednotlivych napisu od sebe
        win.fill((0,0,0))
        for i in [1,2,3,4,5]:
            sc = open(f"scores/level{i}_sc.txt", "rt") #otevreni souboru
            print_time = float(sc.readline()) #skore je jen na prvnim radku -> precte prvni radek a udela z nej float
            sc.close() #zavreni souboru
            text_sco = font_sco.render(f'Level {i}: {print_time}',True,(255,255,255)) #text, ktery se bude vypisovat, zaobleni hran (True), jakou barvou (bila)
            textRect_sco = text_sco.get_rect()
            textRect_sco.center = (800 // 2, 600 // 2 + shift) #vycentruje text na strance a umisti ho v zavislosti na posunuti
            win.blit(text_sco, textRect_sco) #vypise text na pygame obrazovku
            shift += 60
        text_guide = font_guide.render('Press R to reset PBs or space to continue...',True,(255,255,255))
        textRect_gui = text_guide.get_rect()
        textRect_gui.center = (800 // 2, 600 // 2 + 230)
        win.blit(text_guide, textRect_gui)
        pygame.display.update()
    write_it()
    while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    os._exit(1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #stisknuti mezerniku = odchod do menu
                        menu(1)
                    if event.key == pygame.K_r:
                        reset()
                        write_it()
    

  
def timer(): #casovac od prvniho tahu hrace
    global start_ticks, finished, level, time
    def napis(PB): #napis, ktery se objevy po dokonceni hry; True = vytvoren novy PB, False = nevytvoren PB
        win.fill((0,0,0))
        font_napis = pygame.font.Font("font/built_titling_bd.otf", 50)
        font_guide = pygame.font.Font("font/built_titling_bd.otf", 25)
        if PB == True: #new PB
            sc = open(f"scores/level{level}_sc.txt", "rt")
            new_time = float(sc.readline()) #ulozi novy nejlepsi cas do souboru skore z daneho levelu
            sc.close()
            text_napis = font_napis.render(f'New PB! Time: {new_time}',True,(255,255,255)) #vytvoren novy PB + jaky
            textRect_nap = text_napis.get_rect()
            textRect_nap.center = (800 // 2, 600 // 2 - 20)
            text_guide = font_guide.render('Press space to continue...',True,(255,255,255)) #instrukce odchodu do menu
            textRect_gui = text_guide.get_rect()
            textRect_gui.center = (800 // 2, 600 // 2 + 60)
        else:
            text_napis = font_napis.render('Too slow. You can do better!',True,(255,255,255)) #uplynul minimalni cas pro dokonceni nebo byl dosazen horsi
            textRect_nap = text_napis.get_rect()
            textRect_nap.center = (800 // 2, 600 // 2 - 20)
            text_guide = font_guide.render('Press space to continue...',True,(255,255,255))
            textRect_gui = text_guide.get_rect()
            textRect_gui.center = (800 // 2, 600 // 2 + 60)
        win.blit(text_napis, textRect_nap)
        win.blit(text_guide, textRect_gui)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    os._exit(1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: #mezernik = odchod do menu
                        menu(1)

    if finished == False: #pokud hra jeste neni dokoncena
        time = (pygame.time.get_ticks()-start_ticks)/1000 #spocitej, kolik casu uplynulo od prvniho tahu
        font_timer = pygame.font.Font("font/built_titling_bd.otf", 35)
        text_timer = font_timer.render(f"{time}",True,(255,255,255)) #jaky je aktualni cas
        if time>90: #pokud hrac hru nestihl dohrat za 90 sekund
            napis(False)  #vypise napis o nesplneni ukolu
        else:
            win.fill((0,0,0),(575,70,90,40)) #smaze predchozi cas, ktery byl vypsan
            win.blit(text_timer, (575,70)) #vypise novy cas
        pygame.display.update()
    else: #hra je dokoncena
        sc = open(f"scores/level{level}_sc.txt", "rt")
        prev_time = float(sc.readline()) #nacti predchozi nejlepsi cas ze souboru
        sc.close()
        if time<prev_time: #pokud je novy cas lepsi
            sc = open(f"scores/level{level}_sc.txt", "wt")
            sc.write(f"{time}") #uloz ten
            sc.close()
            napis(True) #vypis, ze hrac ma novy PB a jaky
        else:
            napis(False) #pokud je novy cas horsi, vypis, ze neni novy PB

def game_loop(): #cyklus tahů
    global hrac, start_ticks
    start = False #kontroluje, jestli hrac provedl prvni tah
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                os._exit(1)
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: #vlevo
            if start == False: #pokud se jedna o prvni tah, spust hodiny
                start_ticks = pygame.time.get_ticks()
                start = True
            hrac.move(-vel,0) #pohyb hrace po souradnicich
        if keys[pygame.K_RIGHT]: #vpravo
            if start == False:
                start_ticks = pygame.time.get_ticks()
                start = True
            hrac.move(vel,0)
        if keys[pygame.K_UP]: #nahoru
            if start == False:
                start_ticks = pygame.time.get_ticks()
                start = True
            hrac.move(0,-vel)
        if keys[pygame.K_DOWN]: #dolu
            if start == False:
                start_ticks = pygame.time.get_ticks()
                start = True
            hrac.move(0,vel)
        if start == True:
            timer() #pokud uz se zaclo, vypisuj cas
        if finished == True:
            break #pokud je hra dohrana, vyskoc z cyklu kontroly tahu
        clock.tick(19)  #FPS

def submenu(choice): #choice = ktera polozka menu bude vybrana (zabarvena jinak)
    global hrac, level, finished
    finished = False #pokud jsi v podmenu, nastav, ze hra, kterou jako dalsi spustime, je jeste nedohrana
    vybrana_barva = (255,0,0) #barva toho, co se spusti pri stisknuti enteru
    normalni_barva = (212,123,21) #barva ostatniho
    if choice == 1:
        barva_v1 = vybrana_barva
        barva_v2 = barva_v3 = barva_v4 = barva_v5 = barva_v6 = normalni_barva
    elif choice == 2:
        barva_v2 = vybrana_barva
        barva_v1 = barva_v3 = barva_v4 = barva_v5 = barva_v6 = normalni_barva
    elif choice == 3:
        barva_v3 = vybrana_barva
        barva_v1 = barva_v2 = barva_v4 = barva_v5 = barva_v6 = normalni_barva
    elif choice == 4:
        barva_v4 = vybrana_barva
        barva_v1 = barva_v2 = barva_v3 = barva_v5 = barva_v6 = normalni_barva
    elif choice == 5:
        barva_v5 = vybrana_barva
        barva_v1 = barva_v2 = barva_v4 = barva_v3 = barva_v6 = normalni_barva
    else:
        barva_v6 = vybrana_barva
        barva_v2 = barva_v3 = barva_v1 = barva_v5 = barva_v4 = normalni_barva
        
    font_nadpis = pygame.font.Font("font/built_titling_bd.otf", 120)
    text_nadpis = font_nadpis.render('MazeGame',True,(212,123,21))
    font_volba = pygame.font.Font("font/built_titling_bd.otf", 50)
    text_volba1 = font_volba.render('level 1',True,barva_v1)
    text_volba2 = font_volba.render('level 2',True,barva_v2)
    text_volba3 = font_volba.render('level 3',True,barva_v3)
    text_volba4 = font_volba.render('level 4',True,barva_v4)
    text_volba5 = font_volba.render('level 5',True,barva_v5)
    text_volba6 = font_volba.render('back',True,barva_v6)

    textRect_n = text_nadpis.get_rect()
    textRect_n.center = (800 // 2, 600 // 2 - 155)
    textRect_v1 = text_volba1.get_rect()
    textRect_v1.center = (800 // 2, 600 // 2 - 60)
    textRect_v2 = text_volba2.get_rect()
    textRect_v2.center = (800 // 2, 600 // 2 - 10)
    textRect_v3 = text_volba3.get_rect()
    textRect_v3.center = (800 // 2, 600 // 2 + 40)
    textRect_v4 = text_volba4.get_rect()
    textRect_v4.center = (800 // 2, 600 // 2 + 90)
    textRect_v5 = text_volba5.get_rect()
    textRect_v5.center = (800 // 2, 600 // 2 + 140)
    textRect_v6 = text_volba6.get_rect()
    textRect_v6.center = (800 // 2, 600 // 2 + 210)
    
    while True:
        win.fill((0,0,0))
        win.blit(text_nadpis, textRect_n)
        win.blit(text_volba1, textRect_v1)
        win.blit(text_volba2, textRect_v2)
        win.blit(text_volba3, textRect_v3)
        win.blit(text_volba4, textRect_v4)
        win.blit(text_volba5, textRect_v5)
        win.blit(text_volba6, textRect_v6)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                os._exit(1)
            if event.type == pygame.KEYDOWN: #je nutne klavesu opakovane mackat, drzeni klavesy menu neposouva dal
                if event.key == pygame.K_DOWN:
                    if choice == 6: #pokud je vybrana posledni polozka a chci opet dolu, jdi na prvni volbu
                        choice = 1
                        submenu(choice)
                    else:
                        choice += 1
                        submenu(choice)
                if event.key == pygame.K_UP:
                    if choice == 1:
                        choice = 6
                        submenu(choice)
                    else:
                        choice -= 1
                        submenu(choice)
                if event.key == pygame.K_RETURN: #K_RETURN = enter
                    if choice == 1:     #spust level 1
                        level = 1
                        build(f"levels/level{level}.txt")
                        hrac = player()
                        game_loop()
                    elif choice == 2:   #level 2
                        level = 2
                        build(f"levels/level{level}.txt")
                        hrac = player()
                        game_loop()

                    elif choice == 3:   #level 3
                        level = 3
                        build(f"levels/level{level}.txt")
                        hrac = player()
                        game_loop()
                    elif choice == 4:   #level 4
                        level = 4
                        build(f"levels/level{level}.txt")
                        hrac = player()
                        game_loop()
                    elif choice == 5:   #level 5
                        level = 5
                        build(f"levels/level{level}.txt")
                        hrac = player()
                        game_loop()
                    else:               #back = zpet do menu
                        menu(1)
           
def menu(choice): #menu hry, choice = cislo vyberu z menu
    global hrac, level
    vybrana_barva = (255,0,0)
    normalni_barva = (212,123,21)
    if choice == 1:
        barva_v1 = vybrana_barva
        barva_v2 = barva_v3 = barva_v4 = normalni_barva
    elif choice == 2:
        barva_v2 = vybrana_barva
        barva_v1 = barva_v3 = barva_v4 = normalni_barva
    elif choice == 3:
        barva_v3 = vybrana_barva
        barva_v1 = barva_v2 = barva_v4 = normalni_barva
    else:
        barva_v4 = vybrana_barva
        barva_v2 = barva_v3 = barva_v1 = normalni_barva
        
    font_nadpis = pygame.font.Font("font/built_titling_bd.otf", 120)
    text_nadpis = font_nadpis.render('MazeGame',True,(212,123,21))
    font_volba = pygame.font.Font("font/built_titling_bd.otf", 70)
    text_volba1 = font_volba.render('normal game',True,barva_v1)
    text_volba2 = font_volba.render('random game',True,barva_v2)
    text_volba3 = font_volba.render('personal bests',True,barva_v3)
    text_volba4 = font_volba.render('exit',True,barva_v4)
    textRect_n = text_nadpis.get_rect()
    textRect_n.center = (800 // 2, 600 // 2 - 155)
    textRect_v1 = text_volba1.get_rect()
    textRect_v1.center = (800 // 2, 600 // 2 - 40)
    textRect_v2 = text_volba2.get_rect()
    textRect_v2.center = (800 // 2, 600 // 2 + 30)
    textRect_v3 = text_volba3.get_rect()
    textRect_v3.center = (800 // 2, 600 // 2 + 100)
    textRect_v4 = text_volba4.get_rect()
    textRect_v4.center = (800 // 2, 600 // 2 + 170)
    
    while True:
        win.fill((0,0,0))
        win.blit(text_nadpis, textRect_n)
        win.blit(text_volba1, textRect_v1)
        win.blit(text_volba2, textRect_v2)
        win.blit(text_volba3, textRect_v3)
        win.blit(text_volba4, textRect_v4)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                os._exit(1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if choice == 4:
                        choice = 1
                        menu(choice)
                    else:
                        choice += 1
                        menu(choice)
                if event.key == pygame.K_UP:
                    if choice == 1:
                        choice = 4
                        menu(choice)
                    else:
                        choice -= 1
                        menu(choice)
                if event.key == pygame.K_RETURN:
                    if choice == 1:     #play normal
                        submenu(1)
                    elif choice == 2:   #gen+play random
                        gen_maze()
                        level = 6
                        sc = open(f"scores/level{level}_sc.txt", "wt")
                        sc.write(f"90.00") #nastavi cas tak, aby byl kazdy dohrany lepsi (bludiste jsou jedinecna, nemaji PB)
                        sc.close()
                        build("levels/random_level.txt") #postavi nahodne vygenerovane a ulozene bludiste
                        hrac = player()
                        game_loop()
                    elif choice == 3:   #scores
                        scores() #zobrazi jednotliva PBs
                    else:               #exit
                        pygame.quit()
                        os._exit(1) #opusti aplikaci
                    
#Game________________________________________________________________________________________________________________________________________Game_end
                        
#main______main_begin

menu(1) #zacni program tim, ze ukazes menu (dale je vse ve funkcich, odejde se z nich pouze primo rovnou z programu)

#main______main_end
