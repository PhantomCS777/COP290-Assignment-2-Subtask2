import pygame 
from settings import * 
from level import Level
from level import YOrderCameraGroup
from player import Player
from enemy import OpenWEnemy
from tile import Tile
from menu import UpgradeMenu
import random
from pytmx.util_pygame import load_pygame
import pytmx

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
            text_surface2 = font.render("yes : press H", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2))
            text_rect2 = text_surface2.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2 + 50))
            display_surface.blit(text_surface, text_rect)
            display_surface.blit(text_surface2, text_rect2)

            if keys[pygame.K_h]:
                self.player.stats['health'] = self.player.max_stats['health']
                # print(self.player.stats['health'])
    def create_map(self):
        pass 

class Level1(Level):
    def __init__(self,level_name,savefile,control):
        self.reset = False
        self.level_name = level_name
        self.door_to_level2 = pygame.sprite.Group()
        self.hospital = pygame.sprite.Group()
        self.upgrade_shop = pygame.sprite.Group()
        self.heal_check = False
        self.control = control
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
            text_surface2 = font.render("yes : press H", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2))
            text_rect2 = text_surface2.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2 + 50))
            display_surface.blit(text_surface, text_rect)
            display_surface.blit(text_surface2, text_rect2)
            
            if keys[pygame.K_h]:
                self.player.stats['health'] = self.player.max_stats['health']
                # print(self.player.stats['health'])
        
    def update_level(self):
        if pygame.sprite.spritecollide(self.player,self.door_to_level2,False):
                self.control.Home.player.hitbox.x,self.control.Home.player.hitbox.y = (1300,1000)
                
                return 'Home'
        return self.level_name

    
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
                    enem = random.choice(['air_pollution','water_pollution','noise_pollution'])
                    OpenWEnemy(enem,(x,y),[self.visible_sprite,self.attackable_sprites],self.obstacle_sprite,self.loot_sprites,self.visible_sprite,self.dmg_to_player)
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
    def __init__(self,level_name,savefile,control):
        super().__init__(savefile)
        self.level_name = level_name
        self.reset = False
        self.control = control
    def update_level(self):
        return self.level_name


