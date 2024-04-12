import pygame 
from settings import *
from entity import Entity




class Projectile(Entity):
    def __init__(self,weapon,groups,attackable_sprites,obstacle_sprites):
        super().__init__(groups)
        self.weapon = weapon
        self.base = weapon.weapon_tip 
        
        
        self.speed = 10
        projectile_img = 'bullet_' + self.base + '.png'
        self.image = pygame.image.load(f'../graphics/{projectile_img}').convert_alpha()
        self.image = pygame.transform.scale(self.image,(TILE_SIZE//4,TILE_SIZE//4))
        self.attackable_sprites = attackable_sprites
        self.obstacle_sprite = obstacle_sprites
        self.sprtie_type = 'weapon'
        
        if self.base == 'down':
            self.rect = self.image.get_rect(midtop = weapon.rect.midbottom)
            self.direction = pygame.math.Vector2(0,1)
        elif self.base == 'up':
            self.rect = self.image.get_rect(midbottom = weapon.rect.midtop)
            self.direction = pygame.math.Vector2(0,-1)
        elif self.base == 'right':
            self.rect = self.image.get_rect(midleft = weapon.rect.midright)
            self.direction = pygame.math.Vector2(1,0)
        elif self.base== 'left':
            self.direction = pygame.math.Vector2(-1,0)
            self.rect = self.image.get_rect(midright = weapon.rect.midleft)
        
        self.hitbox = self.rect.inflate(0,-10)  
        
    def open_world_collision(self, direction):
        
        if direction == 'horizontal':
            
            for sprite in self.attackable_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    sprite.take_dmg(self.weapon.player)
                    self.kill()
                    
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.kill()
                        
        if direction == 'vertical':
            
            for sprite in self.attackable_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    sprite.take_dmg(self.weapon.player)
                    self.kill()
            
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.kill()    
            
    def update(self):
        self.move(self.speed)
        