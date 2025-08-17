import os

import pygame.image

images = {} # The cache of images
paths = {} # Pahts - map from image to string
def loadImage(path):
    filepath = "assets" + os.sep + path

    if not filepath in images:
        # If the image is not cached load it and add to the cache:
        try:
            image = pygame.image.load(filepath).convert_alpha()
            images[filepath] = image
            paths[image] = filepath
            return image  
        except Exception as e:
            print("Cant load image: " + filepath)
            raise e
    else:
        # Else just return the cached image:
        return images[filepath]


def get_path(image):
    return paths[image]

fonts = {}

def loadFont(path, size):
    filepath = "assets" + os.sep + path
    key = filepath + str(size)
    if not key in fonts:
        font = pygame.font.Font(filepath, size)
        fonts[key] = font
        return font
    else:
        return fonts[key]


sounds = {}
def load_sound(path):
    filepath = "assets/sounds/" + path
    if not path in sounds:
        sound = pygame.mixer.Sound(filepath)
        sounds[filepath] = sound
        return sound
    else:
        return sounds[filepath]
