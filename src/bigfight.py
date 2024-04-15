import pygame 
import sys
from settings import * 
from fighter import Fighter


        
class Ground(pygame.sprite.Sprite):
    def __init__(self,position,groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/ground.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(WIDTH,HEIGTH))
        self.rect = self.image.get_rect(topleft = position)
        
class BigFight:
    def __init__(self):
        self.display_surface = pygame.display.get_surface() 
        self.visible_sprites = pygame.sprite.Group()
        self.back_ground = pygame.image.load('../graphics/background.png').convert_alpha()
        self.back_ground = pygame.transform.scale(self.back_ground,(WIDTH,HEIGTH-HEIGTH//8))
        self.bg_rect = self.back_ground.get_rect(topleft = (0,0))
        self.ground = Ground((0,HEIGTH-HEIGTH),self.visible_sprites)
        self.Fighter1 = Fighter((100,100),self.visible_sprites)
        self.Fighter2 = Fighter((600,100),self.visible_sprites)
        

    def gravity(self):
        if self.Fighter1.rect.y < HEIGTH-HEIGTH//8 - self.Fighter1.rect.height:
                self.Fighter1.gravity += 0.2
                self.Fighter1.rect.y += self.Fighter1.gravity
        else:
            self.Fighter1.rect.y = HEIGTH-HEIGTH//8 - self.Fighter1.rect.height
            self.Fighter1.gravity = 0
            
        if self.Fighter2.rect.y < HEIGTH-HEIGTH//8 - self.Fighter2.rect.height:
                self.Fighter2.gravity += 0.2
                self.Fighter2.rect.y += self.Fighter2.gravity
        else:
            self.Fighter2.rect.y = HEIGTH-HEIGTH//8 - self.Fighter2.rect.height    
            self.Fighter2.gravity = 0
   
   
    
    def run(self):
        self.display_surface.blit(self.back_ground,self.bg_rect)
        self.visible_sprites.draw(self.display_surface)
        self.gravity()
        self.Fighter1.move()
        
        