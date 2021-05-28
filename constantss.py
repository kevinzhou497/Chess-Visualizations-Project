# A declaration of all the constants used in this project

FEN_STARTING_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
FEN_EMPTY = '4k3/8/8/8/8/8/8/4K3 b - - 0 1'
FEN_1E4 = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'
FEN_IMMORTAL_GAME = 'r1bk2nr/p2p1pNp/n2B1Q2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 w - - 0 1'
FEN_ALPHASTOCKFISH7 = '4r3/1b2n1pk/1p1r1p2/pP1p1Pn1/P1pP1NPp/2N1P2P/2R3B1/5RK1 b - - 0 1'

# Game: AlphaZero vs Stockfish (1-0) at TCEC 2018
# Source: https://www.youtube.com/watch?v=JacRX6cKIaY, 
#        https://chess24.com/en/watch/live-tournaments/alphazero-vs-stockfish/3/1/5
# Black to move (Move 24. h4... awaiting black's move)
# Notes: AlphaZero plays e4g5 (Kg5) which 'blunders the knight but is winning long term...
FEN_ALPHASTOCKFISH8 = 'r4r1k/1p2p1b1/2ppb2p/p1Pn1p1q/N1NPn1pP/1P2P1P1/P1Q1BP2/2RRB1K1 b - - 0 24'


BOARD_SIZE = 700 # pixel width and height of chessboard.png
BOARD_OFFSET = 30 # pixels of margin between board and edge in chessboard.png
SQUARE_SIZE = 80 # Each square of our chess board is 80x80 pixels


# Board size? idk where we might need this
NUMROWS = 8
NUMCOLS = 8

# Numerical codes for the type of piece
EMPTY = 0

LTKING = 1
LTQUEEN = 2
LTROOK = 3
LTBISHOP = 4
LTKNIGHT = 5
LTPAWN = 6

DKKING = 7
DKQUEEN = 8
DKROOK = 9
DKBISHOP = 10
DKKNIGHT = 11
DKPAWN = 12

# Paths for all the images used in this project
PATH_CHESSBOARD = r'imgs/chessboard_nbkgd.png'
PATH_LTKING = r'imgs/king_light.png'
PATH_DKKING = r'imgs/king_dark.png'
PATH_LTQUEEN = r'imgs/queen_light.png'
PATH_DKQUEEN = r'imgs/queen_dark.png'
PATH_LTROOK = r'imgs/rook_light.png'
PATH_DKROOK = r'imgs/rook_dark.png'
PATH_LTBISHOP = r'imgs/bishop_light.png'
PATH_DKBISHOP = r'imgs/bishop_dark.png'
PATH_LTKNIGHT = r'imgs/knight_light.png'
PATH_DKKNIGHT = r'imgs/knight_dark.png'
PATH_LTPAWN = r'imgs/pawn_light.png'
PATH_DKPAWN = r'imgs/pawn_dark.png'
PATH_LTUNICORN = r'imgs/unicorn_light.png'
PATH_DKUNICORN = r'imgs/unicorn_dark.png'

# Source: https://www.color-hex.com/color-palette/94102
MONOKAI_RED = (255,97,136)
MONOKAI_REDH = '#ff6188'
MONOKAI_ORANGE = (252,152,103)
MONOKAI_ORANGEH = '#fc9867'
MONOKAI_YELLOW = (255,216,102)
MONOKAI_YELLOWH = '#ffd866'
MONOKAI_GREEN = (169,220,118)
MONOKAI_GREENH = '#a9dc76'
MONOKAI_BLUE = (120,220,232)
MONOKAI_BLUEH = '#78dce8'
MONOKAI_PURPLE = (174,129,255)


