from tkinter import Tk #GUI
from random import choice   
import chess    
import ai
import gui
class Game:
    board = chess.Board() #initialize the board 
    print(board)
    player_turns = [choice([True, False])]  #randomly chooses the players turn 
    # print(player_turns)
    is_player_white = player_turns[-1]

    root = Tk()     #initialises the GUI 
    root.title('CHESS BOARD')

    def __init__(self):
        self.display = gui.GUI(self.root, self, self.board, self.player_turns)
        self.display.pack(
            side='top', fill='both', expand='true', padx=4, pady=4)

    def start(self):
        if self.player_turns[-1]:
            self.display.label_status["text"] = "You play as white."

            self.root.after(1000, self.player_play) #its again start displaying after 1s by calling self.player_play
        else:
            self.display.label_status[
                "text"] = "You play as black. The computer is thinking..."

            self.root.after(1000, self.computer_play)

        self.root.mainloop()

    def player_play(self):
        self.display.label_status["text"] = "Player's turn."

        # wait as long as possible for player's input
        self.root.after(100000000, self.computer_play)

    def computer_play(self):
        ai.AI(self.board, self.is_player_white).ai_move()  #calls AI class

        self.display.refresh()
        self.display.draw_pieces()

        self.player_turns.append(True)
        if self.board.is_checkmate():
            self.display.label_status["text"] = "Checkmate."
        elif self.board.is_stalemate():
            self.display.label_status["text"] = "It was a draw."
        else:
            self.display.label_status[
                "text"] = "Computer's turn. The computer is thinking..."

            self.root.after(100, self.player_play)


Game().start()
