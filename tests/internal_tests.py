import abc
import pygame
from view.sprite import Sprite
from pygame.locals import *
from utils.vectors import *
from tkinter import *


class Test:
    def __init__(self, main):
        self.main = main


    @abc.abstractmethod
    def onInit(self):
        pass

    @abc.abstractmethod
    def update(self, main, clock):
        pass

    @abc.abstractmethod
    def onEvent(self, event: pygame.event.Event):
        pass


class PlacingTest(Test):
    def __init__(self, main):
        super().__init__(main)
        self.placeable = Sprite("factory-pixel.png")
        self.placeable = Sprite("foundation.png")

        self.placeable.set_layer(2)
        self.main.view.add_sprite(self.placeable)

    def update(self, main = None, clock = None):
        super().update(main, clock)
        x,y = pygame.mouse.get_pos()
        loc = self.main.view.unproject(vec2(x, y))
        self.placeable.set_location(loc)
        
    def onEvent(self, event):
        ''' Placing test with MMB'''
        super().onEvent()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            x,y = pygame.mouse.get_pos()
            loc = self.main.view.unproject(vec2(x, y))
            self.placeable.set_location(loc)
            print(loc)

            placed = self.placeable.copy()
            self.main.view.add_sprite(placed)

class PickingTest(Test):
    ''' Picking test with LMB '''
    def onEvent(self, event):
        super().onEvent()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x,y = event.pos
            result = self.main.view.pick(x, y)
            print(result)
    



class TestBuying(Test):

    def onInit(self):
        from ui.buy_dialog import BuyDialog
        d = BuyDialog(self.main.player)
        self.main.gui.add_widget(d)
