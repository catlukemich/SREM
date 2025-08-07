import pygame
from utils.vectors import vec2


class Gui:

    def __init__(self, screen):
        self.screen = screen
        self.widgets = []
        self.hover_widget = None
        self.has_button_down = False

    def get_size(self):
        return self.screen.get_size()

    def add_widget(self, widget):
        if not isinstance(widget, Widget):
            raise Exception(str(widget) + " is not a widget")
        self.widgets.append(widget)

    def remove_widget(self, widget):
        self.widgets.remove(widget)

    def on_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            point = vec2(event.pos[0], event.pos[1])

            previous_hover, current_hover = self.find_hover_widget(point)
            self.dispatch_hover_events(previous_hover, current_hover)

            self.hover_widget = current_hover

            if self.hover_widget is not None and self.has_button_down:
                self.hover_widget.onmousedrag(event)

            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            point = vec2(event.pos[0], event.pos[1])
            self.has_button_down = True
            if self.hover_widget is not None:
                consumed = self.hover_widget.on_click()
                previous_hover, current_hover = self.find_hover_widget(point)
                self.dispatch_hover_events(previous_hover, current_hover)
                self.hover_widget = current_hover
                if consumed:
                    return False

        if event.type == pygame.MOUSEBUTTONUP:
            self.has_button_down = False

    def find_hover_widget(self, mouse):
        previous_hover = self.hover_widget
        current_hover = None
        for widget in self.widgets:
            if widget.contains(mouse):
                current_hover = widget
                break

        return (previous_hover, current_hover)

    def dispatch_hover_events(self, previous_hover, current_hover):
        if previous_hover is not current_hover:
            if previous_hover is not None:
                previous_hover.onmouseout()
            if current_hover is not None:
                current_hover.onmouseover()

    def draw(self):
        for widget in reversed(self.widgets):
            widget.draw(self.screen)



class Widget:
    def __init__(self):
        self.position = vec2(0, 0)
        self.dimensions = vec2(0, 0)


    def contains(self, point):
        if point.x > self.position.x and point.x < self.position.x + self.dimensions.x \
                and point.y > self.position.y and point.y < self.position.y + self.dimensions.y:
            return True
        else:
            return False

    def on_click(self):
        return False

    def onmouseover(self):
        pass

    def onmouseout(self):
        pass

    def onmousedrag(self, event):
        pass

    def draw(self, screen):
        pass

    def align_right(self):
        w, _ = pygame.display.get_surface().get_size()
        if hasattr(self, 'image'):
            im_w, _ = self.image.get_size()
            new_x = w - im_w
            self.set_position(new_x, self.position.y)

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position


class ImageWidget(Widget):
    def __init__(self, image):
        Widget.__init__(self)
        self.image = image
        w, h = image.get_size()
        self.dimensions = vec2(w, h)

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))

    def set_image(self, image):
        self.image = image


class Button(Widget):
    def __init__(self, image, command = None):
        Widget.__init__(self)
        self.command = command
        self.image = image
        w, h = image.get_size()
        self.dimensions = vec2(w, h)

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))

    def on_click(self):
        if self.command is not None:
            self.command()

    def onmouseover(self):
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    def onmouseout(self):
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

class Text(Widget):
    def __init__(self, text, font, color=(0, 0, 0)):
        Widget.__init__(self)
        self.text = text
        self.font = font
        self.color = color
        self.surface = None
        self.create_surface()

    def set_text(self, text):
        self.text = text
        self.create_surface()

    def set_color(self, color):
        self.color = color
        self.create_surface()

    def create_surface(self):
        self.surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.surface, (self.position.x, self.position.y))


class Slider(Widget):
    def __init__(self, rail_img, knob_img, value_change_func):
        Widget.__init__(self)
        self.rail_img = rail_img
        self.knob_img = knob_img
        self.value_change_func = value_change_func
        self.percentage = 50
        self.knob_x = 0
        rail_w, rail_h = rail_img.get_size()
        knob_w, knob_h = knob_img.get_size()
        w = rail_w
        h = knob_h
        self.dimensions = vec2(w, h)
        self.recalculate_knob_x()


    def draw(self, screen):
        rail_w, rail_h = self.rail_img.get_size()
        knob_w, knob_h = self.knob_img.get_size()
        rail_y = (knob_h - rail_h) / 2
        screen.blit(self.rail_img, (self.position.x, self.position.y + rail_y))
        screen.blit(self.knob_img, (self.position.x + self.knob_x, self.position.y))


    def onmousedrag(self, event):
        rel_x = event.pos[0] - self.position.x
        rel_y = event.pos[1] - self.position.y

        if rel_x > 0 and rel_x < self.dimensions.x and rel_y > 0 and rel_y < self.dimensions.y:
            percentage = rel_x / (self.dimensions.x) * 100
            self.knob_x = rel_x - self.knob_img.get_width() / 2
            self.percentage = percentage
            self.value_change_func(percentage)

    def set_percentage(self, percentage):
        self.percentage = percentage
        self.recalculeate_knob_x()

    def recalculate_knob_x(self):
        rel_x = self.percentage / 100 * self.dimensions.x
        self.knob_x = rel_x - self.knob_img.get_width() / 2
