class SpriteList():
    '''
    Spritelist is just a collection of sprites.
    It's use is to simplify the view API such that
    adding a collection by using the add_sprite 
    method works.
    '''

    def __init__(self):
        self.sprites = [] # <-- The sprites belonging to the SpriteList
 
    def __getitem__(self, idx):
        ''' 
        This enables the SpriteList instances 
        to be treated as a Python list.
        '''
        return self.sprites[idx]

    