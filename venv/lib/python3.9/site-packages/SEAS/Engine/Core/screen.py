from SEAS.Engine.Setup import *


class Screen:
    def start(self):
        # 160 	× 	120
        self.wW = 1000 
        self.wH = 1000 
        self.wn = pygame.display.set_mode((self.wW, self.wH))


        # Frame Related
        self.clock = pygame.time.Clock()
        self.frameLimit = 60
        self.frameRate = self.clock.get_fps()


        self.color = "#ffffff"


    def updateBefore(self): # Before updating objects
        self.wn.fill(self.color)

        # Clock
        self.clock.tick(self.frameLimit)
        self.frameRate = self.clock.get_fps()
