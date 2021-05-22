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
        
    
class MCTS_node:
    def __init__(self, board, parent):
        self.board = board
        self.parent = parent
        self.children = []
        
        self.wins = 0
        self.visits = 0
        
        
    def UCT(node):
        if node.visits == 0:
            return np.Inf
        
        return node.wins / node.visits + (2 * np.log(node.parent.visits) / node.visits) ** (1 / 2)
    
        
    # returns the child whose UCT value is the highest of all the other children
    # if there are multiple child nodes with the same value then the node that was found first will be returned
    # maybe fix this and return one random from all the ones with the max value
    def selection(self):
        max_child = self.children[0]
        
        for child in self.children:
            if(self.UCT(child) > self.UCT(max_child)):
                max_child = child
                
        return max_child
    
    
    # plays the game out by chosing random moves from the board which was provided as an argument
    def simulation(board):
        tmp_board = chess.copy.copy(board)
        
        # depth of the simulation, the function will stop at this depth if there is no resolution to the game
        playout_depth = 20
        
        # in case the simulated player looses (always white) the return will be 0, it can also be set to -1 and then it will act as a punishment and the player would be less likely to choose this course of action, but it does not matter if it is set to 0, for testing
        loss_value = 0
        # if the game doesn't end within the playout_depth moves, special value is returned
        # right now that special value is the same as the loss value, 0, this can also be tweaked but it doesn't have to be
        not_enough_playouts_value = 0
        # if the player wins in this playout, this value is returned
        win_value = 1
        
        # simulate moves until the maximum depth has been reached
        while (playout_depth):
            playout_depth -= 1
            
            # this is where our special end game condition comes in
            # it is set to check if a king is under check status, and this is so our computer can actually play a reasonable ammount of games that are enough for us to make any kind of assesment neccessary for the "papper"
            # if we wanted to play the game out until the very end, this is where we would change the main game mechanic/ main game condition
            # in essence a player has lost a game if he has been undre the status CHECK
            if (tmp_board.is_check()):
                break
            
            legal_moves = list(tmp_board.generate_legal_moves())
            random_move = (int) (np.random.random_sample() * len(legal_moves))
            move_to_be_made = legal_moves[random_move]
            tmp_board.push(move_to_be_made)
        
        # the game has not concluded within the given depth, and so the player hasn't won
        if (playout_depth == 0):
            return not_enough_playouts_value
        
        # as the player the program plays is white, if in the while loop happens a break, that means there was a check
        # if the player whose turn it is is black then that means that the white player played the move that lead to the check and so white has won
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
            
    def simulate(self):
        # number of playouts, fit for change
        no_playouts = 20
        
        for _ in range(no_playouts):
            # do a simulation from the current board state, sum the returned value to the 
            a = self.simulation(self.board)
            # a is so far, either 0 or 1
            self.wins += a
            # visits gets incremented regardless of wheter or not the simulation resulted in a win
            self.visits += 1
            
    # todo not entirely done
    def print_tree(self, n = 1):        
        for node in self.children:
            print(f"visits: {node.visits}, wins: {node.wins}, node level: {n}, uct: {self.UCT(node)}")
            print_tree(node, n + 1)


def play():
    root = MCTS_node(chess.Board(), None)

    no_moves = 5

    for _ in range(no_moves):
        start_time = time.time()
        time_for_move = 1
        
        tmp = root
        
        while(time.time() - start_time < time_for_move):
            
            while(len(tmp.children) != 0):
                tmp = tmp.selection()
                
            if(tmp.visits == 0):
                tmp.simulate()
                tmp.back_propagation()
            else:
                tmp.expansion()
                
            tmp = root
            
        chosen = root.selection()
        print(str(f"move number: {_}\n"))
        print(chosen.board)
        print("\n")
        result = engine.play(chosen.board, chess.engine.Limit(depth=1))
        chosen.board.push(result.move)
        
        
        #todo ako nema dece uraditi mu ekspanziju
        
        # here we can't play on the same board that is found in the chosen node
        # we have to find a child node that has the same exact board layout as the chosen board + the move black is about to make
        for node in chosen.children:
            if node.board == chosen.board:
                chosen == node
                break
        
        print(chosen.board)
        print("\n")        
        
        root = chosen
    
#root.print_tree()

# parameters fit for change

# inside simulation 
# playout_depth = 20
# loss_value = 0
# not_enough_playouts_value = 0
# win_value = 1

# np.random.random_sample()
# np.random.random()
# random.random()

# inside simulate
# no_playouts = 20

# inside play
# no_moves = 5
# time_for_move = 1
# stockfish depth = 1

def play10x():
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
