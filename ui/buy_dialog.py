from .uiconstants import UIConstants

from utils.vectors import vec2, vec3
from .gui import *
import assets

class BuyDialog(Container):
    ''' The dialog used to buy estates '''

    def __init__(self, player): # TODO Pass in player object
        super().__init__()

        self.player = player



        self.dimensions = vec2(230, 30)
        self.centerHorizontally()

        self.yes = Text("YES", UIConstants.font)
        self.no  = Text("NO", UIConstants.font)

        self.yes.alignLeft(container=self)
        self.no.alignRight(container=self)

        self.widgets.append(self.yes)
        self.widgets.append(self.no)

        self.setTop(30)
        self.setBackground(UIConstants.panel_color)

        
