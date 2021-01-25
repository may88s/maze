#!/usr/bin/python

""" box.py
    comment
    line 3 """
import pygame,random,menu
pygame.init()
pygame.font.init()
#===================================================================
# Globals:
#===================================================================
BLUE=(0,0,255)
BLACK=(128,128,128)
RED=(255,255,0)
GREEN=(0,255,0)
width=1800         # screen size
height=900
base_x=10        # co-ords of top left of first cell.
base_y=10
#(size_x,size_y,rows,cols)=(50,40,35,30)
#(size_x,size_y,rows,cols)=(25,25,width/25-1,height/25-1)
size=90  #55
smooth=True
anim_hops=10
anim_step=size/anim_hops*1.0
(size_x,size_y,rows,cols)=(size,size,(width-2*base_x)/size-1,(height-2*base_y)/size-1)
total=rows*cols   # number of elements
cells=[]          # list of Cell data
screen=pygame.display.set_mode((width,height))
background=pygame.Surface(screen.get_size())
background=background.convert()
dot_size=0
myfont = pygame.font.SysFont('Comic Sans MS', 30)
flipcount=300
#===================================================================
# Objects:
#===================================================================
class Cell:
  def __init__(self,i):
    self.north=0            # Block(wall) to the north
    self.east=0             # Block(wall) to the east
    self.visit=0            # cell visit count.
#
    x=base_x+(i%rows)*size_x
    y=base_y+(i/rows)*size_y
    x1=x+size_x-1
    y1=y+size_y-1
#
    self.drawNorth=((x,y),(x1,y))         # co-ords of top left corner
    self.drawEast=((x1,y),(x1,y1))     # co-ords of the bottom right corner
#---
class Player(pygame.sprite.Sprite):
  def __init__(self,start_cell,target,colour,name):
    pygame.sprite.Sprite.__init__(self)
    self.cell=start_cell
    self.target=target
    self.colour=colour
    self.name=name
    self.trail=False
    self.image=pygame.Surface((size-2,size-2))
    self.image.fill(BLACK)
    half=9
    pygame.draw.circle(self.image,colour,(size/2,size/2),half,0)
    self.dir=-1           # 0=north, 1=East, 2=South, 3=West, -1 = no move
    self.anim=[]
    x=base_x+(self.cell%rows)*size+(size/2)
    y=base_y+(self.cell/rows)*size+(size/2)
    self.anim.append((x,y))
    self.rect=self.image.get_rect()   ###
    self.set_rect()
    drawTarget(target,colour)

  def set_rect(self):
    (x,y)=self.anim.pop(0)
    if not self.anim: self.anim.append((x,y))    # ensure there is a value in the list.
    self.rect.centerx=x
    self.rect.centery=y
  def update(self):
    if self.dir == -1:
      self.set_rect()
      return
    cx=(self.cell%rows)
    cy=(self.cell/rows)
    dirx=diry=0
    if self.dir == 0 and cy > 0:   # north
      if cells[self.cell].north == 0:           # not blocked
        self.cell-=rows
        diry=anim_step*-1
    elif self.dir == 1 and cx < rows-1 :   # east
      if cells[self.cell].east == 0:           # not blocked
        self.cell+=1
        dirx=anim_step
    elif self.dir == 2 and cy < cols-1:   # South
      tc=self.cell+rows
      if cells[tc].north == 0:           # not blocked
        self.cell=tc
        diry=anim_step
    elif self.dir == 3 and cx > 0:   # West
      tc=self.cell-1
      if cells[tc].east == 0:           # not blocked
        self.cell-=1
        dirx=anim_step*-1
    if smooth:    
      (x,y)=self.anim.pop()
      for i in range(anim_hops):
        x+=dirx
        y+=diry
        self.anim.append((x,y))
    x=base_x+(self.cell%rows)*size+(size/2)  # make sure there is no rounding on the last one.
    y=base_y+(self.cell/rows)*size+(size/2)
    self.anim.append((x,y))
    self.set_rect()
    self.dir=-1
#===================================================================
# FUNCTIONS:
#===================================================================
def Check_cell(direction,c,new_c,last_c):
  if new_c == last_c:             # ignore where you have just came from.
    return False
  if cells[new_c].visit == 0:
    return True
  if cells[c].visit > 0:		# Don't block/draw if backtracking.
    return False
