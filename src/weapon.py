import pygame 
from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        direction  = player.open_world_status.split('_')[0]
        
        self.sprtie_type = 'weapon'
        weapon_path = f'../graphics/{player.weapon}.png'
        self.image = pygame.image.load(weapon_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILE_SIZE//2,TILE_SIZE//2))
        self.player = player
        
        
        if direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom)
            self.weapon_tip = 'down'
            print('down')
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop)
            self.weapon_tip = 'up'
            print('up')
        elif direction == 'right':
            self.weapon_tip = 'right'
            print('right')
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        elif direction == 'left':
            self.weapon_tip = 'left'
            print('left')
            self.rect = self.image.get_rect(midright = player.rect.midleft)
        
        
        