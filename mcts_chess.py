# -*- coding: utf-8 -*-
"""
Created on Sun May 16 23:19:58 2021

@author: Nikola
"""


import chess
import numpy as np

import time


board = chess.Board()


#i = 10000
#board.is_variant_end()
b = 0
c = 0
n = 0
for _ in range(100):
    board.reset_board();
    while (~board.is_variant_end()): #and i > 0):
        print(time.time())
        legal = list(board.generate_legal_moves())
        print(time.time())
        size = len(legal)
        if size == 0 or board.is_insufficient_material():
            break
        #i -= 1
        board.push_san((str)(legal[np.random.randint(0,size)]))
        print(time.time())
                
    tmp = board.outcome().winner
    if(tmp == None):
        n += 1
    elif(tmp == True):
        b += 1
    elif(tmp == False):
        c += 1
    
print(b)
print(c)
print(n)