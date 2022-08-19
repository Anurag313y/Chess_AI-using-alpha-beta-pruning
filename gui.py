import tkinter   #tkinter is the standard GUI Library
from PIL import Image, ImageTk #PIL is the Python Imaging Library 

import chess #python-chess is a pure Python chess library with move generation, move validation and support for common formats.

ROW_NUMBER = 8
COLUMN_NUMBER = 8

ROW_CHARS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

WHITE = '#F0D9B5'
BLACK = '#B58863'
YELLOW = '#AEB188'
GREEN = '#646D40'

class GUI(tkinter.Frame):
    square_size = 64
    pieces = {}
    icons = {}
    selected_piece = None
    start_square = None
    highlighted_pieces = []

    def __init__(self, root, parent, board, player_turns):
        # construction
        self.root = root
        self.parent = parent
        self.board = board
        self.player_turns = player_turns

        # frame
        tkinter.Frame.__init__(self, root)

        # canvas
        canvas_width = COLUMN_NUMBER * self.square_size
        canvas_height = ROW_NUMBER * self.square_size

        self.canvas = tkinter.Canvas(
            self, width=canvas_width, height=canvas_height, background='grey')
        self.canvas.pack(side='top', fill='both', anchor='c', expand=True)
        self.canvas.bind('<Button-1>', self.click)

        # drawing
        self.refresh()
        self.draw_pieces()

        # status bar
        self.statusbar = tkinter.Frame(self, height=32)
        self.label_status = tkinter.Label(self.statusbar, text='', fg='black')
        self.label_status.pack(side=tkinter.LEFT, expand=0, in_=self.statusbar)
        self.statusbar.pack(expand=False, fill='x', side='bottom')

    def click(self, event):
        # block clicks if not in player's turn
        if not self.player_turns[-1]:
            return None

        column_size = row_size = event.widget.master.square_size
        row = int(8 - (event.y / row_size))
        column = int(event.x / column_size)
        position = (row, column)

        # check if player is selecting their other piece
        piece = self.board.piece_at(row * 8 + column)
        is_own = False
        if piece is not None and self.selected_piece is not None:
            is_piece_lower = piece.symbol().islower()
            is_selected_piece_lower = self.selected_piece.symbol().islower()

            is_own = not is_piece_lower ^ is_selected_piece_lower

        # move it or replace it
        if self.selected_piece is None or is_own:
            self.selected_piece = piece
            self.start_square = (row, column)

            self.highlight()
        else:
            self.move(dest_square=position)

            self.selected_piece = None
            self.start_square = None

            self.pieces = {}
            self.highlighted_pieces = []

        self.refresh()
        self.draw_pieces()

    def move(self, dest_square):
        # making move notation, such as e2e4
        move = ROW_CHARS[self.start_square[1]] + str(self.start_square[0] + 1)
        move += ROW_CHARS[dest_square[1]] + str(dest_square[0] + 1)

        legal_moves = [str(legal_move) for legal_move in self.board.legal_moves]

        # handle pawn promotion
        if move + 'q' in legal_moves:
            move += 'q'

        if move in legal_moves:
            self.board.push(chess.Move.from_uci(move))
            self.player_turns.append(False)
            if self.board.is_checkmate():
                self.label_status['text'] = "Checkmate."
            elif self.board.is_stalemate():
                self.label_status['text'] = "It was a draw."
            else:
                self.label_status[
                    'text'] = "Computer's turn. The computer is thinking..."

                self.root.after(100, self.parent.computer_play)
        else:
            self.label_status['text'] = "Wrong move, try again."

    def highlight(self):
        self.highlighted_pieces = []

        legal_moves = [str(legal_move) for legal_move in self.board.legal_moves]

        selected_square = ROW_CHARS[self.start_square[1]] + str(
            self.start_square[0] + 1)

        self.highlighted_pieces = [(int(legal_move[-1]) - 1,
                                    ROW_CHARS.index(legal_move[2])) if
                                   selected_square == legal_move[:2] else None
                                   for legal_move in legal_moves]

    def refresh(self, event={}):
        if event:
            x_size = int((event.width - 1) / COLUMN_NUMBER)
            y_size = int((event.height - 1) / ROW_NUMBER)
            self.square_size = min(x_size, y_size)

        self.canvas.delete('square')
        color = BLACK

        for row in range(ROW_NUMBER):
            color = WHITE if color == BLACK else BLACK

            for col in range(COLUMN_NUMBER):
                start_column = (col * self.square_size)
                start_row = ((7 - row) * self.square_size)
                end_column = start_column + self.square_size
                end_row = start_row + self.square_size

                if (row, col) in self.highlighted_pieces:
                    self.canvas.create_rectangle(
                        start_column,
                        start_row,
                        end_column,
                        end_row,
                        outline='',
                        fill=YELLOW,
                        tags='square')
                elif ((row, col) == self.start_square) and (
                        self.selected_piece is not None):
                    self.canvas.create_rectangle(
                        start_column,
                        start_row,
                        end_column,
                        end_row,
                        outline='',
                        fill=GREEN,
                        tags='square')
                else:
                    self.canvas.create_rectangle(
                        start_column,
                        start_row,
                        end_column,
                        end_row,
                        outline='',
                        fill=color,
                        tags='square')

                color = WHITE if color == BLACK else BLACK

        for name in self.pieces:
            self.place_piece(name, self.pieces[name][0], self.pieces[name][1])

        self.canvas.tag_raise('piece')
        self.canvas.tag_lower('square')

    def draw_pieces(self):
        self.canvas.delete('piece')

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)

            if piece is not None:
                image_name = 'img/%s.png' % (piece.symbol())
                piece_name = '%s%s' % (piece.symbol(), square)

                if image_name not in self.icons:
                    image = Image.open(image_name).resize((64, 64))
                    self.icons[image_name] = ImageTk.PhotoImage(image)

                row = square // 8
                column = square % 8

                self.add_piece(piece_name, self.icons[image_name], row, column)
                self.place_piece(piece_name, row, column)

    def add_piece(self, name, image, row=0, column=0):
        self.canvas.create_image(
            0, 0, image=image, tags=(name, 'piece'), anchor='c')
        self.place_piece(name, row, column)

    def place_piece(self, name, row, column):
        self.pieces[name] = (row, column)

        row_size = (column * self.square_size) + (self.square_size // 2)
        column_size = ((7 - row) * self.square_size) + (self.square_size // 2)

        self.canvas.coords(name, row_size, column_size)
