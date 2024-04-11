import pygame 
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from enemy import OpenWEnemy
class Level:
    def __init__(self):
        # display surface 
        self.display_surface = pygame.display.get_surface()
        # sprite groups 
        self.visible_sprite = YOrderCameraGroup()
        self.obstacle_sprite = pygame.sprite.Group()
        
        self.cur_attack = None 
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
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
                    self.player = Player((x,y),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.destroy_attack)
                if column == 'g':
                    OpenWEnemy('garbage',(x,y),[self.visible_sprite,self.attackable_sprites],self.obstacle_sprite,self.dmg_to_player)
                    
    def create_attack(self):
        self.cur_attack = Weapon(self.player,[self.visible_sprite,self.attack_sprites])
        print('attack_done')       

    def destroy_attack(self):
        if self.cur_attack:
            self.cur_attack.kill()
            self.cur_attack = None 
            print('attack_destroyed')
    
    def player_atk_logic(self):
        if self.attack_sprites:
            for attack in self.attack_sprites:
                collied_sprites = pygame.sprite.spritecollide(attack,self.attackable_sprites,False)
                if collied_sprites:
                    for target in collied_sprites:
                        print('hit')
                        target.take_dmg(self.player)
                    
    def dmg_to_player(self,amount,atk_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False 
            self.player.dmg_time = pygame.time.get_ticks()
            print("player health is ",self.player.health)
                  
        
    def run(self):
        # updates and draws the game
        
        self.visible_sprite.draw(self.player)
        self.visible_sprite.update()
        self.visible_sprite.enemy_update(self.player)
        self.player_atk_logic()
        
    

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

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type=='enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
        
        
    
        
