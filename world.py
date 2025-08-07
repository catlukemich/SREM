import random
import pygame
from utils.utlis import *
from buildings.building import *
from vehicles.car import *
from vehicles.chopper import *
from constants import *
from utils.vectors import *
from path import *

class World:
    '''
    The world class, where everything visible in the view belongs.
    '''
    def __init__(self, main):
        self.main = main
        self.month = 1 # The current world month
        self.day = 1   # The current world day
        self.time = 0  # The time used to update month and day
        self.paths = []
        self.cars  = []
        self.spawn_time = 0 # Car spawn time
        self.chopper = Chopper(self)

        self.create_building()
        self.create_paths()
        self.place_objects()


    def place_objects(self):
        ''' Create ground - thst is - the terrain and the roads. '''
        self.place("land.png", layer = Layer.TERRAIN_LAYER)
        self.place("roads.png", layer = Layer.OVERLAYS_LAYER)
        self.place("park1.png", (9,9,0))
        self.place("park2.png", (3.1, 9, 0))
        self.place("parking.png", (1.6, -6, 0))

        ''' Create the factory in the top-right corner of the screen '''
        self.place("factory.png", (-3.05, -9, 0))
        self.place("factory-pixel.png", (-3.25, -3.8, 0))
        self.place("foundation.png", (-2.899, 2.968, 0))


    def get_month(self):
        return self.month

    def get_day(self):
        return self.day


    def create_building(self):
        ''' Create the main building, the Real Estate '''
        view = self.main.view

        self.building = Building(view)
        self.building.add_to_view()

    def place(self, image_path, loc : tuple = (0, 0, 0), layer = Layer.OBJECTS_LAYER):
            ''' Utility inner function for placing new sprites '''
            view = self.main.view
            building = Sprite(load_image(image_path))
            building.set_layer(layer)
            location = vec3(loc[0], loc[1], loc[2])
            building.set_location(location)

            view.add_sprite(building)
            return building


    def create_paths(self):
        '''
        Create paths that the cars will use to travel.
        '''
        # Bottom row
        path = Path(vec3(6.25, 15), vec3(6.25, -12.5), Heading.NORTH)
        self.paths.append(path)

        path = Path(vec3(5.75, -12.5), vec3(5.75, 15),  Heading.SOUTH)
        self.paths.append(path)

        # Middle row
        path = Path(vec3(0.25, 10), vec3(0.25, -12.5), Heading.NORTH)
        self.paths.append(path)

        path = Path(vec3(-0.25, -12.5), vec3(-0.25, 10), Heading.SOUTH)
        self.paths.append(path)

        # Top row
        path = Path(vec3(-5.75, 26), vec3(-5.75, -26.5), Heading.NORTH)
        self.paths.append(path)

        path = Path(vec3(-6.25, -36.5), vec3(-6.25, 36), Heading.SOUTH)
        self.paths.append(path)

    def update(self, clock, speed):
        if self.time > Gameplay.MILLIS_PER_DAY / speed:
            self.day += 1
            if self.day > 30:
                self.month += 1
                self.day = 1
            self.time = self.time - Gameplay.MILLIS_PER_DAY / speed
            if self.day == 30:
                player = self.main.player
                self.on_day(self.month, self.day)
                player.on_day(self.month, self.day)

        self.time += clock.get_time()

        self.spawn_cars(clock)
        self.update_cars(clock, speed)
        self.building.update(clock)
        self.chopper.update(clock)

    def on_day(self, month, day):
        if day == 30:
            self.building.update_contentment()

   
    def spawn_cars(self, clock):
        '''
        Spawn cars if their number is below certain threshold.
        '''
        view = self.main.view

        max_cars = self.building.get_level() * 2
        if len(self.cars) <  max_cars:
            if self.spawn_time > 500:
                path = random.choice(self.paths)
                car = Car(path)
                self.cars.append(car)
                view.add_sprite(car)
                self.spawn_time = 0

        self.spawn_time += clock.get_time()

    def update_cars(self, clock, speed):
        '''
        Update all the cars - animate their driving animation.
        '''
        for car in self.cars:
            keep_car = car.update(clock, speed) # <-- Update the car with the current game speed (vals 1 - 4)
            if keep_car == False:
                self.cars.remove(car)
                self.main.view.remove_sprite(car)
