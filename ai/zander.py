import sys, os
sys.path.append(os.path.join(sys.path[0],r'chess-alpha-zero'))

from chess_ai import ChessTreeNode

FEN_ALPHASTOCKFISH8 = 'r4r1k/1p2p1b1/2ppb2p/p1Pn1p1q/N1NPn1pP/1P2P1P1/P1Q1BP2/2RRB1K1 b - - 24 1'

player = get_chess_player()

mynode = ChessTreeNode(FEN_ALPHASTOCKFISH8, player).build_tree(FEN_ALPHASTOCKFISH8, B=3, depth=6)

print(mynode.pprint())