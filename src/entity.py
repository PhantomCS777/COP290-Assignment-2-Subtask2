import pygame 




class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index = 0 
        self.direction = pygame.math.Vector2()
    
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