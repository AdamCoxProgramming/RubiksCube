import copy
import math
from enum import Enum, IntEnum

class Container:
    def __init__(self,item,pos):
        self.item = item
        self.pos = pos

class Grid:
    def __init__(self):
        self.items = {}

    def getContianerForPos(self,pos):
        return Container(self.items[(pos.x,pos.y,pos.z)],pos)

    def getContianersWhere(self,x,y,z):
        items = []
        for key, value in self.items.items():
            use = True
            if x != None:
                if x != key[0]:
                    use = False
            if y != None:
                if y != key[1]:
                    use = False
            if z != None:
                if z != key[2]:
                    use = False
            if use:
                items.append(Container(value,Position(key[0],key[1],key[2])))
        return items

    def setItemAtPos(self,item, pos):
        self.items[(pos.x,pos.y,pos.z)] = item

class Position:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class Faces(Enum):
     FRONT = 0
     BACK = 1
     TOP = 2
     BOTTOM = 3
     LEFT = 4
     RIGHT = 5

class RubiksCube:
    def __init__(self):
        self.grid = Grid()
        self.addPiecesToGrid()

    def addPiecesToGrid(self):
        for x in range(3):
            x = x -1
            for y in range(3):
                y = y -1
                for z in range(3):
                    z = z -1
                    self.grid.setItemAtPos(Piece(),Position(x,y,z))

        allContainers = self.grid.getContianersWhere(None,None,None)
        for container in allContainers:
            if container.pos.x == 1:
                container.item.setSide(Colors.BLUE,Faces.RIGHT)
            if container.pos.x == -1:
                container.item.setSide(Colors.GREEN,Faces.LEFT)
            if container.pos.y == 1:
                container.item.setSide(Colors.ORANGE,Faces.TOP)
            if container.pos.y == -1:
                container.item.setSide(Colors.RED,Faces.BOTTOM)
            if container.pos.z == 1:
                container.item.setSide(Colors.WHITE,Faces.FRONT)
            if container.pos.z == -1:
                container.item.setSide(Colors.YELLOW,Faces.BACK)

    def viewFace(self,face):
        containers = self._getContainersForFace(face)
        res = []
        for container in containers:
            res.append(container.item.getColorForSide(face))
        return res

    def rotateFace(self, face,direction):
        if direction == 0:
            self._rotateFace(face)
        else:
            self._rotateFace(face)
            self._rotateFace(face)
            self._rotateFace(face)

    def _rotateFace(self,face):
        containers = self._getContainersForFace(face)
        axis = ''
        if face == Faces.LEFT or face == Faces.RIGHT:
            axis = 'x'
        if face == Faces.TOP or face == Faces.BOTTOM:
            axis = 'y'
        if face == Faces.FRONT or face == Faces.BACK:
            axis = 'z'
        gridCopy = copy.deepcopy(self.grid)
        for container in containers:
            newPos = None
            if axis == 'x':
                rotatedPos = self.rotateAroundOrigin((container.pos.y, container.pos.z), -1.5708)
                newPos = Position(container.pos.x, rotatedPos[0], rotatedPos[1])
            elif axis == 'y':
                rotatedPos = self.rotateAroundOrigin((container.pos.x, container.pos.z), -1.5708)
                newPos = Position(rotatedPos[0], container.pos.y, rotatedPos[1])
            elif axis == 'z':
                rotatedPos = self.rotateAroundOrigin((container.pos.x, container.pos.y), -1.5708)
                newPos = Position(rotatedPos[0], rotatedPos[1], container.pos.z)
            container.item.rotate(axis)
            gridCopy.setItemAtPos(container.item, newPos)
        self.grid = gridCopy
        self.selfTest()


    def rotateAroundOrigin(self, xy, radians):
        x, y = xy
        xx = x * math.cos(radians) + y * math.sin(radians)
        yy = -x * math.sin(radians) + y * math.cos(radians)
        return round(xx), round(yy)

    def selfTest(self):
        def getAllFaces():
            front = self.viewFace(Faces.FRONT)
            back = self.viewFace(Faces.BACK)
            top = self.viewFace(Faces.TOP)
            bottom = self.viewFace(Faces.BOTTOM)
            left = self.viewFace(Faces.LEFT)
            right = self.viewFace(Faces.RIGHT)
            return front + back + top + bottom + left + right
        allFaces = getAllFaces()
        most = max(allFaces, key=allFaces.count)
        if allFaces.count(most) != 9:
            raise Exception()

    def _getContainersForFace(self, face):
        switcher = {
            Faces.FRONT: Position(None,None,1),
            Faces.BACK: Position(None,None,-1),
            Faces.TOP: Position(None,1,None),
            Faces.BOTTOM: Position(None, -1, None),
            Faces.LEFT: Position(-1,None,None),
            Faces.RIGHT: Position(1,None,None),
        }
        xyz = switcher.get(face)
        return copy.deepcopy(self.grid.getContianersWhere(xyz.x,xyz.y,xyz.z))

class Colors(IntEnum):
    RED = 0
    BLUE = 1
    ORANGE = 2
    GREEN = 3
    WHITE = 4
    YELLOW = 5

class Piece:
    def __init__(self):
        self.sides = {}

    def setSide(self,color,face):
        self.sides[face] = color

    def getColorForSide(self,face):
        if self.sides[face] == None:
            raise Exception()
        return self.sides[face]

    def rotate(self,axis):
        sidesCopy = copy.copy(self.sides)
        if axis == 'x':
            sidesCopy[Faces.TOP] = self.sides.get(Faces.BACK)
            sidesCopy[Faces.FRONT] = self.sides.get(Faces.TOP)
            sidesCopy[Faces.BOTTOM] = self.sides.get(Faces.FRONT)
            sidesCopy[Faces.BACK] = self.sides.get(Faces.BOTTOM)
        elif axis =='y':
            sidesCopy[Faces.RIGHT] = self.sides.get(Faces.BACK)
            sidesCopy[Faces.FRONT] = self.sides.get(Faces.RIGHT)
            sidesCopy[Faces.LEFT] = self.sides.get(Faces.FRONT)
            sidesCopy[Faces.BACK] = self.sides.get(Faces.LEFT)
        elif axis =='z':
            sidesCopy[Faces.TOP] = self.sides.get(Faces.RIGHT)
            sidesCopy[Faces.LEFT] = self.sides.get(Faces.TOP)
            sidesCopy[Faces.BOTTOM] = self.sides.get(Faces.LEFT)
            sidesCopy[Faces.RIGHT] = self.sides.get(Faces.BOTTOM)
        self.sides = sidesCopy