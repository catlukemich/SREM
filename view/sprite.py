from assets import *
from functools import cmp_to_key
from utils.vectors import *
from view.view import View


class Sprite:

    def __init__(self, image, anchor=None):
        """ 
        Create isometric sprite providing the image
        of the sprite and optionally the image anchoring point.
        If the anchoring point argument is missing, then the
        sprite's anchoring point is set to the middle of the image.
        """
        if type(image) == str:
            import assets
            self.image = assets.loadImage(image)
        else:
            self.image = image
        self.location = vec3(0, 0, 0)
        self.layer = 0
        if anchor is None:
            w, h = self.image.get_size()
            self.anchor = vec2(w / 2, h / 2)
        else:
            self.anchor = anchor


    def draw(self, view: View):
        if self.image is None: return

        pos = view.project(self.location)
        draw_x = pos.x - self.anchor.x
        draw_y = pos.y - self.anchor.y

        view.window.blit(self.image, (draw_x, draw_y))


    def set_location(self, location):
        self.location = location


    def get_location(self):
        return self.location


    def set_layer(self, layer):
        self.layer = layer


    def set_image(self, image):
        self.image = image

    def copy(self):
        import copy
        return copy.copy(self)


    def contains(self, view, screen_x : int , screen_y : int):
        ''' 
        Check if the sprite contains the mouse coordinate 
        taking transparent pixels (opacity) into account.
        '''
        w, h = self.image.get_size()
        position = view.project(self.get_location())
        rel_x = int(screen_x - position.x + w / 2)
        rel_y = int(screen_y - position.y + h / 2)
        w, h = self.image.get_size()
        if rel_x > 0 and rel_x < w and rel_y > 0 and rel_y < h:
            pixel = self.image.get_at((rel_x, rel_y))
            if pixel.a > 0:
                return self
            else:
                return False


    def __str__(self):
        return f"Sprite {get_path(self.image)}"