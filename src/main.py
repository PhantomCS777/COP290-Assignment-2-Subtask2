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
        
    def run(self):
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.control.update_save_file(self.control.current_level)
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # self.level.toggle_pause()
                        pass
            self.screen.fill('Black')   
            
            self.control.run()
            pygame.display.update()
            self.clock.tick(FPS)     


if __name__ == '__main__':  
    game = Game()
    game.run() 