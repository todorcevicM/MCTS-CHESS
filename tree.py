# -*- coding: utf-8 -*-
"""
Created on Fri May 21 21:08:34 2021

@author: Nikola
"""

import chess
import numpy as np
import time 

import chess.engine
import chess.svg
import stockfish
# TODO: promeniti ovo
engine = chess.engine.SimpleEngine.popen_uci("C:\\Users\\Nikola\\Desktop\\stockfish-11-win\\Windows\\stockfish_20011801_x64.exe")


def simulation(board):
    new_tmp_board = chess.copy.copy(board)
    n = 20;
    while(n):
        n -= 1
        if(new_tmp_board.is_check()):
            break
        legal = list(new_tmp_board.generate_legal_moves())
        new_tmp_board.push((legal[(int)(np.random.random_sample()*len(legal))]))
    
    if(n == 0):
        return 0
    if(new_tmp_board.turn == chess.BLACK):
        return 1
    return 0
    
    
def UCT(node):
    if node.visits == 0:
        return np.Inf
    return node.wins / node.visits + (2* np.log(node.parent.visits)/node.visits) ** (1/2)
    
    
class MCTS_node:
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.children = []
        
        self.wins = 0
        self.visits = 0
        
    def selection(self):
        max_child = self.children[0]
        for child in self.children:
            if(UCT(child) > UCT(max_child)):
                max_child = child
        return max_child

    def expansion(self):
        tmp = list(self.board.generate_legal_moves())
        for move in tmp:
            #print(move)
            new_board = chess.copy.copy(self.board)
            new_board.push(move)
            self.children.append(MCTS_node(new_board, self))
    
    
    def back_propagation(self):
        for _ in range(20):
            a = simulation(self.board)
            self.wins += a
            self.visits += 1
        tmp = self.parent
        while(tmp != None):
            tmp.visits += self.visits
            tmp.wins += self.wins
            tmp = tmp.parent
    
    def print_tree(self, n = 0):
        
        for node in self.children:
            print("posete: {}, pobede: {}, nivo: {}, uct: {}".format(node.visits, node.wins, n, UCT(node)))
#            self.print_tree(n + 1)
    
root = MCTS_node(chess.Board(), None)
# node1 = MCTS_node(chess.Board(), root)
# root.children.append(node1)
# node2 = MCTS_node(chess.Board(), root)
# root.children.append(node2)
# node2.back_propagation()
# a = root.ret_optimal_child()
# print(a.wins)


for _ in range(5):
    start_time = time.time()
    tmp = root
    while(time.time() - start_time < 1):
        while(len(tmp.children) != 0):
            tmp = tmp.selection()
        if(tmp.visits == 0):
            tmp.back_propagation()
        else:
            tmp.expansion()
        tmp = root
        
    izabran = root.selection()
    print(str(_))
    print(izabran.board)
    print("\n")
    result = engine.play(izabran.board, chess.engine.Limit(depth=1))
    izabran.board.push(result.move)
    for node in izabran.children:
        if node.board == izabran.board :
            izabran == node
            break
    
    print(izabran.board)
    print("\n")
    
    
    root = izabran
    
#root.print_tree()
