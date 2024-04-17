import pygame 
from settings import *



class Loot(pygame.sprite.Sprite):
    def __init__(self,enemy,groups):
        super().__init__(groups)
        self.center = enemy.hitbox.center
        self.image = pygame.image.load('../graphics/eddie.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect(center = enemy.hitbox.center)
        self.hitbox = self.rect.inflate(-10,-10)
        
        self.sprite_type = 'loot'
        
        self.health_regenerate = None
        self.eddie = None 
        self.loot_update(enemy)
    
    def loot_update(self,enemy):
        level = enemy.level
        
        if level > 0:
            self.health_regenerate = int(10 * (level/(level+1)))
            self.eddie = 100 *level 
        
        else:
            level = abs(level)
            self.health_regenerate = int(20*(level/(level+1)))
            self.eddie = 1000*level
        
        
        
        
    