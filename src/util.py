from settings import * 
from csv import reader
from os import walk 
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