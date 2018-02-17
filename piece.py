import copy
from graphics import *
from enum import Enum

class Piece:
    def __init__(self, size, color, x, y):
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        if x < 4:
            self.circle = Circle(Point(50 + y*100, 50 + x*100), 10 + size*10)
        else:
            self.circle = Circle(Point(100 + y*100, 500), 10 + size*10)
        self.circle.setFill(color)
    
    def __lt__(self, piece):
        return self.size < piece.size

    def __gt__(self, piece):
        return self.size > piece.size

    def draw(self, window):
        self.circle.draw(window)

    def undraw(self):
        self.circle.undraw()

    def getColor(self):
        return color

    def deepcopy(self):
        new = Piece(copy.deepcopy(self.size),
                    copy.deepcopy(self.color),
                    copy.deepcopy(self.x),
                    copy.deepcopy(self.y))
        return new

    def __str__(self):
        return str(self.size) + " " + self.color

class Piece_Size(Enum):
    small = 0
    medium = 1
    large = 2
    xlarge = 3