#Lookup table for centers of squares
LOOKUP_PIX = {
    'a1': (40, 40),
    'a2': (40, 120),
    'a3': (40, 200),
    'a4': (40, 280),
    'a5': (40, 360),
    'a6': (40, 440),
    'a7': (40, 520),
    'a8': (40, 600),
    'b1': (120, 40),
    'b2': (120, 120),
    'b3': (120, 200),
    'b4': (120, 280),
    'b5': (120, 360),
    'b6': (120, 440),
    'b7': (120, 520),
    'b8': (120, 600),
    'c1': (200, 40),
    'c2': (200, 120),
    'c3': (200, 200),
    'c4': (200, 280),
    'c5': (200, 360),
    'c6': (200, 440),
    'c7': (200, 520),
    'c8': (200, 600),
    'd1': (280, 40),
    'd2': (280, 120),
    'd3': (280, 200),
    'd4': (280, 280),
    'd5': (280, 360),
    'd6': (280, 440),
    'd7': (280, 520),
    'd8': (280, 600),
    'e1': (360, 40),
    'e2': (360, 120),
    'e3': (360, 200),
    'e4': (360, 280),
    'e5': (360, 360),
    'e6': (360, 440),
    'e7': (360, 520),
    'e8': (360, 600),
    'f1': (440, 40),
    'f2': (440, 120),
    'f3': (440, 200),
    'f4': (440, 280),
    'f5': (440, 360),
    'f6': (440, 440),
    'f7': (440, 520),
    'f8': (440, 600),
    'g1': (520, 40),
    'g2': (520, 120),
    'g3': (520, 200),
    'g4': (520, 280),
    'g5': (520, 360),
    'g6': (520, 440),
    'g7': (520, 520),
    'g8': (520, 600),
    'h1': (600, 40),
    'h2': (600, 120),
    'h3': (600, 200),
    'h4': (600, 280),
    'h5': (600, 360),
    'h6': (600, 440),
    'h7': (600, 520),
    'h8': (600, 600)
}

LOOKUP_NUM = {
    'a1': 0,
    'a2': 8,
    'a3': 16,
    'a4': 24,
    'a5': 32,
    'a6': 40,
    'a7': 48,
    'a8': 56,
    'b1': 1,
    'b2': 9,
    'b3': 17,
    'b4': 25,
    'b5': 33,
    'b6': 41,
    'b7': 49,
    'b8': 57,
    'c1': 2,
    'c2': 10,
    'c3': 18,
    'c4': 26,
    'c5': 34,
    'c6': 42,
    'c7': 50,
    'c8': 58,
    'd1': 3,
    'd2': 11,
    'd3': 19,
    'd4': 27,
    'd5': 35,
    'd6': 43,
    'd7': 51,
    'd8': 59,
    'e1': 4,
    'e2': 12,
    'e3': 20,
    'e4': 28,
    'e5': 36,
    'e6': 44,
    'e7': 52,
    'e8': 60,
    'f1': 5,
    'f2': 13,
    'f3': 21,
    'f4': 29,
    'f5': 37,
    'f6': 45,
    'f7': 53,
    'f8': 61,
    'g1': 6,
    'g2': 14,
    'g3': 22,
    'g4': 30,
    'g5': 38,
    'g6': 46,
    'g7': 54,
    'g8': 62,
    'h1': 7,
    'h2': 15,
    'h3': 23,
    'h4': 31,
    'h5': 39,
    'h6': 47,
    'h7': 55,
    'h8': 63
}

# RANDOM FEN STRINGS FOR TESTING:

