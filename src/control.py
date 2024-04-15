import pygame 
import os,json
from settings import * 
from level import Level 
from landing_page import LandingPage
from bossfight import BossFight
from bigfight import BigFight
from levels import *
class Control:
    def __init__(self):
        
        self.savefile = self.load_save_file()
        self.landing_page = LandingPage(self)
        self.level1 = Level(self.savefile) # repalce with Level(save_data) 
        self.level2 = Level1(self.savefile)
        self.game_state = 'landing_page'
        self.current_level = self.level1 
    
        self.input_trigger = True 
        self.bossf = BossFight()
        self.bigf = BigFight()
    def update_game_state(self,mode):
        self.game_state = mode 
         
    def new_save_file(self):
        save_data = {
            "player_stats": {
            "health": 100,
            "ammunition": 100,
            "eddie": 1000
            },
            "player_weapon_stats": {
            "glove":{
            "weapon_type": "melee",
            "weapon_level": 1,
            "weapon_damage": 20,
            "weapon_name": "glove",
            "cooldown": 200},
            "gun":{
            "weapon_type": "ranged",
            "weapon_level": 1,
            "weapon_damage": 40,
            "weapon_name": "gun",
            "cooldown": 100
            }
            },
            "level_data": {
            
            }
        }

        save_file_path = "../savefile/save.json" 
        with open(save_file_path, "w") as save_file:
            json.dump(save_data, save_file)

        print("Save file updated successfully.")

    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            if self.input_trigger:
                self.current_level.toggle_pause()
                self.input_trigger = False
        else:
            self.input_trigger = True
    
    def update_save_file(self,level):
        save_file_path = "../savefile/save.json"   
        with open(save_file_path, "r") as save_file:
            save_data = json.load(save_file)
            player = level.player
            save_data["player_stats"]["health"] = player.stats["health"]
            save_data["player_stats"]["ammunition"] = player.stats["ammunition"]
            save_data["player_stats"]["eddie"] = player.stats["eddie"]


            

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
        
    def run(self):
        if self.game_state == 'landing_page':
            self.landing_page.run()
            
        elif self.game_state == 'new':
            self.new_save_file()
            self.game_state = 'load'
            
            
        elif self.game_state == 'load':
            self.input()
            # self.level1.run()
            self.level2.run()
            # self.bigf.run()
            # self.bossf.run()
        