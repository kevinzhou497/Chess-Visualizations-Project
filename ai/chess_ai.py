
# from ai.chess-alpha-zero.src.chess_zero.manager import *
# from chess-alpha-zero.src.chess_zero.worker.evaluate import *
# from chess-alpha-zero.src.chess_zero.env.chess_env import canon_input_planes, maybe_flip_fen, is_black_turn

from collections import namedtuple
import chess.pgn

import numpy as np
import matplotlib.pyplot as plt
from argparse import Namespace

import stockfish
import collections

def get_chess_player(
    model_json='data/model/model_best_config.json',
    model_h5='data/model/model_best_weight.h5'
):
    '''
    Given model weights, returns a ChessPlayer class
    '''
    args = Namespace(cmd='eval', new=False, type='mini', total_step=None)
    cfg = Config(args.type)
    setup(cfg, args)
    ev = EvaluateWorker(cfg)
    model = ChessModel(cfg)
    model.load(model_json, model_h5)
    return ChessPlayer(
        cfg,
        pipes=ev.cur_pipes,
        play_config=cfg.eval.play_config
    )

'''
Brute force approach to validating move
Format:
<fen>: fen string
<move>: <position1><position2>, e.g. c2c4
'''
def valid_move(fen, move):
    board = chess.Board(fen)
    try:
        board.push_uci(move)
    except ValueError as e:
        return False
    return True

'''
Switches the move from w->b or b->w
'''
def reverse_move(move):
    # ugly as hell
    rev_alpha = {'a':'h','b':'g','c':'f','d':'e','e':'d','f':'c','g':'b','h':'a'}
    return rev_alpha[move[0]] + str(9-int(move[1])) + rev_alpha[move[2]] + str(9-int(move[3]))

'''
Encodes the board state in a 0-1 encoding of the board, determining where one's pieces are
'''
def fen_to_onehot_grid(fen, white=True):
    fen = fen.split(' ')[0].split('/') # trim metadata, split into rows
    grid = np.zeros([8,8])
    for row_idx, row in enumerate(fen):
        col_idx = 0
        for c in row:
            if c.isnumeric(): # space: increment
                for i in range(int(c)): col_idx += 1
            else: # character
                if white and c.isupper():
                    grid[row_idx][col_idx] = 1
                if not white and c.islower():
                    grid[row_idx][col_idx] = 1
                col_idx += 1
    return grid

class ChessTreeNode:
    
    def __init__(self, fen, player):
        self.fen = fen
        self.player = player
        self.children = {}
        
    def viz(self):
        return chess.Board(self.fen)
        
    def pprint(self, level=0, transition_move=''):
        ret = "\t"*level+repr(transition_move)+"\n"
        for move, (node, move_p) in self.children.items():
            ret += node.pprint(level+1, '{}, {:.4f}'.format(move, move_p))
        return ret
    
    '''
    Returns the root node of a tree with depth <depth> and branching factor <B>,
    starting at the board state <fen>.
    '''
    def build_tree(self, fen, B=3, depth=3):
        
        node = ChessTreeNode(fen, self.player)
        if depth == 0:
            return node
        
        # get top B moves
        top_B_moves = self.predict_top_moves(fen, B)
        
        # traverse tree
        for move,move_p in top_B_moves:
            board = chess.Board(fen)
            try:
                board.push_uci(move)
                node.children[move] = (
                    self.build_tree(
                        board.fen(),
                        B=B,
                        depth=depth-1
                    ),
                    move_p
                )
            except ValueError as e:
                print("AI tried illegal move {}".format(move))

        return node
    
    '''
    Given board state <fen> and player model <chess_player>, returns the top <B> moves,
    and their probabilities, ordered from highest to lowest
    '''
    def predict_top_moves(self, fen, B):
        
        # by default player predicts for white: flip board if black to move, then reverse moves
        # - probably better way to do this - try to find one later
        black_to_move = is_black_turn(fen)
        if black_to_move:
            fen = maybe_flip_fen(fen, black_to_move)
            
        # get model predictions for each move
        model_input = canon_input_planes(fen)
        leaf_p, leaf_v = self.player.predict(model_input) # leaf_p: prob array for each move
        top_B_moves = [(self.player.labels[i], leaf_p[i]) for i in np.argsort(-leaf_p)[:B]] # (move, move_prob)
        
        if black_to_move: # reverse moves
            top_B_moves = [(reverse_move(move), move_p) for move,move_p in top_B_moves]
            
        return top_B_moves
    
    '''
    (Called after a tree is constructed) Runs BFS to find all chess states at depth <D>,
    in the format (fen, prob), sorted from highest to lowest probability
    '''
    def bfs_depth_D(self, D):
        result = []
        q = [(self, 1.0, D)]
        while q:
            (node, p, depth), q = q[0], q[1:]
            if depth == 0:
                result.append((node.fen, p))
            else:
                for move, (child, move_p) in node.children.items():
                    q.append((child, p*move_p, depth-1))
        return sorted(result, key=lambda x:x[1], reverse=True)
    
    '''
    (Called after a tree is constructed) Returns the most likely state at depth <D>
    '''
    def most_likely_state(self, D, visualize=True):
        fen, p = self.bfs_depth_D(D)[0]
        if visualize:
            display(chess.Board(fen))
        return fen, p
    
    # visualizes probability heatmap
    # <states>: array of (fen, prob) values
    def heatmap_for_states(self, states, use_prob=True):
        total_grid = np.zeros([8, 8, 3])
        for state,state_p in states:
            total_grid[:,:,0] += fen_to_onehot_grid(state, white=True) * (state_p if use_prob else 1)
            total_grid[:,:,1] += fen_to_onehot_grid(state, white=False) * (state_p if use_prob else 1)
        plt.imshow(total_grid / total_grid.max())
        plt.show()
        return total_grid
    
    # returns json for further use
    def jsonify(self):
        d = {'fen': self.fen, 'children':{}}
        for move, (child, move_p) in self.children.items():
            d['children'][move] = (child.jsonify(), move_p)
        return d
    
    # get top sequences with dfs
    def get_all_sequences(self):

        def helper(node, paths):
            if len(node.children) == 0:
                return paths
            new_paths = []
            for move, (child, move_p) in node.children.items():
                new_paths += helper(child, [(path + [move], path_p * move_p) for (path,path_p) in paths])
            return new_paths

        paths = sorted(helper(self, [([], 1.0)]), key=lambda x:x[1], reverse=True)
        return paths
    
class StockfishTreeNode(ChessTreeNode):
    
    '''
    player: instance of Stockfish object
    hack_probs: hacky way of getting probabilities when there are none
        if True, runs over range of time periods, finding best move for each time period, then produces probability weights proportional to the sum of time periods that resulting in each move.
    '''
    def __init__(self, fen, player, hack_probs=False):
        self.fen = fen
        self.player = player
        self.children = {}
        self.hack_probs = hack_probs
        
    def predict_top_moves(self, fen, B):
        
        self.player.set_fen_position(fen)
        if not self.hack_probs:
            move = self.player.get_best_move()
            return [(move, 1.0)]
        else:
            moves = collections.Counter()
            ts = [10, 25, 100, 250, 1000]
            for t in ts:
                move = self.player.get_best_move_time(t)
                moves[move] += float(t) / sum(ts)
            return moves.most_common()[:B]