import pygame 
import sys 
from settings import * 


        
class Fighter(pygame.sprite.Sprite):
    def __init__(self,position,groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(HEIGTH//4,HEIGTH//4))
        self.rect = self.image.get_rect(topleft = position)
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 4
        self.gravity = 0 
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.gravity == 0:
                self.gravity = -10
                self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
            
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > HEIGTH - self.rect.height:
            self.rect.y = HEIGTH - self.rect.height



            

    
    