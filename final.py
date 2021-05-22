import chess
import numpy as np
import time 
import random

import chess.engine
import chess.svg
import stockfish
engine = chess.engine.SimpleEngine.popen_uci("stockfish_20011801_x64.exe")
        
    
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
            return 1
        
        return node.wins / node.visits + (0.01 * np.log(node.parent.visits) / node.visits) ** (1 / 2)
    
        
    # returns the child whose UCT value is the highest of all the other children
    # if there are multiple child nodes with the same value then the node that was found first will be returned
    # maybe fix this and return one random from all the ones with the max value
    def selection(self):        
        max_child = self.children[0]
        
        for child in self.children:
            childUCT = self.UCT(node = child)
            maxchildUCT = self.UCT(node = max_child)
            if (childUCT > maxchildUCT):
                max_child = child
                
        return max_child
    
    
    def simulation(node):
        tmp_board = chess.copy.copy(node.board)
        loss_value = -1
        not_enough_playouts_value = 0
        win_value = 1
        
        while (not tmp_board.is_check()) and (not tmp_board.is_insufficient_material()):
        # while (not tmp_board.is_game_over()) and (not tmp_board.is_insufficient_material()):
            result = engine.play(tmp_board, chess.engine.Limit(depth = 1))
            tmp_board.push(result.move)
        
        if (tmp_board.outcome() == None):
            return 0
        
        # if its whites turn to move then he was checked by black and has lost
        if (tmp_board.turn == chess.WHITE):
            return loss_value
        elif (tmp_board.turn == chess.BLACK):
            return win_value
        return not_enough_playouts_value
        
# =============================================================================
#         if (tmp_board.outcome().winner == True):
#             return 1
#         elif (tmp_board.outcome().winner == False):
#             return -1
#         return 0
# =============================================================================
    
    
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
        no_playouts = 10
        
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


def play(num_moves = 20, time_for_move = 3, stockfish_depth = 3):
    root = MCTS_node(chess.Board('r1b1kb1r/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'), None)

    #num_moves = 5
    count_moves = num_moves
    while ((num_moves) and ~(root.board.is_checkmate())):
        num_moves -= 1        
        
        tmp = root        
        
        
        start_time = time.time()
        while (time.time() - start_time < time_for_move):
            while (len(tmp.children) != 0):
                tmp = tmp.selection()
                # print(tmp.board)
            if(tmp.visits == 0):
                tmp.simulate_batch()
                tmp.back_propagation()
            else:
                tmp.expansion()
            tmp = root

        #root.print_tree(root)
        
        if(root.board.is_checkmate()):
            break
        if (len(root.children) == 0):
            root.expansion()
        
        chosen = root.selection()
            
        print(str(f"move number: {count_moves - num_moves}\n"))
        #print("selection 22222222222222222222222")
        print(chosen.board)
        print("\n")
        
       
        
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
        
        print(chosen.board)
        print("\n")        
        
        chosen.parent = None
        root = chosen
             

    return root.board   
    

# play(100, 3, 1)

def play10x():
    play_seconds = 20
    play_seconds_increment = 5
    number_of_games = 10
    number_of_moves_per_game = 100
    stockfish_depth = 1
    
    
    d, w, b = 0, 0, 0
    for _ in range(number_of_games):
        board = play(number_of_moves_per_game, play_seconds, stockfish_depth)
        #play_seconds += play_seconds_increment
        
        tmp = board.outcome()
        tmp = board.turn
        
        if(tmp == None):
            d += 1
        elif(tmp == True):
            w += 1
        elif(tmp == False):
            b += 1
            
    print(f"beli: {w}\ncrni: {b}\nnereseno: {d}")
            

# play(100,20,1)

play10x()