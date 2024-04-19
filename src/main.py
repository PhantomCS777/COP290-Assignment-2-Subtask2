import pygame,sys
from settings import * 
from debugger import debug
from level import Level
from landing_page import LandingPage
from control import Control
class Game:
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock() 
        # self.level = Level()
        self.control = Control()
        self.landing_page = LandingPage()
        print("Game Initialized")
    def run(self):
        while True: 
            if self.landing_page.game_state == 'landing_page':
                self.landing_page.run()
                self.screen = pygame.display.set_mode(self.landing_page.aspect_rations[self.landing_page.aspect_ratio])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.control.update_save_file(self.control.current_level)
                    pygame.quit()
                    
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # self.level.toggle_pause()
                        pass
            self.screen.fill('Black')   
            if self.landing_page.game_state != 'landing_page' and self.landing_page.game_state != 'over':
                self.screen = pygame.display.set_mode(self.landing_page.aspect_rations[self.landing_page.aspect_ratio])
            if self.landing_page.game_state == 'new':
                self.control = Control()
                self.control.game_state = 'new'
                self.landing_page.game_state = 'over'
            elif self.landing_page.game_state == 'load':
                self.control = Control()
                self.control.game_state = 'load'
                self.landing_page.game_state = 'over'
            self.control.run()
            pygame.display.update()
            self.clock.tick(FPS)     


if __name__ == '__main__':  
    game = Game()
    game.run() 