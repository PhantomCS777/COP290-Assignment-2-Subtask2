import pygame 
from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        direction  = player.open_world_status.split('_')[0]
        self.weapon_name = player.weapon
        self.sprtie_type = 'weapon'
        
        self.player = player
        
        
        if direction == 'down':
            self.get_img('down')
            self.rect = self.image.get_rect(midtop = player.hitbox.center+pygame.math.Vector2(0,0))
            
            self.weapon_tip = 'down'
            print('down')
            # self.player.hitbox = self.rect.inflate(0,20)
            
        elif direction == 'up':
            self.get_img('up')
            self.rect = self.image.get_rect(midbottom= player.hitbox.center + pygame.math.Vector2(0,-4))
            self.weapon_tip = 'up'
            print('up')
            # self.player.hitbox = self.rect.inflate(0,20)
            
        elif direction == 'right':
            self.get_img('right')
            self.weapon_tip = 'right'
            print('right')
            self.rect = self.image.get_rect(midleft = player.hitbox.center +pygame.math.Vector2(0,8))
            # self.player.hitbox = self.rect.inflate(20,0)
        elif direction == 'left':
            self.get_img('left')
            self.weapon_tip = 'left'
            print('left')
            self.rect = self.image.get_rect(midright = player.hitbox.center - pygame.math.Vector2(2,-8))
            # self.player.hitbox = self.rect.inflate(20,0)
        
        
        
    def get_img(self,dir):
        w_path_name = self.weapon_name + '_' + dir + '.png'
        
        weapon_path = f'../graphics/weapons/{w_path_name}'
        self.image = pygame.image.load(weapon_path).convert_alpha()
        # self.image = pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))
    