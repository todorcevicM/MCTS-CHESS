# -*- coding: utf-8 -*-
"""
Created on Sun May 16 23:19:58 2021

@author: Nikola
"""

import chess
import numpy as np
import time


def playout(board):
    n = 20;
    while(n):
        n -= 1
        if(board.is_check()):
            break
        legal = list(board.generate_legal_moves())
        board.push((legal[(int)(np.random.random_sample()*len(legal))]))

    if(n == 0):
        return 0
    if(board.turn == chess.BLACK):
        return 1
    return -1


tabla = chess.Board()
#i = 10000
#board.is_variant_end()
b = 0
c = 0
n = 0
time_s = time.time()
n1 = 0
#tabla.reset_board()
#winner = playout(tabla)


while (time.time() - time_s < 1):
    n1 += 1
    tabla.reset_board()
    winner = playout(tabla)
    if(winner == 1):
        b += 1
    elif(winner == -1):
        c += 1
    elif(winner == 0):
        n += 1
        
print("aa")
print(b)
print(c)
print(n)
print(n1)