import pygame 
from settings import * 
from level import Level
from player import Player
from enemy import OpenWEnemy
from tile import Tile
from menu import UpgradeMenu
class Hospital(Level):
    def __init__(self,level_name,savefile):
        self.reset = False
        self.level_name = level_name
        self.door_to_level2 = pygame.sprite.Group()
        self.hospital = pygame.sprite.Group()
        super().__init__(savefile)
        
    def heal(self):
        keys = pygame.key.get_pressed()
        if pygame.sprite.spritecollide(self.player,self.hospital,False):
            display_surface = pygame.display.get_surface()
            size = (display_surface.get_width() // 2, display_surface.get_height() // 2)
            overlay_surface = pygame.Surface(size, pygame.SRCALPHA)
            overlay_surface.fill((255, 0, 0, 128))  # Translucent red color
            display_surface.blit(overlay_surface, (WIDTH//4, HEIGTH//4))

            font = pygame.font.Font(None, 36)
            text_surface = font.render("Do you want to heal ?:", True, (255, 255, 255))
            text_surface2 = font.render("yes : press SPACE", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2))
            text_rect2 = text_surface2.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2 + 50))
            display_surface.blit(text_surface, text_rect)
            display_surface.blit(text_surface2, text_rect2)

            if keys[pygame.K_SPACE]:
                self.player.stats['health'] = 100
    def create_map(self):
        pass 

class Level1(Level):
    def __init__(self,level_name,savefile):
        self.reset = False
        self.level_name = level_name
        self.door_to_level2 = pygame.sprite.Group()
        self.hospital = pygame.sprite.Group()
        self.upgrade_shop = pygame.sprite.Group()
        self.heal_check = False
        
        super().__init__(savefile)
        self.upgrade_menu = UpgradeMenu(self.player)
        
    def heal(self):
        keys = pygame.key.get_pressed()

        if pygame.sprite.spritecollide(self.player,self.hospital,False):
            display_surface = pygame.display.get_surface()
            size = (display_surface.get_width() // 2, display_surface.get_height() // 2)
            overlay_surface = pygame.Surface(size, pygame.SRCALPHA)
            overlay_surface.fill((255, 0, 0, 128))  # Translucent red color
            display_surface.blit(overlay_surface, (WIDTH//4, HEIGTH//4))

            font = pygame.font.Font(None, 36)
            text_surface = font.render("Do you want to heal ?:", True, (255, 255, 255))
            text_surface2 = font.render("yes : press SPACE", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2))
            text_rect2 = text_surface2.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2 + 50))
            display_surface.blit(text_surface, text_rect)
            display_surface.blit(text_surface2, text_rect2)
            
            if keys[pygame.K_SPACE]:
                self.player.stats['health'] = 100
        
    def update_level(self):
        if pygame.sprite.spritecollide(self.player,self.door_to_level2,False):
                return 'level-2'
        return self.level_name

    def heal(self):
        keys = pygame.key.get_pressed()
        
        if pygame.sprite.spritecollide(self.player,self.hospital,False):
            display_surface = pygame.display.get_surface()
            size = (display_surface.get_width() // 2, display_surface.get_height() // 2)
            overlay_surface = pygame.Surface(size, pygame.SRCALPHA)
            overlay_surface.fill((255, 0, 0, 128))  # Translucent red color
            display_surface.blit(overlay_surface, (WIDTH//4, HEIGTH//4))
        
            font = pygame.font.Font(None, 36)
            text_surface = font.render("Do you want to heal ?:", True, (255, 255, 255))
            text_surface2 = font.render("yes : press SPACE", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2))
            text_rect2 = text_surface2.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2 + 50))
            display_surface.blit(text_surface, text_rect)
            display_surface.blit(text_surface2, text_rect2)
            
            if keys[pygame.K_SPACE]:
                self.player.stats['health'] = 100
    def up_menu(self):
        if pygame.sprite.spritecollide(self.player,self.upgrade_shop,False):
            self.upgrade_menu.upgrade_menu()                       
    
        
                    
               
    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            # print(row_index,row)
            for column_index,column in enumerate(row):
                x = column_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if column == 'x':
                    img = pygame.image.load('../graphics/tree.png').convert_alpha()
                    img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
                    Tile((x,y),[self.visible_sprite,self.obstacle_sprite],'object',img)
                if column == 'p':
                    self.player = Player((x,y),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.destroy_attack,self,self.savefile)
                if column == 'g':
                    OpenWEnemy('garbage',(x,y),[self.visible_sprite,self.attackable_sprites],self.obstacle_sprite,self.loot_sprites,self.visible_sprite,self.dmg_to_player)
                if column == 'd':
                    img = pygame.image.load('../graphics/door2.png').convert_alpha()
                    img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
                    door = Tile((x,y),[self.visible_sprite,self.obstacle_sprite,self.door_to_level2],'object',img)
                    self.door_to_level2.add(door)
                if column == 'h':
                    img = pygame.image.load('../graphics/hospital.png').convert_alpha()
                    img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
                    Tile((x,y),[self.visible_sprite,self.obstacle_sprite,self.hospital],'object',img)
                if column == 'u':
                    img = pygame.image.load('../graphics/upgrade_shop.png').convert_alpha()
                    img = pygame.transform.scale(img,(TILE_SIZE,TILE_SIZE))
                    Tile((x,y),[self.visible_sprite,self.obstacle_sprite,self.upgrade_shop],'object',img)
    def new_update(self):
        self.heal()
        self.up_menu()

class Level2(Level):
    def __init__(self,level_name,savefile):
        super().__init__(savefile)
        self.level_name = level_name
        self.reset = False
    def update_level(self):
        return self.level_name
