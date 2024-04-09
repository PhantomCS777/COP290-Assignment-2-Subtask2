import pygame 
from settings import *
import os
from debugger import debug


class Tile(pygame.sprite.Sprite):
    def __init__(self,position,groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/tree.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))
       
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0,-10)