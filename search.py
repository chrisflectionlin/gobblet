from board import *
import copy
import sys
from eval import evaluate

MAX = sys.maxsize
MIN = -sys.maxsize - 1

def max_value(b, depth, a, be):
    if depth == 0:
        i = evaluate(b.board)
        return (b, i)

    v = (b, MIN)

    """
    This was an attempt to sort the list of generated moves before pruning them,
    but it ended up slowing down the algorithm.

    evalls = []

    for s in b.generate_moves():
        new_b = b.deepcopy()
        new_b.make_move(s)
        evalls.append((s,evaluate(new_b.board)))
    sorted(evalls,key=lambda tup : tup[1],reverse=True)"""
    
    
    for s in b.generate_moves():
        new_b = b.deepcopy()
        new_b.make_move(s)
        value = min_value(new_b, depth - 1, a, be)[1]
        
        if v[1] < value:
            v = (new_b, value)

        if v[1] >= be:
            return v
        a = max(a, v[1])

    return v

def min_value(b, depth, a, be):
    if depth == 0:
        i = evaluate(b.board)
        return (b, i)

    v = (b, MAX)

    """
    This was part of the above attempt to sort the moves.

    evalls = []

    for s in b.generate_moves():
        new_b = b.deepcopy()
        new_b.make_move(s)
        evalls.append((s,evaluate(new_b.board)))
    sorted(evalls,key=lambda tup : tup[1],reverse=False)"""

    for s in b.generate_moves():
        new_b = b.deepcopy()
        new_b.make_move(s)
        value = max_value(new_b, depth - 1, a, be)[1]

        if v[1] > value:
            v = (new_b, value)

        if v[1] <= a:
            return v
        be = min(be, v[1])

    return v
            

def alphabeta_minimax(b, depth, a, be):
    if b.last_move_won(): return -1
    
    if b.playerturn:
        i = max_value(b, depth, a, be)
        move = i[0].unmake_last_move()
        return move

    if not b.playerturn:
        i = min_value(b, depth, a, be)
        move = i[0].unmake_last_move()
        return move

def alphabeta_root(b, depth):
    move = alphabeta_minimax(b, depth, MIN, MAX)

    if move == -1 and b.playerturn:
        return (-1, None)
    elif move == -1 and not b.playerturn:
        return (1, None)
    else:
        return (0, move)
