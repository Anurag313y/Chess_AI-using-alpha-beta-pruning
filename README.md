# Chess_AI-using-alpha-beta-pruning

The project is build in python3 in which you can play chess against an AI with a specified decision tree depth ( depth = 3) that uses minimax algorithm ( which is recursive backtracking algorithm) for best optimal move for the player, assuming that both player play optimally and further optimized using alpha-beta pruning. Aside from basic moves, this chess-Ai also implements chess rules such as castling, en passant, fifty-move rule, threefold repetition, and pawn promotion.<br/> 
   For the further optimization here I applied the concept of dynamic programming, by caching the states and use the state value when needed.

## Libraries used :
   PIL
   chess
   numpy
   
## Modules used :
   pickle
   tkinter
   random
   
## How It Works :
   ### Min-max tree : It's a decision tree used to find the best optimal move for the player. Here we use tree with depth 3.<br/>
   <img src="https://github.com/Anurag313y/Chess_AI-using-alpha-beta-pruning/blob/master/img/Decision%20Tree.png" width="128"/>


   
How to Play:<br/>
    1.git clone https://github.com/Anurag313y/Chess_AI-using-alpha-beta-pruning<br/>
    2.cd CHESS-AI/src<br/>
    3.make    #Run the make file which installs all the requirements<br/>
    4.python3 main.py<br/>
