# -*- coding: utf-8 -*-
"""
Created on Fri May 21 21:08:34 2021

@author: Nikola
"""

import chess
import numpy as np
import time 
        
    
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
            if(node.board.turn):
                return 1
            else:
                return -1
        if(node.board.turn):#ako je true igra beli
            return node.wins / node.visits + (1 * np.log(node.parent.visits) / node.visits) ** (1 / 2)
        return (node.wins / node.visits - (1 * np.log(node.parent.visits) / node.visits) ** (1 / 2))
        
    # returns the child whose UCT value is the highest of all the other children
    # if there are multiple child nodes with the same value then the node that was found first will be returned
    # maybe fix this and return one random from all the ones with the max value
    def selection(self):        
        ret_child = self.children[0]
        #min_child = self.children[0]
        for child in self.children:
            childUCT = self.UCT(node = child)
            retchildUCT = self.UCT(node = ret_child)
            if(self.board.turn):
                #beli
                if(childUCT < retchildUCT):
                    ret_child = child
            else:
                #print("BBB")
                if(childUCT > retchildUCT):
                    ret_child = child
        #print(self.UCT(node = child))
        return ret_child
    
    
    def simulation(node):
        new_tmp_board = chess.copy.copy(node.board)
        n = 20;
        while(n):
            n -= 1
            if(new_tmp_board.is_check()):
                break
            legal = list(new_tmp_board.generate_legal_moves())
            if(len(legal) == 0):
                break
            new_tmp_board.push((legal[(int)(np.random.random_sample()*(len(legal)-1))]))
        
        if(n == 0):
            return 0
        if(new_tmp_board.turn):#beli je na redu i pod matom je
            #print("crni pobedio ako true")
            #print(new_tmp_board.turn)
            return 1
        if(~new_tmp_board.turn):
            #print("beli pobedio ako false")
            #print(new_tmp_board.turn)
            return -1
        return 0
    
    
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
            print(node.board)
            print(f"visits: {node.visits}, wins: {node.wins}, node level: {n}, uct: {self.UCT(node)}")
            #self.print_tree(node, n + 1)


def play(num_moves = 20, time_for_move = 3):
    root = MCTS_node(chess.Board(), None)
    #print(root.board.turn);
    #num_moves = 5
    while ((num_moves) and ~(root.board.is_checkmate())):
        num_moves -= 1        
        root.parent = None
        tmp = root
        if(root.board.is_checkmate() or root.board.is_insufficient_material()):
            return root.board
        start_time = time.time()
        while (time.time() - start_time < time_for_move):
            tmp = root        
            #print("a")
            while (len(tmp.children) != 0):
                tmp = tmp.selection()
                #print("{} {} {}".format(tmp.visits, tmp.wins, tmp.UCT(tmp)))
                
            tmp.expansion()
            if(tmp.visits == 0):
                tmp.simulate_batch()
                tmp.back_propagation()
                #tmp.expansion()
            #else:
        
        visits = root.visits
            #tmp = tmp.selection()
        #for node in root.children:
            #print("{} {} {}".format(node.visits, node.wins, node.UCT(node)))
        root = root.selection()
        if(root.board.is_checkmate() or root.board.is_insufficient_material()):
            return root.board
        #for node in root.children:
        #    print("{}AAAA {} {}".format(node.visits, node.wins, node.UCT(node)))
        #print("Izabran uct {}".format(root.UCT(root)))
        #print("\n")
        #print(root.board.turn);
        #root = root.selection()
        #print(root.board);
        #print(root.board.turn);
        #print("\n")
    return visits   

            
#play(100,1)


def play10x():
    n, b, c = 0, 0, 0
    avgVisits = 0
    
    for _ in range(10):       
        
        avgVisits += play(1, 60)
        
        
                
        
    print(f"{avgVisits / 10}")
        
        

play10x()



























