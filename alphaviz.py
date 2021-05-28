from tkinter import constants
from typing import cast
import constantss
import validateFEN
import tkinter as tk
import tkinter.scrolledtext as tkst
from PIL import ImageTk
import PIL.Image
# import PIL.ImageTk
import re
from tkinter import *
from functools import partial
import json
import math
import os
# TODO: uncomment
from ai.chess_ai import StockfishTreeNode
from stockfish import Stockfish

DEBUG = False
CORN = True
global double_click_flag

global arrow
global draw_arrow
global first_x
global first_y
global converted_x
global converted_x2
global converted_y
global converted_y2

arrow = False
draw_arrow = False


class ChessGui(tk.Frame):

    # Initializes the AlphaViz GUI
    # Sets many instance variables, loads images used for the GUI, creates
    # most GUI components, and prepares the GUI for human interaction.

    def __init__(self, parent):
        if DEBUG:
            print("DEBUG MODE: ON")
            print("ChessGui.__init__() executing...")

        global double_click_flag
        double_click_flag = False

        # stockfish model
        self.os_type = 'windows' # CHANGE THIS DEPENDING ON SYSTEM OS
        assert self.os_type in ['windows','linux']
        if self.os_type == 'linux':
            self.stockfish_player = Stockfish(r'./stockfish_13_linux_x64.exe')
        elif self.os_type == 'windows':
            self.stockfish_player = Stockfish(r'./stockfish_13_win_x64.exe')

        # json for storing trees
        self.json_tree_path = 'formatted_trees.json'

        # GUI display variables
        self.selected = None  # selected square
        self.selected_piece = None
        self.highlighted_imgs = []
        self.highlighted_rects = []  # reference to all highlighted squares
        self.arrows = []

        # Set parent GUI element (most likely root)
        self.parent = parent

        # Initialize tk.Frame of root
        tk.Frame.__init__(self, parent)

        # Initialize Game State Variables
        self.reset_board_state()

        # Load the images used
        self.load_images()

        # Get the width and height of the chessboard to define the initial
        # size of the canvas
        canvas_width = self.IMG_CHESSBOARD.width()
        canvas_height = self.IMG_CHESSBOARD.height()

        # Create the canvas component
        self.canvas = tk.Canvas(self, width=canvas_width,
                                height=canvas_height, background="white")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        # Draw the chessboard on the canvas
        self.draw_board()

        # Directs configuration event of the canvas to call self.refresh()
        self.canvas.bind("<Configure>", self.refresh)
        # Directs left mouse click event to call self.click()
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)

        # Create GUI frame at the bottom of the root frame,
        # below the chessboard canvas
        self.statusbar = tk.Frame(self, height=64)

        self.button_reopen = tk.Button(
            self.statusbar, text="REOPEN", fg="black", command=self.reopen)
        self.button_reopen.pack(side=tk.LEFT, in_=self.statusbar)

        # Create new game button and link it to the function self.reset()
        self.button_new = tk.Button(
            self.statusbar, text="NEW", fg="black", command=self.reset)
        self.button_new.pack(side=tk.LEFT, in_=self.statusbar)

        # Create save game button and link it to the function [NONE] currently...
        self.button_save = tk.Button(
            self.statusbar, text="CLEAR", fg="black", command=self.clear_board)
        self.button_save.pack(side=tk.LEFT, in_=self.statusbar)

        # # [TEMPORARY DEMO FEATURE]
        # self.button_immortal = tk.Button(
        #     self.statusbar, text='IMMORTAL', fg="black", command=self.immortal)
        # self.button_immortal.pack(side=tk.LEFT, in_=self.statusbar)

        # Creates the input box for a FEN string using Entry
        self.fen_string = tk.Entry(self.statusbar, exportselection=0, width=80)
        self.fen_string.pack(side=tk.LEFT, in_=self.statusbar)

        # Creates the load fen button and link to the load_fen(fen_string) function
        self.button_fen = tk.Button(text='Load Fen String',
                                    command=self.input_fen)
        self.button_fen.pack(side=tk.LEFT, in_=self.statusbar)
        self.statusbar.pack(expand=False, fill="x", side='bottom')

     # Display black/white's turn
        self.label_status = tk.Label(self.statusbar,
                                     text="   White to move  " if self.whitetomove else "   Black to move  ",
                                     fg="black")
        self.label_status.pack(side=tk.LEFT, expand=0, in_=self.statusbar)

        # Create the quit button and link it to self.parent.destroy() function
        self.button_quit = tk.Button(
            self.statusbar, text="Quit", fg="black", command=self.exit)
        self.button_quit.pack(side=tk.RIGHT, in_=self.statusbar)
        self.statusbar.pack(expand=False, fill="x", side='bottom')

        # Creates the button for activating drawing arrows
        self.button_arrow = tk.Button(text='Draw Arrows',
                                      command=self.activate_arrow)
        self.button_arrow.pack(side=tk.RIGHT, in_=self.statusbar)
        self.statusbar.pack(expand=False, fill="x", side='bottom')
        self.reset()

        '''
        self.button_best_move = tk.Button(text='Show Best Move',
                                          command=self.draw_AI_arrow)
        self.button_best_move.pack(side=tk.RIGHT, in_=self.statusbar)
        self.statusbar.pack(expand=False, fill="x", side='bottom')
        '''
        self.last_disp = None


    def reopen(self):
        self.exit()
        exec(open('temporary.py').read())


    def load_images(self):
        self.IMG_CHESSBOARD = ImageTk.PhotoImage(
            file=constantss.PATH_CHESSBOARD)
        self.IMG_LTKING = ImageTk.PhotoImage(file=constantss.PATH_LTKING)
        self.IMG_DKKING = ImageTk.PhotoImage(file=constantss.PATH_DKKING)
        self.IMG_LTQUEEN = ImageTk.PhotoImage(file=constantss.PATH_LTQUEEN)
        self.IMG_DKQUEEN = ImageTk.PhotoImage(file=constantss.PATH_DKQUEEN)
        self.IMG_LTROOK = ImageTk.PhotoImage(file=constantss.PATH_LTROOK)
        self.IMG_DKROOK = ImageTk.PhotoImage(file=constantss.PATH_DKROOK)
        self.IMG_LTBISHOP = ImageTk.PhotoImage(file=constantss.PATH_LTBISHOP)
        self.IMG_DKBISHOP = ImageTk.PhotoImage(file=constantss.PATH_DKBISHOP)
        self.IMG_LTKNIGHT = ImageTk.PhotoImage(
            file=constantss.PATH_LTUNICORN if CORN else constantss.PATH_LTKNIGHT)
        self.IMG_DKKNIGHT = ImageTk.PhotoImage(
            file=constantss.PATH_DKUNICORN if CORN else constantss.PATH_DKKNIGHT)
        self.IMG_LTPAWN = ImageTk.PhotoImage(file=constantss.PATH_LTPAWN)
        self.IMG_DKPAWN = ImageTk.PhotoImage(file=constantss.PATH_DKPAWN)

    def activate_arrow(self):
        if DEBUG:
            print(f'ChessGui.activate_arrow() executing...')
        global arrow
        arrow = True

    def load_fen(self, fen_string):
        if DEBUG:
            print(f'ChessGui.load_fen(\'{fen_string}\') executing...')

        self.reset_board_state()
        self.clear_board()

        if validateFEN.fenPass(fen_string):
            if DEBUG:
                print(f'\'{fen_string}\' is a valid FEN string!')

            # Tokenize
            tokens = fen_string.split(' ')
            board_str = tokens[0]
            bwturn_str = tokens[1]
            castles_str = tokens[2]
            enpassant_str = tokens[3]
            halfmoves_str = tokens[4]
            moves_str = tokens[5]

            # set self.whitetomove
            if bwturn_str == 'w':
                self.whitetomove = True
            else:
                self.whitetomove = False

            # set en passant move
            self.possible_enpassant = enpassant_str
            # set the half moves and moves
            self.half_moves = int(halfmoves_str)
            self.moves = int(moves_str)

            # parse castling
            if 'K' in castles_str:
                self.wk_castle = True
            if 'Q' in castles_str:
                self.wq_castle = True
            if 'k' in castles_str:
                self.bk_castle = True
            if 'q' in castles_str:
                self.bq_castle = True

            # parse board
            # DO NOT TWEAK THESE NUMBERS THEY WERE CAREFULLY MANUFACTURED
            i = 56
            for character in board_str:
                if character == '/':
                    i -= 16
                elif character.isdigit():
                    i += int(character)
                elif character == 'P':
                    self.board[i] = constantss.LTPAWN
                    i += 1
                elif character == 'p':
                    self.board[i] = constantss.DKPAWN
                    i += 1
                elif character == 'R':
                    self.board[i] = constantss.LTROOK
                    i += 1
                elif character == 'r':
                    self.board[i] = constantss.DKROOK
                    i += 1
                elif character == 'K':
                    self.board[i] = constantss.LTKING
                    i += 1
                elif character == 'k':
                    self.board[i] = constantss.DKKING
                    i += 1
                elif character == 'B':
                    self.board[i] = constantss.LTBISHOP
                    i += 1
                elif character == 'b':
                    self.board[i] = constantss.DKBISHOP
                    i += 1
                elif character == 'Q':
                    self.board[i] = constantss.LTQUEEN
                    i += 1
                elif character == 'q':
                    self.board[i] = constantss.DKQUEEN
                    i += 1
                elif character == 'N':
                    self.board[i] = constantss.LTKNIGHT
                    i += 1
                elif character == 'n':
                    self.board[i] = constantss.DKKNIGHT
                    i += 1
        else:
            if DEBUG:
                print(f'{fen_string} is NOT a valid FEN string!')
                print('[ERROR] load_fen() Failed.')
        self.label_status.configure(
            text="   White to move  " if self.whitetomove else "   Black to move  ")

    def board_to_fen(self):
        if DEBUG:
            print('ChessGui.board_to_fen() executing...')

    def arrow_helper(self):
        for tup in self.arrows:
            first_x = tup[0]
            first_y = tup[1]
            second_x = tup[2]
            second_y = tup[3]
            self.canvas.create_line(first_x, first_y,
                                    second_x, second_y, fill=constantss.MONOKAI_ORANGEH, width=10, arrow=tk.LAST)

    def start_arrow(self, first_x, first_y, second_x, second_y):
        tup = (first_x, first_y, second_x, second_y)
        self.arrows.append(tup)

        self.canvas.delete('all')
        self.draw_board()
        self.highlight_helper()
        self.draw_pieces()
        self.arrow_helper()

        global arrow
        global draw_arrow
        arrow = False
        draw_arrow = False

    # Coordinate transform for (x',y') = (0,0) is the top left corner (entire canvas) to
    # (x, y) = (0,0) is the bottom left corner(chessboard) is
    # (x = x' - 30,y = 700 - 30 - y')

    def draw_AI_arrow(self):
        global converted_x
        global converted_x2
        global converted_y
        global converted_y2
        self.start_arrow(converted_x, converted_y, converted_x2, converted_y2)

    def left_click(self, event):
        global draw_arrow
        global first_x
        global first_y
        global arrow
        x_pix = event.x - constantss.BOARD_OFFSET  # [-30, 670] left to right
        y_pix = constantss.BOARD_SIZE - constantss.BOARD_OFFSET - \
            event.y  # [-30, 670] bottom to top
        if arrow:
            # print("hello")
            draw_arrow = True
            first_x = event.x
            first_y = event.y
            arrow = False
        elif draw_arrow:
            # print("hello2")
            self.start_arrow(first_x, first_y, event.x, event.y)
        if DEBUG:
            print(f'left_click() at ({x_pix},{y_pix})')

    def right_click(self, event):
        x_pix = event.x - constantss.BOARD_OFFSET  # [-30, 670] left to right
        y_pix = constantss.BOARD_SIZE - constantss.BOARD_OFFSET - \
            event.y  # [-30, 670] bottom to top
        if DEBUG:
            print(f'right_click() at ({x_pix},{y_pix})')

        # Do nothing if the click occurred outside of board region.
        if (x_pix > (constantss.BOARD_SIZE - 2*constantss.BOARD_OFFSET)) or (y_pix > (constantss.BOARD_SIZE - 2*constantss.BOARD_OFFSET)) or (x_pix < 0) or (y_pix < 0):
            return

        # 0 through 7
        x_square = int(x_pix / constantss.SQUARE_SIZE)
        y_square = int(y_pix / constantss.SQUARE_SIZE)
        square = y_square*8 + x_square
        self.highlight(square)

        # Not sure what this is for yet
        # if self.board[square] >= 7:
        #     # Then black piece, i.e. AI
        #     # TODO: Display all possible moves from the AI
        #     self.highlight(square,color="blue")
        # elif self.board[square] >= 1:
        #     # Then white piece, i.e. human player
        #     # TODO: display all moves
        #     self.display_moves(square)

    def display_moves(self, square):
        letters = self.letters_from_square(square)
        fen = self.fen_string.get()
        for i in range(8):
            for j in range(8):
                to_square = i * 8 + j
                piece = self.board[to_square]
                if piece >= 1 and piece <= 7:
                    # Then white, so we can't move there
                    continue
                to_letters = self.letters_from_square(square)
                # TODO: fix errors then uncomment below
                # if valid_move(fen, letters + to_letters):
                #     self.highlight(to_square, "blue")

    # Returns letters of the square, e.g. "e1"

    def letters_from_square(self, square):
        x_sq = square % 8
        y_sq = 1 + int(square / 8)
        return "abcdefgh"[x_sq] + str(y_sq)

    def square_from_letters(self, letters):
        row = int(letters[1]) - 1
        col = ord(letters[0]) - ord("a")
        return row * 8 + col

    # Returns top left coordinates of square
    def coord_from_square(self, square):
        x_sq = square % 8
        y_sq = 1 + int(square / 8)
        x_pix = constantss.BOARD_OFFSET + x_sq * constantss.SQUARE_SIZE
        y_pix = constantss.BOARD_OFFSET + y_sq * constantss.SQUARE_SIZE
        return x_pix, y_pix

    # Returns square from coordinates
    def square_from_coord(self, x, y):
        x_pix = x - constantss.BOARD_OFFSET  # [-30, 670] left to right
        y_pix = constantss.BOARD_SIZE - constantss.BOARD_OFFSET - \
            y  # [-30, 670] bottom to top
        # Do nothing if the click occurred outside of board region.
        if (x_pix > (constantss.BOARD_SIZE - 2 * constantss.BOARD_OFFSET)) or (
                y_pix > (constantss.BOARD_SIZE - 2 * constantss.BOARD_OFFSET)) or (x_pix < 0) or (y_pix < 0):
            return -1

        # 0 through 7
        x_square = int(x_pix / constantss.SQUARE_SIZE)
        y_square = int(y_pix / constantss.SQUARE_SIZE)
        square = y_square * 8 + x_square

    def move(self, p1, p2):
        if DEBUG:
            print('ChessGui.move() executing...')

    def perform_highlight(self, tup):
        sq = tup[0]
        color = tup[1]
        alpha = tup[2]

        x_pix = int(sq % 8) * constantss.SQUARE_SIZE
        y_pix = int(sq / 8) * constantss.SQUARE_SIZE
        # Coordinate transfrom (x', y') = (0,0) is lower left (with margin) to
        # (x,y) = (0,0) is upper left without margin. (x = x' + 30, y = 700 - 30 - 80 - y' - 1)
        x_pos = x_pix + constantss.BOARD_OFFSET
        y_pos = constantss.BOARD_SIZE - constantss.BOARD_OFFSET - \
                y_pix - constantss.SQUARE_SIZE - 1

        alpha = int(alpha * 255)
        base = color  # If color is a tuple, we will use it directly
        if (color == 'red'):
            base = constantss.MONOKAI_RED
        elif (color == 'orange'):
            base = constantss.MONOKAI_ORANGE
        elif (color == 'yellow'):
            base = constantss.MONOKAI_YELLOW
        elif (color == 'green'):
            base = constantss.MONOKAI_GREEN
        elif (color == 'blue'):
            base = constantss.MONOKAI_BLUE
        elif (color == 'purple'):
            base = constantss.MONOKAI_PURPLE
        else:
            print("Possible error in highlight() if color was not a tuple...")

        color = base + (alpha,)
        image = PIL.Image.new(
            'RGBA', (constantss.SQUARE_SIZE, constantss.SQUARE_SIZE), color)
        self.highlighted_imgs.append(ImageTk.PhotoImage(image))
        return self.canvas.create_image(
            x_pos, y_pos, anchor='nw', image=self.highlighted_imgs[-1])

    def highlight_helper(self):
        for tup in self.highlighted_rects:
            self.perform_highlight(tup)

    # Highlights the square at the event.x, event.y
    def highlight(self, sq, color='purple', alpha=0.65):
        algsq = self.letters_from_square(sq)
        if DEBUG:
            print(f'ChessGui.highlight() on square [{algsq}]...')

        tup = (sq, color, alpha)


        if(tup in self.highlighted_rects):
            self.highlighted_rects.remove(tup)

            self.canvas.delete('all')
            self.draw_board()
            self.highlight_helper()
            self.draw_pieces()
            self.arrow_helper()
        else:
            self.highlighted_rects.append(tup)
            self.canvas.delete('all')
            self.draw_board()
            self.highlight_helper()
            self.draw_pieces()
            self.arrow_helper()

    def highlight_multiple(self, squares, colors, alphas):
        self.highlighted_rects = []
        for tup in zip(squares, colors, alphas):
            self.highlighted_rects.append(tup)
        self.canvas.delete('all')
        self.draw_board()
        self.highlight_helper()
        self.draw_pieces()
        self.arrow_helper()

    def addpiece(self, name, image, row=0, column=0):
        if DEBUG:
            print('ChessGui.addpiece() executing...')

    def placepiece(self, name, row, column):
        if DEBUG:
            print('ChessGui.placepiece() executing...')

    def refresh(self, event={}):
        # NEED TO IMPLEMENT!!
        if DEBUG:
            print('ChessGui.refresh() executing...')

    def draw_figure(self, ind, x_pos, y_pos):
        # The ordering of these if statements were created in the wee hours
        # of the night by Zander. The logic is strange but they matter
        # for efficiency. If you are unconvinced, that is okay.
        # The gist of it is that we check the most likely pieces first

        if self.board[ind] == constantss.EMPTY:
            # Don't draw anything if the square is empty
            pass
        elif self.board[ind] == constantss.LTPAWN:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_LTPAWN)
        elif self.board[ind] == constantss.DKPAWN:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_DKPAWN)
        elif self.board[ind] == constantss.LTROOK:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_LTROOK)
        elif self.board[ind] == constantss.DKROOK:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_DKROOK)
        elif self.board[ind] == constantss.LTKING:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_LTKING)
        elif self.board[ind] == constantss.DKKING:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_DKKING)
        elif self.board[ind] == constantss.LTBISHOP:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_LTBISHOP)
        elif self.board[ind] == constantss.DKBISHOP:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_DKBISHOP)
        elif self.board[ind] == constantss.LTQUEEN:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_LTQUEEN)
        elif self.board[ind] == constantss.DKQUEEN:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_DKQUEEN)
        elif self.board[ind] == constantss.LTKNIGHT:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_LTKNIGHT)
        elif self.board[ind] == constantss.DKKNIGHT:
            self.canvas.create_image(
                x_pos, y_pos, anchor='nw', image=self.IMG_DKKNIGHT)
        else:
            print(
                "[ERROR] ChessGui.draw_pieces(): board[ind] value matches no piece!")

    def draw_pieces(self):
        if DEBUG:
            print('ChessGui.draw_pieces() executing...')
        # Starting pixel counts for A1-square
        x_pos = constantss.BOARD_OFFSET  # = 30
        y_pos = constantss.BOARD_SIZE - constantss.BOARD_OFFSET - constantss.SQUARE_SIZE
        # = 590

        for rank in range(0, 8):
            for file in range(0, 8):
                ind = rank*8 + file

                self.draw_figure(ind, x_pos, y_pos)

                x_pos += constantss.SQUARE_SIZE
            # End inner for loop
            x_pos = constantss.BOARD_OFFSET
            y_pos -= 80
        # End outer for loop
    # End draw_pieces()

    def draw_board(self):
        if DEBUG:
            print('ChessGui.draw_board() executing...')
        self.canvas.create_image(0, 0, anchor='nw', image=self.IMG_CHESSBOARD)

    def reset_board_state(self):
        # initialize empty board. index 0 is A1 and 63 is H8
        self.board = [0]*64
        self.whitetomove = True
        self.wk_castle = True
        self.wq_castle = True
        self.bk_castle = True
        self.bq_castle = True
        self.possible_enpassant = '-'
        self.half_moves = 0
        self.full_moves = 1

    def input_fen(self):
        
        if DEBUG:
            print('ChessGui.input_fen() executing...')
        # uses partial from functools to help call load_fen with arguments from the button
        fen_input = self.fen_string.get()
        if DEBUG:
            print(f'Loading the following FEN string: {fen_input}')

        if(validateFEN.fenPass(fen_input)):
            self.canvas.delete('all')
            self.draw_board()
            self.load_fen(fen_input)
            self.draw_pieces()
        else:
            print(
                f'[ERROR] ChessGui.input_fen() failed to execute on "{fen_input}"')

        # if(fen_input == '4r1k1/2n1bppp/p3p3/1p6/8/1P2B1P1/P3PPBP/R5K1 w - - 1 1'
        #    or fen_input == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        #    or fen_input == '4r3/1b2n1pk/1p1r1p2/pP1p1Pn1/P1pP1NPp/2N1P2P/2R3B1/5RK1 b - - 0 1'):
        if DEBUG:
            print("heatmap")
        self.heatmap_analysis(fen_input)

    def clear_board(self):
        if DEBUG:
            print('ChessGui.clear_board() executing...')

        self.canvas.delete('all')
        self.highlighted_img = []
        self.highlighted_rects = []
        self.arrows = []
        self.draw_board()
        self.draw_pieces()

    def reset(self):
        if DEBUG:
            print('ChessGui.reset() executing...')
        self.update()
        # Reset board state
        self.canvas.delete('all')
        self.draw_board()
        self.load_fen(constantss.FEN_STARTING_POSITION)
        self.draw_pieces()

    def exit(self):
        if DEBUG:
            print("ChessGui.exit() executing...")
        self.parent.destroy()



    def heatmap_analysis(self, fen_input):
        with open(self.json_tree_path, 'r') as f:
            tree_dict = json.load(f)
        f.close()
        if DEBUG:
            print("loaded json")

        sequences = None

        if fen_input in tree_dict:
            sequences = tree_dict[fen_input]['sequences']
        else:
            tree = StockfishTreeNode(
                fen_input,
                self.stockfish_player,
                hack_probs=True
            ).build_tree(
                fen_input,
                B = 3,
                depth = 6
            )
            sequences = [[seq,p] for (seq,p) in tree.get_all_sequences()]
            # write to json to save time in future
            tree_dict[fen_input] = {
                'fen': fen_input,
                'json': tree.jsonify(),
                'sequences': sequences
            }
            json.dump(tree_dict, open(self.json_tree_path, 'w'))

        # if(fen_input == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        #     sequences = tree_dict[0]['sequences']
        # elif(fen_input == '4r3/1b2n1pk/1p1r1p2/pP1p1Pn1/P1pP1NPp/2N1P2P/2R3B1/5RK1 b - - 0 1'):
        #     sequences = tree_dict[1]['sequences']
        # elif(fen_input == '4r1k1/2n1bppp/p3p3/1p6/8/1P2B1P1/P3PPBP/R5K1 w - - 1 1'):
        #     sequences = tree_dict[2]['sequences']

        if DEBUG:
            print("sequences")
            print(sequences)

        self.display_text(sequences)

        self.display_multiple_sequences(
            sequences[0:min(15, len(sequences))],
            ['green' for _ in range(min(15, len(sequences)))],
            [(i < 8) for i in range(min(15, len(sequences)))]
        )

        if(DEBUG):
            print("ChessGui.heatmap_analysis() executed!")
            print("display sequence")

    def show_move_with_arrows(self, move):
        start = move[0] + move[1]
        end = move[2] + move[3]
        start_coords = constantss.LOOKUP_PIX[start]
        end_coords = constantss.LOOKUP_PIX[end]
        # Apply coordinate transform
        start_coords = (start_coords[0] + constantss.BOARD_OFFSET,
                        constantss.BOARD_SIZE - start_coords[1] - constantss.BOARD_OFFSET)
        end_coords = (end_coords[0] + constantss.BOARD_OFFSET,
                      constantss.BOARD_SIZE - end_coords[1] - constantss.BOARD_OFFSET)
        self.start_arrow(
            start_coords[0], start_coords[1], end_coords[0], end_coords[1])

    def display_sequence(self, seq_dict, color, arrow=False):
        seq = seq_dict[0]
        prob = seq_dict[1]

        if(arrow):
            first_move = seq[0]
            response = seq[1]
            self.show_move_with_arrows(first_move)
            self.show_move_with_arrows(response)
        if DEBUG:
            print("show move with arrows")

        squares = []
        colors = []
        vals = []
        for move in seq:
            start = move[0] + move[1]
            target = move[2] + move[3]
            start_sq = int(constantss.LOOKUP_NUM[start])
            target_sq = int(constantss.LOOKUP_NUM[target])
            squares.extend([start_sq,target_sq])
            colors.extend(['red', color])
            vals.extend([max(0.25, prob), max(0.25, prob)])
        self.highlight_multiple(squares, colors, vals)

        # for move in seq:
        #     start = move[0] + move[1]
        #     target = move[2] + move[3]
        #     start_sq = int(constantss.LOOKUP_NUM[start])
        #     target_sq = int(constantss.LOOKUP_NUM[target])
        #     print(start_sq, target_sq)
        #     self.highlight(start_sq, 'red', max(0.25, prob))
        #     self.highlight(target_sq, color, max(0.25, prob))
        #     print("highlight")

    def display_multiple_sequences(self, seqs, colors, use_arrows):

        squares = []
        clrs = []
        vals = []

        for seq_dict, color, use_arrow in zip(seqs, colors, use_arrows):
            seq = seq_dict[0]
            prob = seq_dict[1]
            if use_arrow:
                first_move = seq[0]
                response = seq[1]
                self.show_move_with_arrows(first_move)
                self.show_move_with_arrows(response)
            for move in seq:
                start = move[0] + move[1]
                target = move[2] + move[3]
                start_sq = int(constantss.LOOKUP_NUM[start])
                target_sq = int(constantss.LOOKUP_NUM[target])
                squares.extend([start_sq,target_sq])
                clrs.extend(['red', color])
                vals.extend([max(0.25, prob), max(0.25, prob)])

        self.highlight_multiple(squares, clrs, vals)

    def display_text(self, sequences):
        # self.log = self.canvas.create_rectangle(canvas_width + 20, 10, canvas_width+550, canvas_height-5, fill='red')
        canvas_width = self.IMG_CHESSBOARD.width()
        canvas_height = self.IMG_CHESSBOARD.height()
        self.text_x = canvas_width + 30
        self.text_y = 15
        dy = 0
        spacing = 5
        for i in range(min(len(sequences), 5)):
            dx = 0
            move = sequences[i][0]
            probability = float(sequences[i][1])
            p_lbl = tk.Label(text="Probability: " + str(probability)[:4], fg="green")
            p_lbl.place(x=self.text_x + dx, y = self.text_y + dy)
            dx += p_lbl.winfo_reqwidth() + spacing
            i = 0
            for elem in move:
                s = str(i+1) + ". " + elem[:2] + "→" + elem[2:]
                c = "#001DB2" # light blue
                if i % 2 == 0:
                    c = "#3377FF" # dark blue
                lbl = tk.Label(text=s, fg=c, cursor="hand1")
                lbl.place(x = self.text_x + dx, y = self.text_y + dy)
                disp_fun = lambda elem, lbl, b : (lambda x : self.disp_move(x, elem, lbl, b))
                lbl.bind("<Button-1>", disp_fun(elem,lbl, i%2 == 0))
                lbl.bind("<Button-2>", lambda e: self.hide_move(e))
                lbl.bind("<Button-3>", lambda e: self.hide_move(e))
                dx += lbl.winfo_reqwidth() + spacing
                i += 1
            dy += p_lbl.winfo_reqheight() + spacing

    def hide_move(self, event = None):
        if self.last_disp is None:
            return
        self.canvas.delete(self.last_disp[0])
        self.canvas.delete(self.last_disp[1])


    def disp_move(self, event, moveseq,lbl, b):
        square1 = self.square_from_letters(moveseq[:2])
        square2 = self.square_from_letters(moveseq[2:])
        self.hide_move()
        if b:
            color = "blue"
        else:
            color = "purple"
        self.last_disp = (self.perform_highlight((square1, color, 0.5)),
                          self.perform_highlight((square2, color, 0.5)))

        # if DEBUG:
        #     print(squares, clrs, vals)

        #self.highlight_multiple(squares, clrs, vals)
            
def display():
    root = tk.Tk()
    root.title('AlphaViz')
    root.resizable(width=False, height=False)
    root.wm_geometry("1280x760")

    gui = ChessGui(root)
    gui.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    root.mainloop()
    if DEBUG:
        print('display() completed gracefully')


if __name__ == "__main__":
    display()
    if DEBUG:
        print('chess_gui main completed gracefully')
