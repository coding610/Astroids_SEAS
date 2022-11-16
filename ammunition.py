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

        self.maxAmmo = 3
        self.totalAmmo = 0

    def update(self):
        self.aCounter -= SEAS.deltaTime
        if self.aCounter <= 0 and self.totalAmmo <= self.maxAmmo:
            self.spawnA([random.randint(1, SEAS.getCoreModule('Screen').wW), random.randint(1, SEAS.getCoreModule('Screen').wH)])
            self.aCounter = 3
            self.totalAmmo += 1

    def spawnA(self, cent):
        cords = self.transformShape(cent)
        SEAS.getScene().addObject('Ammunition', components=[TransformPoly(cords), RenderPoly(), CollidePoly(), HitboxPoly(), Ammunition()])

    def transformShape(self, cent):
        cords = np.multiply(self.ammoShape, self.ammoSize)
        cordsX = []
        cordsY = []

        for c in cords:
            cordsX.append(c[0])
            cordsY.append(c[1])

        cordsX = np.add(cordsX, cent[0])
        cordsY = np.add(cordsY, cent[1])

        cords = []
        for x, y in zip(cordsX, cordsY):
            cords.append([x, y])

        return cords

class Ammunition:
    def start(self):
        SEAS.addRawInitHitboxGroup('Ammo', [SEAS.getScene().getObject()])
        self.coll = SEAS.getScene().getComponent("CollidePoly")
    def update(self): pass
