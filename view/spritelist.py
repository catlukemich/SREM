class SpriteList():

    def __init__(self):
        self.sprites = []

    def __getitem__(self, idx):
        return self.sprites[idx]
