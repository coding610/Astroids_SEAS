from typing import Any
from SEAS.Engine.Setup import *


class Font:
    def start(self):
        self.fonts = {}

    def updateBefore(self): pass
    def update(self): pass

    def createFont(self, fontName:str, fontType:str='freesansbold.ttf', fontSize:int=20) -> None:
        self.fonts[fontName] = pygame.font.Font(fontType, fontSize)
        return self.fonts[fontName]

    def getFont(self, fontName:str) -> Any:
        return self.fonts[fontName]
