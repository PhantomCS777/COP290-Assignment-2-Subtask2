import pygame ,sys
from settings import *


class LandingPage:
    def __init__(self,control):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 32)
        self.control = control 
        self.new_game_button = pygame.Rect(100, 200, 200, 50)
        self.new_game_text = self.font.render('New Game', True, (255, 255, 255))
        self.thumbnail = pygame.image.load('../graphics/landing_page/thumbnail.png')
        self.thumbnail = pygame.transform.scale(self.thumbnail,(WIDTH,HEIGTH))
        self.load_game_button = pygame.Rect(100, 300, 200, 50)
        self.load_game_text = self.font.render('Load Game', True, (255, 255, 255))
        
        self.settings_button = pygame.Rect(100, 400, 200, 50)
        self.settings_text = self.font.render('Settings', True, (255, 255, 255))
        
        self.back_button = pygame.Rect(100, 500, 200, 50)
        self.back_text = self.font.render('Back', True, (255, 255, 255))
        self.toggle_settings = False 
        self.clock = pygame.time.Clock()
    def draw(self):
        
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.new_game_button)
        self.display_surface.blit(self.new_game_text, (self.new_game_button.x + 50, self.new_game_button.y + 10))
        
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.load_game_button)
        self.display_surface.blit(self.load_game_text, (self.load_game_button.x + 50, self.load_game_button.y + 10))
        
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.settings_button)
        self.display_surface.blit(self.settings_text, (self.settings_button.x + 50, self.settings_button.y + 10))
        
    def draw_settings(self):
        aspect_ratios = ['16:9', '4:3', '5:4', '16:10']
        button_width = 200
        button_height = 50
        button_margin = 20
        settings_buttons = []
        
        for i, ratio in enumerate(aspect_ratios):
            button_x = 100
            button_y = 200 + (i * (button_height + button_margin))
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_text = self.font.render(ratio, True, (255, 255, 255))
            settings_buttons.append((button_rect, button_text))
            
        for button_rect, button_text in settings_buttons:
            pygame.draw.rect(self.display_surface, (0, 255, 0), button_rect)
            self.display_surface.blit(button_text, (button_rect.x + 50, button_rect.y + 10))
        
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.back_button)
        self.display_surface.blit(self.back_text, (self.back_button.x + 50, self.back_button.y + 10))
            
    def run(self):
        while True:
            # print('landing page running')
            self.display_surface.blit(self.thumbnail, (0,0))
            if self.toggle_settings:
                self.draw_settings()
            else: self.draw()
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('mouse clicked')
                    if self.new_game_button.collidepoint(event.pos) and not self.toggle_settings:
                        
                        self.control.update_game_state('new')
                        return 
                        
                    elif self.load_game_button.collidepoint(event.pos) and not self.toggle_settings:
                        
                        self.control.update_game_state('load')
                        print("Load game button clicked")
                        return
                    
                    elif self.settings_button.collidepoint(event.pos) and not self.toggle_settings:
                        self.toggle_settings = True 
                    elif self.back_button.collidepoint(event.pos) and self.toggle_settings:
                        self.toggle_settings = False
                        
                        
                
            pygame.display.update()
            self.clock.tick(FPS)
            
        