import pygame as pg
import random,noise
# Constantes :
FPS = 60  # les fps tabernak
WIND = 750 # dimentions de la fentere
dep=1
pg.init()
f = pg.display.set_mode(size=(WIND, WIND))
pg.display.set_caption("The //) game")
fpsClock = pg.time.Clock()
font = pg.font.SysFont('consolas', 30) #police//roxane
depx,depy=0,0#la caméra
zoom=1
b = True
tuiles:list=[]
anim=[pg.image.load("sprite//b_"+format(i,"02")+".png") for i in range(11)]
stop=pg.image.load("sprite//assis.png")
grav=0.4
vitesse=5
fond=pg.image.load("fond.png")
width=fond.get_rect().width
sachet=pg.image.load("crispy pix.png").convert()
sachet=pg.transform.scale(sachet,(25,25))
score=0
pg.mixer.init()
pg.mixer.music.load("sounds//zik.mp3")
pg.mixer.music.play(-1)
class Perso:
    """Le personnage principal"""
    def __init__(self):
        self.img=anim
        self.index_anim=0
        self.rect=self.img[0].get_rect()
        self.vy=0.0
        self.jump=False
        
    def draw(self):
        global score
        self.vy+=grav
        self.rect=self.rect.move(0,self.vy)
        if self.rect.y+self.rect.height/2>WIND:
            self.rect.y=0
            self.vy=0
        elif self.rect.y-self.rect.height/2+self.vy<0:
            self.rect.y=self.rect.height/2
            self.vy=0
        if self.jump:
            self.vy-=15
            self.jump=False
        self.Assis=False
        for jacko in tuiles:
            if jacko.fertile:
                if self.rect.colliderect(jacko.fertile):
                    jacko.fertile=False
                    score+=1
                    self.son=pg.mixer.Sound("sounds//ohh.mp3")
                    self.son.play()
            if self.rect.colliderect(jacko):
                self.Assis=True
                if self.vy>0:
                    self.vy=0
                    self.rect.y=jacko.rect.y-4-self.rect.height/2
                self.rect.x-=vitesse
                break
            
        if not self.Assis:
            self.index_anim+=1
        self.index_anim=self.index_anim%11
        if self.Assis:
            f.blit(stop,self.rect)
        else:
            f.blit(self.img[self.index_anim],self.rect)
        
class Sol:
    """Les planchers"""
    def __init__(moi,hauteur):
        moi.rect=pg.Rect((WIND,hauteur),(random.randrange(10,20)*20,10))
        moi.coul=(150,150,150)
        
        if random.randint(0,4):
            moi.fertile=False
        else:
            moi.fertile=Crispy(moi.rect.center)
    def draw(self):
        pg.draw.rect(f,self.coul,self.rect)
        self.rect.x-=vitesse
        if self.fertile:
            self.fertile.draw()
        if self.rect.x+self.rect.width<0:
            tuiles.pop(tuiles.index(self))
            print(len(tuiles))

class Crispy:
    """Les sachets à recupérer"""
    def __init__(moi,pos):
        moi.img=sachet
        moi.rect=sachet.get_rect()
        moi.rect.center=pos
        moi.rect.y-=moi.rect.height/2
    def draw(moi):
        f.blit(moi.img,moi.rect)
        moi.rect=moi.rect.move(-vitesse,0)
tuiles.append(Sol((noise.pnoise1(0)+0.5)*WIND/2))
uol=Perso()
tour=0
i=0
defil1,defil2=0,width
try:
    while b:
        # Actualiser:
        pg.display.flip()

        # Appliquer les images de fond sur la fenetre

        text = font.render(('Score: '+str(score)), True, (0,0,0))
        textRect = text.get_rect()
        
        p = pg.key.get_pressed()  # SI la touche est appuyée
        if p[pg.K_d]:uol.rect.x+=dep
        if p[pg.K_q]:uol.rect.x-=dep
        vitesse+=0.001

        tour+=1
        if tour>=500/vitesse:
            tour=0
            tuiles.append(Sol(noise.pnoise1(i/10)*WIND/3+WIND/2))
            i+=1
            i=i%10
        f.blit(fond, (defil1, -500))
        f.blit(fond,(defil2,-500))
        defil1-=5
        defil2-=5
        if defil1<-width:
            defil1=defil2+width
        if defil2<-width:
            defil2=defil1+width
        pointer=pg.mouse
        for event in pg.event.get():  # QUAND la touche est appuyée
            if event.type == pg.QUIT:
                b = False
                print("=> Fin du jeu  babe")
            elif event.type == pg.KEYDOWN:
                if event.dict['key']==pg.K_z:
                    if uol.Assis:
                        uol.jump=True
                
                    
            elif event.type==pg.MOUSEBUTTONUP:
                """if event.button==1: #click gauche
                    pos=event.pos


                    

                if event.button==3: #click droit
                   
                elif event.button==4: #vers le haut
                    zoom+=0.01
                elif event.button==5: #vers le bas
                    zoom-=0.01"""

        
        f.blit(text, (0,0))
        for jack in tuiles:
            jack.draw()
        uol.draw()
        fpsClock.tick(FPS)
except :
    pg.quit()
    raise
finally:
    pg.quit()
