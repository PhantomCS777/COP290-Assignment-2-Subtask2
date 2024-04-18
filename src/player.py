import pygame 
from settings import *
from entity import Entity
from util import *
import math
class Player(Entity):
    def __init__(self,position,groups,obstacle_sprite,create_attack,destroy_attack,level,savefile):
        super().__init__(groups)
        
        self.sheet = Spritesheet('../graphics/player/player.png',"player")
        self.sheet_idle = Spritesheet('../graphics/player/player_idle.png',"player_idle")
        self.frame_index = 0
        self.animation_speed = 0.1
        self.animations = {
            'down_attack':[self.sheet.parse_sprite(f'frame_down_{i}') for i in range(4)],
            'left_attack':[self.sheet.parse_sprite(f'frame_left_{i}') for i in range(4)],
            'right_attack':[self.sheet.parse_sprite(f'frame_right_{i}') for i in range(4)],
            'up_attack':[self.sheet.parse_sprite(f'frame_up_{i}') for i in range(4)],
            'down' : [self.sheet_idle.parse_sprite(f'frame_down_{i}') for i in range(4)],
            'left' : [self.sheet_idle.parse_sprite(f'frame_left_{i}') for i in range(4)],
            'right' : [self.sheet_idle.parse_sprite(f'frame_right_{i}') for i in range(4)],
            'up' : [self.sheet_idle.parse_sprite(f'frame_up_{i}') for i in range(4)],
            'down_idle' : [self.sheet_idle.parse_sprite(f'frame_down_{0}') for i in range(4)],
            'left_idle' : [self.sheet_idle.parse_sprite(f'frame_left_{0}') for i in range(4)],
            'right_idle' : [self.sheet_idle.parse_sprite(f'frame_right_{0}') for i in range(4)],
            'up_idle' : [self.sheet_idle.parse_sprite(f'frame_up_{0}') for i in range(4)],
            
            }
        # self.animations = {k:[pygame.transform.scale(i,(1.5*TILE_SIZE,1.5*TILE_SIZE)) for i in v] for k,v in self.animations.items()}
        self.frames_down = [self.sheet.parse_sprite(f'frame_down_{i}') for i in range(4)]
        self.frame_left = [self.sheet.parse_sprite(f'frame_left_{i}') for i in range(4)]
        self.frame_right = [self.sheet.parse_sprite(f'frame_right_{i}') for i in range(4)]
        self.frame_up = [self.sheet.parse_sprite(f'frame_up_{i}') for i in range(4)]
        self.image = self.animations['down_idle'][0]
        # self.image = pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect(topleft = position)
        
        # movement
        self.speed = PLAYER_SPEED 
        self.level = level
        
        # self.max_stats  = {'health':100,'ammunition':100,'eddie':1000}
        # self.stats = {'health':100,'ammunition':100,'eddie':1000}
    
        self.savefile = savefile 
        
        # self.stats = self.savefile['player_stats']
        
        self.obstacle_sprite = obstacle_sprite
        self.hitbox = self.rect.inflate(-10,-20)
        self.orig_hitbox = self.hitbox.copy()
        
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
        # self.weapon = self.savefile['player_current_weapon'][str(self.weapon_index+1)]
        self.update_stats(self.savefile)
        self.weapon_images = {}
        for w in self.savefile['player_weapon_stats'].keys():
            self.weapon_images[w] = pygame.transform.scale(weapon_image(w),(TILE_SIZE,TILE_SIZE))
    def update_stats(self,savefile):
        self.savefile = savefile
        self.stats = self.savefile['player_stats']
        self.max_stats = self.savefile['player_max_stats']
        self.weapon = self.savefile['player_current_weapon'][str(self.weapon_index+1)]
        
    def get_open_world_status(self):
        
        if self.direction.x == 0 and self.direction.y ==0 : 
            if not 'idle' in self.open_world_status and not 'attack' in self.open_world_status:
                self.open_world_status = self.open_world_status + '_idle'
        if self.attacking:
            self.direction.x = 0 
            self.direction.y = 0 
            if not 'attack' in self.open_world_status:
                if 'idle' in self.open_world_status:
                    self.open_world_status = self.open_world_status.replace('idle','attack')
                else:
                    self.open_world_status = self.open_world_status + '_attack' 
        else:
            if 'attack' in self.open_world_status:
                self.open_world_status = self.open_world_status.replace('_attack','')
                
    def animate(self):
        animation = self.animations[self.open_world_status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        if self.direction.x ==0 and self.direction.y == 0: self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        # self.image = pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))
        # print(self.vulnerable)
        if not self.vulnerable:
            
            ttaken = pygame.time.get_ticks()
            alpha = (lambda x: 255 if math.sin(x) > 0 else 0)(ttaken)
            
            self.image.set_alpha(alpha)
        else:
            alpha = 255
            self.image.set_alpha(alpha)
        self.rect = self.image.get_rect(center = self.hitbox.center)
          
        
    def draw_health_bar(self):
        
        health_width = max(int((self.stats['health'])),0)
        display_surface = pygame.display.get_surface()
        health_bar_surface = pygame.Surface((self.max_stats['health'], 19))
        health_bar_surface.fill((255, 0, 0))  
        
         
        health_bar_surface.set_colorkey((0, 0, 0))  # Set black color as transparent
        
        # Add border to health bar
        border_rect = pygame.Rect(0, 0, self.max_stats['health'], 20)
        pygame.draw.rect(health_bar_surface, (255, 255, 255), border_rect, 2)
        
        
        
        remaining_health_surface = pygame.Surface((health_width, 17))
        remaining_health_surface.fill((0, 255, 0)) 
        
        
        health_bar_surface.blit(remaining_health_surface, (1, 1))
        
        
        health_bar_position = (10, 10)
        
      
        display_surface.blit(health_bar_surface, health_bar_position)
    
        
    def draw_ammo_bar(self):
        ammo_width = max(int((self.stats['ammunition'])),0)
        display_surface = pygame.display.get_surface()
        ammo_bar_surface = pygame.Surface((self.max_stats['ammunition'], 19))
        ammo_bar_surface.fill((255, 0, 0))  
        ammo_bar_surface.set_colorkey((0,0,0))
        
        border_rect = pygame.Rect(0, 0, self.max_stats['ammunition'], 20)
        pygame.draw.rect(ammo_bar_surface, (255, 255, 255), border_rect, 2)
        
        remaining_ammo_surface = pygame.Surface((ammo_width, 17))
        remaining_ammo_surface.fill((0, 0, 255))
        ammo_bar_surface.blit(remaining_ammo_surface, (1,1))
        ammo_bar_position = (10, 40)
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
        
        # or pygame.mouse.get_pressed()[0]
        # melee attack inp 
        if (keys[pygame.K_SPACE] ) and not self.attacking:
            print(self.player_weapon_attr('atk_cost'))
            if self.stats['ammunition'] >= self.player_weapon_attr('atk_cost'):
                self.stats['ammunition'] -= self.player_weapon_attr('atk_cost')
                self.attacking = True 
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()    
        
        # weapon switch
        for i in range(len(WEAPONS)):
            if keys[getattr(pygame,f'K_{i+1}')]:
                self.weapon_index = i 
        self.weapon = self.savefile['player_current_weapon'][str(self.weapon_index+1)]
                
            
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
    def death_screen(self):
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
            self.get_open_world_status()
            self.cooldown()
            self.move(self.speed)
            self.draw_health_bar()
            self.draw_ammo_bar()
            # self.draw_eddie_number()
            self.draw_cur_weapon()
            
            self.animate()
            
        else:
            # self.death_scren()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.level.reset = True
            pass
        
        


