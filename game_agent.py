"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

# ###########################################################################
# call one of three versions
#
# ###########################################################################
def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    #print("custom_score() player=",player)

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")



    # set to "A", "B", or "C"
    select = "A"
    
    if select=="A":
        return custom_score_A(game, player)
    elif select=="B":
        return custom_score_B(game, player)
    elif select=="C":
        return custom_score_C(game, player)
    else:
        print("Error - please select a valid custom_score()")    
   
    
    
# ###########################################################################
# strategy changes with the number of blank spaces remaining - the stage of
# the game. 
#
# early game (over 20 squares remaining):  
#    - use the standard (own_moves minus opp_moves) heuristic
#                       
# end game:
#    - use the second moves (own second move minus opponent second moves)
#    - if we can block the opponent's next move, increase the score
#    
# ###########################################################################
def custom_score_A(game, player):
    opponent = game.get_opponent(player)
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)
    own_count = len(own_moves)
    opp_count = len(opp_moves)
    blank_count = len(game.get_blank_spaces())
    
    # can we block the opponent 
    # and still have a move after that?
    can_block = False
    for m1 in own_moves:
        if m1 in opp_moves:
            new_game = game.forecast_move(m1)
            next_moves = new_game.get_legal_moves(new_game.inactive_player)
            if len(next_moves)>0:
                can_block = True
        
    # unique second move counts
    own_moves_level2_unique = []
    for m1 in own_moves:
        new_game = game.forecast_move(m1)
        own_moves_level2 = new_game.get_legal_moves(new_game.inactive_player)
        for m2 in own_moves_level2:
            if m2 not in own_moves_level2_unique:
                own_moves_level2_unique.append(m2)
                     
    opp_moves_level2_unique = []
    for m1 in opp_moves:
        new_game = game.forecast_move(m1)
        opp_moves_level2 = new_game.get_legal_moves(new_game.active_player)
        for m2 in opp_moves_level2:
            if m2 not in opp_moves_level2_unique:
                opp_moves_level2_unique.append(m2)  
    
   
    
    # game start
    if blank_count>20:  
        ret = own_count - opp_count
        
    # end game    
    else:  
        ret = len(own_moves_level2_unique) - len(opp_moves_level2_unique)
        if can_block:
            ret += 2
            
    
    return float(ret)
    


# ###########################################################################
# assume a 7x7 board
# tier 0 = the ring of 24 outer squares
# tier 1 = the ring of 16 squares one space in from the outer ring
# tier 2 = the center 9 squares
# 
# Score based on current position
# Inner squares are better than outer squares
# ###########################################################################    
def custom_score_B(game, player):
    opponent = game.get_opponent(player)
    own_pos = game.get_player_location(player)
    opp_pos = game.get_player_location(opponent)                          
       
    tier1 = [ (1,1),(2,1), (3,1), (4,1), (5,1), (5,2), (5,3), (5,4), (5,5),
             (4,5), (3,5), (2,5), (1,5), (1,4), (1,3), (1,2)]
    tier2 = [ (2,2), (2,3), (2,4), (3,2), (3,3), (3,4), (4,2), (4,3), (4,4)]
    own_tier_score = 0
    if own_pos in tier1:
        own_tier_score = 1
    elif own_pos in tier2:
        own_tier_score = 2.5
    
    opp_tier_score = 0
    if opp_pos in tier1:
        opp_tier_score = 1
    elif own_pos in tier2:
        opp_tier_score = 2.5
   
    ret = (own_tier_score - opp_tier_score) 
    return float(ret)

# ###########################################################################
# count the number of unique second moves for each player
#
# heuristic = own second moves minus opponent second moves
#
# ###########################################################################
def custom_score_C(game, player):  
    opponent = game.get_opponent(player)
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opponent)

    # unique second move counts
    own_moves_level2_unique = []
    for m1 in own_moves:
        new_game = game.forecast_move(m1)
        own_moves_level2 = new_game.get_legal_moves(new_game.inactive_player)
        for m2 in own_moves_level2:
            if m2 not in own_moves_level2_unique:
                own_moves_level2_unique.append(m2)
                     
    opp_moves_level2_unique = []
    for m1 in opp_moves:
        new_game = game.forecast_move(m1)
        opp_moves_level2 = new_game.get_legal_moves(new_game.active_player)
        for m2 in opp_moves_level2:
            if m2 not in opp_moves_level2_unique:
                opp_moves_level2_unique.append(m2)  
    
    ret = len(own_moves_level2_unique) - len(opp_moves_level2_unique)
    return float(ret)



