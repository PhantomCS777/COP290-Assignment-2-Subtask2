import pygame ,sys
from settings import *


class LandingPage:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 32)
        self.game_state = 'landing_page'
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
        self.settings_buttons = []
        self.aspect_rations = {'16:9': (WIDTH_DEFAULT, HEIGTH_DEFAULT), '4:3': (800, 600), '5:4': (800, 640), '16:10': (800, 500),'big': (1920, 1080)}
        self.aspect_ratio = '16:9'
        
        self.clock = pygame.time.Clock()
        
    def draw(self):
        
        pygame.draw.rect(self.display_surface, (0,0,255), self.new_game_button)
        self.display_surface.blit(self.new_game_text, (self.new_game_button.x + 50, self.new_game_button.y + 10))
        
        pygame.draw.rect(self.display_surface, (0,0,255), self.load_game_button)
        self.display_surface.blit(self.load_game_text, (self.load_game_button.x + 50, self.load_game_button.y + 10))
        
        pygame.draw.rect(self.display_surface, (0,0,255), self.settings_button)
        self.display_surface.blit(self.settings_text, (self.settings_button.x + 50, self.settings_button.y + 10))
        
    def draw_settings(self):
        current_aspect_ratio_text = self.font.render(f'Current Aspect Ratio: {self.aspect_ratio}', True, (128,0,128))
        self.display_surface.blit(current_aspect_ratio_text, (100, 100))
        
        aspect_ratios = ['16:9', '4:3', '5:4', '16:10','big']
        button_width = 150
        button_height = 30
        button_margin = 20
        settings_buttons = []
        
        for i, ratio in enumerate(aspect_ratios):
            button_x = 100
            button_y = 200 + (i * (button_height + button_margin))
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_text = self.font.render(ratio, True, (255, 255, 255))
            settings_buttons.append((button_rect, button_text, ratio))
            
        for button_rect, button_text,_ in settings_buttons:
            pygame.draw.rect(self.display_surface, (0, 0, 255), button_rect)
            self.display_surface.blit(button_text, (button_rect.x + 40, button_rect.y + 5))
        
        pygame.draw.rect(self.display_surface, (0, 0, 255), self.back_button)
        self.display_surface.blit(self.back_text, (self.back_button.x + 50, self.back_button.y + 5))
        return settings_buttons
            
    def run(self):
        while True:
            # print('landing page running')
            self.display_surface.blit(self.thumbnail, (0,0))
            if self.toggle_settings:
                self.settings_buttons = self.draw_settings()
            else: self.draw()
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('mouse clicked')
                    if self.new_game_button.collidepoint(event.pos) and not self.toggle_settings:
                        
                        self.game_state = 'new'
                        return 
                        
                    elif self.load_game_button.collidepoint(event.pos) and not self.toggle_settings:
                        
                        self.game_state = 'load'
                       
                        return
                    
                    elif self.settings_button.collidepoint(event.pos) and not self.toggle_settings:
                        self.toggle_settings = True 
                    elif self.back_button.collidepoint(event.pos) and self.toggle_settings:
                        self.toggle_settings = False
                        
                    elif self.toggle_settings:
                        for button in self.settings_buttons:
                            if button[0].collidepoint(event.pos):
                                print('button clicked')
                                self.aspect_ratio = button[2]
                            
                            
                
            pygame.display.update()
            self.clock.tick(FPS)
            
        