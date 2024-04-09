import pygame 
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self,position,groups,obstacle_sprite):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect(topleft = position)
        
        self.speed = PLAYER_SPEED 
        self.direction = pygame.math.Vector2()
        
        self.obstacle_sprite = obstacle_sprite
        self.hitbox = self.rect.inflate(0,-20)
        
    def open_world_input(self):
        keys = pygame.key.get_pressed() 
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1 
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else: 
            self.direction.y = 0
            
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1 
        else:
            self.direction.x = 0
    def move(self,speed):
        if self.direction.magnitude() > 0:
            self.direction.normalize_ip()
        self.hitbox.x += self.direction.x * speed 
        self.open_world_collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.open_world_collision('vertical')
        self.rect.center = self.hitbox.center
        
    def open_world_collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        
        if direction == 'vertical':
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
            
        
    def update(self):
        self.open_world_input()
        self.move(self.speed)
        


