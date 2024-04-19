import pygame 
from settings import * 
from util import * 
import sys 
from debugger import debug


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_width() // 2
        self.half_h = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(50,50)
        self.floor_surf = pygame.image.load('../map/Home_map/map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
    
    def draw(self,player):
        sprites = sorted(self.sprites(),key = lambda sprite: sprite.rect.centery)
        self.offset.x = self.half_w - player.rect.centerx
        self.offset.y = self.half_h - player.rect.centery
        
        floor_offset_pos = self.floor_rect.topleft + self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        
        for sprite in sprites: 
            self.display_surface.blit(sprite.image,sprite.rect.topleft + self.offset)

 
class Pointer(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        # self.image = pygame.image.load('../graphics/pointer.png').convert_alpha()
        # self.rect = self.image.get_rect(center = (WIDTH // 2, HEIGTH // 2))
        self.display_surface = pygame.display.get_surface()
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 20
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.display_surface.get_rect().center)
        
    def move(self,speed):
        if self.direction.magnitude() > 0:
            self.direction.normalize_ip()
            self.rect.x += self.direction.x * speed 
            
            self.rect.y += self.direction.y * speed
            
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction = pygame.math.Vector2(0,0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            
        

class WorldMap:
    def __init__(self,savefile):
        self.display_surface = pygame.display.get_surface()
        self.savefile = savefile
        self.camera = Camera()
        self.pointer = Pointer([self.camera])
        self.current_level = None 
        self.input_trigger = False
        self.mouse_trigger = False 
        self.map_icon_image = pygame.image.load('../graphics/asset/map_icon.png').convert_alpha()
        self.map_icon_image = pygame.transform.scale(self.map_icon_image, (TILE_SIZE, TILE_SIZE))
        self.map_icon_rect = self.map_icon_image.get_rect()
        self.map_icon_rect.topright = (self.display_surface.get_width() - 10, 10)
        self.toggle = True
        
        
        
    def run(self):
        
        self.pointer.input()
        self.pointer.move(self.pointer.speed)
        self.camera.draw(self.pointer)
        self.display_surface.blit(self.map_icon_image, self.map_icon_rect)
        
        
    def assign_level(self,level):
        self.current_level = level
    
    def exit_map(self):
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_m]:
        #     if not self.input_trigger:
        #         self.input_trigger = True
        #         return self.current_level
                
        # else:
        #     self.input_trigger = False


        # if self.map_icon_rect.collidepoint(pygame.mouse.get_pos()):
        #     if pygame.mouse.get_pressed()[0]:
        #         if not self.mouse_trigger:
        #             self.mouse_trigger = True 
        #             return self.current_level
        #     else:
        #         self.mouse_trigger = False 
        
        if self.toggle:
            return self.current_level
                
        return 'worldmap'
        

        
        
         