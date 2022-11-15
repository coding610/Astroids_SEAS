from SEAS.Engine.Setup import *


class Event:
    def start(self):
        pass

    def updateBefore(self): # Check screen for descrition
        self.events = []

        for event in pygame.event.get():
            self.events.append(event)
