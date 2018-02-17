from graphics import *
from search import *
from board import *
from tiles import *
from piece import *

class Game:
    def __init__(self, window, board):
        self.window = window
        self.board = board
        
        col1 = Line(Point(100, 0), Point(100, 400))
        col1.setWidth(5)
        col1.draw(self.window)
        col2 = Line(Point(200, 0), Point(200, 400))
        col2.setWidth(5)
        col2.draw(self.window)
        col3 = Line(Point(300, 0), Point(300, 400))
        col3.setWidth(5)
        col3.draw(self.window)
        row1 = Line(Point(0, 100), Point(400, 100))
        row1.setWidth(5)
        row1.draw(self.window)
        row2 = Line(Point(0, 200), Point(400, 200))
        row2.setWidth(5)
        row2.draw(self.window)
        row3 = Line(Point(0, 300), Point(400, 300))
        row3.setWidth(5)
        row3.draw(self.window)
        border = Line(Point(0, 425), Point(400, 425))
        border.setFill("saddlebrown")
        border.setWidth(50)
        border.draw(self.window)

        for tile in board.hpieces:
            tile.draw(window)

    def player(self):
        moveDone = False
        move = []
        toPlay = None

        while not moveDone:
            mouse = self.window.getMouse()

            if toPlay == None:
                for i in range(5):
                    for j in range(4):
                        if i < 4:
                            tile = self.board.board[i][j]
                            coords = tile.graphCoords()
                            if coords[0][0] <= mouse.getX() and coords[0][1] >= mouse.getX() and coords[1][0] <= mouse.getY() and coords[1][1] >= mouse.getY():
                                toPlay = tile.peakPiece()
                                if toPlay == None:                                    continue
                                if toPlay.color == "blue":
                                    toPlay = None
                                    continue
                                toPlay.undraw()
                                move.append(tile.row)
                                move.append(tile.col)
                        else:
                            if j < 3:
                                tile = self.board.hpieces[j]
                                coords = tile.graphCoords()
                                if coords[0][0] <= mouse.getX() and coords[0][1] >= mouse.getX() and coords[1][0] <= mouse.getY() and coords[1][1] >= mouse.getY():
                                    toPlay = tile.peakPiece()
                                    if toPlay == None:
                                        continue
                                    toPlay.undraw()
                                    move.append(tile.row)
                                    move.append(tile.col)
                continue
            else:
                for i in range(4):
                    for j in range(4):
                        tile = self.board.board[i][j]
                        coords = tile.graphCoords()
                        if coords[0][0] <= mouse.getX() and coords[0][1] >= mouse.getX() and coords[1][0] <= mouse.getY() and coords[1][1] >= mouse.getY():
                            if tile.isEmpty() or (tile.peakPiece() < toPlay and tile.peakPiece().color == "blue"):
                                self.board.make_move(Move(move[0],move[1],tile.row,tile.col))
                                toPlay.draw(self.window)
                                toPlay = None
                                moveDone = True

    def computer(self, depth):
        board = self.board
        if not board.last_move_won():
            turn = alphabeta_root(board, depth)
            if turn[0] == 0:
                start_coords = turn[1].start
                end_coords = turn[1].end
                if start_coords[0] < 4:
                    start_tile = board.board[start_coords[0]][start_coords[1]]
                else:
                    start_tile = board.cpieces[start_coords[1]]
                end_tile = board.board[end_coords[0]][end_coords[1]]
                toPlay = start_tile.peakPiece()
                toPlay.undraw()
                board.make_move(Move(start_tile.row, start_tile.col, end_tile.row, end_tile.col))
                toPlay.draw(self.window)

def play(game, difficulty):
    inProgress = True

    while inProgress:
        game.player()
        if game.board.last_move_won():
            print("Human wins!")
            break
        game.computer(difficulty)
        if game.board.last_move_won():
            print("Computer wins!")
            break

def main():
    board = Board()
    window = GraphWin("Gobblet",400,550)
    window.setBackground("tan")
    game = Game(window, board)
    play(game, 2)
    
main()
