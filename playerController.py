from SEAS import *
import copy
import sys


class PlayerController:
    def start(self):
        self.rotAcc = 400
        self.rotVel = 0

        self.acc = 200
        self.vel = 0

        self.trns = SEAS.getScene().getComponent('TransformPoly')
        self.ctrl = SEAS.getScene().getComponent('CharacterPolyController')
        self.coll = SEAS.getScene().getComponent('CollidePoly')

    def update(self):
        self.checkRotations()
        self.checkMovement()
        self.checkDeath()

    def checkDeath(self):
        if self.coll.collide[0] and self.coll.collide[1] == 'Player':
            print("GAME OVER")
            sys.exit()


    def checkRotations(self):
        if SEAS.input('a'):
            self.ctrl.rotate(-self.rotAcc*SEAS.deltaTime)
            self.rotVel = self.rotAcc
        else: self.rotVel = 0

        if SEAS.input('d'):
            self.ctrl.rotate(self.rotAcc*SEAS.deltaTime)
            self.rotVel = -self.rotAcc
        else: self.rotVel = 0

    def checkMovement(self):
        if SEAS.input('w'): self.ctrl.move(vel=self.acc*SEAS.deltaTime, angle=self.trns.angle)
        if SEAS.input('s'): self.ctrl.move(vel=-self.acc*SEAS.deltaTime, angle=self.trns.angle)

class PlayerShooter:
    def start(self):
        self.trns = SEAS.getScene().getComponent('TransformPoly')
        self.ctrl = SEAS.getScene().getComponent('CharacterPolyController')
        self.coll = SEAS.getScene().getComponent('CollidePoly')

        self.useP = SEAS.getScene().getComponent('TransformPoly').points[1]
        self.makeCords = [self.useP, [ self.useP[0]-3, self.useP[1]-13 ], [ self.useP[0]+3, self.useP[1]-13 ]]
        self.makeCordsAngle = 0

        self.lock = False
        self.spamTimeout = 1.2
        self.spamTimeoutCounter = 0
        self.spamCounter = 0
        self.spamSpeed = 1
        self.bulletCount = 50
        
        SEAS.getScene().addText(
                font=SEAS.getCoreModule('Font').getFont('regularFont'),
                textName='bulletCount',
                text=str(self.bulletCount),
                color="#ffffff",
                position=[
                        SEAS.getCoreModule('Screen').wW // 2,
                        20])

    def update(self):
        self.updateVars()
        self.shootBullet()
        self.checkAmmo()
        SEAS.getScene().updateText(
                font=SEAS.getCoreModule('Font').getFont('regularFont'),
                textName='bulletCount',
                text=str(self.bulletCount),
                color="#ffffff")

    def checkAmmo(self):
        if self.coll.collide[0] and self.coll.collide[1] == "Ammo":
            self.bulletCount += 10
            SEAS.getScene().removeRawInitObject(self.coll.collide[2])

    def shootBullet(self):
        if SEAS.input('SPACE'):
            self.spamTimeoutCounter += 2 * SEAS.deltaTime
            if self.spamCounter > 0:
                self.spamCounter -= 10 * SEAS.deltaTime
            self.addBullet()
        else:
            self.spamTimeoutCounter = 0
            self.spamTimoutCounter = 0
            self.spamCounter = 0
            self.lock = False

    def addBullet(self):
        if (self.lock == False or self.spamTimeoutCounter > self.spamTimeout) and self.spamCounter <= 0 and self.bulletCount > 0:
            SEAS.getScene().addObject('bullet', components=[TransformPoly(self.makeCords, self.trns.angle), RenderPoly(), CharacterPolyController(), CollidePoly(), HitboxPoly(), Bullet()])
            ################
            self.lock = True
            ################
            self.spamCounter = self.spamSpeed
            self.bulletCount -= 1

    def updateVars(self):
        self.makeCordsAngle = 0
        self.useP = self.centroid(self.trns.points)
        self.makeCords = [self.useP, [ self.useP[0]-3, self.useP[1]-13 ], [ self.useP[0]+3, self.useP[1]-13 ]]
        self.makeCords, self.makeCordsAngle = self.ctrl.rawRotate(self.makeCords, self.makeCordsAngle, self.trns.angle-90, _axis=self.useP)

    def centroid(self, points):
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

class Bullet:
    def start(self):
        self.trns = SEAS.getScene().getComponent('TransformPoly')
        self.coll = SEAS.getScene().getRawComponent('bullet', 'CollidePoly')
        self.ctrl = SEAS.getScene().getComponent('CharacterPolyController')
        self.bulletSpeed = 10

        SEAS.addRawInitHitboxGroup('Bullet', [SEAS.getScene().getObject()])

    def update(self):
        self.ctrl.move(self.bulletSpeed)

        if not self.trns.isVisible:
            SEAS.getScene().removeObject()

        if self.coll.collide[0] and self.coll.collide[1] == 'Bullet':
            SEAS.getScene().removeObject()
