# -*- coding: utf-8 -*-
"""
Created on Sun May 16 23:19:58 2021

@author: Nikola
"""


import chess
import numpy as np
import random


import time


board = chess.Board()


#i = 10000
#board.is_variant_end()

def regular_play(): 
    #board = chess.Board()
    b = 0
    c = 0
    n = 0
    start_time = time.time()
    for _ in range(100):
        board.reset_board();
        while (~board.is_variant_end()): 
            legal = list(board.generate_legal_moves())
            
            if board.is_insufficient_material():
                break
            
            board.push_san((str)(legal[np.random.randint(0, len(legal))]))
                    
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
    
    print("vreme izvrsavanja: " + str(time.time() - start_time))

def playout(board):
    
    n = 20
    
    while (n):
        n -= 1
        if (board.is_check()):
            break
        
        legal = list(board.generate_legal_moves())
        
        size = len(legal)
        
        #if (board.is_insufficient_material()):
        #   break
        
        
        board.push(legal[(int) (random.random() * size)])
        
        
    if (n == 0):
        return 0
    if (board.turn == chess.BLACK):
        return 1
    elif (board.turn == chess.WHITE):
        return -1


def game():
    #board = chess.Board()
    
    w, b, d = 0, 0, 0
    n = 0
    
    start_time = time.time()
    time_for_move = 10
    for _ in range(100):
        while (time.time() - start_time < time_for_move):
            board.reset_board()
            winner = playout(board)
            
            if (winner == 1):
                w += 1
            elif (winner == -1):
                b += 1
            else:
                d += 1
            
            n += 1
            
    print("\nwhite won " + str(w) + " times")
    print("black won " + str(b) + " times")
    print("noone won " + str(d) + " times")
    
    return n

game()


def play10():
    for _ in range(10):
        regular_play()
        
def game10():
    n = 0
    no_playouts = 10
    start_time = time.time()
    for _ in range(no_playouts):
        print("\ngame # " + str(_))
        i = game1s()
        n += i
    no = n / no_playouts
    print(f"\n\naverage moves per game {no}")
    print(f"total playtime of {no_playouts} is {time.time() - start_time}")
    return no
        
def game1s():
    n = game()
    print("played " + str(n) + " games")
    return n

def game1010():
    n = 0
    for i in range(10):
        print(f"{i} iteration")
        n += game10()
    
    print(f"average playouts in 10 tries of game10 is: {n / 10}")

#play10()






























