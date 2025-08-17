import os
import pygame
from pygame.locals import *
import assets
import player
from screens.screen import MainMenu, SplashScreen
import view.sprite as sprite
import ui.gui as gui
import world
import ui.interface as interface
from utils.vectors import *
from tkinter import *
from tests.internal_tests import *
from screens.click_chain import * # TODO Make a click chain from splash to main menu

# The main game class that is intantiated on startup.
class Game:

    def __init__(self, w, h):
        # Screen setup
        os.environ['SDL_VIDEO_WINDOW_POS'] = '300,40' 
        pygame.init()
        self.window = pygame.display.set_mode((w, h) ) # TODO Use scaled mode in the future for pixel art
        pygame.display.set_caption("SREM")
        pygame.display.set_icon(assets.loadImage("icon.png"))
        # The onscreen display objects creation:
        self.view = sprite.View(self.window)
        self.gui = gui.Gui(self.window)
        # Player control object
        self.player = player.Player(self)
        # World creation
        self.world = world.World(self)
        # Interface creation
        self.interface = interface.Interface(self)
        self.interface.display()
        # Utilities
        self.done = False  # A flag for the game loop indicating if the game is done playing.
        self.clock = pygame.time.Clock() # Clock to control the framerate

        self.speed = 1 # <-- The game speed - int in range 1 - 4

        self.tests = [ # <-- The current tests to pefrrm while initializing
            # PlacingTest(self),
            # PickingTest(self),
            TestBuying(self)
        ]
        for test in self.tests:
            test.onInit()

        self.screen_chain = ClickChain([
            SplashScreen(), 
            MainMenu(),
            GameScreen()
        ])
            

    def loop(self):
        while not self.done:
            for event in pygame.event.get():
                os_wants_quit = event.type == QUIT
                esc_pressed = event.type == KEYDOWN and event.key == K_ESCAPE

                # Event propagation - from the main game handler to the underlying layers
                # 1. The game layer
                # 2. The UI layer
                # 3. The main world view
                for test in self.tests:
                    test.onEvent(event)
                if os_wants_quit or esc_pressed:
                    self.done = True
                else:
                    self.gui.on_event(event)
                self.view.handle_event(event)
                
                # Game speed handling, propgated to the world for faster/slower simulation
                # and further - to each car present on screen, including spawning of vehicles.
                if event.type == pygame.KEYDOWN:
                    speed_map = { pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4 }
                    self.speed = speed_map[event.key]

            # Update and drawing calls in sequence after events handling
            self.update(self.clock)
            self.draw()

            # Display update and flip using the desired framerate
            framerate = 20
            pygame.display.flip()
            self.clock.tick(framerate)
            

    def update(self, clock : pygame.time.Clock):
        self.view.update()
        self.world.update(clock, self.speed)
        self.interface.update(clock)
        
        for test in self.tests:
            test.update(self, clock)


    def draw(self):
        self.window.fill((0, 0, 0))
        self.view.draw()
        self.gui.draw()
    
 


if __name__ == "__main__":
    w = 800
    h = 420
    game = Game(w, h)
    game.loop()
