# -*- coding: utf-8 -*-
"""
Created on Fri May 21 21:08:34 2021

@author: Nikola
"""

import chess
import numpy as np
import time 
import random

import chess.engine
import chess.svg
import stockfish
engine = chess.engine.SimpleEngine.popen_uci("C:\\Users\\todor\\source\\repos\\MCTS-CHESS\\stockfish_20011801_x64.exe")

    
class MCTS_node:
    
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.children = []
        
        self.wins = 0
        self.visits = 0
        
    @staticmethod
    def UCT(node):
        if node.visits == 0:
            return np.Inf
        
        return node.wins / node.visits + (0.01 * np.log(node.parent.visits) / node.visits) ** (1 / 2)
    
        
    # returns the child whose UCT value is the highest of all the other children
    # if there are multiple child nodes with the same value then the node that was found first will be returned
    # maybe fix this and return one random from all the ones with the max value
    def selection(self):        
        max_child = self.children[0]
        
        for child in self.children:
            childUCT = self.UCT(node = child)
            maxchildUCT = self.UCT(node = max_child)
            if(childUCT > maxchildUCT):
                max_child = child
                
        return max_child
    
    
    def simulation(node):
        tmp_board = chess.copy.copy(node.board)
        
        playout_ammount = 1000
        
        loss_value = -1
        not_enough_playouts_value = 0
        win_value = 1
        
        while (playout_ammount):
            playout_ammount -= 1
            if (tmp_board.is_check()):
                break
            
            legal_moves = list(tmp_board.generate_legal_moves())
            if (len(legal_moves) == 0):
                return loss_value
            
            random_move = (int) (np.random.random_sample() * (len(legal_moves) - 1))
            move_to_be_made = legal_moves[random_move]
            tmp_board.push(move_to_be_made)
            
        if (playout_ammount == 0):
            return not_enough_playouts_value
        if (tmp_board.turn == chess.BLACK):
            return win_value
        
        return loss_value
    
    
    # expansion is done by generating all legal moves and then appending them to the tree
    def expansion(self):
        legal_moves = list(self.board.generate_legal_moves())
        
        for move in legal_moves:
            # a new board must be made for every node, and must then be updated with the current move
            new_board = chess.copy.copy(self.board)
            new_board.push(move)
            self.children.append(MCTS_node(new_board, self))
    
    
    # updates all the node that are on the path from the current node, up until it reaches the root node
    def back_propagation(self):
        # used to iterate over parents
        tmp = self.parent
        
        while(tmp != None):
            tmp.visits += self.visits
            tmp.wins += self.wins
            tmp = tmp.parent
            
    def simulate_batch(self):
        # number of playouts, fit for change
        no_playouts = 1
        
        for _ in range(no_playouts):
            # do a simulation from the current board state, sum the returned value to the 
            a = self.simulation()
            # a is so far, either 0 or 1
            self.wins += a
            # visits gets incremented regardless of wheter or not the simulation resulted in a win
            self.visits += 1
            
    @staticmethod
    # todo not entirely done
    def print_tree(self, n = 1):        
        for node in self.children:
            print(f"visits: {node.visits}, wins: {node.wins}, node level: {n}, uct: {self.UCT(node)}")
            #self.print_tree(node, n + 1)


def play(num_moves = 20, time_for_move = 3, stockfish_depth = 3):
    root = MCTS_node(chess.Board(), None)

    #num_moves = 5
    count_moves = num_moves
    while ((num_moves) and ~(root.board.is_checkmate())):
        num_moves -= 1        
        
        tmp = root        
        
        
        start_time = time.time()
        while (time.time() - start_time < time_for_move):
            while (len(tmp.children) != 0):
                tmp = tmp.selection()
            if(tmp.visits == 0):
                tmp.simulate_batch()
                tmp.back_propagation()
            else:
                tmp.expansion()
            tmp = root

        # root.print_tree(root)
        visits = root.visits
        
        if(root.board.is_checkmate()):
            break
        if (len(root.children) == 0):
            # print("AAAA")
            root.expansion()

        chosen = root.selection()
            
        # print(str(f"move number: {count_moves - num_moves}\n"))
        # print(chosen.board)
        # print("\n")
        
       
        
        if (len(chosen.children) == 0):
            chosen.expansion()

        # stockfish' turn
        result = engine.play(chosen.board, chess.engine.Limit(depth = stockfish_depth))
        chosen.board.push(result.move)        
        
        # here we can't play on the same board that is found in the chosen node
        # we have to find a child node that has the same exact board layout as the chosen board + the move black is about to make
        for node in chosen.children:
            if node.board == chosen.board:
                chosen = node
                break
        
        # print(chosen.board)
        # print("\n")        
        
        chosen.parent = None
        root = chosen
        
             

    return visits  
    

#play(1, 10, 1)

def play10x():
    avgVisits = 0
    
    for _ in range(20):       
        
        avgVisits += play(1, 60, 1)
        
        
                
        
    print(f"{avgVisits / 20}")
            


play10x()
























# parameters fit for change

# inside simulation 
# playout_depth = 20
# loss_value = 0
# not_enough_playouts_value = 0
# win_value = 1

# np.random.random_sample()
# np.random.random()
# random.random()

# inside simulate_batch
# no_playouts = 20

# inside play
# no_moves = 5
# time_for_move = 1
# stockfish depth = 1

#move, time, depth