#
# the new cell has already been visited.  Block this off.
  if direction == 0:
    cells[c].north=1
    (start_pos,end_pos)=cells[c].drawNorth
  elif direction == 1:
    cells[c].east=1
    (start_pos,end_pos)=cells[c].drawEast
  elif direction == 2:
    cells[new_c].north=1
    (start_pos,end_pos)=cells[new_c].drawNorth
  else:
    cells[new_c].east=1
    (start_pos,end_pos)=cells[new_c].drawEast
#
  pygame.draw.line(background,RED,start_pos,end_pos, 1)
  return False
#---
# backtrack.  No virgin cell to move to.
# need to move to the lowest visited unblocked cell
def backtrack(c,cx,cy):
  visit=9999999
  if cy > 0:  #North
    tc=c-rows
    if cells[c].north == 0:	# not blocked
      new_c=tc
      visit=cells[tc].visit
  if cx < rows-1:  #East
    tc=c+1
    if cells[c].east == 0:	# not blocked
      if cells[tc].visit < visit:
        new_c=tc
        visit=cells[tc].visit
  if cy < cols-1:  #South
    tc=c+rows
    if cells[tc].north == 0:	# not blocked
      if cells[tc].visit < visit:
        new_c=tc
        visit=cells[tc].visit
  if cx > 0:  #West
    tc=c-1
    if cells[tc].east == 0:	# not blocked
      if cells[tc].visit < visit:
        new_c=tc
        #visit=cells[tc].visit
  return new_c
#---
def hold(winner):
  keepGoing=True
  clock=pygame.time.Clock()
  drainAnim=True
  while keepGoing:  
    clock.tick(30)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        keepGoing=False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
          keepGoing=False
    if drainAnim:
      allSprites.clear(screen, background)
      allSprites.update()
      allSprites.draw(screen)                   
      pygame.display.flip()
      if len(winner.anim) == 1:
        drainAnim=False
#---
def winner(winner,loser):
  x=base_x+(loser.cell%rows)*size+size
  y=base_y+(loser.cell/rows)*size+size
  textsurface = myfont.render(winner.name+" wins", False, winner.colour)
  screen.blit(textsurface,(x,y))
  pygame.display.flip()
  hold(winner)
#---
def maze(doDraw):
  global  cells, background
  background.fill(BLACK)
  pygame.draw.rect(background,RED,(base_x,base_y,size_x*rows,size_y*cols), 1)
  flipme=flipcount
#
# build maze and draw maze
  cells=[]
  for i in range(total):
    cells.append(Cell(i))
#
  c=random.randrange(total)     # cell element.
  last_c=c          # previous Cell - start on self.
  visited=0
  while True:
    cx=(c%rows)
    cy=(c/rows)
    options=[]            # looking ahead to where we could moved to.
    if cy > 0:  #North
      if Check_cell(0,c,c-rows,last_c):
        options.append(c-rows)
    if cx < rows-1:  #East
      if Check_cell(1,c,c+1,last_c):
        options.append(c+1)
    if cy < cols-1:  #South
      if Check_cell(2,c,c+rows,last_c):
        options.append(c+rows)
    if cx > 0:  #West
      if Check_cell(3,c,c-1,last_c):
        options.append(c-1)
#
    if cells[c].visit == 0:       # visit cherry popped.
      visited+=1
    if visited >= total:         # are we done yet?
      pygame.display.flip()
      break
    cells[c].visit+=1             # increment the visited cell
    if options: 
      new_c=options[random.randint(0,len(options)-1)]   # pick one of the available options at random.
    else:
      cells[c].visit+=1
      new_c=backtrack(c,cx,cy)           		    # Dead-end, we need to backtrack
    last_c=c
    c=new_c
    flipme-=1
    if not flipme:
      pygame.display.flip()
      flipme=flipcount
#---012
def drawTarget(target,colour):
  x=base_x+(target%rows)*size+(size/2)
  y=base_y+(target/rows)*size+(size/2)
  pygame.draw.circle(background,colour,(x,y),5,1)
#---
def game1():
  maze(True)
