import pygame 
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from enemy import OpenWEnemy
from projectile import Projectile
from debugger import debug
from enemydrop import Loot
from menu import PauseMenu
from util import *
import random 
class Level:
    def __init__(self,savefile):
        # display surface 
        
        self.display_surface = pygame.display.get_surface()
        # sprite groups 
        self.visible_sprite = YOrderCameraGroup()
        self.obstacle_sprite = pygame.sprite.Group()
        self.weapon_sprite = pygame.sprite.Group()
        self.cur_weapon = None 
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
        self.loot_sprites = pygame.sprite.Group()
        
        self.game_paused = False    
        self.savefile = savefile
        # sprite setup 
        self.create_map()
        
        self.pause_menu = PauseMenu(self.player)
    
    def create_map(self):
        layouts = {
			'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_Objects.csv'),
			'entities': import_csv_layout('../map/map_Entities.csv')
		}
        # for row_index,row in enumerate(WORLD_MAP):
        #     print(row_index,row)
        #     for column_index,column in enumerate(row):
        #         x = column_index * TILE_SIZE
        #         y = row_index * TILE_SIZE
        #         if column == 'x':
        #             Tile((x,y),[self.visible_sprite,self.obstacle_sprite])
        #         if column == 'p':
        #             self.player = Player((x,y),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.destroy_attack,self.savefile)
        #         if column == 'g':
        #             OpenWEnemy('garbage',(x,y),[self.visible_sprite,self.attackable_sprites],self.obstacle_sprite,self.loot_sprites,self.visible_sprite,self.dmg_to_player)
        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprite],'invisible')
                        if style == 'grass':
                            random_grass_image = pygame.image.load('../graphics/tree.png').convert_alpha() #random_grass_image = choice(graphics['grass'])
                            random_grass_image = pygame.transform.scale(random_grass_image,(TILE_SIZE,TILE_SIZE))
                            Tile(
                                (x,y),
                                [self.visible_sprite,self.obstacle_sprite],
                                'grass',
                                random_grass_image)

                        if style == 'object':
                            surf = pygame.image.load('../graphics/building.png').convert_alpha()  # surf = graphics['objects'][int(col)]
                            surf = pygame.transform.scale(surf,(TILE_SIZE,TILE_SIZE))
                            Tile((x,y),[self.visible_sprite,self.obstacle_sprite],'object',surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x,y),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.destroy_attack,self,self.savefile)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name ='raccoon'
                                else: monster_name = 'squid'
                                OpenWEnemy(
                                    'garbage',
                                    (x,y),
                                    [self.visible_sprite,self.attackable_sprites],self.obstacle_sprite,self.loot_sprites,self.visible_sprite,self.dmg_to_player)
    def get_player(self):
        return self.player                 
    def create_attack(self):
        
        self.cur_weapon = Weapon(self.player,[self.visible_sprite,self.attack_sprites])
        
        if self.player.player_weapon_attr('weapon_type') == 'ranged':  
            Projectile(self.cur_weapon,[self.visible_sprite,self.attack_sprites],self.attackable_sprites,self.obstacle_sprite)
        
        print('attack_done')       

    def regen_ammo(self):
        if self.player.stats['ammunition'] < self.player.max_stats['ammunition']:
            self.player.stats['ammunition'] += 0.1
            self.player.stats['ammunition'] = min(self.player.stats['ammunition'],self.player.max_stats['ammunition'])
            self.player.stats['ammunition'] = max(self.player.stats['ammunition'],0)
            
            
    def destroy_attack(self):
        if self.cur_weapon:
            self.cur_weapon.kill()
            self.cur_weapon = None 
            print('attack_destroyed')
    
    def player_atk_logic(self):
        if self.attack_sprites:
            for attack in self.attack_sprites:
                collied_sprites = pygame.sprite.spritecollide(attack,self.attackable_sprites,False)
                if collied_sprites:
                    for target in collied_sprites:
                        if self.player.player_weapon_attr('weapon_type') == 'melee':
                            print('hit')
                            target.take_dmg(self.player)
                        else:
                            pass
        if self.loot_sprites:
            for loot in self.loot_sprites:
                if loot.rect.colliderect(self.player.hitbox):
                    self.after_loot(loot)
                    loot.kill()
                    print('loot_taken')
                else:
                    loot.rect.center = loot.center + random.choice([pygame.math.Vector2(0,0),pygame.math.Vector2(0,-2)])
                            
    
    def after_loot(self,loot):
        self.player.stats['health'] += loot.health_regenerate 
        self.player.stats['health'] = min(self.player.stats['health'],self.player.max_stats['health'])
        self.player.stats['eddie'] += loot.eddie
        
        pass  
    def dmg_to_player(self,amount,atk_type):
        if self.player.vulnerable:
            self.player.stats['health'] -= amount
            self.player.vulnerable = False 
            self.player.dmg_time = pygame.time.get_ticks()
            print("player health is ",self.player.stats['health'])
    def toggle_pause(self):
        self.game_paused = not self.game_paused
        pass
    def draw_pause_button(self):
        pause_button_image = pygame.image.load('../graphics/pause_button.png').convert_alpha()
        pause_button_image = pygame.transform.scale(pause_button_image,(TILE_SIZE,TILE_SIZE))
        pause_button_rect = pause_button_image.get_rect()
        pause_button_rect.topleft = (10, 60)
        self.display_surface.blit(pause_button_image, pause_button_rect)
    def draw_eddie_number(self):
        eddie_image = pygame.image.load('../graphics/eddie.png').convert_alpha()
        eddie_image = pygame.transform.scale(eddie_image, (TILE_SIZE, TILE_SIZE))
        eddie_rect = eddie_image.get_rect()
        eddie_rect.topleft = (10, TILE_SIZE*2)
        self.display_surface.blit(eddie_image, eddie_rect)

        font = pygame.font.Font(None, 24)
        eddie_count_text = font.render(str(self.player.stats['eddie']), True, (255, 255, 255))
        eddie_count_rect = eddie_count_text.get_rect()
        eddie_count_rect.topleft = (10 + TILE_SIZE, TILE_SIZE*2+20)
        self.display_surface.blit(eddie_count_text, eddie_count_rect)
        
    def run(self):
        # updates and draws the game
        
        
        
        if self.game_paused:
            self.pause_menu.display()
            
            
            
        else:
            
            self.visible_sprite.draw(self.player)
            # self.weapon_sprite.draw(self.display_surface)
            self.visible_sprite.update()
            self.visible_sprite.enemy_update(self.player)
            self.player_atk_logic()
            self.regen_ammo()
            self.draw_pause_button()
            self.draw_eddie_number()
              
        
        
        # debug(self.player.stats['ammunition'])
    

class YOrderCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(50,50)
        self.floor_surf = pygame.image.load('../graphics/ground_1.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
    
    def draw(self,player):
        sprites = sorted(self.sprites(),key = lambda sprite: sprite.rect.centery)
        self.offset.x = self.half_w - player.rect.centerx
        self.offset.y = self.half_h - player.rect.centery
        
        floor_offset_pos = self.floor_rect.topleft + self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        
        for sprite in sprites: 
            self.display_surface.blit(sprite.image,sprite.rect.topleft + self.offset)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type=='enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
        
        
    
        
