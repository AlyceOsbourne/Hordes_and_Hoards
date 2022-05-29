# pygame UI components to build GUIs

class UIElement:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True
        self.properties = {}

    def set_property(self, key, value):
        self.properties[key] = value

    def get_property(self, key):
        return self.properties[key]

    def set_visible(self, visible):
        self.visible = visible

    def set_enabled(self, enabled):
        self.enabled = enabled

    def get_visible(self):
        return self.visible

    def get_enabled(self):
        return self.enabled

    def toggle_visible(self):
        self.visible = not self.visible

    def toggle_enabled(self):
        self.enabled = not self.enabled


