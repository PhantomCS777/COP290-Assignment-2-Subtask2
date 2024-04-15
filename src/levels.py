import pygame 
from settings import * 
from level import Level
from player import Player
from enemy import OpenWEnemy
from tile import Tile



class Level1(Level):
    
        
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
                    self.player = Player((x,y),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.destroy_attack,self.savefile)
                if column == 'g':
                    OpenWEnemy('garbage',(x,y),[self.visible_sprite,self.attackable_sprites],self.obstacle_sprite,self.loot_sprites,self.visible_sprite,self.dmg_to_player)
        