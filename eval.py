from board import *
from piece import *
from tiles import *


def evaluate(board):
    return horizontals(board) + verticals(board) + diag1(board) + diag2(board)

def horizontals(board):
    score = 0
    tally = 0
    for row in range(4):
        row_score = 0
        for col in range(4):
            piece = board[row][col].peakPiece()
            if piece != None:
                if piece.color == "red":
                    row_score += piece.size
                    tally += 1
                if piece.color == "blue":
                    row_score -= piece.size
                    tally -= 1
        score += row_score
        if tally == 4:
            score += 10000
        elif tally == -4:
            score -= 10000

    return score

def verticals(board):
    score = 0
    tally = 0
    for col in range(4):
        col_score = 0
        for row in range(4):
            piece = board[row][col].peakPiece()
            if piece != None:
                if piece.color == "red":
                    col_score += piece.size
                    tally += 1
                if piece.color == "blue":
                    col_score -= piece.size
                    tally -= 1
        score += col_score
        if tally == 4:
            score += 10000
        elif tally == -4:
            score -= 10000

    return score

def diag1(board):
    pieces = []
    piece1 = board[0][0].peakPiece()
    pieces.append(piece1)
    piece2 = board[1][1].peakPiece()
    pieces.append(piece2)
    piece3 = board[2][2].peakPiece()
    pieces.append(piece3)
    piece4 = board[3][3].peakPiece()
    pieces.append(piece4)

    score = 0
    tally = 0
    for p in pieces:
        if p != None:
            if p.color == "red":
                score += p.size
                tally += 1
            if p.color == "blue":
                score -= p.size
                tally -= 1

    if tally == 4:
        score += 10000
    elif tally == -4:
        score -= 10000

    return score

def diag2(board):
    pieces = []
    piece1 = board[0][3].peakPiece()
    pieces.append(piece1)
    piece2 = board[1][2].peakPiece()
    pieces.append(piece2)
    piece3 = board[2][1].peakPiece()
    pieces.append(piece3)
    piece4 = board[3][0].peakPiece()
    pieces.append(piece4)

    score = 0
    tally = 0
    for p in pieces:
        if p != None:
            if p.color == "red":
                score += p.size
                tally += 1
            if p.color == "blue":
                score -= p.size
                tally -= 1

    if tally == 4:
        score += 10000
    elif tally == -4:
        score -= 10000

    return score

