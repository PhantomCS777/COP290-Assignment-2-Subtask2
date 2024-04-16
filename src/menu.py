import pygame 
from settings import *
import random
import sys
import math

class PauseMenu():
    def __init__(self,player):
        
        self.display_surface = pygame.display.get_surface()
        self.player = player 
        
    def display(self):
        self.display_surface.fill('Red')
        

class UpgradeMenu:
    def __init__(self,player):
        
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.upgrade_check = False
        self.u_check = False 

        self.current_max_health = self.player.savefile['player_max_stats']['health']
        self.current_max_ammunition = self.player.savefile['player_max_stats']['ammunition']
        self.current_eddie = self.player.stats['eddie']
        self.current_weapon = self.player.weapon
        self.max_allowed_health = 200 
        self.max_allowed_ammunition = 200
        self.added_health = 0 
        self.lost_eddie = 0 
        self.added_ammo = 0
        
        self.current_option = 0 
        width = self.display_surface.get_width()
        height = self.display_surface.get_height()
        self.width = width
        self.height = height
        self.op1pos = (width//2, 2*height//16)
        self.op2pos = (width//2, 6*height//16)
        self.op3pos = (width//2, 10*height//16)
        self.op4pos = (width//2, 14*height//16)
        self.option1 = pygame.Rect(self.display_surface.get_width()//2, self.display_surface.get_height()//16, self.display_surface.get_width()//2, 100)
        
        self.option2 = pygame.Rect(self.display_surface.get_width()//2, 4*self.display_surface.get_height()//16,  self.display_surface.get_width()//2, 100)
        self.option3 = pygame.Rect(self.display_surface.get_width()//2, 8*self.display_surface.get_height()/16,  self.display_surface.get_width()//2, 100)
        self.option4 = pygame.Rect(self.display_surface.get_width()//2, 12*self.display_surface.get_height()//16,  self.display_surface.get_width()//2, 100)
        self.option1.center = self.op1pos
        self.option2.center = self.op2pos
        self.option3.center = self.op3pos
        self.option4.center = self.op4pos
        self.highlight = None
    def count_upgrade(self):
        rem_eddie = self.current_eddie - self.lost_eddie
        if rem_eddie == 0:
            return
        if self.current_option == 0:
            self.lost_eddie += 100
            if self.current_eddie-self.lost_eddie >=0:
                self.added_health += 10
            else:
                self.lost_eddie -= 100
            
        elif self.current_option == 1:
            self.lost_eddie += 100
            if self.current_eddie-self.lost_eddie >=0:
                self.added_ammo += 10
            else:
                self.lost_eddie -= 100
                
        elif self.current_option == 2:
            pass
        elif self.current_option == 3:
            pass
    def reverse_upgrade(self):
        
        if self.current_option == 0:
            self.lost_eddie -= 100
            self.added_health -= 10
        elif self.current_option == 1:
            self.lost_eddie -= 100
            self.added_ammo -= 10
        elif self.current_option == 2:
            pass
        elif self.current_option == 3:
            pass
        
        self.lost_eddie = max(0,self.lost_eddie)
        self.added_health = max(0,self.added_health)
        self.current_max_ammunition = max(0,self.current_max_ammunition)
        self.added_ammo = max(0,self.added_ammo)
        
    def draw(self):
        surf = pygame.display.get_surface()
        
        # Calculate the width of the health bar based on the current health and maximum health
        health_percentage = (self.current_max_health + self.added_health) / self.max_allowed_health
        health_bar_width = int(200 * health_percentage)
        # Create a health bar surface with the calculated width
        health_bar = pygame.Surface((health_bar_width, 50))
        health_bar.fill('Blue')
        health_rect = health_bar.get_rect()
        health_rect.midleft = self.option1.midleft + pygame.math.Vector2(10, 0)
        
        ammunition_percentage = (self.current_max_ammunition + self.added_ammo) / self.max_allowed_ammunition
        ammunition_width = int(200 * ammunition_percentage)
        ammunition_bar = pygame.Surface((ammunition_width, 50))
        ammunition_bar.fill('Blue')
        ammunition_rect = ammunition_bar.get_rect()
        ammunition_rect.midleft = self.option2.midleft + pygame.math.Vector2(10, 0)
        
        pygame.draw.rect(self.display_surface, 'White', self.option1)
        pygame.draw.rect(self.display_surface, 'Blue', health_rect)
        
        pygame.draw.rect(self.display_surface, 'White', self.option2)
        pygame.draw.rect(self.display_surface, 'Blue', ammunition_rect)
        
        pygame.draw.rect(self.display_surface, 'White', self.option3)
        pygame.draw.rect(self.display_surface, 'White', self.option4)
        
        
        if self.current_option == 0:
            self.highlight = pygame.Rect(self.op1pos[0],self.op1pos[1],self.width//2+60,120)
            self.highlight.center = self.option1.center
            pygame.draw.rect(self.display_surface, 'Yellow', self.highlight)
            pygame.draw.rect(self.display_surface, 'White', self.option1)
            pygame.draw.rect(self.display_surface,'Blue',health_rect)
            
        elif self.current_option == 1:
            self.highlight = pygame.Rect(self.op2pos[0],self.op2pos[1],self.width//2+60,120)
            self.highlight.center = self.option2.center
            pygame.draw.rect(self.display_surface, 'Yellow', self.highlight)
            pygame.draw.rect(self.display_surface, 'White', self.option2)
            pygame.draw.rect(self.display_surface,'Blue',ammunition_rect)
            
        elif self.current_option == 2:
            self.highlight = pygame.Rect(self.op3pos[0],self.op3pos[1], self.width//2+60,120)
            self.highlight.center = self.option3.center
            pygame.draw.rect(self.display_surface, 'Yellow', self.highlight)
            pygame.draw.rect(self.display_surface, 'White', self.option3)
        elif self.current_option == 3:
            self.highlight = pygame.Rect(self.op4pos[0],self.op4pos[1], self.width//2+60,120)
            self.highlight.center = self.option4.center
            pygame.draw.rect(self.display_surface, 'Yellow', self.highlight)
            pygame.draw.rect(self.display_surface, 'White', self.option4)
    def display_current_eddie(self):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Current Eddie: {self.current_eddie-self.lost_eddie}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(7*self.display_surface.get_width() // 8, self.display_surface.get_height() // 16))
        self.display_surface.blit(text_surface, text_rect)
        
    def upgrade_menu(self):
       
                    
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_u] and not self.u_check:
            self.upgrade_check = not self.upgrade_check
            self.u_check = True
    
        if not keys[pygame.K_u]:
            self.u_check = False
        if self.upgrade_check:    
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                        self.upgrade_check = not self.upgrade_check
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        self.current_option += 1
                        self.current_option = min(3,self.current_option)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        self.current_option -= 1
                        self.current_option = max(0,self.current_option)
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                       self.count_upgrade()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        self.reverse_upgrade()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.current_max_health += self.added_health
                        self.current_max_ammunition += self.added_ammo
                        self.current_eddie -= self.lost_eddie
                        self.added_health = 0
                        self.added_ammo = 0
                        self.lost_eddie = 0
                        
                        self.player.max_stats['health'] = self.current_max_health
                        self.player.max_stats['ammunition'] = self.current_max_ammunition
                        self.player.stats['eddie'] = self.current_eddie
                        
                        return
            
                    display_surface = pygame.display.get_surface()
                    display_surface.fill('Green')
                    self.draw()
                    self.display_current_eddie()
                    
                
                pygame.display.update()