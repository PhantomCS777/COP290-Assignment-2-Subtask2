from settings import * 
from csv import reader
from os import walk 
import json 
import pygame

def import_csv_layout(path):
    terrain = []
    with open(path) as lvlmap:
        layout = reader(lvlmap,delimiter= ',')
        for row in layout:
            terrain.append(list(row))
        return terrain


def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list


def weapon_image(name):
    return pygame.image.load(f'../graphics/{name}.png').convert_alpha()




class Spritesheet:
    def __init__(self, filename,file):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.meta_data = '../animation/' + file + '.json'
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()



    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image





