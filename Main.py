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
screen = pygame.display.set_mode((screenWidth,screenHeight))
screen.fill([255,255,255])

class Player():
    def __init__(self):
        self.playerPos=((screenWidth//2)*10,(screenHeight//2)*10) # player's parameters
        self.playerHeight = 20
        self.playerWidth = 20
        self.baseSpeed = 5
        self.playerSpeed = 2
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
        self.ultiCoolDown = 2
        self.ultiTime = 0.5
        self.timeSinceUlti = 0
        self.rangeUlti = 75
        self.ultiDamage = 2
        self.timeInvicible = 0.6
        self.timeSinceBit = 0
        self.playerRedRectanglePos = [0, -5]        
        self.s , self.h= self.playerPos


    def move(self):
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

        if key[pygame.K_UP] or key[pygame.K_z]:  #if "z" or "up" keys are pressed, player goes up 
            if self.h > 0 + self.playerSpeed + self.playerHeight//2:
                self.h = self.h- self.playerSpeed
                self.playerRedRectanglePos = [-5, -10]
                self.directionAttack = 3 * math.pi/4
                self.attackSide = "up"

        if key[pygame.K_DOWN] or key[pygame.K_s]:  #if "s" or "down" keys are pressed, player goes down
            if self.h < 10 * (screenHeight - self.playerSpeed - self.playerHeight//2):
                self.h = self.h+ self.playerSpeed
                self.playerRedRectanglePos = [-5, 0]
                self.directionAttack = 7 * math.pi/4
                self.attackSide = "down"

        if key[pygame.K_LEFT] or key[pygame.K_q]:  #if "q" or "left" keys are pressed, player goes left
            if self.s > 0 + self.playerSpeed + self.playerWidth//2:
                self.s = self.s- self.playerSpeed
                self.playerRedRectanglePos = [-10, -5]
                self.directionAttack = 5 * math.pi/4
                self.attackSide = "left"

        if key[pygame.K_RIGHT] or key[pygame.K_d]:  #if "d" or "right" keys are pressed, player goes right
            if self.s < 10 * (screenWidth - self.playerSpeed + self.playerWidth//2):
                self.s = self.s+ self.playerSpeed
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
            xAttack = self.s/10 + (self.rangeAttack) * math.sin(self.directionAttack+((math.pi/2) * ((time.time() - self.timeSinceAttack)/self.attackTime)))
            yAttack = self.h/10 + (self.rangeAttack) * math.cos(self.directionAttack+((math.pi/2) * ((time.time() - self.timeSinceAttack)/self.attackTime)))
            pygame.draw.line(screen, (175, 175, 175), (self.s/10, self.h/10), (xAttack, yAttack))

        if self.playerUlti == True:  #draw ulti
            xUlti = self.s/10 + (self.rangeUlti) * math.sin((math.pi/2) * ((time.time() - self.timeSinceAttack)/(2*self.attackTime)))
            yUlti = self.h/10 + (self.rangeUlti) * math.cos((math.pi/2) * ((time.time() - self.timeSinceAttack)/(2*self.attackTime)))
            pygame.draw.line(screen, (175, 175, 175), (self.s/10, self.h/10), (xUlti, yUlti))

        pygame.draw.rect(screen,(0,0,0),[(self.s/10)-10,(self.h/10)-10,20,20]) #big black rectangle
        pygame.draw.rect(screen,(255,0,0),[(self.s/10) + self.playerRedRectanglePos[0],(self.h/10) + self.playerRedRectanglePos[1],10,10])  #small rectangle on the side
        
        if time.time() - self.timeSinceBit < self.timeInvicible:  # draw a "-1"  if hit
            font = pygame.font.SysFont("calibri",15)
            text = pygame.font.Font.render(font,"-1", True, (0, 0, 255))
            screen.blit(text,((self.s/10), (self.h/10) - 23))
        
        

    def pos(self):  #gives the position of the player
        return self.s, self.h

    def isBittenByMonster(self, monster):
        if math.sqrt((self.s - monster.monsterPos[0])**2 + (self.h - monster.monsterPos[1])**2) < 10 * monster.rangeAttack and time.time() - self.timeSinceBit > self.timeInvicible :
            self.playerHealth -= 1
            self.timeSinceBit = time.time()

class Monster():
    def __init__(self):
        self.monsterPos = ((screenWidth//4)*10,(screenHeight//4)*10)  #monster's parameters
        self.monsterSpeed = 0.6
        self.monsterState = True
        self.monsterHealth = 5
        self.timeInvicible = 0.6
        self.timeSinceHit = 0
        self.damageTaken = 0
        self.rangeAttack = 10
        self.timeToRespawn = 1
        self.vector=[0,0]
        self.s, self.h = self.monsterPos
        self.spawn()

    def draw(self):  #design of the monster
        pygame.draw.rect(screen,(79,105,54),[(self.s/10)-10,(self.h/10)-10,20,20])
        if time.time() - self.timeSinceHit < self.timeInvicible:
            font = pygame.font.SysFont("calibri",15)
            text = pygame.font.Font.render(font,str(self.damageTaken), True, (255,0,0))
            screen.blit(text,((self.s/10), (self.h/10) - 23))

    def move(self, player):
        self.deltax = self.s - player.playerPos[0]
        self.deltay = self.h - player.playerPos[1]
        self.vector[0] = self.deltax / math.sqrt((self.deltax**2) + self.deltay**2)
        self.vector[1] = self.deltay / math.sqrt((self.deltax**2) + self.deltay**2)
        self.s -= self.monsterSpeed * self.vector[0]
        self.h -= self.monsterSpeed * self.vector[1]

    def pos(self):
        return self.s, self.h
    
    def isHitByPlayer(self, player):
        if player.playerAttack == True and math.sqrt((self.s - player.playerPos[0])**2 + (self.h - player.playerPos[1])**2) < 10 * player.rangeAttack and time.time() - self.timeSinceHit > self.timeInvicible:
            
            if player.attackSide == "up" and abs(self.s - player.playerPos[0]) < abs(self.h - player.playerPos[1]) and (self.h - player.playerPos[1]) < 0:
                self.monsterHealth -= player.attackDamage
                self.damageTaken = "-"+str(player.attackDamage)
                self.timeSinceHit = time.time()
            
            if player.attackSide == "down" and abs(self.s - player.playerPos[0]) < abs(self.h - player.playerPos[1]) and (self.h - player.playerPos[1]) > 0:
                self.monsterHealth -= player.attackDamage
                self.damageTaken = "-"+str(player.attackDamage)
                self.timeSinceHit = time.time()
            
            if player.attackSide == "left" and abs(self.s - player.playerPos[0]) > abs(self.h - player.playerPos[1]) and (self.s - player.playerPos[0]) < 0:
                self.monsterHealth -= player.attackDamage
                self.damageTaken = "-"+str(player.attackDamage)
                self.timeSinceHit = time.time()
            
            if player.attackSide == "right" and abs(self.s - player.playerPos[0]) > abs(self.h - player.playerPos[1]) and (self.s - player.playerPos[0]) > 0:
                self.monsterHealth -= player.attackDamage
                self.damageTaken = "-"+str(player.attackDamage)
                self.timeSinceHit = time.time()


        if player.playerUlti == True and math.sqrt((self.s - player.playerPos[0])**2 + (self.h - player.playerPos[1])**2) < 10 * player.rangeUlti and time.time() - self.timeSinceHit > self.timeInvicible:
            self.monsterHealth -= player.ultiDamage
            self.damageTaken = "-"+str(player.ultiDamage)
            self.timeSinceHit = time.time()
    def spawn(self):
        if time.time() - self.timeSinceHit > self.timeToRespawn:
                self.s, self.h = random.randint(0 , screenWidth) *10, random.randint(0 , screenHeight) * 10
                self.monsterHealth = 5




        
        

class Game():
    def __init__(self):
        player = Player()

        monster=[]
        monsterDeathTime=[]
        monster.append(Monster())
        monster.append(Monster())
        monsterTimeToRespawn = 1

        pause = False
        pauseWaitTime = 0.5
        timePause = 0

        walls = []


        while True:
            key = pygame.key.get_pressed() #look at which key is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT  or key[pygame.K_ESCAPE]: #used to stop the program when the cross to close the window or escape is pressed
                    sys.exit()
            if key[pygame.K_p]:
                if time.time() - timePause > pauseWaitTime:
                    pause = not pause
                    timePause = time.time()

            if pause:
                pygame.draw.rect(screen,(0,0,0),[screenWidth - 120,100,15,40])
                pygame.draw.rect(screen,(0,0,0),[screenWidth - 100,100,15,40])
                pygame.display.flip()
            
            else:
                screen.fill([255,255,255])
                for entity in monster:
                    player.isBittenByMonster(entity)
                if player.playerHealth > 0:
                    player.move()
                    player.playerPos = player.pos()
                    player.draw()
                else:
                    time.sleep(0.2)
                    monster, walls = Game.gameOver(player)   #game over returns an empty list
                    if key[pygame.K_RETURN]:
                        player.playerHealth = player.playerMaxHealth
                        player.playerScore = 0
                        monster.append(Monster())
                        monster.append(Monster())

                for entity in monster:
                    entity.isHitByPlayer(player)

                    if entity.monsterHealth > 0:
                        entity.move(player)
                        entity.monsterPos = entity.pos()
                        entity.draw()
                    else:
                        monster.remove(entity)
                        monsterDeathTime.append(time.time())
                        player.playerScore += 1
                
                for entity in walls:
                    entity.draw()
                
                for timeSinceDeath in monsterDeathTime:
                    if time.time() - timeSinceDeath > monsterTimeToRespawn:
                        monster.append(Monster())
                        monster.append(Monster())
                        monsterDeathTime.remove(timeSinceDeath)
                print(len(monsterDeathTime))
                Game.draw(player, len(monster))

                pygame.display.flip()

    def draw(player, nbmonster):
        font = pygame.font.SysFont("calibri",30)
        text = pygame.font.Font.render(font, f"Score = " + str(player.playerScore), True, (0, 0, 0))
        screen.blit(text, (50, 50))
        text = pygame.font.Font.render(font, f"number entities = " + str(nbmonster), True, (0, 0, 0))
        screen.blit(text, (550, 50))

        redHeart = pygame.image.load("coeurPlein.png")
        redHeart = pygame.transform.scale(redHeart, (30, 30))
        blackHeart = pygame.image.load("coeurVide.png")
        blackHeart = pygame.transform.scale(blackHeart, (30, 30))

        for i in range(player.playerMaxHealth//10):
            for j in range((player.playerHealth - 10 *i) if (player.playerHealth - 10 *i)<10 else 10):
                rect = redHeart.get_rect()
                rect = rect.move(1050 + j * 31, 50 + 15*i)
                screen.blit(redHeart, rect)
            for k in range((10 - player.playerHealth - 10 *i) if (player.playerHealth - 10 *i)<10 else 0):
                rect = blackHeart.get_rect()
                rect = rect.move(1050 + player.playerHealth * 31 + k * 31, 50 + 15 * i)
                screen.blit(blackHeart, rect)
    
    def gameOver(player):
        font = pygame.font.SysFont("calibri",70)
        text = pygame.font.Font.render(font, f"Game Over", True, (0, 0, 0))
        screen.blit(text, (540, 315))
        font2 = pygame.font.SysFont("calibri",40)
        text = pygame.font.Font.render(font2, f"Score = " + str(player.playerScore), True, (0, 0, 0))
        screen.blit(text, (615, 395))
        return [], []


class myApp():
    Game()

App=myApp()