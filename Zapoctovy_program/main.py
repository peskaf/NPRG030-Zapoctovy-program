import pygame, sys, time, os, random
from pygame.locals import *
pygame.init()
#Generovani bludiste_________________________________________________________________________________________________________________________Generovani bludiste_begin
def gen_maze():
    global finished
    bludiste = []

    def template(): #0 = zed, 1 = zaklad, 2 = volno
        bludiste.append([0 for _ in range(21)])
        bludiste.append([0]+[2 for _ in range(19)]+[0])
        for _ in range(9):
            bludiste.append([0,2]+[ x for _ in range(9) for x in (1,2)]+[0])
            bludiste.append([0]+[2 for _ in range(19)]+[0])
        bludiste.append([0 for _ in range(21)])

    def uloz_bludiste():
        f = open("levels/random_level.txt","wt")
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
    uloz_bludiste()
    finished = False
            
#Generovani bludiste_________________________________________________________________________________________________________________________Generovani bludiste_end

#Game________________________________________________________________________________________________________________________________________Game_begin
    
strana = 25 #strana jednoho ctverecku
kde_y = 30
kde_x = 40
vel = 5 #rychlost (zmena), delitelne 5!
clock = pygame.time.Clock()
win=pygame.display.set_mode((800, 600))
pygame.display.set_caption("MazeGame")
level = 0 #number of level that is being played

class player():
    global strana, kde_x, kde_y
    def __init__(this):
        this.px = strana+kde_x
        this.py = strana+kde_y
        pygame.draw.rect(win, (78, 255, 0), (this.px,this.py,strana,strana))
        pygame.display.update()
    def move(this,zmenax,zmenay):
        if win.get_at((this.px+zmenax, this.py+zmenay)) == (212,123,21) or win.get_at((this.px+zmenax+strana-1, this.py+zmenay)) == (212,123,21) or win.get_at((this.px+zmenax+strana-1, this.py+zmenay+strana-1)) == (212,123,21) or win.get_at((this.px+zmenax, this.py+zmenay+strana-1)) == (212,123,21):    #hranice
            pass
        elif win.get_at((this.px+zmenax, this.py+zmenay)) == (255,0,0) or win.get_at((this.px+zmenax+strana-1, this.py+zmenay)) == (255,0,0) or win.get_at((this.px+zmenax+strana-1, this.py+zmenay+strana-1)) == (255,0,0) or win.get_at((this.px+zmenax, this.py+zmenay+strana-1)) == (255,0,0):  #cil
            global finished
            finished = True
        else:
            pygame.draw.rect(win, (0, 0, 0), (this.px,this.py,strana,strana))
            this.px += zmenax
            this.py += zmenay
            pygame.draw.rect(win, (78, 255, 0), (this.px,this.py,strana,strana))
            pygame.display.update()
               
def build(co):
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
    pygame.draw.rect(win, (255, 0, 0), (515,530,strana,strana)) #cil
    font_timer = pygame.font.Font("font/built_titling_bd.otf", 35) #timer
    text_timer_label = font_timer.render('Time elapsed:',True,(255,255,255)) #timer
    win.blit(text_timer_label, (575,25)) #timer
    pygame.display.update()
    f.close()