class Home(Level):
    def __init__(self,level_name,savefile,control):
        self.control = control
        self.reset = False
        self.level_name = level_name
        self.door_to_level1 = pygame.sprite.Group()
        self.door_to_room1 = pygame.sprite.Group()
        self.door_to_room2 = pygame.sprite.Group()
        self.hospital = pygame.sprite.Group()
        self.upgrade_shop = pygame.sprite.Group()
        self.heal_check = False
        self.boat_cordinates = (1300,1000)
        self.boat = None 
        super().__init__(savefile)
        self.upgrade_menu = UpgradeMenu(self.player)
    
    def heal(self):
        keys = pygame.key.get_pressed()

        if pygame.sprite.spritecollide(self.player,self.hospital,False):
            display_surface = pygame.display.get_surface()
            size = (display_surface.get_width() // 2, display_surface.get_height() // 2)
            overlay_surface = pygame.Surface(size, pygame.SRCALPHA)
            overlay_surface.fill((255, 0, 0, 128))  # Translucent red color
            display_surface.blit(overlay_surface, (display_surface.get_width()//4, display_surface.get_height()//4))

            font = pygame.font.Font(None, 36)
            text_surface = font.render("Do you want to heal ?:", True, (255, 255, 255))
            text_surface2 = font.render("yes : press H", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2))
            text_rect2 = text_surface2.get_rect(center=(display_surface.get_width() // 2, display_surface.get_height() // 2 + 50))
            display_surface.blit(text_surface, text_rect)
            display_surface.blit(text_surface2, text_rect2)
            
            if keys[pygame.K_h]:
                self.player.stats['health'] = self.player.max_stats['health']
                # print(self.player.stats['health'])
    def update_level(self):
        if pygame.sprite.spritecollide(self.player,self.door_to_level1,False):
                
                return 'room1'
        
        if pygame.sprite.spritecollide(self.player,self.door_to_room1,False):
            self.control.room1.player.hitbox.x,self.control.room1.player.hitbox.y = (16*12*2,16*17*2)
            return 'room1'
        
        if pygame.sprite.spritecollide(self.player,self.door_to_room2,False):
            self.control.room2.player.hitbox.x,self.control.room2.player.hitbox.y = (16*3*2,16*16*2)
            return 'room2'
        return self.level_name

    
    def up_menu(self):
        if pygame.sprite.spritecollide(self.player,self.upgrade_shop,False):
            self.upgrade_menu.upgrade_menu()       
            
    def create_map(self):
        self.player = Player((1300,1000),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.destroy_attack,self,self.savefile)
        gameMap = load_pygame('../map/Home_map/HomeMap.tmx')
        # print(gameMap.layers)
        door_to_room1 = [(70,29)] 
        door_to_room1 = list(map(lambda x: (x[0]*16,x[1]*16),door_to_room1))
        door_to_room2 = [(92,72)]
        door_to_room2 = list(map(lambda x: (x[0]*16,x[1]*16),door_to_room2))
        for cordi in door_to_room1:
            Tile(cordi,[self.door_to_room1],'object')
        for cordi in door_to_room2:
            Tile(cordi,[self.door_to_room2],'object')
            
        for layer in gameMap.layers:
            if layer.id == 2:
                print(dir(layer))
                data = layer.data 
                for row_index,row in enumerate(data):
                    for column_index,column in enumerate(row):
                        x = column_index*16
                        y = row_index*16
                        
                        if column != 0:
                            Tile((x,y),[self.obstacle_sprite],'invisible')
        for layer in gameMap.objectgroups:
            for object in layer: 
                # print((object.id))
                # print(object.type)
                # Tile((object.x,object.y),[self.visible_sprite,self.obstacle_sprite],'objec',(lambda x:pygame.transform.scale(x,(object.width,object.height)))(object.image))
                if object.name == 'FloorBlock':
                    print("FloorBlock"*1000)
                    return
                
                if object.name =='hospital':
                    Tile((object.x,object.y),[self.visible_sprite,self.obstacle_sprite,self.hospital],'object',(lambda x:pygame.transform.scale(x,(object.width,object.height)))(object.image))
                elif object.name == 'shop':
                    Tile((object.x,object.y),[self.visible_sprite,self.obstacle_sprite,self.upgrade_shop],'object',(lambda x:pygame.transform.scale(x,(object.width,object.height)))(object.image))
                elif object.name == 'boat':
                    self.boat_cordinates = (object.x+128,object.y)
                    self.boat = Tile((object.x,object.y),[self.visible_sprite,self.obstacle_sprite,self.door_to_level1],'object',(lambda x:pygame.transform.scale(x,(object.width,object.height)))(object.image))
                else:
                    Tile((object.x,object.y),[self.visible_sprite,self.obstacle_sprite],'object',(lambda x:pygame.transform.scale(x,(object.width,object.height)))(object.image))
        
        enemy_cordi = [(48,61),(55,64),(95,50),(95,55),(85,60)]
        enemy_cordi = list(map(lambda x: (x[0]*16,x[1]*16),enemy_cordi))
        for cordi in enemy_cordi:
            enem = random.choice(['water_pollution'])
            OpenWEnemy(enem,cordi,[self.visible_sprite,self.attackable_sprites],self.obstacle_sprite,self.loot_sprites,self.visible_sprite,self.dmg_to_player)
        
       
           
    def new_update(self):
        self.heal()
        self.up_menu()



class Room(Level):
    def __init__(self,level_name,savefile,control):
       
        self.control = control
        self.reset = False
        self.level_name = level_name
        self.door_to_Home = pygame.sprite.Group()
        self.door_to_dungeon = pygame.sprite.Group()    
        super().__init__(savefile)
        self.visible_sprite = YOrderCameraGroup('../map/Room/Room1.png')
        self.create_map()
        
    def update_level(self):
        if pygame.sprite.spritecollide(self.player,self.door_to_Home,False):
            self.control.Home.player.hitbox.x,self.control.Home.player.hitbox.y = (71*16,33*16)
            return 'Home'
        if pygame.sprite.spritecollide(self.player,self.door_to_dungeon,False):
            self.control.dungeon.player.hitbox.x,self.control.dungeon.player.hitbox.y = (47*32,29*32)
            return 'dungeon'
            
        return self.level_name
    
    def create_map(self):
        door_to_home = [(11,19),(12,19),(13,19)]
        door_to_home = list(map(lambda x: (x[0]*16,x[1]*16),door_to_home))
        door_to_dungeon = [(22,5)]
        door_to_dungeon = list(map(lambda x: (x[0]*16,x[1]*16),door_to_dungeon))
        playercord = (2*12,2*17)
        self.player = Player((playercord[0]*16,playercord[1]*16),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.destroy_attack,self,self.savefile)
        gameMap = load_pygame('../map/Room/Room1.tmx')
        for layer in gameMap.layers:
            if layer.id == 5:
                
                data = layer.data 
                for row_index,row in enumerate(data):
                    for column_index,column in enumerate(row):
                        x = column_index*16
                        y = row_index*16
                        if column != 0:
                            Tile((2*x,2*y),[self.obstacle_sprite],'invisible')
                            if (x,y) in door_to_home:
                                Tile((2*x,2*y),[self.door_to_Home],'invisible')
                            if (x,y) in door_to_dungeon:
                                Tile((2*x,2*y),[self.door_to_dungeon],'invisible')
    
class Room2(Level):
    def __init__(self,level_name,savefile,control):
       
        self.control = control
        self.reset = False
        self.level_name = level_name
        self.door_to_Home = pygame.sprite.Group()
        self.door_to_dungeon = pygame.sprite.Group()    
        super().__init__(savefile)
        self.visible_sprite = YOrderCameraGroup('../map/Room2/room2.png')
        self.create_map()
        
    def update_level(self):
        if pygame.sprite.spritecollide(self.player,self.door_to_Home,False):
            self.control.Home.player.hitbox.x,self.control.Home.player.hitbox.y = (91*16,79*16)
            return 'Home'
        if pygame.sprite.spritecollide(self.player,self.door_to_dungeon,False):
            self.control.dungeon.player.hitbox.x,self.control.dungeon.player.hitbox.y = (4*32,44*32)
            return 'dungeon'
            
        return self.level_name
    
    def create_map(self):
        door_to_home = [(3,19)]
        door_to_home = list(map(lambda x: (x[0]*16,x[1]*16),door_to_home))
        door_to_dungeon = [(1,5),(2,6),(0,6)]
        door_to_dungeon = list(map(lambda x: (x[0]*16,x[1]*16),door_to_dungeon))
        playercord = (2*3,2*7)
        self.player = Player((playercord[0]*16,playercord[1]*16),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.destroy_attack,self,self.savefile)
        gameMap = load_pygame('../map/Room2/room2.tmx')
        for layer in gameMap.layers:
            if layer.id == 4:
                
                data = layer.data 
                for row_index,row in enumerate(data):
                    for column_index,column in enumerate(row):
                        x = column_index*16
                        y = row_index*16
                        if column != 0:
                            Tile((2*x,2*y),[self.obstacle_sprite],'invisible')
                            if (x,y) in door_to_home:
                                Tile((2*x,2*y),[self.door_to_Home],'invisible')
                            if (x,y) in door_to_dungeon:
                                Tile((2*x,2*y),[self.door_to_dungeon],'invisible')   

class Dungeon(Level):
    def __init__(self,level_name,savefile,control):
        self.control = control
        self.reset = False
        self.level_name = level_name
        self.door_to_room1 = pygame.sprite.Group()
        self.door_to_room2 = pygame.sprite.Group()
        super().__init__(savefile)
        self.visible_sprite = YOrderCameraGroup('../map/Dungeon/map.png')
        self.create_map()
    def update_level(self):
        if pygame.sprite.spritecollide(self.player,self.door_to_room1,False):
            self.control.room1.player.hitbox.x,self.control.room1.player.hitbox.y = (22*32,8*32)
            return 'room1'
        if pygame.sprite.spritecollide(self.player,self.door_to_room2,False):
            self.control.room2.player.hitbox.x,self.control.room2.player.hitbox.y = (3*16*2,7*16*2)
            return 'room2'
        return self.level_name

    def new_update(self):
        pass 
    
    def create_map(self):
        self.player = Player((48*32,33*32),[self.visible_sprite],self.obstacle_sprite,self.create_attack,self.destroy_attack,self,self.savefile)
        gameMap = load_pygame('../map/Dungeon/MapDungeon.tmx')
        door_to_room = [(47,33),(48,33),(49,33),(50,33)]
        door_to_room = list(map(lambda x: (x[0]*16,x[1]*16),door_to_room))
        door_to_room2 = [(4,42),(5,42)]
        door_to_room2 = list(map(lambda x: (2*x[0]*16,2*x[1]*16),door_to_room2))
        for cordi in door_to_room2:
            Tile(cordi,[self.door_to_room2],'object')
        
        for layer in gameMap.layers:
            if layer.id == 3:
                print(dir(layer))
                data = layer.data 
                for row_index,row in enumerate(data):
                    for column_index,column in enumerate(row):
                        x = column_index*16
                        y = row_index*16
                        if column != 0:
                            Tile((2*x,2*y),[self.obstacle_sprite],'invisible')
                            if (x,y) in door_to_room:
                                Tile((2*x,2*y),[self.obstacle_sprite,self.door_to_room1],'invisible')
                            if (x,y) in door_to_room2:
                                Tile((2*x,2*y),[self.obstacle_sprite,self.door_to_room2],'invisible')
            elif layer.id == 4:
                data = layer.data 
                for row_index,row in enumerate(data):
                    for column_index,column in enumerate(row):
                        x = column_index*16
                        y = row_index*16
                        if column != 0:
                            enem = random.choice(['air_pollution','water_pollution'])
                            OpenWEnemy(enem,(2*x,2*y),[self.visible_sprite,self.attackable_sprites],self.obstacle_sprite,self.loot_sprites,self.visible_sprite,self.dmg_to_player)
                            
        
        