#
  players=[]
  players.append(Player(0,total-1,BLUE,"player1"))
  players.append(Player(total-1,0,GREEN,"player2"))
  allSprites=pygame.sprite.Group(players)
  screen.blit(background,(0,0))
  keepGoing=True
  clock=pygame.time.Clock()
  ##L-loop
  while keepGoing:  
    ##T-time
    clock.tick(30)
    ##E-events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        keepGoing=False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          keepGoing=False
        elif event.key == pygame.K_w:
          players[0].dir=0
        elif event.key == pygame.K_d:
          players[0].dir=1
        elif event.key == pygame.K_s:
          players[0].dir=2
        elif event.key == pygame.K_a:
          players[0].dir=3
        elif event.key == pygame.K_UP:
          players[1].dir=0
        elif event.key == pygame.K_RIGHT:
          players[1].dir=1
        elif event.key == pygame.K_DOWN:
          players[1].dir=2
        elif event.key == pygame.K_LEFT:
          players[1].dir=3
    allSprites.clear(screen, background)
    allSprites.update()
    allSprites.draw(screen)          
    j=1
    for i in [0,1]:
      if players[i].cell == players[i].target:
        winner(players[i],players[j])
        keepGoing=False
      else:
        j=0
  return True
#---
def game2():
#
# init screen
  maze(False)
  top_x=10
  top_y=10
  bot_x=top_x+800
  bot_y=top_y+600
  points=[]
  x=top_x
  for a in (70,100,76,56,36,24,20):
    x+=a
    y=(x/4)*3
    points.append((x,y))
    print x,x%4
  background.fill(BLACK)
  pygame.draw.rect(screen,RED,(top_x,top_y,800,600), 1)
  pygame.draw.line(screen,RED,(top_x,top_y),(bot_x,bot_y), 1)
  pygame.draw.line(screen,RED,(bot_x,top_y),(top_x,bot_y), 1)
  for (x,y) in points:
    pygame.draw.line(screen,RED,(x,y),(x,bot_y-y), 1)
    pygame.draw.line(screen,GREEN,(bot_x-x,y),(bot_x-x,bot_y-y), 1)
    pygame.draw.line(screen,BLUE,(x,y),(bot_x-x,y), 1)
    pygame.draw.line(screen,BLUE,(x,bot_y-y),(bot_x-x,bot_y-y), 1)
  #  pygame.draw.rect(screen,RED,(cx,cy,size_x,size_y), 1)
  pygame.display.flip()
#
  keepGoing=True
  clock=pygame.time.Clock()
  ##L-loop
  while keepGoing:  
    ##T-time
    clock.tick(30)
    ##E-events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        keepGoing=False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          keepGoing=False
  return True
#---
def options():
#
# init screen
  maze(False)
  top_x=10
  top_y=10
  bot_x=top_x+800
  bot_y=top_y+600
  points=[]
  x=top_x
  for a in (70,100,76,56,36,24,20):
    x+=a
    y=(x/4)*3
    points.append((x,y))
    print x,x%4
  background.fill(BLACK)
  pygame.draw.rect(screen,RED,(top_x,top_y,800,600), 1)
  pygame.draw.line(screen,RED,(top_x,top_y),(bot_x,bot_y), 1)
  pygame.draw.line(screen,RED,(bot_x,top_y),(top_x,bot_y), 1)
  for (x,y) in points:
    pygame.draw.line(screen,RED,(x,y),(x,bot_y-y), 1)
    pygame.draw.line(screen,GREEN,(bot_x-x,y),(bot_x-x,bot_y-y), 1)
    pygame.draw.line(screen,BLUE,(x,y),(bot_x-x,y), 1)
    pygame.draw.line(screen,BLUE,(x,bot_y-y),(bot_x-x,bot_y-y), 1)
  #  pygame.draw.rect(screen,RED,(cx,cy,size_x,size_y), 1)
  pygame.display.flip()
#
  keepGoing=True
  clock=pygame.time.Clock()
  ##L-loop
  while keepGoing:  
    ##T-time
    clock.tick(30)
    ##E-events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        keepGoing=False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          keepGoing=False
  return True
#-----------
# main program loop
def main():
  pygame.display.set_caption("May's maze")
#
  keepGoing=True
  while keepGoing:
    choice=menu.menu(screen,"A Maze Zing",["Dual","game2","Options"])
    if choice == 1:
      keepGoing=game1()
    elif choice == 2:
     keepGoing=game2()
    elif choice == 3:
        keepGoing=options()
    else:
      keepGoing=False   # menu returned 0 or an invalid option.
#===================================================================
# CODE:
#===================================================================
if __name__ == "__main__":
    main()
pygame.quit()
###fin
