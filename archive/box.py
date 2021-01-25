""" box.py
    comment
    line 3 """
import pygame,random
pygame.init()


base_x=100
base_y=100
size_x=20
size_y=15
running = 1
BLUE=(0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
width=800
height=600
rows=20
cols=15
total=rows*cols
visited=0
cells=[]

#===================================================================
# FUNCTIONS:
#===================================================================
class Cell:
  def __init__(self,i):
    self.top=0              # wall on top flag
    self.right=0            # wall on right flag
    self.visit=0            # cell visit count.
#    
    x=base_x+(i%rows)*size_x
    y=base_y+(i/rows)*size_y
    x1=x+size_x-1
    y1=y+size_y-1
#
    self.drawTop=((x,y),(x1,y))         # co-ords of top left corner
    self.drawRight=((x1,y),(x1,y1))     # co-ords of the bottom right corner
#---
class Player:
  def __init__(self,start_cell,name):
    self.cell=start_cell
    self.name=name
    self.trail=0
#===================================================================
# FUNCTIONS:
#===================================================================
def Check_cell(new_c,last_c):
  if new_c == last_c:             # ignore where you have just came from.
    return false
  if cells[new_c].visit == 0:
    return true
  
#---
def game1():
#
# init screen
  linecolour=RED
  bgcolour=BLACK
  #screen = pygame.display.set_mode((width, height))
  screen.fill(bgcolour)
#
# build maze and draw maze
  for i in range(total):
    cells[i]=Cell(i)
#
  cx=0              # cell co-ordinates
  cy=0
  c=cx*rows+cy*cols # cell element.
  last_c=c          # previous Cell - start on self.
  while visitied < total:
    if cells[c].visit == 0:
      visited+=1
    cells[c].visit+=1     # increment the visited cell
    options=[]            # looking ahead to where we could moved to.
    if cy > 0:  #North
      if Check_cell(c-rows,last_c):
        options.append(c-rows)
    if cx < rows-1:  #East
      if Check_cell(c+1,last_c):
        options.append(c+1)
    if cy < cols-1:  #South
      if Check_cell(c+rows,last_c):
        options.append(c+rows)
    if cx > 0:  #West
      if Check_cell(c-1,last_c):
        options.append(c-1)
  ##up to here  define fuction Check_cell
    
  for oc in (c-rows, c+1, c+rows, c-1):   # nesw
    if oc <0 or oc > total-1:
      continue
    
  
#-----------
# main program loop
def main():
  screen=pygame.display.set_mode((width,height))
  pygame.display.set_caption("May's maze")
#
  keepGoing=True
  while keepGoing:
    choice=menu.menu(screen,"Astrobelt Main Menu")
    if choice == 1:
      keepGoing=game1(screen)
#    elif choice == 2:
#     keepGoing=game2(screen)
#    elif choice == 3:
#        keepGoing=game3(screen)
    else:
      keepGoing=False   # menu returned 0 or an invalid option.
#===================================================================
# CODE:
#===================================================================
if __name__ == "__main__":
    main()
pygame.quit()
###fin
