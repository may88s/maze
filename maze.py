""" Maze
    Simon May
    9/12/18
    maze.py
"""
#IDEAL
#I-init
import pygame,random
pygame.init()
pygame.mixer.init()

#-Globals
INITBOOMSIZE=10  ##KEEP EVEN
MAXBOOMSIZE=70
MINBOOMSIZE=5
BOOMRATE=0.5
#
class Label(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.font=pygame.font.Font("data/Asimov.ttf",25)
    self.text=""
    self.center=(400,240)
  def update(self,screen,grot):
    self.image=self.font.render(self.text, True, (0xcc,0xcc,0xcc))
    self.rect=self.image.get_rect()
    self.rect.center=self.center
#        
class Boom(pygame.sprite.Sprite):
    def __init__(self,screen,sx=None,sy=None):
        pygame.sprite.Sprite.__init__(self)
        self.size=INITBOOMSIZE
        c=random.randrange(100,0xcc)
        self.colour=(0xff,c,c)
        self.image=pygame.Surface((self.size,self.size))
        self.image.fill(self.colour)
        self.rect=self.image.get_rect()
        if sx != None:
            self.rect.centerx=sx
        else:
            self.rect.centerx=random.randrange(0,screen.get_width())
        if sy != None:
            self.rect.centery=sy
        else:
            self.rect.centery=random.randrange(0,screen.get_height())
        self.centerx=float(self.rect.centerx)
        self.centery=float(self.rect.centery)
        self.moving=True  # Boom is either moving or booming.
        rate=2.0+(random.random()*1.5)
        if random.random() >= 0.9:
          rate*=1.5
        if random.random() >= 0.5:
          rate*=-1
        if random.random()>= 0.5:
          self.dx=rate
          self.dy=0.0
        else:
          self.dx=0.0
          self.dy=rate
        if random.random()<= 0.2:  # smal chance the boom moved diagonally.
          self.dx=rate
          self.dy=rate
        self.inflating=True
        self.inflate_rate=BOOMRATE
        self.inflate_size=float(self.size)
    def update(self,screen,inflatingSprites):
        if self.moving:
            self.move(screen)
        else:
            self.boom(screen,inflatingSprites)
    def move(self,screen):
        self.centerx+=self.dx
        self.centery+=self.dy
        self.rect.centerx=int(self.centerx)
        self.rect.centery=int(self.centery)
        if self.rect.top < 0:
            self.rect.centery=self.size/2
            self.dy*=-1
            self.centery=float(self.rect.centery)
        elif self.rect.bottom > screen.get_height():
            self.rect.centery=screen.get_height()-(self.size/2)
            self.dy*=-1
            self.centery=float(self.rect.centery)
        if self.rect.left < 0:
            self.rect.centerx=self.size/2
            self.dx*=-1
            self.centerx=float(self.rect.centerx)
        elif self.rect.right > screen.get_width():
            self.rect.centerx=screen.get_width()-(self.size/2)
            self.dx*=-1
            self.centerx=float(self.rect.centerx)
    def boom(self,screen,inflatingSprites):
        (x,y)=self.rect.center
        if self.inflating:
            self.inflate_size+=self.inflate_rate
            newsize=int(self.inflate_size)
            if newsize > self.size:
                self.size=newsize
                self.rect.inflate_ip(1,1)
                self.image=pygame.Surface((newsize,newsize))
                self.image.fill(self.colour)
            if newsize >= MAXBOOMSIZE:
                self.inflating=False
        else:            
            self.inflate_size-=self.inflate_rate
            newsize=int(self.inflate_size)
            if newsize < self.size:
                self.size=newsize
                self.rect.inflate_ip(-1,-1)
                self.image=pygame.Surface((newsize,newsize))
                self.image.fill(self.colour)
            if newsize <= MINBOOMSIZE:
                self.kill()
        self.rect.center=(x,y)
def splashScreen(screen,background,text1,text2,music):
  """ Display a text prompt on it's own screen.
      """
  message1=Label()
  message1.text=text1
  message1.center=(400,180)
  message2=Label()
  message2.text=text2
  hitSpace=Label()
  hitSpace.text="Press Space to Continue"
  hitSpace.center=(400,300)
  allSprites=pygame.sprite.Group(message1,message2,hitSpace)
  screen.blit(background,(0,0))
  keepGoing=True
  clock=pygame.time.Clock()
  pygame.mixer.music.load(music)
  pygame.mixer.music.play(-1)
  doExit=False
  while keepGoing:
    ##T-time
    clock.tick(30)
    ##E-events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        keepGoing=False                    
        doExit=True
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          keepGoing=False                    
          doExit=True
        if event.key == pygame.K_SPACE:
          keepGoing=False
      elif event.type == pygame.MOUSEBUTTONDOWN:    
        (button1,button2,button3)=pygame.mouse.get_pressed()
        if button1:
          keepGoing=False
    ##R-refresh screen
    allSprites.clear(screen, background)
    allSprites.update(screen,None)
    allSprites.draw(screen)
    #
    pygame.display.flip()
  #
  screen.blit(background,(0,0))
  pygame.display.flip()
  pygame.mixer.music.fadeout(1000)
  return doExit
  
def main():
    #D-display
    screen=pygame.display.set_mode((800,480),pygame.FULLSCREEN)
    pygame.display.set_caption("Boom3 - a crude Boomshine clone.")
    #E-entities
    (W,H)=screen.get_size()
    background=pygame.Surface((W,H))
    background.fill((0x0,0x0,0x0))
    screen.blit(background,(0,0))
    intro="data/intro.ogg"
    mainSection="data/mainSection.ogg"
    plinks=[]
    plinks.append(pygame.mixer.Sound("data/A1.ogg"))
    plinks.append(pygame.mixer.Sound("data/D1.ogg"))
    plinks.append(pygame.mixer.Sound("data/D2.ogg"))
    plinks.append(pygame.mixer.Sound("data/F1.ogg"))
    pygame.mixer.music.fadeout(500)
#
    label=Label()
#
    inflatingSprites=pygame.sprite.Group(label)  ## define the group.
    inflatingSprites.empty()
    #A-action
    ##ALTER
    ##A-assign
    #pygame.mouse.set_visible(False)
    keepGoing=True
    clock=pygame.time.Clock()
    levels=[(100,75),(10,3),(20,5),(30,8),(40,10),(50,15),(60,30),(60,40),(10,5)]
    level=0
    total=0
    text1="Welcome"
    ##L-loop
    while keepGoing:
      (numberBooms,numberNeeded)=levels[level]
      boomers=[]
      for i in range(numberBooms):
        boomers.append(Boom(screen))
      movingSprites=pygame.sprite.Group(boomers)
      allSprites=movingSprites.copy()   # rebuild allSprites
      allSprites.add(label)
      keepLevel=True
      started=False
      score=0
      label.text=""
      if splashScreen(screen,background,text1,"Level %d! You need %d of %d." % (level+1,numberNeeded,numberBooms),intro):
        pygame.quit()
      pygame.mixer.music.load(mainSection)
      pygame.mixer.music.play(-1)
      while keepLevel:
        ##T-time
        clock.tick(30)
        ##E-events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing=False
                keepLevel=False
            elif event.type == pygame.MOUSEBUTTONDOWN:    
                (button1,button2,button3)=pygame.mouse.get_pressed()
                if button1 and not started:
                    (x,y)=pygame.mouse.get_pos()
                    boomer=Boom(screen,x,y)
                    inflatingSprites=pygame.sprite.Group(boomer)
                    allSprites.add(boomer)
                    boomer.moving=False
                    started=True
        # collisions
        for boomer in pygame.sprite.groupcollide(movingSprites, inflatingSprites, False, False).keys():
          plinks[random.randrange(0,4)].play()
          boomer.add(inflatingSprites)
          boomer.remove(movingSprites)
          boomer.moving=False
          score+=1
          label.text="Score: %d/%d" % (score,numberNeeded)
          (x,y)=label.font.size(label.text)
          label.center=(screen.get_width()-(x+5),screen.get_height()-(y+5))
        if started and not inflatingSprites:
          keepLevel=False
        ##R-refresh screen
        allSprites.clear(screen, background)
        allSprites.update(screen,inflatingSprites)
        allSprites.draw(screen)
        #
        pygame.display.flip()
      #end of level.
      pygame.mixer.music.fadeout(1000)  
      if score < numberNeeded:     
        total-=(numberNeeded-score)
        text1="Sorry you only scored %d and needed %d. Total score=%d" % (score,numberNeeded,total)
      else:
        level+=1
        total+=score
        if level == len(levels):
          keepGoing=False
        else:
          text1="Level completed! You scored %d. Total Score=%d" % (score,total)
    #L-Leave
    #pygame.mouse.set_visible(True)
    splashScreen(screen,background,"","Game Over! You scored %d with a total of %d." % (score,total),intro)
if __name__ == "__main__":
    main()
pygame.quit()
###fin
