# -*- coding: utf-8 -*-
"""
Created on Sun May 16 23:40:02 2021

@author: Nikola
"""

import chess
import chess.engine
import chess.svg

import stockfish


#stockfish = stockfish.Stockfish("C:\\Users\\Nikola\\Desktop\\stockfish-11-win\\Windows\\stockfish_20011801_x64.exe")
engine = chess.engine.SimpleEngine.popen_uci("C:\\Users\\Nikola\\Desktop\\stockfish-11-win\\Windows\\stockfish_20011801_x64.exe")


board = chess.Board()
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.01))
    board.push(result.move)
print(board.outcome().winner)
print(board)
engine.quit()
