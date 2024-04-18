import pygame 
from settings import *
from util import *





class DailogBox:
    def __init__(self):
        self.font = pygame.font.Font(None,20)
        self.inv_speed = 3 
        self.counter = 0 
        self.done = False 
        
        
        self.snippet = self.font.render('',True,'white')
        self.box = pygame.image.load('../graphics/asset/dialog_box.png')
        self.box = pygame.transform.scale(self.box,(WIDTH,HEIGTH//4))
        self.surface = pygame.display.get_surface()
        self.active_messsage = 0 
        self.check_enter = False 

    def draw(self,snippets):
        snippet = snippets[self.active_messsage]
        keys = pygame.key.get_pressed()
        
        pygame.draw.rect(self.surface,(0,0,0),(0,HEIGTH - HEIGTH//4,WIDTH,HEIGTH//4))
        
        if self.counter < self.inv_speed*len(snippet):
            
            self.counter += 1
        elif self.counter >=  self.inv_speed*len(snippet):
            self.done = True 
            
        message = self.font.render(snippet[0:self.counter//self.inv_speed],True,'white')
        
        self.surface.blit(message,(20,HEIGTH - HEIGTH//4 + 20))
        pygame.display.flip()
        
        if keys[pygame.K_RETURN] and self.done and (len(snippets) > self.active_messsage + 1):
            if not self.check_enter:
                self.active_messsage += 1
                self.done = False 
                self.counter = 0 
                self.check_enter = True
        else:
            self.check_enter = False
        
        
        