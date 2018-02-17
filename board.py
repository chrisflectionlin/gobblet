import numpy as np
from tiles import *
from piece import *
from move import *
from eval import evaluate

class Board:
    def __init__(self):
        self.playerturn = True #True is player1 false is player2
        self.board = [[Tile(0,0),Tile(0,1),Tile(0,2),Tile(0,3)],
                      [Tile(1,0),Tile(1,1),Tile(1,2),Tile(1,3)],
                      [Tile(2,0),Tile(2,1),Tile(2,2),Tile(2,3)],
                      [Tile(3,0),Tile(3,1),Tile(3,2),Tile(3,3)]]
        
        self.movesP1 = []
        self.movesP2 = []
        
        self.hpieces = [Tile(4,0), Tile(4,1), Tile(4,2)]
        for i in range(0,3):
            for size in Piece_Size:
                self.hpieces[i].addPiece(Piece(size.value, "red", 4, i))
                                    
        self.cpieces = [Tile(5,0), Tile(5,1), Tile(5,2)]
        for i in range(0,3):
            for size in Piece_Size:
                self.cpieces[i].addPiece(Piece(size.value, "blue", 5, i))

    def empty_space(self):
        empty = []
        for i in range(0,4):
            for j in range(0,4):
                tile = self.board[i][j]
                if tile.isEmpty():
                    empty.append((tile.row, tile.col))
        return empty

    def opponent_spaces(self):
        non_empty = []
        for i in range(0,4):
            for j in range(0,4):
                tile = self.board[i][j]
                piece = tile.peakPiece()
                if not tile.isEmpty():
                    if self.playerturn:
                        if piece.color == "blue":
                            non_empty.append(((tile.row, tile.col), piece))
                    if not self.playerturn:
                        if piece.color == "red":
                            non_empty.append(((tile.row, tile.col), piece))
        return non_empty

    def my_spaces(self):
        mine = []
        for i in range(0,4):
            for j in range(0,4):
                tile = self.board[i][j]
                piece = tile.peakPiece()
                if not tile.isEmpty():
                    if self.playerturn:
                        if piece.color == "red":
                            mine.append(((tile.row, tile.col), piece))
                    if not self.playerturn:
                        if piece.color == "blue":
                            mine.append(((tile.row, tile.col), piece))
        return mine

    """def count_tiles(self):
        count = 0
        for i in range(0,4):
            for j in range(0,4):
                if self.board[i][j].pieces == []:
                    count+=1
        return count"""

    def generate_moves(self): #return a list of moves
        moves=[]
        empties = self.empty_space()
        opponents = self.opponent_spaces()
        mine = self.my_spaces()
        #corners = [(0,0),(3,3),(3,0),(0,3)]

        """
        We attempted to speed up the algorithm by generating moves that led to
        corner Tiles when the board was relatively empty. This ended up slowing
        down the algorithm.

        if self.count_tiles()<3:
            for i in range(0,3):
                if self.playerturn:
                    tile=self.hpieces[i]
                    if not tile.isEmpty():
                        piece = tile.peakPiece()
                        for to in corners:
                            moves.append(Move(piece.x, piece.y, to[0], to[1]))
                else:
                    tile = self.cpieces[i]
                    if not tile.isEmpty():
                        piece = tile.peakPiece()
                        for to in corners:
                            moves.append(Move(piece.x, piece.y, to[0], to[1]))                   
                
        
          else:"""
        #Possible moves for each players' pieces not on the board
        for i in range(0,3):
            if self.playerturn:
                tile = self.hpieces[i]
                if not tile.isEmpty():
                    piece = tile.peakPiece()
                    for to in empties:
                        moves.append(Move(piece.x, piece.y, to[0], to[1]))
            else:
                tile = self.cpieces[i]
                if not tile.isEmpty():
                    piece = tile.peakPiece()
                    for to in empties:
                        moves.append(Move(piece.x, piece.y, to[0], to[1]))

        #Possible moves for each players' pieces on the board
        for space in mine:
            pos = space[0]
            piece = space[1]
            for to in empties:
                moves.append(Move(pos[0], pos[1], to[0], to[1]))
            for to in opponents:
                op_pos = to[0]
                op_piece = to[1]
                if piece > op_piece:
                    moves.append(Move(pos[0], pos[1], op_pos[0], op_pos[1]))

        """
        This was an attempt to sort the list of generated moves but ended up
        slowing down the algorithm.


        evalls = []
 
        for m in moves:
            new_b = self.deepcopy()
            new_b.make_move(m)
            evalls.append((m,evaluate(new_b.board)))

        moves = []

        if self.playerturn:
            highToLow = True
        else:
            highToLow = False
            
        sorted(evalls,key=lambda tup : tup[1],reverse=highToLow)

        for tup in evalls:
            moves.append(tup[0])
        """
            
        
        return moves

    def make_move(self, move):
        start = move.start
        end = move.end
        board = self.board
        if start[0] == 4:
            start_tile = self.hpieces[start[1]]
        elif start[0] == 5:
            start_tile = self.cpieces[start[1]]
        else:
            start_tile = board[start[0]][start[1]]
        end_tile = board[end[0]][end[1]]

        piece = start_tile.getPiece()
        end_tile.addPiece(piece)

        if self.playerturn:
            self.movesP1.append(move)
            self.playerturn = False
        else:
            self.movesP2.append(move)
            self.playerturn = True

    def unmake_last_move(self):
        if self.playerturn:
            move = self.movesP2.pop()
            end = move.start
            start = move.end
            board = self.board
            
            if end[0] == 4:
                end_tile = self.hpieces[end[1]]
            elif end[0] == 5:
                end_tile = self.cpieces[end[1]]
            else:
                end_tile = board[end[0]][end[1]]

            start_tile = board[start[0]][start[1]]

            piece = start_tile.getPiece()
            end_tile.addPiece(piece)
            self.playerturn = False
            return move
        else:
            move = self.movesP1.pop()
            end = move.start
            start = move.end
            board = self.board
            
            if end[0] == 4:
                end_tile = self.hpieces[end[1]]
            elif end[0] == 5:
                end_tile = self.cpieces[end[1]]
            else:
                end_tile = board[end[0]][end[1]]

            start_tile = board[start[0]][start[1]]

            piece = start_tile.getPiece()
            end_tile.addPiece(piece)
            self.playerturn = True
            return move

    def last_move_won(self):
        color = ""
        
        if self.playerturn:
            color = "blue"
        else:
            color = "red"

        #Horizontal Win
        for row in range(4):
            if self.board[row][0].peakPiece() != None and self.board[row][1].peakPiece() != None and self.board[row][2].peakPiece() != None and self.board[row][3].peakPiece() != None:
                if self.board[row][0].peakPiece().color == color and self.board[row][1].peakPiece().color == color and self.board[row][2].peakPiece().color == color and self.board[row][3].peakPiece().color == color:
                    return True

        #Vertical Win
        for col in range(4):
            if self.board[0][col].peakPiece() != None and self.board[1][col].peakPiece() != None and self.board[2][col].peakPiece() != None and self.board[3][col].peakPiece() != None:
                if self.board[0][col].peakPiece().color == color and self.board[1][col].peakPiece().color == color and self.board[2][col].peakPiece().color == color and self.board[3][col].peakPiece().color == color:
                    return True

        #Diagonal Win
        if self.board[0][0].peakPiece() != None and self.board[1][1].peakPiece() != None and self.board[2][2].peakPiece() != None and self.board[3][3].peakPiece() != None:
            if self.board[0][0].peakPiece().color == color and self.board[1][1].peakPiece().color == color and self.board[2][2].peakPiece().color == color and self.board[3][3].peakPiece().color == color:
                return True

        if self.board[0][3].peakPiece() != None and self.board[1][2].peakPiece() != None and self.board[2][1].peakPiece() != None and self.board[3][0].peakPiece() != None:
            if self.board[0][3].peakPiece().color == color and self.board[1][2].peakPiece().color == color and self.board[2][1].peakPiece().color == color and self.board[3][0].peakPiece().color == color:
                return True

        return False

    def deepcopy(self):
        b = Board()
        b.playerturn = copy.deepcopy(self.playerturn)
        for row in range(4):
            for col in range(4):
                tileCopy = self.board[row][col].deepcopy()
                b.board[row][col] = tileCopy

        b.movesP1 = copy.deepcopy(self.movesP1)
        b.movesP2 = copy.deepcopy(self.movesP2)

        for i in range(3):
            tileCopy1 = self.hpieces[i].deepcopy()
            tileCopy2 = self.cpieces[i].deepcopy()
            b.hpieces[i] = tileCopy1
            b.cpieces[i] = tileCopy2

        return b
            
    
    def __str__(self):
        matrix = self.board
        temp = ""
        for i in matrix:
            for j in i:
                if j.pieces == []:
                    temp = temp + "EMP" + " "
                else:
                    if j.peakPiece().color == "red":
                        if j.peakPiece().size == 0:
                            temp = temp + "S:P1"+ " "
                        if j.peakPiece().size == 1:
                            temp = temp + "M:P1"+ " "
                        if j.peakPiece().size == 2:
                            temp = temp + "L:P1"+ " "
                        if j.peakPiece().size == 3:
                            temp = temp + "X:P1"+ " "
    
                    if j.peakPiece().color == "blue":
                        if j.peakPiece().size == 0:
                            temp = temp + "S:P2"+ " "
                        if j.peakPiece().size == 1:
                            temp = temp + "M:P2"+ " "
                        if j.peakPiece().size == 2:
                            temp = temp + "L:P2"+ " "
                        if j.peakPiece().size == 3:
                            temp = temp + "X:P2"+ " "
                if i.index(j) == len(i)-1:
                    temp = temp + "\n"
                    
        temp = temp + "\n"
        temp = temp + "Player1: "
        
        for tile in self.hpieces:
            tempsize = tile.peakPiece().size
            if tempsize == 0:
                temp = temp + "S" + " "
            if tempsize == 1:
                temp = temp + "M" + " "
            if tempsize == 2:
                temp = temp + "L"+ " "
            if tempsize == 3:
                temp = temp + "XL" + " "
        temp = temp + "\n"
        
        temp = temp + "Player2: "
        for tile in self.cpieces:
            tempsize = tile.peakPiece().size
            if tempsize == 0:
                temp = temp + "S" + " "
            if tempsize == 1:
                temp = temp + "M" + " "
            if tempsize == 2:
                temp = temp + "L"+ " "
            if tempsize == 3:
                temp = temp + "XL" + " "

        temp = temp + "\n"
        
        return temp
