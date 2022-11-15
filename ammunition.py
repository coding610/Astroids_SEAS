from SEAS import *
import numpy as np
import random


class AmmunitionSpawner:
    def start(self):
        self.aCounter = 2
        self.ammoShape = [
                [10, 6],
                [8, 12],
                [8, 15],
                [12, 15],
                [12, 12]]

        self.ammoSize = 2

    def update(self):
        self.aCounter -= SEAS.deltaTime

        if self.aCounter <= 0:
            self.spawnA()
            self.aCounter = 3

    def spawnA(self):
        cords = self.transformShape()
        SEAS.getScene().addObject('Ammunition', components=[TransformPoly(cords), RenderPoly(), CollidePoly(), HitboxPoly(), Ammunition()])

    def transformShape(self):
        cords = np.multiply(self.ammoShape, self.ammoSize)
        cordsX = []
        cordsY = []
        for c in cords:
            cordsX.append(c[0])
            cordsY.append(c[1])
        cordsX = np.add(cordsX, random.randint(1, SEAS.getCoreModule('Screen').wW))
        cordsY = np.add(cordsY, random.randint(1, SEAS.getCoreModule('Screen').wH))
        cords = []
        for x, y in zip(cordsX, cordsY):
            cords.append([x, y])

        return cords

class Ammunition:
    def start(self):
        SEAS.addRawInitHitboxGroup('Ammo', [SEAS.getScene().getObject()])
        self.coll = SEAS.getScene().getComponent("CollidePoly")
    def update(self): pass
