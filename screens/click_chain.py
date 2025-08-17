class ClickChain:

    def __init__(self, screens):
        self.screens = screens
        self.current_screen = 0
    
    def display(self):
        self.screens[self.current_screen].display()

    def next(self):
        # Another screen doesn't exist, return false, 
        # indicating, there are no more screens in the chain
        if self.current_screen > len(self.screens) - 1: return False

        # Else - continue switching
        else:
            self.screens[self.current_screen].hide()
            self.current_screen += 1
            self.screens[self.current_screen].display()
            return True