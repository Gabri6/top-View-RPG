# -*- coding: utf-8 -*-
#
#Created on Mon Feb  8 22:26:09 2021
#
#@author: gabri
#

import sys
import random
import time
import pygame
import math


screenHeight = 700
screenWidth = 1400
timeSinceLastCommand=0
waitTime=1000



pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((screenWidth,screenHeight))
screen.fill([255,255,255])

class Player():
    def __init__(self, walls):
        self.s , self.h= ((screenWidth//2),(screenHeight//2)) # player's parameters
        self.playerHeight = 20
        self.playerWidth = 20
        self.baseSpeed = 5/10
        self.timeSinceMove = time.time()
        self.playerSpeed = 2/10
        self.playerMaxHealth = 10
        self.playerHealth = self.playerMaxHealth
        self.playerScore = 0
        self.playerAttack = False
        self.attackCoolDown = 0.35
        self.attackTime = 0.2
        self.timeSinceAttack = 0
        self.rangeAttack = 50
        self.attackDamage = 1
        self.directionAttack = math.pi/4
        self.attackSide = "right"
        self.playerUlti = False
        self.ultiCoolDown = 2.3
        self.ultiTime = 0.5
        self.timeSinceUlti = 0
        self.rangeUlti = 75
        self.ultiDamage = 2
        self.timeInvicible = 0.6
        self.timeSinceBit = 0
        self.canGoUp = True
        self.canGoDown = True
        self.canGoRight = True
        self.canGoLeft = True
        self.playerRedRectanglePos = [0, -5]
        self.collidesWithAWall(walls)
        while not (self.canGoUp and self.canGoDown and self.canGoLeft and self.canGoRight):
            self.s, self.h = random.randint(0 , screenWidth), random.randint(0 , screenHeight)                
            self.collidesWithAWall(walls)
        self.playerPos = self.s, self.h


    def move(self, walls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #used to stop the program when the cross to close the window is pressed
                sys.exit()
        key = pygame.key.get_pressed() #look at which key is pressed
        if key[pygame.K_ESCAPE]:  #use the escape key to close the window
            sys.exit()
        if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]:  #use the shift key to make the player "run" by increasing its speed when pressed
            self.playerSpeed = 1.75 * self.baseSpeed
        else:
            self.playerSpeed = self.baseSpeed

        self.collidesWithAWall(walls)

        deltaTime = (time.time() - self.timeSinceMove) *200
        self.timeSinceMove = time.time()

        if key[pygame.K_UP] or key[pygame.K_z]:  #if "z" or "up" keys are pressed, player goes up 
            if self.h > 0 + self.playerSpeed + self.playerHeight//2 and self.canGoUp:
                self.h -= self.playerSpeed * deltaTime
                self.playerRedRectanglePos = [-5, -10]
                self.directionAttack = 3 * math.pi/4
                self.attackSide = "up"


        if key[pygame.K_DOWN] or key[pygame.K_s]:  #if "s" or "down" keys are pressed, player goes down
            if self.h < (screenHeight - self.playerSpeed - self.playerHeight//2) and self.canGoDown:
                self.h += self.playerSpeed * deltaTime
                self.playerRedRectanglePos = [-5, 0]
                self.directionAttack = 7 * math.pi/4
                self.attackSide = "down"

        if key[pygame.K_LEFT] or key[pygame.K_q]:  #if "q" or "left" keys are pressed, player goes left
            if self.s > 0 + self.playerSpeed + self.playerWidth//2 and self.canGoLeft:
                self.s -= self.playerSpeed * deltaTime
                self.playerRedRectanglePos = [-10, -5]
                self.directionAttack = 5 * math.pi/4
                self.attackSide = "left"

        if key[pygame.K_RIGHT] or key[pygame.K_d]:  #if "d" or "right" keys are pressed, player goes right
            if self.s < (screenWidth - self.playerSpeed - self.playerWidth//2) and self.canGoRight:
                self.s += self.playerSpeed * deltaTime
                self.playerRedRectanglePos = [0, -5]
                self.directionAttack = math.pi/4
                self.attackSide = "right"

        if key[pygame.K_SPACE]:
            if time.time() - self.timeSinceAttack >= self.attackCoolDown:
                self.playerAttack = True
                self.timeSinceAttack = time.time()
            elif time.time() - self.timeSinceAttack < self.attackTime:
                self.playerAttack = True
            else:
                self.playerAttack = False
        else:
            if time.time() - self.timeSinceAttack < self.attackTime:
                self.playerAttack = True
            else:
                self.playerAttack = False

        if key[pygame.K_b]:
            if time.time() - self.timeSinceUlti >= self.ultiCoolDown:
                self.playerulti = True
                self.timeSinceUlti = time.time()
            elif time.time() - self.timeSinceUlti < self.ultiTime:
                self.playerUlti = True
            else:
                self.playerUlti = False
        else:
            if time.time() - self.timeSinceUlti < self.ultiTime:
                self.playerUlti = True
            else:
                self.playerUlti = False

    def draw(self):   #draw the player
        if self.playerAttack == True:  #draw attack
            xAttack = self.s + (self.rangeAttack) * math.sin(self.directionAttack+((math.pi/2) * ((time.time() - self.timeSinceAttack)/self.attackTime)))
            yAttack = self.h + (self.rangeAttack) * math.cos(self.directionAttack+((math.pi/2) * ((time.time() - self.timeSinceAttack)/self.attackTime)))
            pygame.draw.line(screen, (175, 175, 175), (self.s, self.h), (xAttack, yAttack))

        if self.playerUlti == True:  #draw ulti
            xUlti = self.s + (self.rangeUlti) * math.sin((math.pi/2) * ((time.time() - self.timeSinceAttack)/(2*self.attackTime)))
            yUlti = self.h + (self.rangeUlti) * math.cos((math.pi/2) * ((time.time() - self.timeSinceAttack)/(2*self.attackTime)))
            pygame.draw.line(screen, (175, 175, 175), (self.s, self.h), (xUlti, yUlti))

        pygame.draw.rect(screen,(0,0,0),[(self.s)-10,(self.h)-10,20,20]) #big black rectangle
        pygame.draw.rect(screen,(255,0,0),[(self.s) + self.playerRedRectanglePos[0],(self.h) + self.playerRedRectanglePos[1],10,10])  #small rectangle on the side
        
        if time.time() - self.timeSinceBit < self.timeInvicible:  # draw a "-1"  if hit
            font = pygame.font.SysFont("calibri",15)
            text = pygame.font.Font.render(font,"-1", True, (0, 0, 255))
            screen.blit(text,((self.s), (self.h) - 23))
        
        

    def pos(self):  #gives the position of the player
        return self.s, self.h

    def isBittenByMonster(self, monster): #look at the distance between player and monster, player loses 1 health if monster too close
        if math.sqrt((self.s - monster.monsterPos[0])**2 + (self.h - monster.monsterPos[1])**2) < monster.rangeAttack and time.time() - self.timeSinceBit > self.timeInvicible :
            self.playerHealth -= 1
            self.timeSinceBit = time.time()
    
    def collidesWithAWall(self, walls):
        underWall = False
        overWall = False
        wallToLeft = False
        wallToRight = False
        for group in walls: #run for every group of walls
            for brick in group.listBricks: #run for every brick in the wall
                if ((brick.s) - (self.playerWidth/2) +1 < self.s < (brick.s + brick.size + self.playerWidth/2) -1): #if between left and right sides of the wall
                    if ((brick.h + brick.size/2 - (self.playerHeight + self.playerSpeed *10)/2 )< self.h < (brick.h + brick.size/2 + self.playerHeight + self.playerSpeed *10)) :
                        underWall = True
                    if ((brick.h + brick.size/2 + (self.playerHeight + self.playerSpeed *10)/2) > self.h > (brick.h + brick.size/2 - (self.playerHeight + self.playerSpeed *10))) :
                        overWall = True
                if ((brick.h + brick.size/2 - (self.playerHeight + self.playerSpeed)) +1 < self.h < (brick.h + brick.size/2 + (self.playerHeight + self.playerSpeed)) -1): #if between top and bottom of the wall
                    if ((brick.s) - (self.playerWidth/2) + brick.size/2 < self.s < (brick.s + brick.size + self.playerWidth/2)):
                        wallToLeft = True
                    if ((brick.s) - (self.playerWidth/2) < self.s < (brick.s + brick.size/2 + self.playerWidth/2)):
                        wallToRight = True
                    pass
        if underWall:
            self.canGoUp = False
        else:
            self.canGoUp = True

        if overWall:
            self.canGoDown = False
        else:
            self.canGoDown = True
        
        if wallToLeft:
            self.canGoLeft = False
        else:
            self.canGoLeft = True
        
        if wallToRight:
            self.canGoRight = False
        else:
            self.canGoRight = True



class Monster():
    def __init__(self, walls, speed, health):
        self.monsterPos = ((screenWidth//4),(screenHeight//4))  #monster's parameters
        self.monsterHeight = 30
        self.monsterWidth = 30

        self.monsterSpeed = speed
        self.timeSinceMove = time.time()
        self.monsterSide = "right"
        self.whichImage = 1
        self.legsClosing = True
        self.timeLastImageChange=time.time()
        self.timeBetweenImageChange=0.02/(self.monsterSpeed)
        self.canGoUp = True
        self.canGoDown = True
        self.canGoLeft = True
        self.canGoRight = True

        self.isHit = False
        self.monsterFullHealth = health
        self.monsterHealth = health
        self.timeInvicible = 0.6
        self.timeSinceHit = 0
        self.damageTaken = 0
        self.timeToRespawn = 1

        self.soundStab = pygame.mixer.Sound("sound/swordStab.wav")
        self.soundSlice = pygame.mixer.Sound("sound/swordSlice.wav")
        self.soundStab2 = pygame.mixer.Sound("sound/swordStab2.wav")
        self.soundRareSlice = pygame.mixer.Sound("sound/rareSwordSlice.mp3")

        self.soundSwordUlti = pygame.mixer.Sound("sound/swordUlti.ogg")

        self.rangeAttack = 10

        self.vector=[0,0]
        self.s, self.h = self.monsterPos
        self.spawn(walls)

    def draw(self):  #design of the monster
        if time.time()-self.timeLastImageChange > self.timeBetweenImageChange:
            self.timeLastImageChange = time.time()
            if self.whichImage == 1 or self.whichImage == 3:
                self.whichImage = 2
            elif not self.legsClosing:
                self.whichImage = 1
                self.legsClosing = not self.legsClosing
            else:
                self.whichImage = 3
                self.legsClosing = not self.legsClosing
        if self.vector[0] < 0:  #checks to wich side the zombie is going and uses the right image, so that he faces the player
            zombie = pygame.image.load("images/monster/zombie_right_"+str(self.whichImage)+".png")
            self.monsterSide = "right"
        elif self.vector[0] > 0:    
            zombie = pygame.image.load("images/monster/zombie_left_"+str(self.whichImage)+".png")
            self.monsterSide = "left"
        else:   #if the zombie hits a wall, uses the last side where the zombie was going, so that he faces the player
            zombie = pygame.image.load("images/monster/zombie_"+self.monsterSide+"_"+str(self.whichImage)+".png")
        zombie = pygame.transform.scale(zombie, (self.monsterWidth, self.monsterHeight))
        rect = zombie.get_rect()
        rect.center= (self.monsterWidth/2, self.monsterHeight/2)
        rect = rect.move(self.s- self.monsterWidth/2, self.h - self.monsterHeight/2)
        screen.blit(zombie, rect)
        pygame.draw.rect(screen,(255,0,0),[(self.s)-10,(self.h)-20,self.monsterHealth/self.monsterFullHealth * 20, 2])       
        if time.time() - self.timeSinceHit < self.timeInvicible:
            font = pygame.font.SysFont("calibri",15)
            text = pygame.font.Font.render(font,str(self.damageTaken), True, (255,0,0))
            screen.blit(text,((self.s), (self.h) - 23))

    def move(self, player, walls):
        self.collidesWithAWall(walls)

        self.deltax = self.s - player.playerPos[0]
        self.deltay = self.h - player.playerPos[1]
        self.vector[0] = self.deltax / math.sqrt((self.deltax**2) + self.deltay**2)
        self.vector[1] = self.deltay / math.sqrt((self.deltax**2) + self.deltay**2)


        if (self.vector[1]>0 and not self.canGoUp) or (self.vector[1]<0 and not self.canGoDown) :
            self.vector[1] = 0
            self.vector[0] = (self.vector[0]/abs(self.vector[0]))
            if (self.vector[0] > 0 and not self.canGoLeft) or (self.vector[0] < 0 and not self.canGoRight):
                self.vector[0] = 0
        
        elif (self.vector[0] > 0 and not self.canGoLeft) or (self.vector[0] < 0 and not self.canGoRight):
            self.vector[0] = 0
            self.vector[1] = (self.vector[1]/abs(self.vector[1]))
            if (self.vector[1]>0 and not self.canGoUp) or (self.vector[1]<0 and not self.canGoDown) :
                self.vector[1] = 0
        
        deltaTime = (time.time() - self.timeSinceMove) *200
        self.timeSinceMove = time.time()


        self.s -= self.monsterSpeed * self.vector[0] * deltaTime
        self.h -= self.monsterSpeed * self.vector[1] * deltaTime

    def pos(self):
        return self.s, self.h
    
    def isHitByPlayer(self, player):
        if player.playerAttack == True and math.sqrt((self.s - player.playerPos[0])**2 + (self.h - player.playerPos[1])**2) < player.rangeAttack and time.time() - self.timeSinceHit > self.timeInvicible:
            
            if player.attackSide == "up" and abs(self.s - player.playerPos[0]) < abs(self.h - player.playerPos[1]) and (self.h - player.playerPos[1]) < 0:
                self.isHit = True
            
            if player.attackSide == "down" and abs(self.s - player.playerPos[0]) < abs(self.h - player.playerPos[1]) and (self.h - player.playerPos[1]) > 0:
                self.isHit = True
            
            if player.attackSide == "left" and abs(self.s - player.playerPos[0]) > abs(self.h - player.playerPos[1]) and (self.s - player.playerPos[0]) < 0:
                self.isHit = True
            
            if player.attackSide == "right" and abs(self.s - player.playerPos[0]) > abs(self.h - player.playerPos[1]) and (self.s - player.playerPos[0]) > 0:
                self.isHit = True
            
            if self.isHit:
                self.monsterHealth -= player.attackDamage
                self.damageTaken = "-"+str(player.attackDamage)
                self.timeSinceHit = time.time()
                self.isHit = False

                soundChoice = random.randint(0,200) #launch a random sound in the chosen sounds
                if soundChoice <= 75:
                    pygame.mixer.Sound.play(self.soundStab)
                elif 75 < soundChoice <= 150:
                    pygame.mixer.Sound.play(self.soundSlice)
                elif 150 < soundChoice <= 175:
                    pygame.mixer.Sound.play(self.soundStab2)
                else:
                    pygame.mixer.Sound.play(self.soundRareSlice)



        if player.playerUlti == True and math.sqrt((self.s - player.playerPos[0])**2 + (self.h - player.playerPos[1])**2) < player.rangeUlti and time.time() - self.timeSinceHit > self.timeInvicible:
            self.monsterHealth -= player.ultiDamage
            self.damageTaken = "-"+str(player.ultiDamage)
            self.timeSinceHit = time.time()
            pygame.mixer.Sound.play(self.soundSwordUlti)
    
    def spawn(self, walls):
        if time.time() - self.timeSinceHit > self.timeToRespawn:
            self.s, self.h = random.randint(0 , screenWidth), random.randint(0 , screenHeight)
            self.collidesWithAWall(walls)
            while not (self.canGoUp and self.canGoDown and self.canGoLeft and self.canGoRight):
                self.s, self.h = random.randint(0 , screenWidth), random.randint(0 , screenHeight)
                self.collidesWithAWall(walls)
            self.monsterHealth = self.monsterFullHealth
    
    def collidesWithAWall(self, walls):
        underWall = False
        overWall = False
        wallToLeft = False
        wallToRight = False
        for group in walls: #run for every group of walls
            for brick in group.listBricks: #run for every brick in the wall
                if ((brick.s) - (self.monsterWidth/2) +1 < self.s < (brick.s + brick.size + self.monsterWidth/2) -1): #if between left and right sides of the wall
                    if ((brick.h + brick.size/2 - (self.monsterHeight + self.monsterSpeed *10)/2 )< self.h < (brick.h + brick.size/2 + self.monsterHeight + self.monsterSpeed *10)) :
                        underWall = True
                    if ((brick.h + brick.size/2 + (self.monsterHeight + self.monsterSpeed *10)/2) > self.h > (brick.h + brick.size/2 - (self.monsterHeight + self.monsterSpeed *10))) :
                        overWall = True
                if ((brick.h + brick.size/2 - (self.monsterHeight + self.monsterSpeed)) +1 < self.h < (brick.h + brick.size/2 + (self.monsterHeight + self.monsterSpeed)) -1): #if between top and bottom of the wall
                    if ((brick.s) - (self.monsterWidth/2) + brick.size/2 < self.s < (brick.s + brick.size + self.monsterWidth/2)):
                        wallToLeft = True
                    if ((brick.s) - (self.monsterWidth/2) < self.s < (brick.s + brick.size/2 + self.monsterWidth/2)):
                        wallToRight = True

        if underWall:
            self.canGoUp = False
        else:
            self.canGoUp = True

        if overWall:
            self.canGoDown = False
        else:
            self.canGoDown = True
        
        if wallToLeft:
            self.canGoLeft = False
        else:
            self.canGoLeft = True
        
        if wallToRight:
            self.canGoRight = False
        else:
            self.canGoRight = True



class Brick():
    def __init__(self, posX, posY) -> None:
        self.size = 30
        self.internalColor = (167, 103, 38)
        self.externalColor = (136, 66, 29)
        self.s = posX /10
        self.h = posY /10
    
    def draw(self):
        Brick = pygame.image.load("Brick.png")
        Brick = pygame.transform.scale(Brick, (self.size, self.size))
        rect = Brick.get_rect()
        rect = rect.move(self.s, self.h)
        screen.blit(Brick, rect)
        


class Wall():
    def __init__(self):
        self.listBricks = []
        self.nbBricks = random.randint(3, 6)
        self.startPosX = random.randint(1, 42) * 30
        self.startPosY = random.randint(1,18) * 30
        self.direction = random.randint(0, 1)

        if self.direction == 0:
            incrementInX = 30
            incrementInY = 0
        else:
            incrementInX = 0
            incrementInY = 30

        for i in range(self.nbBricks):
            self.listBricks.append(Brick((self.startPosX + (i * incrementInX)) *10 , (self.startPosY + (i * incrementInY)) *10))
    
    def draw(self):
        for entity in self.listBricks:
            entity.draw()

class SpawningHeart():
    def __init__(self, walls):
        self.heartWidth = 30
        self.heartHeight = 30
        self.posX, self.posY = random.randint(self.heartWidth/2 , screenWidth - self.heartWidth/2), random.randint(self.heartHeight/2 , screenHeight - self.heartHeight/2)
        self.canGoUp = False
        self.canGoDown = False
        self.canGoLeft = False
        self.canGoRight = False
        self.spawn(walls)
        self.soundPicked = pygame.mixer.Sound("sound/heartPickUp.ogg")

    
    def spawn(self, walls):
        self.s, self.h = random.randint(self.heartWidth/2 , screenWidth - self.heartWidth/2), random.randint(self.heartHeight/2 , screenHeight - self.heartHeight/2)
        self.collidesWithAWall(walls)
        while not (self.canGoUp and self.canGoDown and self.canGoLeft and self.canGoRight):
            self.s, self.h = random.randint(self.heartWidth/2 , screenWidth - self.heartWidth/2), random.randint(self.heartHeight/2 , screenHeight - self.heartHeight/2)
            self.collidesWithAWall(walls)
    
    def draw(self):
        redHeart = pygame.image.load("coeurPlein.png")
        redHeart = pygame.transform.scale(redHeart, (self.heartWidth, self.heartHeight))
        rect = redHeart.get_rect()
        rect.center= (self.heartWidth/2, self.heartHeight/2)
        rect = rect.move(self.posX- self.heartWidth/2, self.posY - self.heartHeight/2)
        screen.blit(redHeart, rect)

    def collidesWithPlayer(self, player):
        if abs(self.posX - player.s) < abs(self.heartWidth/2 + player.playerWidth/2) and abs(self.posY - player.h) < abs(self.heartHeight/2 + player.playerHeight/2):
            if player.playerHealth == player.playerMaxHealth:
                player.playerMaxHealth += 1
            player.playerHealth += 1
            pygame.mixer.Sound.play(self.soundPicked)
            return True
        else:
            return False
    
    def collidesWithAWall(self, walls):
        underWall = False
        overWall = False
        wallToLeft = False
        wallToRight = False
        for group in walls: #run for every group of walls
            for brick in group.listBricks: #run for every brick in the wall
                if ((brick.s) - (self.heartWidth)/2 - 1 < self.s < (brick.s + (brick.size) + (self.heartWidth)/2) +1): #if between left and right sides of the wall
                    if ((brick.h + brick.size/2 - (self.heartHeight) -1 )< self.h < (brick.h + brick.size/2 + self.heartHeight/2) +1) :
                        underWall = True
                    if ((brick.h + brick.size/2 + (self.heartHeight)) > self.h > (brick.h + brick.size/2 - (self.heartHeight))) :
                        overWall = True
                if ((brick.h + brick.size/2 - (self.heartHeight) - 1) < self.h < (brick.h + brick.size/2 + (self.heartHeight)) + 1): #if between top and bottom of the wall
                    if ((brick.s) - (self.heartWidth)/2 + brick.size/2 -1 < self.s < (brick.s + brick.size + self.heartWidth/2) +1):
                        wallToLeft = True
                    if ((brick.s) - (self.heartWidth/2) -1 < self.s < (brick.s + brick.size/2 + self.heartWidth/2) +1):
                        wallToRight = True

        if underWall:
            self.canGoUp = False
        else:
            self.canGoUp = True

        if overWall:
            self.canGoDown = False
        else:
            self.canGoDown = True
        
        if wallToLeft:
            self.canGoLeft = False
        else:
            self.canGoLeft = True
        
        if wallToRight:
            self.canGoRight = False
        else:
            self.canGoRight = True  
        

class Button():
    def __init__(self, X, Y, Width, Height, text, policeSize):  #Button([pos in X], [pos in Y], [width], [height], [text], [<which key to prees to engage the button (facultative)>])
        self.mousePressedX, self.mousePressedY = 0, 0
        self.X = X
        self.Y = Y
        self.Width = Width
        self.Height = Height
        self.text = text
        self.policeSize = policeSize
        
    def draw(self):
        pygame.draw.rect(screen,(0,0,0),[self.X,self.Y,self.Width, self.Height])
        pygame.draw.rect(screen,(255, 255, 255),[self.X + 3,self.Y + 3,self.Width - 6, self.Height - 6])
        font3 = pygame.font.SysFont("calibri", self.policeSize)
        textRestart = pygame.font.Font.render(font3, str(self.text), True, (0, 0, 0))
        restartRect = textRestart.get_rect()
        restartRect.center = (self.X + self.Width/2, self.Y + (self.Height)/2 +2)
        screen.blit(textRestart, restartRect)

    def isPressed(self, mouseX, mouseY, key=False):
        if (self.X< mouseX < self.X + self.Width and self.Y < mouseY < self.Y + self.Height) or key:     #returns true when the mouse is pressed while inside the button
            return True
        else:
            return False
 

class Game():
    def __init__(self):
        self.title = f"Zomb's"
        
        self.difficulty = "easy" #"easy", "medium" or "hard", for now it only changes the way of spawning of monsters
        #music
        music = pygame.mixer.music.load("sound/backgroundMusic.oggvorbis.ogg")
        pygame.mixer.music.play(-1)

        #commands

        self.mousePressedX=0
        self.mousePressedY=0
        self.posX1RestartButton = screenWidth/2 - 100
        self.posX2RestartButton = screenWidth/2 + 100
        self.posY1RestartButton = screenHeight/2 + 100
        self.posY2RestartButton = screenHeight/2 + 140

        

        #entities
        self.walls = []
        

        self.monster=[]
        self.monsterDeathTime=[]
        
        self.nbMonster = len(self.monster)
        self.monsterTimeToRespawn = 1

        self.toPickHeart = []
        
        self.heartSpawnProbability = 1/5000

        self.commandWaitTime = 0.5
        self.timePause = 0
        self.timeRestart = 0

        #home page
        self.homePage()

        while True:
            key = pygame.key.get_pressed() #look at which key is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT  or key[pygame.K_ESCAPE]: #used to stop the program when the cross to close the window or escape is pressed
                    sys.exit()
            if key[pygame.K_p]:
                if time.time() - self.timePause > self.commandWaitTime:
                    self.timePause = time.time()
                    self.pause(self.player)


            
            else:
                screen.fill([255,255,255])
                for entity in self.monster:
                    self.player.isBittenByMonster(entity)
                
                if self.player.playerHealth == 0:
                    time.sleep(0.2)
                    if time.time() - self.timePause > self.commandWaitTime:
                        self.monster, self.walls, self.toPickHeart = Game.gameOver(self, self.player)   #game over returns three empty lists, so remove alls the walls and monsters
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT  or key[pygame.K_ESCAPE]: #used to stop the program when the cross to close the window or escape is pressed
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_presses = pygame.mouse.get_pressed()  #get the position of the mouse if pressed
                                if mouse_presses[0]:
                                    self.mousePressedX, self.mousePressedY = pygame.mouse.get_pos()
                        if key[pygame.K_RETURN] or (self.posX1RestartButton< self.mousePressedX < self.posX2RestartButton and self.posY1RestartButton < self.mousePressedY < self.posY2RestartButton):                    #restarts the game when "enter" key is pressed
                            self.homePage()
                            self.mousePressedX, self.mousePressedY = 0, 0
                            

                else :
                    self.player.move(self.walls)
                    self.player.playerPos = self.player.pos()
                    self.player.draw()
                
                if len(self.toPickHeart) != 0:
                    if self.toPickHeart[0].collidesWithPlayer(self.player):
                        self.toPickHeart=[]
                else:
                    if random.randint(0,1/self.heartSpawnProbability) < 1:  #if there is no heart on the map, there is a little percentage of chance of another one spawning at each iteration
                        self.toPickHeart.append(SpawningHeart(self.walls))
                for newHeart in self.toPickHeart:
                    newHeart.draw()

                for entity in self.monster:
                    entity.isHitByPlayer(self.player)

                    if entity.monsterHealth > 0: #the actions the monster has to execute if he is alive
                        entity.move(self.player, self.walls)
                        entity.monsterPos = entity.pos()
                        entity.draw()
                    else:                   #when the monster is dead, remove him and put the time in the monsterDeathTime list so that it will respawn after a certain time
                        self.monster.remove(entity)
                        self.monsterDeathTime.append(time.time())
                        self.player.playerScore += 1
                
                for entity in self.walls:
                    entity.draw()
                
                self.monsterRespawn()
                
                self.draw(len(self.monster))

                pygame.display.flip()
    

    def monsterRespawn(self):  #changes the way the monster spawns depending on the difficulty
        if self.difficulty == "easy":
            monsterSpeed = 0.6/10
            monsterHealth = 5
            if len(self.monster) == 0:
                self.nbMonster += random.randint(1,4)
                for i in range(self.nbMonster):
                    self.monster.append(Monster(self.walls, monsterSpeed, monsterHealth))


        if self.difficulty == "medium":
            monsterSpeed = 2.8/10
            monsterHealth = 6
            for timeSinceDeath in self.monsterDeathTime: #check the time since each monster's death and make two respawn if the monster is dead for long enough
                if time.time() - timeSinceDeath > self.monsterTimeToRespawn:
                    self.monster.append(Monster(self.walls, monsterSpeed, monsterHealth))
                    self.monster.append(Monster(self.walls, monsterSpeed, monsterHealth))
                    self.monsterDeathTime.remove(timeSinceDeath)
            
        if self.difficulty == "hard":
            monsterSpeed = 5/10
            monsterHealth = 7
            nbMonster = len(self.monster)
            for timeSinceDeath in self.monsterDeathTime: #check the time since each monster's death and make respawn as much as there are on the map if the monster is dead for long enough
                if time.time() - timeSinceDeath > self.monsterTimeToRespawn:
                    self.monster.append(Monster(self.walls, monsterSpeed, monsterHealth))
                    self.monster.append(Monster(self.walls, monsterSpeed, monsterHealth))
                    self.monsterDeathTime.remove(timeSinceDeath)

    def restart(self):
        nbWalls = random.randint(8, 12)
        for i in range(nbWalls):
            self.walls.append(Wall())
        player = Player(self.walls)
        player.playerScore = 0
        speed = 0.6/10 if self.difficulty == "easy" else 2.8/10 if self.difficulty == "medium" else 5/10
        health = 5 if self.difficulty == "easy" else 6 if self.difficulty == "medium" else 7
        self.monster.append(Monster(self.walls, speed, health))
        self.monster.append(Monster(self.walls, speed, health))
        self.toPickHeart.append(SpawningHeart(self.walls))
        self.mousePressedX, self.mousePressedY = 0, 0


    def draw(self, nbmonster):
        font = pygame.font.SysFont("calibri",30)    #define the police used
        text = pygame.font.Font.render(font, f"Score = " + str(self.player.playerScore), True, (0, 0, 0))    #writes the score in the top left corner
        screen.blit(text, (50, 50))
        text = pygame.font.Font.render(font, f"number entities = " + str(nbmonster), True, (0, 0, 0))   #writes the number of entities at the middle top of the screen
        screen.blit(text, (550, 50))

        redHeart = pygame.image.load("coeurPlein.png")
        redHeart = pygame.transform.scale(redHeart, (30, 30))
        blackHeart = pygame.image.load("coeurVide.png")
        blackHeart = pygame.transform.scale(blackHeart, (30, 30))

        for i in range(self.player.playerMaxHealth//10 +1):      #divide the number of hearts of the player by 10 to display them as lines of ten hearts
            for j in range((self.player.playerHealth - 10 *i) if (self.player.playerHealth - 10 *i)<10 else 10):
                rect = redHeart.get_rect()
                rect = rect.move(1050 + j * 31, 50 + 15*i)
                screen.blit(redHeart, rect)
            for k in range((10 - self.player.playerHealth - 10 *i) if (self.player.playerHealth - 10 *i)<10 else 0):
                rect = blackHeart.get_rect()
                rect = rect.move(1050 + self.player.playerHealth * 31 + k * 31, 50 + 15 * i)
                screen.blit(blackHeart, rect)
    
    def homePage(self): #design how the home screen is when you press "p" in-game
        Done = True
        self.posXEasyButton = 50
        self.posYEasyButton = 100
        self.posXMediumButton = 50
        self.posYMediumButton = 150
        self.posXHardButton = 50
        self.posYHardButton = 200

        self.posXQuitButton = screenWidth - 170
        self.posYQuitButton = screenHeight - 75

        startButton = Button(self.posX1RestartButton, self.posY1RestartButton,self.posX2RestartButton - self.posX1RestartButton, self.posY2RestartButton - self.posY1RestartButton, "Start!", 40)
        easyButton = Button(self.posXEasyButton, self.posYEasyButton, 120, 35, "easy", 30)
        mediumButton = Button(self.posXMediumButton, self.posYMediumButton, 120, 35, "medium", 30)
        hardButton = Button(self.posXHardButton, self.posYHardButton, 120, 35, "hard", 30)
        quitButton = Button(self.posXQuitButton, self.posYQuitButton, 120, 35, "Quit", 30)

        while Done:
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT  or key[pygame.K_ESCAPE]: #used to stop the program when the cross to close the window or escape is pressed
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()  #get the position of the mouse if pressed
                    if mouse_presses[0]:
                        self.mousePressedX, self.mousePressedY = pygame.mouse.get_pos()
            screen.fill([255,255,255])
            font = pygame.font.SysFont("calibri",70)
            text = pygame.font.Font.render(font, str(self.title), True, (0, 0, 0)) #maybe "Perseus' Death Battle"
            textRect = text.get_rect()
            textRect.center = (screenWidth/2, screenHeight/2) #used to put the center of the text at the center of the screen
            screen.blit(text, textRect)

            font2 = pygame.font.SysFont("calibri",40)
            score = pygame.font.Font.render(font2, f"Difficulty : " + self.difficulty, True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (screenWidth/2, screenHeight/2 + 65)
            screen.blit(score, scoreRect)
            
            startButton.draw()

            easyButton.draw()     
            
            mediumButton.draw()

            hardButton.draw()

            quitButton.draw()


            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()  #get the position of the mouse if pressed
                    if mouse_presses[0]:
                        self.mousePressedX, self.mousePressedY = pygame.mouse.get_pos()

                        if startButton.isPressed(self.mousePressedX, self.mousePressedY, key[pygame.K_RETURN]):
                            nbWalls = random.randint(8, 12)
                            for i in range(nbWalls):
                                self.walls.append(Wall())
                            self.player = Player(self.walls)
                            self.player.playerScore = 0
                            speed = 0.6/10 if self.difficulty == "easy" else 2.8/10 if self.difficulty == "medium" else 5/10
                            health = 5 if self.difficulty == "easy" else 6 if self.difficulty == "medium" else 7
                            self.monster.append(Monster(self.walls, speed, health))
                            self.monster.append(Monster(self.walls, speed, health))
                            self.toPickHeart.append(SpawningHeart(self.walls))
                            self.mousePressedX, self.mousePressedY = 0, 0
                            Done = False

                        if easyButton.isPressed(self.mousePressedX, self.mousePressedY, key[pygame.K_a]):
                            self.mousePressedX, self.mousePressedY = 0, 0
                            self.difficulty = "easy"
                        
                        if mediumButton.isPressed(self.mousePressedX, self.mousePressedY, key[pygame.K_z]):
                            self.mousePressedX, self.mousePressedY = 0, 0
                            self.difficulty = "medium"
                        
                        if hardButton.isPressed(self.mousePressedX, self.mousePressedY, key[pygame.K_e]):
                            self.mousePressedX, self.mousePressedY = 0, 0
                            self.difficulty = "hard"
                        
                        if quitButton.isPressed(self.mousePressedX, self.mousePressedY, key[pygame.K_ESCAPE]):
                            sys.exit()
            
            pygame.display.flip()

    def pause(self, player): #design how the pause screen is when you press "p" in-game
        Done = True
        screen.fill([255,255,255])
        font = pygame.font.SysFont("calibri",70)
        text = pygame.font.Font.render(font, f"Pause", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (screenWidth/2, screenHeight/2) #used to put the center of the text at the center of the screen
        screen.blit(text, textRect)
        pygame.draw.rect(screen,(0,0,0),[screenWidth - 120,100,15,40]) 
        pygame.draw.rect(screen,(0,0,0),[screenWidth - 100,100,15,40])
        pygame.draw.rect(screen,(0,0,0),[self.posX1RestartButton,self.posY1RestartButton,self.posX2RestartButton - self.posX1RestartButton, self.posY2RestartButton - self.posY1RestartButton])
        pygame.draw.rect(screen,(255, 255, 255),[self.posX1RestartButton + 3,self.posY1RestartButton + 3,self.posX2RestartButton - self.posX1RestartButton - 6, self.posY2RestartButton - self.posY1RestartButton - 6])
        font3 = pygame.font.SysFont("calibri",40)
        textRestart = pygame.font.Font.render(font3, f"Restart", True, (0, 0, 0))
        restartRect = textRestart.get_rect()
        restartRect.center = (screenWidth/2, self.posY1RestartButton + (self.posY2RestartButton - self.posY1RestartButton)/2 +2)
        screen.blit(textRestart, restartRect)

        continueButton = Button(self.posX1RestartButton, screenHeight/2 + 45, 200, 40, "Continue", 40)
        continueButton.draw()
        pygame.display.flip()


        while Done:
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT  or key[pygame.K_ESCAPE]: #used to stop the program when the cross to close the window or escape is pressed
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()  #get the position of the mouse if pressed
                    if mouse_presses[0]:
                        self.mousePressedX, self.mousePressedY = pygame.mouse.get_pos()
            
            if key[pygame.K_RETURN] or (self.posX1RestartButton< self.mousePressedX < self.posX2RestartButton and self.posY1RestartButton < self.mousePressedY < self.posY2RestartButton):                    #restarts the game when "enter" key is pressed
                self.monster, self.walls, self.toPickHeart, self.monsterDeathTime = [], [], [], []
                self.homePage()     #sends player to main menu
                Done = False

            if time.time() - self.timePause > self.commandWaitTime:
                if continueButton.isPressed(self.mousePressedX, self.mousePressedY) or key[pygame.K_p]:
                    Done = False
                    self.timePause = time.time()
                    for entity in self.monster:
                        entity.timeSinceMove = time.time()
                    player.timeSinceMove = time.time()
                    self.mousePressedX, self.mousePressedY = 0, 0
            

    def gameOver(self, player): #define the game-over page when the player doesn't have any health left
        font = pygame.font.SysFont("calibri",70)
        text = pygame.font.Font.render(font, f"Game Over", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (screenWidth/2, screenHeight/2) #used to put the center of the text at the center of the screen
        screen.blit(text, textRect)
        font2 = pygame.font.SysFont("calibri",40)
        score = pygame.font.Font.render(font2, f"Score = " + str(player.playerScore), True, (0, 0, 0))
        scoreRect = score.get_rect()
        scoreRect.center = (screenWidth/2, screenHeight/2 + 65)
        screen.blit(score, scoreRect)
        pygame.draw.rect(screen,(0,0,0),[self.posX1RestartButton,self.posY1RestartButton,self.posX2RestartButton - self.posX1RestartButton, self.posY2RestartButton - self.posY1RestartButton])
        pygame.draw.rect(screen,(255, 255, 255),[self.posX1RestartButton + 3,self.posY1RestartButton + 3,self.posX2RestartButton - self.posX1RestartButton - 6, self.posY2RestartButton - self.posY1RestartButton - 6])
        font3 = pygame.font.SysFont("calibri",40)
        textRestart = pygame.font.Font.render(font3, f"Restart", True, (0, 0, 0))
        restartRect = textRestart.get_rect()
        restartRect.center = (screenWidth/2, self.posY1RestartButton + (self.posY2RestartButton - self.posY1RestartButton)/2 +2)
        screen.blit(textRestart, restartRect)
        return [], [], []


class myApp():
    Game()

App=myApp()