def scores():
    font_guide = pygame.font.Font("font/built_titling_bd.otf", 25)
    font_sco = pygame.font.Font("font/built_titling_bd.otf", 50)
    shift = -150
    win.fill((0,0,0))
    for i in [1,2,3,4,5]:
        sc = open(f"scores/level{i}_sc.txt", "rt")
        print_time = float(sc.readline()) 
        sc.close()
        text_sco = font_sco.render(f'Level {i}: {print_time}',True,(255,255,255))
        textRect_sco = text_sco.get_rect()
        textRect_sco.center = (800 // 2, 600 // 2 + shift)
        win.blit(text_sco, textRect_sco)
        shift += 60
    text_guide = font_guide.render('Press space to continue...',True,(255,255,255))
    textRect_gui = text_guide.get_rect()
    textRect_gui.center = (800 // 2, 600 // 2 + 230)
    win.blit(text_guide, textRect_gui)
    pygame.display.update()
    while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    os._exit(1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        menu(1)
    

  
def timer():
    global start_ticks, finished, level, time
    def napis(PB):
        win.fill((0,0,0))
        font_napis = pygame.font.Font("font/built_titling_bd.otf", 50)
        font_guide = pygame.font.Font("font/built_titling_bd.otf", 25)
        if PB == True: #new PB
            sc = open(f"scores/level{level}_sc.txt", "rt")
            new_time = float(sc.readline()) 
            sc.close()
            text_napis = font_napis.render(f'New PB! Time: {new_time}',True,(255,255,255))
            textRect_nap = text_napis.get_rect()
            textRect_nap.center = (800 // 2, 600 // 2 - 20)
            text_guide = font_guide.render('Press space to continue...',True,(255,255,255))
            textRect_gui = text_guide.get_rect()
            textRect_gui.center = (800 // 2, 600 // 2 + 60)
        else:
            text_napis = font_napis.render('Too slow. You can do better!',True,(255,255,255))
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
                    if event.key == pygame.K_SPACE:
                        menu(1)

    if finished == False:
        time = (pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
        font_timer = pygame.font.Font("font/built_titling_bd.otf", 35)
        text_timer = font_timer.render(f"{time}",True,(255,255,255))
        if time>250: # if more than 250 seconds print "too slow"
            napis(False)
        else:
            win.fill((0,0,0),(575,70,90,40))
            win.blit(text_timer, (575,70))
        pygame.display.update()
    else:
        sc = open(f"scores/level{level}_sc.txt", "rt")
        prev_time = float(sc.readline()) 
        sc.close()
        if time<prev_time:
            sc = open(f"scores/level{level}_sc.txt", "wt")
            sc.write(f"{time}")
            sc.close()
            napis(True)
        else:
            napis(False)

def game_loop():
    global hrac, start_ticks
    start = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                os._exit(1)
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if start == False:
                start_ticks = pygame.time.get_ticks()
                start = True
            hrac.move(-vel,0)
        if keys[pygame.K_RIGHT]:
            if start == False:
                start_ticks = pygame.time.get_ticks()
                start = True
            hrac.move(vel,0)
        if keys[pygame.K_UP]:
            if start == False:
                start_ticks = pygame.time.get_ticks()
                start = True
            hrac.move(0,-vel)
        if keys[pygame.K_DOWN]:
            if start == False:
                start_ticks = pygame.time.get_ticks()
                start = True
            hrac.move(0,vel)
        if start == True:
            timer()
        if finished == True:
            break
        clock.tick(19)  #FPS

def submenu(choice): #mod True = play, False = scores
    global hrac, level, finished
    finished = False
    vybrana_barva = (255,0,0)
    normalni_barva = (212,123,21)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if choice == 6:
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
                if event.key == pygame.K_RETURN:
                    if choice == 1:     #level 1
                        level = 1
                        build("levels/level1.txt")
                        hrac = player()
                        game_loop()
                    elif choice == 2:   #level 2
                        level = 2
                        build("levels/level2.txt")
                        hrac = player()
                        game_loop()

                    elif choice == 3:   #level 3
                        level = 3
                        build("levels/level3.txt")
                        hrac = player()
                        game_loop()
                    elif choice == 4:   #level 4
                        level = 4
                        build("levels/level4.txt")
                        hrac = player()
                        game_loop()
                    elif choice == 5:   #level 5
                        level = 5
                        build("levels/level5.txt")
                        hrac = player()
                        game_loop()
                    else:               #back
                        menu(1)
           
def menu(choice):
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
                        sc.write(f"999.99")
                        sc.close()
                        build("levels/random_level.txt")
                        hrac = player()
                        game_loop()
                    elif choice == 3:   #scores
                        scores()
                    else:               #exit
                        pygame.quit()
                        os._exit(1)
                    
#Game________________________________________________________________________________________________________________________________________Game_end                       
#main

menu(1)

        

