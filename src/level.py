import pygame 
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        # display surface 
        self.display_surface = pygame.display.get_surface()
        # sprite groups 
        self.visible_sprite = YOrderCameraGroup()
        self.obstacle_sprite = pygame.sprite.Group()
        
        # sprite setup 
        self.create_map()
    
    
    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            print(row_index,row)
            for column_index,column in enumerate(row):
                x = column_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if column == 'x':
                    Tile((x,y),[self.visible_sprite,self.obstacle_sprite])
                if column == 'p':
                    self.player = Player((x,y),[self.visible_sprite],self.obstacle_sprite)
                    
                    
                
    def run(self):
        # updates and draws the game
        
        self.visible_sprite.draw(self.player)
        self.visible_sprite.update()
        
    

class YOrderCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(50,50)
    
    def draw(self,player):
        sprites = sorted(self.sprites(),key = lambda sprite: sprite.rect.centery)
        self.offset.x = self.half_w - player.rect.centerx
        self.offset.y = self.half_h - player.rect.centery
        for sprite in sprites: 
            self.display_surface.blit(sprite.image,sprite.rect.topleft + self.offset)
     
    
        
