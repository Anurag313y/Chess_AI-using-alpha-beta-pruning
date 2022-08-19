import pickle 
#it's the process of converting a Python object into a byte stream to store it in a file/database,
#maintain program state across sessions, or transport data over the network.

from random import randint

import chess
from chess.polyglot import open_reader
from board import evaluate_board


class AI:
    depth = 3  #maximum depth of the tree

    board_caches = {}
    cache_hit = 0
    cache_miss = 0
    try:
        cache = open('./data/cache.p', 'rb')#reading a file in a binary format
    except IOError:
        cache = open('./data/cache.p', 'wb')
        pickle.dump(board_caches, cache)
    else:
        board_caches = pickle.load(cache)

    def __init__(self, board, is_player_white):
        self.board = board
        self.is_ai_white = not is_player_white

        with open_reader('./data/opening.bin') as reader: #here for given board states reader.find_all(board) gives the opening moves
            self.opening_moves = [
                str(entry.move)for entry in reader.find_all(board)
            ]
        print(self.opening_moves)
    def ai_move(self):
        global_score = -1e8 if self.is_ai_white else 1e8
        chosen_move = None

        # can move from opening book
        if self.opening_moves:
            chosen_move = chess.Move.from_uci(
                self.opening_moves[randint(0, len(self.opening_moves) // 2)])
            print(chosen_move)
        else:
            print("I am here")
            for move in self.board.legal_moves:
                self.board.push(move)

                local_score = self.minimax(self.depth - 1, not self.is_ai_white,
                                           -1e8, 1e8)
                self.board_caches[self.hash_board(
                    self.depth - 1, not self.is_ai_white)] = local_score

                if self.is_ai_white and local_score > global_score:
                    global_score = local_score
                    chosen_move = move
                elif not self.is_ai_white and local_score < global_score:
                    global_score = local_score
                    chosen_move = move

                self.board.pop()

                print(local_score, move)

            print('\ncache_hit: ' + str(self.cache_hit))
            print('cache_miss: ' + str(self.cache_miss) + '\n')

        print(str(global_score) + ' ' + str(chosen_move) + '\n')

        self.board.push(chosen_move)

        with open('./data/cache.p', 'wb') as cache:
            pickle.dump(self.board_caches, cache)

    def minimax(self, depth, is_maxing_white, alpha, beta):
        # if board in cache
        if self.hash_board(depth, is_maxing_white) in self.board_caches:
            self.cache_hit += 1

            return self.board_caches[self.hash_board(depth, is_maxing_white)]

        self.cache_miss += 1

        # if depth is 0 or game is over
        if depth == 0 or not self.board.legal_moves:
            self.board_caches[self.hash_board(
                depth, is_maxing_white)] = evaluate_board(self.board)
            return self.board_caches[self.hash_board(depth, is_maxing_white)]

        # else
        best_score = -1e8 if is_maxing_white else 1e8
        for move in self.board.legal_moves:
            self.board.push(move)

            local_score = self.minimax(depth - 1, not is_maxing_white, alpha,
                                       beta)
            self.board_caches[self.hash_board(
                depth - 1, not is_maxing_white)] = local_score

            if is_maxing_white:
                best_score = max(best_score, local_score)
                alpha = max(alpha, best_score)
            else:
                best_score = min(best_score, local_score)
                beta = min(beta, best_score)

            self.board.pop()

            if beta <= alpha:
                break
        self.board_caches[self.hash_board(depth, is_maxing_white)] = best_score
        return self.board_caches[self.hash_board(depth, is_maxing_white)]

    def hash_board(self, depth, is_maxing_white):
        # print(str(self.board) + ' ' + str(depth) + ' ' + str(is_maxing_white))
        return str(self.board) + ' ' + str(depth) + ' ' + str(is_maxing_white)
