import math
import random
import sys

import numpy as np
from SEAS import *

class EnemySpawner:
    def start(self):
        self.spawnCounter = 0
        self.spawnLimit = 6
        self.maxEnemies = 200
        self.totalEnemies = 0
            
        self.enemyShape = [
                [0, 0],
                [-1, 2],
                [-2, 1],
                [-1, 4],
                [0, 5],
                [1, 4],
                [2, 1],
                [1, 2]]

        self.enemySize = 6

    def update(self):
        self.spawnCounter += 1 * SEAS.deltaTime
        if self.spawnCounter > self.spawnLimit and self.totalEnemies < self.maxEnemies:
            # Magnify the enemy
            enemyCords = np.multiply(self.enemySize, self.enemyShape)
            enemyY = []
            enemyX = []
            for e in enemyCords:
                enemyY.append(e[1])
                enemyX.append(e[0])

            # Make spawning point random
            enemyY = np.add(random.randint(1, SEAS.getCoreModule('Screen').wW), enemyY)
            enemyX = np.add(random.randint(1, SEAS.getCoreModule('Screen').wW), enemyX)

            # Relocate the cords
            enemyCords = []
            for x, y in zip(enemyX, enemyY):
                enemyCords.append([x, y])

            SEAS.getScene().addObject('enemy', components=[TransformPoly(enemyCords), RenderPoly(), CharacterPolyController(), HitboxPoly(), Enemy(), CollidePoly()])
            self.spawnCounter = 0
            self.totalEnemies += 1


class Enemy:
    def start(self):
        self.trns = SEAS.getScene().getComponent('TransformPoly')
        self.coll = SEAS.getScene().getComponent('CollidePoly')
        self.ctrl = SEAS.getScene().getComponent('CharacterPolyController')
        self.shtr = SEAS.getScene().getRawComponent('enemySpawner', 'EnemySpawner')
        self.pkll = SEAS.getScene().getRawComponent('player', 'PlayerKill')

        # ADD ME TO HITBOX GROUP BULLET, PLAYER
        SEAS.addRawInitHitboxGroup('Bullet', [SEAS.getScene().getObject()])
        SEAS.addRawInitHitboxGroup('Player', [SEAS.getScene().getObject()])

        self.mSpeed = 100

    def update(self):
        if self.coll.collide[0] and self.coll.collide[1] == 'Bullet':
            self.pkll.kills += 1

            self.shtr.totalEnemies -= 1
            self.shtr.spawnLimit *= 0.95
            self.mSpeed += 1

            SEAS.getScene().removeRawInitObject(self.coll.collide[2])
            SEAS.getScene().removeObject()

        # Move towarads player
        self.movePlayer()

    def movePlayer(self):
        # FIND CENTROID
        sC = self.findCentroid(self.trns.points)
        oC = self.findCentroid(SEAS.getScene().getRawComponent('player', 'TransformPoly').points)

        # Identifying the relative quadrant of Enemy()
        if sC[0] >= oC[0] and sC[1] >= oC[1]: q = "+-"
        elif sC[0] <= oC[0] and sC[1] >= oC[1]: q = "--"
        elif sC[0] <= oC[0] and sC[1] <= oC[1]: q = "-+"
        elif sC[0] >= oC[0] and sC[1] <= oC[1]: q = "++"

        # Angle between sC and oC
        angle = self.findAngle(sC, oC)

        if q == "-+": pass
        elif q == "+-": angle = 180 + angle
        elif q == "++": angle = 90 + angle
        elif q == "--": angle = 270 + angle


        # Move towards player
        self.ctrl.move(vel=self.mSpeed*SEAS.deltaTime, angle=angle)

    def findAngle(self, p1, p2):
        a = abs(p1[1]-p2[1])
        b = abs(p1[0]-p2[0])

        return np.degrees(np.arctan(a/b))

    def findCentroid(self, points):
        centroid = self.axis(points)
        return centroid 
    
    def axis(self, points):
        xPoints = []
        for p in points:
            xPoints.append(p[0])
        yPoints = []
        for p in points:
            yPoints.append(p[1])
        cX = sum(xPoints)/len(xPoints)
        cY = sum(yPoints)/len(yPoints)
        axis = [cX, cY]
        return axis
