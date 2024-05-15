import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
import main
import map
pygame.init()

name_bullet="bullet"
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height,bullet_name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.bullet_name =bullet_name
        sprites = self.load_sprite_sheet("item", "bullet", width, height) 
        self.image = sprites[bullet_name]  

    def draw(self, window):
        window.blit(self.image, self.rect)

    def load_sprite_sheet(self, dir1, dir2, width, height):  # Thêm width và height vào đây
        path = join("assets", dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]
        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
            sprite = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            sprite.blit(sprite_sheet, (0, 0))
            scaled_sprite = pygame.transform.scale(sprite, (width, height))  # Scale sprite lên gấp đôi
            all_sprites[image.replace(".png", "")] = scaled_sprite

        return all_sprites
        