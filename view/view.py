import pygame
from functools import cmp_to_key
from constants import *
from utils.vectors import *
from .sprite import *
from .spritelist import *

HTW = 36
HTH = 18
VSTEP = 26

class View:

    def __init__(self, window):
        self.center = vec2(0, 0) # <-- The center of the view relative to the world's center
        self.window = window # <-- Reference to the window instance for drawing purposes
        self.sprites: list[Sprite] = [] # <-- List of sprites in the view
        self.scroll_button_down = False # <-- Is the scrolling mouse button pressed


    def project(self, location: vec3) -> vec2:
        x = (location.x - location.y - self.center.x + self.center.y) * HTW
        y = (location.x + location.y - self.center.x - self.center.y) * HTH - location.z * VSTEP

        w, h = self.window.get_size()

        x += w / 2
        y += h / 2

        return vec2(x, y)


    def add_sprite(self, sprite):
        if isinstance(sprite, SpriteList):
            for sprite_element in sprite:
                if not sprite_element in self.sprites:
                    self.sprites.append(sprite_element)
        else:
            if not sprite in self.sprites:
                self.sprites.append(sprite)

    def remove_sprite(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)


    def draw(self):
        self.sort_sprites()

        for sprite in self.sprites:
            sprite.draw(self)


    def sort_sprites(self):
        self.sprites.sort(key=cmp_to_key(self.compare_sprites))


    def compare_sprites(self, sprite1, sprite2):
        if sprite1.layer != sprite2.layer:
            return sprite1.layer - sprite2.layer
        else:
            spr1_loc = sprite1.get_location()
            spr2_loc = sprite2.get_location()

            sum1 = spr1_loc.x + spr1_loc.y + spr1_loc.z
            sum2 = spr2_loc.x + spr2_loc.y + spr2_loc.z

            return sum1 - sum2

    def update(self):
        '''Update the view every second - update means here
        a call to a function every frame, not updating the screen graphics '''
        self.scroll_with_keyboard()


    def scroll_with_keyboard(self):
        ''' Scrolling by keyboard keys '''
        up_key = pygame.K_UP
        down_key = pygame.K_DOWN
        left_key = pygame.K_LEFT
        right_key = pygame.K_RIGHT
        keys = pygame.key.get_pressed()

        rel_x = rel_y = 0
        if keys[up_key]:
            rel_y = 1
        if keys[down_key]:
            rel_y = -1
        if keys[left_key]:
            rel_x = 1
        if keys[right_key]:
            rel_x = -1

        multiplier = 0.1
        new_center = vec2(self.center.x, self.center.y)
        new_center.x -= rel_x * multiplier 
        new_center.y += rel_x * multiplier 
        new_center.x -= rel_y * multiplier
        new_center.y -= rel_y * multiplier

        self.constrain(new_center)


    def unproject(self, position : vec2, iso_z = 0):
        w, h  = self.window.get_size()
        position.x -= w / 2
        position.y -= h / 2
        iso_x = (position.x * HTH + position.y * HTW + HTH * 1 * iso_z) / (2 * HTW * HTH) 
        iso_y = iso_x - position.x / HTW 
        return vec3(iso_x + self.center.x , iso_y + self.center.y , iso_z)

    def pick(self, x, y):
        for sprite in self.sprites:
            sprite = self.sprites[7]
            if sprite.layer == Layer.OBJECTS_LAYER:
                position = self.project(sprite.get_location())
                x -= position.x
                y -= position.y
                print(x)
                if sprite.contains(int(x), int(y)):
                    return sprite



    def handle_event(self, event):
        ''' 
        Event handling code for view manipulation:
        View manipulation includes:
        - scrolling the viewport with mouse or keyboard
        - constraining the viewport to boundaries
        '''
        scroll_button = 3
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == scroll_button:
            self.scroll_button_down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == scroll_button:
            self.scroll_button_down = False

        is_mouse_motion = event.type == pygame.MOUSEMOTION and self.scroll_button_down
        
        if is_mouse_motion:
            if self.scroll_button_down:
                multiplier = 0.03
                rel_x, rel_y = event.rel
                
                new_center = vec2(self.center.x, self.center.y)

                new_center.x -= rel_x * multiplier / 2
                new_center.y += rel_x * multiplier / 2
                new_center.x -= rel_y * multiplier
                new_center.y -= rel_y * multiplier

                self.constrain(new_center)


    def constrain(self, new_center):
        ''' Viewport constraining function '''
        nc = new_center
        distance = 10
        d = distance
        if new_center.x < distance and new_center.x > -distance and new_center.y < distance and new_center.y > -distance:
            self.center = new_center

 