class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=30.):  # was 10.
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
    
    
    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        
        no_move = -1, -1
        best_move = no_move
        best_score = float("-inf")
        
        # if no moves, return -1,-1
        if len(legal_moves)==0:
            return no_move
        

        # make calls based on self.method and self.iterative:
        #    minimax with interative deepening
        #    minimax without fixed depth
        #    alphabeta with iteractive deepening
        #    alphabeta with fixed depth
        try:
            if (self.method=="minimax"):
                # minimax iterative deepening
                if self.iterative:
                    for iter_depth in range(1,10000):
                        score, move = self.minimax(game, iter_depth)
                        if score>best_score:
                            best_score = score
                            best_move = move 
                
                # minimax fixed depth
                else:
                    best_score, best_move = self.minimax(game, self.search_depth)
                       
                            
            elif (self.method=="alphabeta"):
                # alphabeta iterative deepening
                if self.iterative:
                    for iter_depth in range(1,10000):
                        score, move = self.alphabeta(game, iter_depth)
                        if score>best_score:
                            best_score = score
                            best_move = move
                
                # alphabeta fixed depth
                else:
                    best_score, best_move = self.alphabeta(game, self.search_depth)
                        
            else:
                print("============ unexpected method=========", self.method)
                
                    
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            
        except Timeout:
            pass
         
         
        if (best_move[0]==-1 and best_move[1]==-1 and len(legal_moves)>0):
            best_move = legal_moves[0] 
         
        #print("get_move() best move=",best_move,game.active_player) 
        #print(game.to_string())
        return best_move
        
       


    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        # set a higher threshold (+20 rather than +10) to allow more time after timout
        if self.time_left() < (self.TIMER_THRESHOLD+20):
            raise Timeout()

         # return score when we reach the lowest depth
        if (depth<=0):
            player = game.active_player
            if (maximizing_player==False):
                player = game.inactive_player  
           
            score = self.score(game, player)
            return score, None
        
        
        
        # initialize  
        best_score = float("-inf")
        if (maximizing_player==False):
             best_score = float("inf") 
        best_move = -1,-1
        next_maximize = not maximizing_player
        
      
        
        # loop through the legal moves for the active player at this level
        # forecast each move and score it using recursion
        # we will use the values propagated to us from the lowest level (depth==0)   
        legal_moves_active = game.get_legal_moves(game.active_player)   
        for move in legal_moves_active:
            next_game = game.forecast_move(move)
            
            score, _ = self.minimax(next_game, depth-1, next_maximize)
            if (maximizing_player==True):
                if (score>best_score):
                    best_score = score
                    best_move = move
            else:  # maximizing_player = false
                if (score<best_score):
                    best_score = score
                    best_move = move
           
        # if best_move is -1,-1, return a good move    
        if (best_move[0]==-1 and best_move[1]==-1 and len(legal_moves_active)>0):
            best_move = legal_moves_active[0]
              
        return best_score,best_move
        
          
       

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
       
        best_move = -1,-1 
        
        # return score when we reach the lowest depth
        if (depth<=0):
            player = game.active_player
            if (maximizing_player==False):
                player = game.inactive_player 
            score = self.score(game, player)
            return score, None
        
                  
        legal_moves_active = game.get_legal_moves(game.active_player) 
        
        # use local variables to store parameters
        # not necessary, but cleaner (does not change input parms)
        this_alpha = alpha
        this_beta = beta

        if maximizing_player==True:
            best_score = float("-inf")
            for move in legal_moves_active:
                #print("move=",move)
                next_game = game.forecast_move(move)
                score, _ = self.alphabeta(next_game, depth-1, this_alpha, this_beta, False) 
                
                if score>best_score:
                    best_move = move    
                best_score = max(best_score, score)
                this_alpha = max(this_alpha, best_score)
                
                # prune
                if this_beta<=this_alpha:
                    break
        
        else:      # minimizing player
            best_score = float("inf")
            for move in legal_moves_active:
                next_game = game.forecast_move(move)
                score, _ = self.alphabeta(next_game, depth-1, this_alpha, this_beta, True) 
                
                if score<best_score:
                    best_move = move    
                
                best_score = min(best_score, score)
                this_beta = min(this_beta, best_score)
                   
                # prune
                if this_beta<=this_alpha:
                    break
    
         # if best_move is -1,-1, return a good move    
        if (best_move[0]==-1 and best_move[1]==-1 and len(legal_moves_active)>0):
            best_move = legal_moves_active[0]
            
        return best_score, best_move    
