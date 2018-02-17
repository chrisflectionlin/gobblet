import piece
from graphics import *
import copy

class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.pieces = []

    def addPiece(self,piece):
        if (self.pieces ==[]):
            self.pieces.append(piece)
        else:
            if(self.pieces[0] < piece):
                self.pieces.insert(0,piece)
            else:
                return "invalid move"
        piece.x = self.row
        piece.y = self.col
        if piece.x < 4:
            piece.circle = Circle(Point(50 + piece.y*100, 50 + piece.x*100), 10 + piece.size*10)
        else:
            piece.circle = Circle(Point(100 + piece.y*100, 500), 10 + piece.size*10)
        piece.circle.setFill(piece.color)

    def getPiece(self):
        if not self.isEmpty():
            p = self.pieces.pop(0)
            p.undraw()
            return p

    def peakPiece(self):
        if not self.isEmpty():
            return self.pieces[0]
        else:
            return None

    def isEmpty(self):
        return self.pieces == []

    def draw(self, window):
        for piece in reversed(self.pieces):
            piece.draw(window)

    def graphCoords(self):
        if self.row < 4:
            return [(self.col*100, (self.col+1)*100), (self.row*100, (self.row+1)*100)]
        else:
            return [(self.col*100 + 50, (self.col+1)*100 + 50), (450, 550)]

    def deepcopy(self):
        temprow = copy.deepcopy(self.row)
        tempcol = copy.deepcopy(self.col)
        temp = Tile(temprow,tempcol)
        for piece in self.pieces:
            temp.pieces.append(piece.deepcopy())
        return temp

    def __str__(self):
        if self.isEmpty():
            return []
        else:
            return str(self.peakPiece())
