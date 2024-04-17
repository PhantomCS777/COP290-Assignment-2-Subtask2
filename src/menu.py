import pygame 
from settings import *
import random
import sys
from util import weapon_image
import math

class PauseMenu():
    def __init__(self,player):
        
        self.display_surface = pygame.display.get_surface()
        self.player = player 
        self.menu_bg = pygame.image.load('../graphics/pause_menu.png').convert_alpha() 
        self.menu_bg = pygame.transform.scale(self.menu_bg,(self.display_surface.get_width(),self.display_surface.get_height())) 
        
    def display(self):
        self.display_surface.blit(self.menu_bg,(0,0))
        

class UpgradeMenu:
    def __init__(self,player):
        
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.upgrade_check = False
        self.u_check = False 
        self.menuimg = pygame.image.load('../graphics/upgrade_menu.png').convert_alpha()
        self.menuimg = pygame.transform.scale(self.menuimg,(self.display_surface.get_width(),self.display_surface.get_height()))
        
        # limit to upgrades 
        self.max_allowed_health = 200 
        self.max_allowed_ammunition = 200
        self.max_gun_lvl = 2
        self.max_glove_lvl = 2
        
        # current max stats 
        self.initialize()
        
        
        # track user input 
        self.added_health = 0 
        self.lost_eddie = 0 
        self.added_ammo = 0
        self.new_glove = self.current_glove
        self.new_gun = self.current_gun
        self.current_option = 0 
        
        # UI elements 
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
    def initialize(self):
        self.current_max_health = self.player.savefile['player_max_stats']['health']
        self.current_max_ammunition = self.player.savefile['player_max_stats']['ammunition']
        self.current_eddie = self.player.stats['eddie']
        self.current_weapon = self.player.weapon
        
        self.current_glove = self.player.savefile['player_current_weapon']['1']
        self.cur_glove_lvl = self.player.savefile['player_weapon_stats'][self.current_glove]['weapon_level']
        self.current_gun = self.player.savefile['player_current_weapon']['2']
        self.cur_gun_lvl = self.player.savefile['player_weapon_stats'][self.current_gun]['weapon_level']
        self.current_glove = self.player.savefile['player_current_weapon']['1']
        self.cur_glove_lvl = self.player.savefile['player_weapon_stats'][self.current_glove]['weapon_level']
        self.current_gun = self.player.savefile['player_current_weapon']['2']
        self.cur_gun_lvl = self.player.savefile['player_weapon_stats'][self.current_gun]['weapon_level']
        
        self.check_max_glove = True
        self.check_max_gun = True
        
        self.nxt_glove = None 
        self.nxt_gun = None 
        self.orig_glove_lvl = self.cur_glove_lvl
        self.orig_gun_lvl = self.cur_gun_lvl
        
        if self.cur_glove_lvl < self.max_glove_lvl:
            self.check_max_glove = False
            self.nxt_glove = self.current_glove.removesuffix(str(self.cur_glove_lvl)) + str(self.cur_glove_lvl+1)
        else:
            self.nxt_glove = self.current_glove
        if self.cur_gun_lvl < self.max_gun_lvl:
            self.check_max_gun = False
            self.nxt_gun = self.current_gun.removesuffix(str(self.cur_gun_lvl)) + str(self.cur_gun_lvl+1)
        else:
            self.nxt_gun = self.current_gun
        
        self.glove_cost = self.player.savefile['player_weapon_stats'][self.nxt_glove]['cost']
        self.gun_cost = self.player.savefile['player_weapon_stats'][self.nxt_gun]['cost']
         
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
            self.lost_eddie += self.glove_cost
            if (self.current_eddie-self.lost_eddie >=0) and not self.check_max_glove:
                self.new_glove = self.nxt_glove
                self.cur_glove_lvl += 1
                if self.cur_glove_lvl == self.max_glove_lvl:
                    self.check_max_glove = True
            else:
                self.lost_eddie -= self.glove_cost
        elif self.current_option == 3:
            self.lost_eddie += self.gun_cost
            if (self.current_eddie-self.lost_eddie >=0) and not self.check_max_gun:
                self.new_gun = self.nxt_gun
                self.cur_gun_lvl += 1
                if self.cur_gun_lvl == self.max_gun_lvl:
                    self.check_max_gun = True
            else:
                self.lost_eddie -= self.gun_cost
        
    def reverse_upgrade(self):
        
        if self.current_option == 0:
            self.lost_eddie -= 100
            self.added_health -= 10
        elif self.current_option == 1:
            self.lost_eddie -= 100
            self.added_ammo -= 10
            
        elif self.current_option == 2:
            if self.cur_glove_lvl == self.max_glove_lvl:
                self.check_max_glove = False
            self.cur_glove_lvl -= 1
            self.lost_eddie -= self.glove_cost
            self.new_glove = self.current_glove
        elif self.current_option == 3:
            if self.cur_gun_lvl == self.max_gun_lvl:
                self.check_max_gun = False
            self.cur_gun_lvl -= 1
            self.lost_eddie -= self.gun_cost
            self.new_gun = self.current_gun
        
        self.lost_eddie = max(0,self.lost_eddie)
        self.added_health = max(0,self.added_health)
        self.current_max_ammunition = max(0,self.current_max_ammunition)
        self.added_ammo = max(0,self.added_ammo)
        self.cur_glove_lvl = max(self.orig_glove_lvl,self.cur_glove_lvl)
        self.cur_gun_lvl = max(self.orig_gun_lvl,self.cur_gun_lvl)
    def draw_text(self):
        font = pygame.font.Font(None, 36)
        mhealth = font.render("Max Hp (cost 100)", True, (0,0,0))
        mammo = font.render("Max Ammo (cost 100)", True, (0,0,0))
        mglove = font.render("Upgrade Glove", True, (0,0,0))
        mgun = font.render("Upgrade Gun", True, (0,0,0))
        mhealth_rect = mhealth.get_rect(midright=self.option1.midleft-pygame.math.Vector2(40,0))
        mammo_rect = mammo.get_rect(midright=self.option2.midleft - pygame.math.Vector2(40,0))
        mglove_rect = mglove.get_rect(midright=self.option3.midleft - pygame.math.Vector2(40,0))
        mgun_rect = mgun.get_rect(midright=self.option4.midleft - pygame.math.Vector2(40,0))
        self.display_surface.blit(mhealth, mhealth_rect)
        self.display_surface.blit(mammo, mammo_rect)
        self.display_surface.blit(mglove, mglove_rect)
        self.display_surface.blit(mgun, mgun_rect)
        
        esc = font.render("Press: U to exit", True, (0,0,0))
        esc_rect = esc.get_rect(midleft = self.option1.midright + pygame.math.Vector2(40,40))
        self.display_surface.blit(esc, esc_rect)
        
        spc = font.render("Press Space to upgrade", True, (0,0,0))
        spc_rect = spc.get_rect(midleft = self.option1.midright + pygame.math.Vector2(40,100))
        self.display_surface.blit(spc, spc_rect)
        
        bck = font.render("Backspace to", True, (0,0,0))
        bck2 = font.render("reverse upgrade", True, (0,0,0))
        bck_rect = bck.get_rect(midleft = self.option1.midright + pygame.math.Vector2(40,160))
        bck2_rect = bck2.get_rect(midleft = self.option1.midright + pygame.math.Vector2(40,200))
        self.display_surface.blit(bck, bck_rect)
        self.display_surface.blit(bck2, bck2_rect)
        
        ent = font.render("Press Enter to confirm ", True, (0,0,0))
        ent_rect = ent.get_rect(midleft = self.option1.midright + pygame.math.Vector2(40,260))
        self.display_surface.blit(ent, ent_rect)
        
        arrow = font.render("Use up and down keys", True, (0,0,0))
        arrow2 = font.render("to navigate", True, (0,0,0))
        arrow_rect = arrow.get_rect(midleft = self.option1.midright + pygame.math.Vector2(40,320))
        arrow2_rect = arrow2.get_rect(midleft = self.option1.midright + pygame.math.Vector2(40,360))
        self.display_surface.blit(arrow, arrow_rect)
        self.display_surface.blit(arrow2, arrow2_rect)
         
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
        
        orig_glove = weapon_image(self.current_glove)
        orig_glove = pygame.transform.scale(orig_glove,(TILE_SIZE,TILE_SIZE))
        orig_gun = weapon_image(self.current_gun)
        orig_gun = pygame.transform.scale(orig_gun,(TILE_SIZE,TILE_SIZE))
        
        nxt_glove = weapon_image(self.nxt_glove)
        nxt_glove = pygame.transform.scale(nxt_glove,(TILE_SIZE,TILE_SIZE))
        nxt_gun = weapon_image(self.nxt_gun)
        nxt_gun = pygame.transform.scale(nxt_gun,(TILE_SIZE,TILE_SIZE)) 
        
        font = pygame.font.Font(None, 36)
        text_surface_max = font.render("Max", True, (255, 0, 0))
        text_surface_max2 = font.render("Max", True, (255, 0, 0))
        text_surface_mrect = text_surface_max.get_rect(center=self.option3.center)
        text_surface_mrect2 = text_surface_max2.get_rect(center=self.option4.center)
        

        # Draw original glove image
        orig_glove_rect = orig_glove.get_rect()
        orig_glove_rect.midleft = self.option3.midleft + pygame.math.Vector2(10, 0)
       

        # Draw "upgrade to" text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Upgrade to (cost is {self.glove_cost})", True, (255,0, 0))
        text_rect = text_surface.get_rect(center=self.option3.center)


        # Draw the next glove image
        nxt_glove_rect = nxt_glove.get_rect()
        nxt_glove_rect.midright = self.option3.midright - pygame.math.Vector2(10, 0)

        # Draw the original gun image
        orig_gun_rect = orig_gun.get_rect()
        orig_gun_rect.midleft = self.option4.midleft + pygame.math.Vector2(10, 0)
        
        
        font = pygame.font.Font(None, 36)
        text_surface2 = font.render(f"Upgrade to (cost is {self.gun_cost})", True, (255,0, 0))
        text_rect2 = text_surface2.get_rect(center=self.option4.center)
        
        # Draw next gun image
        nxt_gun_rect = nxt_gun.get_rect()
        nxt_gun_rect.midright = self.option4.midright - pygame.math.Vector2(10, 0)
        
        pygame.draw.rect(self.display_surface, 'White', self.option1)
        pygame.draw.rect(self.display_surface, 'Blue', health_rect)
        
        pygame.draw.rect(self.display_surface, 'White', self.option2)
        pygame.draw.rect(self.display_surface, 'Blue', ammunition_rect)
       
        
        pygame.draw.rect(self.display_surface, 'White', self.option3)
        if not self.check_max_glove:
            self.display_surface.blit(orig_glove, orig_glove_rect)
            self.display_surface.blit(text_surface, text_rect)
            self.display_surface.blit(nxt_glove, nxt_glove_rect)
        else:
            self.display_surface.blit(text_surface_max, text_surface_mrect)
        
        pygame.draw.rect(self.display_surface, 'White', self.option4)
        if not self.check_max_gun:
            self.display_surface.blit(orig_gun, orig_gun_rect)
            self.display_surface.blit(text_surface2, text_rect2)
            self.display_surface.blit(nxt_gun, nxt_gun_rect)
        else:
            self.display_surface.blit(text_surface_max2, text_surface_mrect2)
        
        
        if self.current_option == 0:
            self.highlight = pygame.Rect(self.op1pos[0],self.op1pos[1],self.width//2+40,120)
            self.highlight.center = self.option1.center
            pygame.draw.rect(self.display_surface, 'Yellow', self.highlight)
            pygame.draw.rect(self.display_surface, 'White', self.option1)
            pygame.draw.rect(self.display_surface,'Blue',health_rect)
            
        elif self.current_option == 1:
            self.highlight = pygame.Rect(self.op2pos[0],self.op2pos[1],self.width//2+40,120)
            self.highlight.center = self.option2.center
            pygame.draw.rect(self.display_surface, 'Yellow', self.highlight)
            pygame.draw.rect(self.display_surface, 'White', self.option2)
            pygame.draw.rect(self.display_surface,'Blue',ammunition_rect)
            
        elif self.current_option == 2:
            self.highlight = pygame.Rect(self.op3pos[0],self.op3pos[1], self.width//2+40,120)
            self.highlight.center = self.option3.center
            pygame.draw.rect(self.display_surface, 'Yellow', self.highlight)
            pygame.draw.rect(self.display_surface, 'White', self.option3)
            
            if not self.check_max_glove:
                self.display_surface.blit(orig_glove, orig_glove_rect)
                self.display_surface.blit(text_surface, text_rect)
                self.display_surface.blit(nxt_glove, nxt_glove_rect)
            else:
                self.display_surface.blit(text_surface_max, text_surface_mrect)
                
        elif self.current_option == 3:
            self.highlight = pygame.Rect(self.op4pos[0],self.op4pos[1], self.width//2+40,120)
            self.highlight.center = self.option4.center
            pygame.draw.rect(self.display_surface, 'Yellow', self.highlight)
            pygame.draw.rect(self.display_surface, 'White', self.option4)
            if not self.check_max_gun:
                self.display_surface.blit(orig_gun, orig_gun_rect)
                self.display_surface.blit(text_surface2, text_rect2)
                self.display_surface.blit(nxt_gun, nxt_gun_rect)
            else:
                self.display_surface.blit(text_surface_max2, text_surface_mrect2)
            
    def display_current_eddie(self):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Current Eddie: {self.current_eddie-self.lost_eddie}", True, (0,0,0))
        text_rect = text_surface.get_rect(center=(7*self.display_surface.get_width() // 8, self.display_surface.get_height() // 16))
        self.display_surface.blit(text_surface, text_rect)
        
    def draw_upgrade_success(self):
        display_surface = pygame.display.get_surface()
        size = (display_surface.get_width() // 2, display_surface.get_height() // 2)
        overlay_surface = pygame.Surface(size, pygame.SRCALPHA)
        overlay_surface.fill((255, 0, 0, 128))  # Translucent red color
        display_surface.blit(overlay_surface, (WIDTH//4, HEIGTH//4))

        font = pygame.font.Font(None, 36)
        text_surface = font.render("Upgrades applied", True, (255, 255, 255))
        
        text_rect = text_surface.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2))
        
        display_surface.blit(text_surface, text_rect)
        
        pass    
    def upgrade_menu(self):
       
        display_surface = pygame.display.get_surface()
        size = (display_surface.get_width() // 2, display_surface.get_height() // 2)
        overlay_surface = pygame.Surface(size, pygame.SRCALPHA)
        overlay_surface.fill((255, 0, 0, 128))  # Translucent red color
        display_surface.blit(overlay_surface, (WIDTH//4, HEIGTH//4))

        font = pygame.font.Font(None, 36)
        text_surface = font.render("Press U to open upgrade menu", True, (255, 255, 255))
        # text_surface2 = font.render("yes : press H", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2))
        # text_rect2 = text_surface2.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2 + 50))
        display_surface.blit(text_surface, text_rect)
        # display_surface.blit(text_surface2, text_rect2)
                    
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_u] and not self.u_check:
            self.upgrade_check = not self.upgrade_check
            self.u_check = True
    
        if not keys[pygame.K_u]:
            self.u_check = False
        if self.upgrade_check:
            self.initialize()    
            check_enter = False 
            while True:
                for event in pygame.event.get():
                    check_enter = False
                    if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                        check_enter = True
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
                        check_enter = True
                        self.current_max_health += self.added_health
                        self.current_max_ammunition += self.added_ammo
                        self.current_eddie -= self.lost_eddie
                        self.added_health = 0
                        self.added_ammo = 0
                        self.lost_eddie = 0
                        
                        self.player.savefile['player_max_stats']['health'] = self.current_max_health
                        self.player.savefile['player_max_stats']['ammunition'] = self.current_max_ammunition
                        self.player.savefile['player_stats']['eddie'] = self.current_eddie
                        
                        self.player.savefile['player_current_weapon'] = {'1':self.new_glove,'2':self.new_gun}
                        self.player.update_stats(self.player.savefile)
                        
                    
                    # display_surface = pygame.display.get_surface()
                    
                    # display_surface.fill((0, 255, 0, 50))
                    self.display_surface.blit(self.menuimg,(0,0))
                    
                    # display_surface.fill('Green')
                    self.draw()
                    self.display_current_eddie()
                    self.draw_text()
                    if check_enter:
                            self.draw_upgrade_success()
                
                pygame.display.update()