''' 
1q6/p1p5/kP1P1p1r/2R1bnP1/1B2p3/2P5/2P2P2/4KN2 w - - 0 1
kr6/2pP4/P1PB4/Pb5P/Pn4p1/2K2R1p/P4N2/8 b - - 0 1
8/4k3/8/r7/PP2nPK1/4N3/3PR1p1/8 w - - 0 1
2k5/p4PR1/p2Q1p2/5B2/8/K7/r1P2PP1/7N b - - 0 1
1B6/P1k5/4p2R/1PPPK3/4P2P/4Q3/1P1N2p1/8 w - - 0 1
8/k3Q2B/1p3p1N/2N5/1B3p2/1R5K/1p1p1p2/8 b - - 0 1
6q1/1r2K3/2p3pn/n1Rb4/3PP2P/6N1/6PP/2k1b3 w - - 0 1
6N1/P1BR4/P2pPQ2/4k3/2P5/1Pp4p/1K6/6r1 b - - 0 1
3R2k1/3rp3/P1PpK3/8/5P2/1pQ4N/2pBP2p/4B3 w - - 0 1
kb6/N1PqP1P1/1P1p1nK1/p1p5/3P4/2p1p3/p4P2/Rn3r1b b - - 0 1
nbr5/pp1p1P2/3R3p/KBN1PpP1/3qP1P1/4PP2/1p1k1bp1/2Q5 w - - 0 1
8/1P1PP2p/4qk1p/n3PbP1/Np4Pp/2n1p2K/bP1p1p2/3Rr3 b - - 0 1
8/K4p1p/3p4/5p2/PP3k2/1P2P3/3p2P1/8 w - - 0 1
3K1N2/6Q1/1k2b3/3P1RP1/1PP2r2/P1PP1n2/8/6B1 b - - 0 1
b7/8/4r1Pb/1pR5/1pPN3q/1P3K2/PPpn4/1k6 w - - 0 1
4n3/5bP1/4PPP1/1PP5/2k2P2/q6r/6K1/3R4 b - - 0 1
2k5/1p2Pp1P/8/P3B1R1/P5P1/6K1/3N4/8 w - - 0 1
6k1/1p5r/8/2R1p1P1/P2p2P1/1KpP4/5P2/8 b - - 0 1
6q1/1n1P4/2p2P1Q/3pK3/2N5/4b2k/p5p1/2r1BR2 w - - 0 1
4K3/8/8/8/2R5/6k1/8/8 b - - 0 1
qN1B4/7p/6PR/P1p2p1p/1Pp1n1bb/2p4K/pQ2nB2/1Nrk4 w - - 0 1
n3K3/2pN4/b2P1B1P/5R2/rkP5/pp6/8/8 b - - 0 1
1r6/5n1p/3k4/8/8/1p3p2/2p5/5K2 w - - 0 1
7n/1P5P/5k2/7p/P1r5/K2PR1P1/1bN5/8 b - - 0 1
3Q4/2kbb3/3N3P/7P/p2nrK1R/3q2PP/3B4/n7 w - - 0 1
nbq5/p6p/K1p5/1r3p2/1p3k2/3p1P1p/N7/7R b - - 0 1
Q7/pN2k2p/3P1p2/p4p2/6pr/4pBNP/2K2n2/4R2B w - - 0 1
6k1/1pp1P3/1r4P1/2R3n1/1P1p1p2/1KPp2pP/PpP5/8 b - - 0 1
8/1P4p1/2pkn1p1/pr2B3/1p2N3/Kp1R1Qp1/2P5/8 w - - 0 1
3r2B1/5Q1P/P3P1P1/NB5p/2n1Pp1n/P2q1NK1/2p1p1pP/kRb2b2 b - - 0 1
8/5kP1/2qPpP2/1P6/1K1b4/6p1/7r/n7 w - - 0 1
8/1B2pkP1/P3QRp1/1P6/5N1P/1PP3pp/p2KpP1p/2B5 b - - 0 1
5b1Q/4pr2/1pp4N/k5q1/3R4/p2n3p/3K1Pp1/2B5 w - - 0 1
7r/2R2p2/1PPb4/3q4/2n3Bb/3P3K/4NB1Q/k6N b - - 0 1
k6r/3R4/7P/8/P2Kn3/2p1P3/2P5/8 w - - 0 1
1k6/8/1b2P1B1/nb6/1R1pP2r/B7/1Q5K/2Nq4 b - - 0 1
5n1r/8/8/3k4/4Q3/2q1R3/1B1b1B2/4N2K w - - 0 1
6N1/4p3/2B4r/1kB3p1/6P1/1R1K4/8/Q7 b - - 0 1
B7/5QNK/2P4P/2PP1k2/1p4R1/4B3/pp5P/4n2r w - - 0 1
3k4/P2np1p1/P3pQp1/1pq1rpP1/5K2/bnBPPp2/1PBN2R1/6b1 b - - 0 1
K7/P2nQr1P/1N1R4/8/7B/p3pPk1/4pp2/6B1 w - - 0 1
K7/1R6/2p5/3P4/5Bk1/8/pp1P1P1P/4N3 b - - 0 1
7n/4pPp1/P6p/P2P4/5p2/3rpK2/p3P1R1/1N1k4 w - - 0 1
1BN5/8/1R4pp/pP1P2P1/2P2p2/4p1PK/2Pn3p/3k1r2 b - - 0 1
6B1/2P1Np2/k2P1p2/P7/Pp1p3R/3pK3/2p3P1/8 w - - 0 1
8/2p1q1p1/1p2r1pb/8/2n1K3/p7/R3N2p/k7 b - - 0 1
K7/3pP1b1/PP2nPk1/5P2/P6b/3p2q1/1nP5/2r5 w - - 0 1
8/1n1P4/Kq6/1P6/b7/8/3r2kb/4n3 b - - 0 1
8/1k6/6p1/1P1K4/8/7R/2p5/8 w - - 0 1
8/2Q4N/1p4b1/8/n1B1PkB1/R4p2/3Pp2K/4r1q1 b - - 0 1
'''