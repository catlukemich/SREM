from utils.vectors import *
from .gui import *
import assets

class BuyDialog(Container):
    def __init__(self, player): # TODO Pass in player object
        super().__init__()

        self.player = player

        font = assets.load_font("Teko-Bold.ttf", 24)
        self.center_horizontally()
        
        self.yes = Text("YES", font)
        self.no = Text("NO", font)

        self.widgets.append(self.yes)
        self.widgets.append(self.no)

        self.yes.align_left()
        self.no.align_right()

        self.dimensions = vec2(230, 30)
        
