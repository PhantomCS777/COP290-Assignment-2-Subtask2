import pygame 
from settings import * 
from level import Level
from player import Player
from enemy import OpenWEnemy
from tile import Tile



class Level1(Level):
    def __init__(self,level_name,savefile):
        self.reset = False
        self.level_name = level_name
        self.door_to_level2 = pygame.sprite.Group()
        super().__init__(savefile)
        
        
    def update_level(self):
        for sprite in self.door_to_level2:
            if pygame.sprite.collide_rect(self.player,sprite):
                return 'level-2'
        return self.level_name
        
    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            print(row_index,row)
            for column_index,column in enumerate(row):
                x = column_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if column == 'x':
                    img = pygame.image.load('../graphics/tree.png').convert_alpha()
                    img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
                    Tile((x,y),[self.visible_sprite,self.obstacle_sprite],'object',img)
                if column == 'p':
                    self.player = Player((x,y),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.destroy_attack,self,self.savefile)
                if column == 'g':
                    OpenWEnemy('garbage',(x,y),[self.visible_sprite,self.attackable_sprites],self.obstacle_sprite,self.loot_sprites,self.visible_sprite,self.dmg_to_player)
                if column == 'd':
                    img = pygame.image.load('../graphics/door2.png').convert_alpha()
                    img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
                    door = Tile((x,y),[self.visible_sprite,self.obstacle_sprite,self.door_to_level2],'object',img)
                    self.door_to_level2.add(door)
    
  
            


class Level2(Level):
    def __init__(self,level_name,savefile):
        super().__init__(savefile)
        self.level_name = level_name
        self.reset = False
    def update_level(self):
        return self.level_name
