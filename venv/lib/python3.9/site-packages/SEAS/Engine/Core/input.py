from SEAS.Engine.Setup import *


class Input:
    def start(self):
        self.keys = pygame.key.get_pressed()

    def updateBefore(self):
        self.keys = pygame.key.get_pressed()
