import pygame 
from settings import *
from entity import Entity
from util import *

class Player(Entity):
    def __init__(self,position,groups,obstacle_sprite,create_attack,destroy_attack,level,savefile):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect(topleft = position)
        
        # movement
        self.speed = PLAYER_SPEED 
        self.level = level
        
        # self.max_stats  = {'health':100,'ammunition':100,'eddie':1000}
        # self.stats = {'health':100,'ammunition':100,'eddie':1000}
    
        self.savefile = savefile 
        
        # self.stats = self.savefile['player_stats']
        self.update_stats(self.savefile)
        self.obstacle_sprite = obstacle_sprite
        self.hitbox = self.rect.inflate(0,-20)
        
        # status 
        self.open_world_status = 'down'
        
        self.create_attack = create_attack  
        self.destroy_attack = destroy_attack
        self.attacking = False 
        self.attack_cooldown = 10
        self.attack_time = None 
        
        # dmg taken cooldown 
        self.dmg_time = None
        self.vulnerable = True
        self.dmg_cooldown = 300
        
        
        self.weapon_index = 0 
        self.weapon = list(WEAPONS.keys())[self.weapon_index]
        self.weapon_images = {}
        for w in WEAPONS:
            self.weapon_images[w] = pygame.transform.scale(weapon_image(w),(TILE_SIZE,TILE_SIZE))
    def update_stats(self,savefile):
        self.savefile = savefile
        self.stats = self.savefile['player_stats']
        self.max_stats = self.savefile['player_max_stats']
    def draw_health_bar(self):
        
        health_width = max(int((self.stats['health'] / self.max_stats['health']) * TILE_SIZE*4),0)
        display_surface = pygame.display.get_surface()
        health_bar_surface = pygame.Surface((self.max_stats['health'], 5))
        health_bar_surface.fill((255, 0, 0))  
        
        
        remaining_health_surface = pygame.Surface((health_width, 20))
        remaining_health_surface.fill((0, 255, 0))  # Fill the remaining health with green color
        
        
        health_bar_surface.blit(remaining_health_surface, (0, 0))
        
        
        health_bar_position = (10, 10)
        
        # Draw the health bar overlay on the main surface
        display_surface.blit(health_bar_surface, health_bar_position)
    def draw_ammo_bar(self):
        ammo_width = int((self.stats['ammunition'] / self.max_stats['ammunition']) * TILE_SIZE*4)
        display_surface = pygame.display.get_surface()
        ammo_bar_surface = pygame.Surface((self.max_stats['ammunition'], 5))
        ammo_bar_surface.fill((255, 0, 0))  
        
        
        remaining_ammo_surface = pygame.Surface((ammo_width, 20))
        remaining_ammo_surface.fill((0, 255, 0))
        ammo_bar_surface.blit(remaining_ammo_surface, (0, 0))
        ammo_bar_position = (10, 20)
        display_surface.blit(ammo_bar_surface, ammo_bar_position)
        
    def draw_cur_weapon(self):
        display_surface = pygame.display.get_surface()
        
        weapon_img = self.weapon_images[self.weapon]
        weapon_rect = weapon_img.get_rect(bottomleft=(10, display_surface.get_height() - 10))
        pygame.draw.rect(display_surface, (255, 255, 255), weapon_rect, 2)
        display_surface.blit(weapon_img, weapon_rect)
        
    def open_world_input(self):
        keys = pygame.key.get_pressed() 
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1 
            self.open_world_status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.open_world_status = 'down'
        else: 
            self.direction.y = 0
            
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.open_world_status = 'left'
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1 
            self.open_world_status = 'right'
        else:
            self.direction.x = 0
            
        # melee attack inp 
        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and not self.attacking:
            if self.stats['ammunition'] >= self.player_weapon_attr('atk_cost'):
                self.stats['ammunition'] -= self.player_weapon_attr('atk_cost')
                self.attacking = True 
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            
            print('attack initiated')
            
        # gun 
        if keys[pygame.K_e] and not self.attacking:
            self.attacking = True 
            self.attack_time = pygame.time.get_ticks()
            print('gun')
        
        # weapon switch
        for i in range(len(WEAPONS)):
            if keys[getattr(pygame,f'K_{i+1}')]:
                self.weapon_index = i 
                self.weapon = list(WEAPONS.keys())[self.weapon_index]
                print(self.weapon)
            
    def cooldown(self):
        cur_time = pygame.time.get_ticks()  
        
        if self.attacking:
            if (cur_time - self.attack_time) > (self.attack_cooldown + self.player_weapon_attr('cooldown')):
                self.attacking = False
                self.attack_time = None 
                self.destroy_attack()
        if not self.vulnerable:
            if (cur_time - self.dmg_time) > self.dmg_cooldown:
                self.vulnerable = True 
                self.dmg_time = None
                 
        
    def player_weapon_attr(self,attr):
       return self.savefile['player_weapon_stats'][self.weapon][attr]     
     
   
    def player_alive(self):
        return self.stats['health'] > 0        
    def death_scren(self):
        display_surface = pygame.display.get_surface()
        overlay_surface = pygame.Surface(display_surface.get_size(), pygame.SRCALPHA)
        overlay_surface.fill((255, 0, 0, 128))  # Translucent red color
        display_surface.blit(overlay_surface, (0, 0))
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render("YOU DIED", True, (255, 255, 255))
        text_surface2 = font.render("Saving the World is important, however so is your life", True, (255, 255, 255))
        text_surface3 = font.render("Lets Press SPACE to restart !", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2))
        text_rect2 = text_surface2.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2 + 50))
        text_rect3 = text_surface3.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2 + 100))
        display_surface.blit(text_surface, text_rect)
        display_surface.blit(text_surface2, text_rect2)
        display_surface.blit(text_surface3, text_rect3)
       
    
    def update(self):
        if self.player_alive():
            self.open_world_input()
            self.cooldown()
            self.move(self.speed)
            self.draw_health_bar()
            self.draw_ammo_bar()
            self.draw_cur_weapon()
            print(self.stats['health'])
        else:
            self.death_scren()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.level.reset = True
            pass
        
        


