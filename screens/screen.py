from globvars import *
import assets
import pygame
import abc
from ui.gui import *

class Screen:

    @staticmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def display(self):
        pass

    @abc.abstractmethod
    def hide(self):
        pass

class SplashScreen(Screen):

    def __init__(self):
        super().__init__()

    def show(self):
        splash_image = assets.loadImage("assets/logo.png")
        image_widget = ImageWidget(splash_image) 
        gui.addWidget(image_widget)


class MainMenu(Screen):

    def __init__(self):
        super().__init__()


class GameScreen(Screen):

    def __init__(self):
        super().__init__()

    def show(self):
        splash_image = assets.loadImage("assets/factory.png")
        image_widget = ImageWidget(splash_image) 
        gui.addWidget(image_widget)



        