import pygame
from data.constants import *

#method for getting an image from a spritesheet
class SpriteSheet():
    def __init__(self, sheet, sprite_dimensions, scale_factor):
        self.sheet = sheet
        self.sprite_width = sprite_dimensions[0]
        self.sprite_height = sprite_dimensions[1]
        self.scale_factor = scale_factor

    def get_image(self, x, y, flip):
        image = pygame.Surface((self.sprite_width, self.sprite_height)).convert()
        image.blit(self.sheet, (0, 0), ((x * self.sprite_width), (y * self.sprite_height), self.sprite_width, self.sprite_height))
        image = pygame.transform.scale(image, (self.sprite_width * self.scale_factor, self.sprite_height * self.scale_factor))
        
        if flip:
            image = pygame.transform.flip(image, True, False)
            
        image.set_colorkey(BLACK)
        return image
    
class Map:
    def __init__(self, filename):
        self.data = []
        with open (filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILE_SIZE
        self.height = self.tileheight * TILE_SIZE
        
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = - target.rect.centerx + int(DISPLAY_WIDTH / 2)
        y = - target.rect.centery + int(DISPLAY_HEIGHT/ 2) 

        x = min(0, x)
        y = min(0, y)

        x = max(-(self.width - DISPLAY_WIDTH), x)
        y = max(-(self.height - DISPLAY_HEIGHT), y)

        self.camera = pygame.Rect(x, y, self.width, self.height)
        
