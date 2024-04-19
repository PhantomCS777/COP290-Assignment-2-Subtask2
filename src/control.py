import pygame 
import os,json
from settings import * 
from level import Level 
from landing_page import LandingPage
from levels import *
import subprocess
from threading import Thread
from worldmap import *
class Control:
    def __init__(self):
        
        self.savefile = self.load_save_file()
        
        
        
        
        self.input_trigger = True 
        self.input_trigger_m = True
        self.input_mouse_m = True
        # self.level1 = Level1('level-1',self.savefile) # repalce with Level(save_data) 
        # self.level2 = Level2('level-2',self.savefile)
        self.Home = None
        self.dungeon = None
        self.level1 = None
        self.level2 = None
        self.room1 = None 
        self.room2 = None 
        level_thread1 = Thread(target=self.initialize_level, args=('Home',))
        level_thread2 = Thread(target=self.initialize_level, args=('dungeon',))
        home_thread3 = Thread(target=self.initialize_level, args=('room1',))
        dungeon_thread4 = Thread(target=self.initialize_level, args=('room2',))
        level_thread1.start()
        level_thread2.start()
        home_thread3.start()
        dungeon_thread4.start()
        level_thread1.join()
        level_thread2.join()
        home_thread3.join()
        dungeon_thread4.join()
        
        # self.room1 = Room('room1',self.savefile,self)
        # self.room2 = Room2('room2',self.savefile,self)
        self.game_state = 'landing_page'
        self.transition = False
        self.transition_counter = 0
        self.current_level_name = self.savefile['level_data']['current_level']
        self.current_level = self.get_current_level(self.current_level_name)
        self.worldmap = WorldMap(self.savefile,self)
      
        
    def all_levels_processed(self):
            
            return True
            
    def initialize_level(self, level_name):
        if level_name == 'Home':
            self.Home  = Home(level_name, self.savefile,self)
        elif level_name == 'dungeon':
            self.dungeon = Dungeon(level_name, self.savefile,self)
        elif level_name == 'Home':
            self.Home = Home(level_name, self.savefile,self)
        elif level_name == 'room1':
    
            self.room1 = Room(level_name, self.savefile,self)
        elif level_name == 'room2':
            self.room2 = Room2(level_name, self.savefile,self)
            
        
            
    def get_current_level(self,level):
        if level == 'level-1':
            return self.level1
        if level == 'level-2':
            return self.level2
        if level == 'Home':
            return self.Home
        if level == 'dungeon':
            return self.dungeon
        if level == 'room1':
            return self.room1
        if level == 'room2':
            return self.room2
    def update_game_state(self,mode):
        self.game_state = mode 
         
    def new_save_file(self):
        # subprocess.run(["rm","../savefile/save.json"])
        new_save_path = "../savefile/new_save.json"
        with open(new_save_path, "r") as save_file:
            save_data = json.load(save_file)


        save_file_path = "../savefile/save.json" 
        with open(save_file_path, "w") as save_file:
            json.dump(save_data, save_file)

        print("Save file updated successfully. adasf")

    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            if self.input_trigger:
                self.current_level.toggle_pause()
                self.input_trigger = False
        else:
            self.input_trigger = True
        
        

    def check_world_map(self):
        print('maps')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            if self.input_trigger_m:
                self.current_level_name = 'worldmap'
                self.worldmap.assign_level(self.current_level.level_name)
                self.worldmap.toggle  = not self.worldmap.toggle
                self.input_trigger_m = False
        else:
            self.input_trigger_m = True
        
             
        if self.current_level.map_icon_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                if self.input_mouse_m:
                    self.current_level_name = 'worldmap'
                    self.worldmap.assign_level(self.current_level.level_name)
                    self.worldmap.toggle = not self.worldmap.toggle
                    self.input_mouse_m = False
            else:
                self.input_mouse_m = True
    
    def update_save_file(self,level):
        save_file_path = "../savefile/save.json"   
        with open(save_file_path, "r") as save_file:
            save_data = json.load(save_file)
            player = level.player
            save_data["player_stats"]["health"] = player.stats["health"]
            save_data["player_stats"]["ammunition"] = player.stats["ammunition"]
            save_data["player_stats"]["eddie"] = player.stats["eddie"]
            
            save_data["player_max_stats"]["health"] = player.max_stats["health"]
            save_data["player_max_stats"]["ammunition"] = player.max_stats["ammunition"]
            save_data["player_max_stats"]["eddie"] = player.max_stats["eddie"]
            
            save_data["level_data"]["current_level"] = level.level_name

            save_data["player_current_weapon"] = player.savefile["player_current_weapon"]
            

            with open(save_file_path, "w") as save_file:
                json.dump(save_data, save_file)
            print("Save file updated successfully.")
        pass 
    def load_save_file(self):
        save_file_path = "../savefile/save.json"   
        try:
            with open(save_file_path, "r") as save_file:
                save_data = json.load(save_file)
                return save_data
        except:
            self.new_save_file()
            return self.load_save_file()
    def transition_screen(self):
        
        surface = pygame.display.get_surface()
        
        transition_color = pygame.Color(0, 0, 0, min(255, self.transition_counter * 2))  # Fade to black

       
        surface.fill(transition_color)

        # Increase the transition counter until it reaches 100
        if self.transition_counter < 100:
            self.transition_counter += 5
        else:
            self.transition_counter = 0
            self.transition = False
        
         
         
        
    def run(self):
        if self.game_state == 'landing_page':
            # self.landing_page.run()
            pass
            
        elif self.game_state == 'new':
            self.new_save_file()
            self.__init__()
            # self.savefile = self.load_save_file()
            # print(self.savefile)
            # self.current_level.get_player().update_stats(self.savefile)
            # print(self.current_level.get_player().stats)
            self.game_state = 'load'
            
            
        elif self.game_state == 'load':
            if not self.all_levels_processed():
                return 
            self.input()
            self.check_world_map()
            if self.transition:
                self.transition_screen()
                return
            if self.current_level_name == 'worldmap':
                self.worldmap.run()
                self.current_level_name = self.worldmap.exit_map()
                return
            if self.current_level_name == 'Home':
                self.current_level = self.Home
                
                print(self.Home.player.rect.x,self.Home.player.rect.y)
                self.Home.run()
                self.current_level.new_update()
                self.current_level_name = self.Home.update_level()
                if self.current_level_name != 'Home':
                    self.transition = True
                    
                if self.Home.reset:
                    self.Home.get_player().stats['health'] = 70
                    self.Home.reset = False
                    self.transition =  True
                    self.Home = Home('Home',self.savefile,self)   
                return 
            elif self.current_level_name == 'dungeon':
                self.current_level = self.dungeon
                self.dungeon.run()
                self.current_level_name = self.dungeon.update_level()
                if self.dungeon.reset:
                    self.dungeon.get_player().stats['health'] = 70
                    self.dungeon.reset = False
                    self.dungeon = Dungeon('dungeon',self.savefile,self)
                return
            elif self.current_level_name == 'room1':
                self.current_level = self.room1
                self.room1.run()
                self.current_level_name = self.room1.update_level()
                if self.room1.reset:
                    self.room1.get_player().stats['health'] = 70
                    self.room1.reset = False
                    self.room1 = Room('room1',self.savefile,self)
                return 
            elif self.current_level_name == 'room2':
                self.current_level = self.room2
                self.room2.run()
                self.current_level_name = self.room2.update_level()
                if self.room2.reset:
                    self.room2.get_player().stats['health'] = 70
                    self.room2.reset = False
                    self.room2 = Room2('room2',self.savefile,self)
                return 
            
        