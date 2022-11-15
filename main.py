from SEAS import *
from playerController import *
from enemy import *
from ammunition import *

# SCENES
mainScene = SEAS.addScene('mainScene') # I guess u could save it

# OBJECTS
playerCords = [ [110, 110], [115, 125], [120, 110] ]
playerComps = [TransformPoly(playerCords, 90), RenderPoly(), CharacterPolyController(),
               HitboxPoly(), CollidePoly(), PlayerController(), PlayerShooter()]
mainScene.addObject('player', components=playerComps)

mainScene.addObject('enemySpawner', components=[EnemySpawner()])
mainScene.addObject('ammunitionSpawner', components=[AmmunitionSpawner()])

# HITBOX
SEAS.createHitboxGroup('Player', True)
SEAS.createHitboxGroup('Bullet', True)
SEAS.createHitboxGroup('Ammo', True)
SEAS.addRawNameHitboxGroup('Player', ['player'])
SEAS.addRawNameHitboxGroup('Ammo', ['player'])

# FONTS
SEAS.getCoreModule('Font').createFont('regularFont', fontSize=20)
SEAS.getCoreModule('Font').createFont('gmFont', fontSize=70)


# MATERIALS
SEAS.createMaterial('playerMat', '#ffffff')
SEAS.addMaterial('playerMat', 'player')
SEAS.getCoreModule('Screen').color = "#000000"

run()
