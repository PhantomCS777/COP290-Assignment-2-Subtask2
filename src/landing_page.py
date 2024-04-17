import pygame ,sys
from settings import *


class LandingPage:
    def __init__(self,control):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 32)
        self.control = control 
        self.new_game_button = pygame.Rect(100, 200, 200, 50)
        self.new_game_text = self.font.render('New Game', True, (255, 255, 255))
        
        self.load_game_button = pygame.Rect(100, 300, 200, 50)
        self.load_game_text = self.font.render('Load Game', True, (255, 255, 255))

    def draw(self):
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.new_game_button)
        self.display_surface.blit(self.new_game_text, (self.new_game_button.x + 50, self.new_game_button.y + 10))
        
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.load_game_button)
        self.display_surface.blit(self.load_game_text, (self.load_game_button.x + 50, self.load_game_button.y + 10))
        

  
               
                        
             
        
    def run(self):
        while True:
            print('landing page running')
            self.draw()
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('mouse clicked')
                    if self.new_game_button.collidepoint(event.pos):
                        
                        self.control.update_game_state('new')
                        return 
                        
                    elif self.load_game_button.collidepoint(event.pos):
                        
                        self.control.update_game_state('load')
                        print("Load game button clicked")
                        return
                
            pygame.display.update()
            
        