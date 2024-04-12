import pygame 
from settings import * 
from entity import Entity
from debugger import debug
from enemydrop import Loot
import math
import random 

class OpenWEnemy(Entity):
    def __init__(self,enemy_name,position,groups,obstacle_sprites,loot_sprites,visible_sprite,dmg_to_player):
        super().__init__(groups)
        self.sprite_type = 'enemy' 
        
        self.import_graphics(enemy_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = position)
        self.dmg_to_player = dmg_to_player
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprite = obstacle_sprites
        self.loot_sprites = loot_sprites
        self.visible_sprite = visible_sprite
        # enemy stats 
 
        self.enemy_name=  enemy_name
        enemy_data = ENEMY_BASE[self.enemy_name]
        self.health = enemy_data['health']
        
        self.dmg = enemy_data['dmg']
        self.level = enemy_data['level']
        self.atk_type = enemy_data['atk_type']
        self.atk_sound = enemy_data['atk_sound']
        self.atk_radius = enemy_data['atk_radius']
        self.notice_radius = enemy_data['notice_radius']
        self.speed = enemy_data['speed']
        self.pushback_res = enemy_data['pushback_res']
        self.drop_rate = enemy_data['drop_rate']
        # player interaction 
        self.can_attack = True
        self.atk_time = None 
        self.cooldown = 400
        
        # dmg not taken timer 
        self.dmg_time = None
        self.vulnerable = True
        self.dmg_cooldown = 300
        
        self.initial_delay = 50
        
        
    def import_graphics(self,name):
        self.animations = {'idle':[],'move':[],'atk':[]}
        path = f'../graphics/{name+".png"}'
        for animation in self.animations.keys():
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
            self.animations[animation].append(img)
    
    def get_player_dist_dir(self,player):
        enemy_loc = pygame.math.Vector2(self.rect.center)
        player_loc = pygame.math.Vector2(player.rect.center)
        distance = (player_loc - enemy_loc).magnitude()
        
        if distance > 0:
            direction = (player_loc - enemy_loc).normalize()
        else:
            direction = pygame.math.Vector2(0,0)
        
        return (distance,direction)
    
    def actions(self,player):
        if self.status == 'atk':
            pass
        elif self.status == 'move':
            self.direction = self.get_player_dist_dir(player)[1]
        elif self.status == 'idle':
            self.direction = pygame.math.Vector2()
        
    def get_status(self,player):
        distance = self.get_player_dist_dir(player)[0]
        
        if distance <= self.atk_radius and self.can_attack:
            self.status = 'atk'
            self.dmg_to_player(self.dmg,self.atk_type)
            self.atk_time = pygame.time.get_ticks()
            
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += 0.1
        if self.frame_index >= len(animation):
            if self.status == 'atk':
                self.can_attack = False
                
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        if not self.vulnerable:
            
            ttaken = pygame.time.get_ticks()
            alpha = (lambda x: 255 if math.sin(x) > 0 else 0)(ttaken)
            
            self.image.set_alpha(alpha)
        else:
            alpha = 255
            self.image.set_alpha(alpha)
        
    def atk_cooldown(self):
        if not self.can_attack:
            if pygame.time.get_ticks() - self.atk_time >= self.cooldown:
                self.can_attack = True
                self.atk_time = None 
    
    def take_dmg(self,player):
        if self.vulnerable:
            self.direction = self.get_player_dist_dir(player)[1]    
            self.health -= player.player_weapon_attr('dmg')
            print(self.health)
            print(self.health)
            self.dmg_time = pygame.time.get_ticks()
            self.vulnerable = False
        
    def take_dmg_cooldown(self):
        if not self.vulnerable:
            if pygame.time.get_ticks() - self.dmg_time >= self.dmg_cooldown:
                self.vulnerable = True
                self.dmg_time = None
                
    def death(self):
       
        if self.health <= 0:
            
            print('dead')
            if self.drop_loot():
                Loot(self,[self.visible_sprite,self.loot_sprites])
            
            self.kill()
    
    def drop_loot(self):
        chance = random.random()
        print(self.drop_rate,chance)
        if chance <= self.drop_rate:
            return True
        else:
            return False
        
    def poise(self):
        if not self.vulnerable:
            self.direction *= -self.pushback_res
    def update(self):
        self.poise()
        self.move(self.speed)
        self.animate()
        self.atk_cooldown() 
        self.take_dmg_cooldown()
    
        self.death()
        
     
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
        
        