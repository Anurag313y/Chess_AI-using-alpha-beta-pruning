# Chess_AI-using-alpha-beta-pruning

The project is build in python3 in which you can play chess against an AI with a specified decision tree depth ( depth = 3) that uses minimax algorithm ( which is recursive backtracking algorithm) for best optimal move for the player, assuming that both player play optimally and further optimized using alpha-beta pruning. Aside from basic moves, this chess-Ai also implements chess rules such as castling, en passant, fifty-move rule, threefold repetition, and pawn promotion.<br/> 
   For the further optimization here I applied the concept of dynamic programming, by caching the states and use the state value when needed.

## Libraries & Modules used :
   *PIL<br/> 
   *chess<br/> 
   *numpy<br/> 
   *pickle<br/> 
   *tkinter<br/> 
   *random<br/> 
  
   
## How It Works :
    Min-max tree : 
   It's a decision tree used to find the best optimal move for the player. Here we use tree with depth 3.<br/>
   <img src="https://github.com/Anurag313y/Chess_AI-using-alpha-beta-pruning/blob/master/img/Decision%20Tree.png" width="600"/>
   
    Board evaluation : 
    Each piece has a different table influencing where to go and a piece value determining its importance. The king has two         tables, early game and late game tables to determine how it moves.
    The board score is calculated using the board evaluation function .
    The entire board score = (White position score + white piece score) - (Black position score + black piece score)
    Here we used following piece values for the different chess pieces : 
    pawn    = 1000 (since it is least important)
    rook    = 5000
    knight  = 3000
    bishop  = 3000
    queen   = 9000
    king    = 1000000 (since it is most important)
    
   
   
   Min-max algorithm: 
   This algorithm is used in game playing & uses DFS traversal to explore the decision tree. One player is called Maximizer and    other is called Minimizer. Here maximizer will take maximum value while minimizer will take minimum value. 
   In this algorithm both player will try to get maximum benifits and trying to minimize the profit of his opponent player. 

   This will decide which move has to be taken by checking all the possible valid moves & their board value .
   <img src="https://github.com/Anurag313y/Chess_AI-using-alpha-beta-pruning/blob/master/img/minmax.png" width="600"/>
   
   Alpha-Beta Pruning : 
   It removes all the nodes which are not really affecting the final decision but making algorithm slow. Hence by pruning these    nodes, it makes the algorithm fast.
    <img src="https://github.com/Anurag313y/Chess_AI-using-alpha-beta-pruning/blob/master/img/alphabeta.png" width="600"/>
    
    

   
How to Play:<br/>
    1.git clone https://github.com/Anurag313y/Chess_AI-using-alpha-beta-pruning<br/>
    2.cd CHESS-AI/src<br/>
    3.make    #Run the make file which installs all the requirements<br/>
    4.python3 main.py<br/>
