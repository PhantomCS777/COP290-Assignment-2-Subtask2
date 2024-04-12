import pygame 
from settings import *




class PauseMenu():
    def __init__(self,player):
        
        self.display_surface = pygame.display.get_surface()
        self.player = player 
        
    def display(self):
        self.display_surface.fill('Red')
        
        