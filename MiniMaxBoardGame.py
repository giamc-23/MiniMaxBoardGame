from board import Board
from player import Player
from gamestate import GameState
import math
import time

count = 0
dcount = 0

class MinimaxInfo:
    def __init__(self, value, bestmove):
        self.value = value
        self.bestmove = bestmove

def is_terminal(board):
    if board.game_state == GameState.MAX_WIN or board.game_state == GameState.MIN_WIN or board.game_state == GameState.TIE:
        return True
    return False

def ACTIONS(board):
    actions = []
    for cols in range(board.num_cols):
        if board.is_column_full(cols):
            continue
        actions.append(cols)

    return actions         

def is_cutoff(board, depth):
    if depth == dcount:
        return True
    return False


#With the heuristic I attempted to create was where if there was a situation where it was 2 in a row
#you give the current value 50 points, if there's 3 in a row they get 150 points
def EVAL(board):
    count = 0
    for r in range(0, board.num_rows):
            for c in range(0, board.num_cols):
                
                if ((c <= board.num_cols - board.consec_to_win and board.two_match_in_a_row(r, c))
                    or (r <= board.num_rows - board.consec_to_win and board.two_match_in_a_col(r, c))
                    or (r <= board.num_rows - board.consec_to_win and c <= board.num_cols - board.consec_to_win and board.two_match_in_ne_diag(r, c))
                    or (r <= board.num_rows - board.consec_to_win and c - board.consec_to_win >= -1 and board.two_match_in_nw_diag(r, c))):

                    if board.board[r][c] == 1:
                        count += 50
                    elif board.board[r][c] == -1:
                        count -= 50
                        
                if ((c <= board.num_cols - board.consec_to_win and board.three_match_in_a_row(r, c))
                    or (r <= board.num_rows - board.consec_to_win and board.three_match_in_a_col(r, c))
                    or (r <= board.num_rows - board.consec_to_win and c <= board.num_cols - board.consec_to_win and board.three_match_in_ne_diag(r, c))
                    or (r <= board.num_rows - board.consec_to_win and c - board.consec_to_win >= -1 and board.three_match_in_nw_diag(r, c))):

                    if board.board[r][c] == 1:
                        count += 150
                    elif board.board[r][c] == -1:
                        count -= 150
                        
    return count 
    
    

def utility(board):
    if board.game_state == GameState.MAX_WIN:
        return int(10000.0 * board.num_rows * board.num_cols / board.moves_made_so_far)
    elif board.game_state == GameState.MIN_WIN:
        return int(-1 * 10000.0 * board.num_rows * board.num_cols / board.moves_made_so_far)
    else:
        return 0

def to_move(board):
    return board.player_to_move

def result(board, action):
    return board.make_move(action)
    
    
        
def MiniMax(board, table):
    if board in table:
        return table[board]
    
    elif is_terminal(board):
        util = utility(board)
        info = MinimaxInfo(util, None)
        table[board] = info
        return info
    
    elif to_move(board) == Player.MAX:
        v = -math.inf
        best_move = None
        for action in ACTIONS(board):
            child_board = result(board, action)
            child_info = MiniMax(child_board, table)
            v2 = child_info.value
            if v2 > v:
                v = v2
                best_move = action        
        info = MinimaxInfo(v, best_move)
        table[board] = info
        return info

    else:
        v = math.inf
        best_move = None
        for action in ACTIONS(board):
            child_board = result(board, action)
            child_info = MiniMax(child_board, table)
            v2 = child_info.value
            if v2 < v:
                v = v2
                best_move = action
        info = MinimaxInfo(v, best_move)
        table[board] = info
        return info

def AlphaBeta(board, alpha, beta, table):
    global count
    
    if board in table:
        return table[board]
    
    elif is_terminal(board):
        util = utility(board)
        info = MinimaxInfo(util, None)
        table[board] = info
        return info
    
    elif to_move(board) == Player.MAX:
        v = -math.inf
        best_move = None
        for action in ACTIONS(board):
            child_board = result(board, action)
            child_info = AlphaBeta(child_board,alpha, beta, table)
            v2 = child_info.value
            if v2 > v:
                v = v2
                best_move = action
                alpha = max(alpha,  v)
            if v >= beta:
                count += 1
                return MinimaxInfo(v, best_move) 
        info = MinimaxInfo(v, best_move)
        table[board] = info
        return info

    else:
        v = math.inf
        best_move = None
        for action in ACTIONS(board):
            child_board = result(board, action)
            child_info = AlphaBeta(child_board,alpha, beta, table)
            v2 = child_info.value
            if v2 < v:
                v = v2
                best_move = action
                beta = min(beta, v)
            if v <= alpha:
                count += 1 
                return MinimaxInfo(v, best_move)
        info = MinimaxInfo(v, best_move)
        table[board] = info
        return info

def AlphaBetaH(board, alpha, beta, depth, table):
    if board in table:
        return table[board]
    
    elif is_terminal(board):
        util = utility(board)
        info = MinimaxInfo(util, None)
        table[board] = info
        return info

    elif is_cutoff(board, depth):
        heuristic = EVAL(board)
        info = MinimaxInfo(heuristic, None)
        table[board] = info       
        return info
    
    elif to_move(board) == Player.MAX:
        v = -math.inf
        best_move = None
        for action in ACTIONS(board):
            child_board = result(board, action)
            child_info = AlphaBetaH(child_board,alpha, beta, depth + 1, table)
            v2 = child_info.value
            if v2 > v:
                v = v2
                best_move = action
                alpha = max(alpha,  v)
            if v >= beta:
                return MinimaxInfo(v, best_move) 
        info = MinimaxInfo(v, best_move)
        table[board] = info
        return info

    else:
        v = math.inf
        best_move = None
        for action in ACTIONS(board):
            child_board = result(board, action)
            child_info = AlphaBetaH(child_board,alpha, beta, depth + 1, table)
            v2 = child_info.value
            if v2 < v:
                v = v2
                best_move = action
                beta = min(beta, v)
            if v <= alpha:
                return MinimaxInfo(v, best_move)
        info = MinimaxInfo(v, best_move)
        table[board] = info
        return info  

def main():
    while(True):
        global dcount 
        runpart = input("Run part A, B, or C? ")
        debug = input("Include debugging info? (y/n) ")
        rowinput = int(input("Enter rows: "))
        colinput = int(input("Enter columns: "))
        rowtowin = int(input("Enter number in a row to win: "))

        board = Board(rowinput, colinput, rowtowin)
        table = dict()

            
        if(runpart == "A"):
            start_time = time.time()
            MiniMax(board, table)
        elif(runpart == "B"):
            start_time = time.time()
            AB = AlphaBeta(board, -math.inf, math.inf, table)
            print("The tree was pruned " + str(count) + " time")
        else:
            # account for depth with C 
            dcount = int(input("Number of moves to look ahead(depth): "))


        # Since C doesn't immediately determine if someone will win    
        if runpart != "C":
            if debug == "y":
                for key, value in table.items():
                    print(key.to_2d_string())
                    print("MinimaxInfo [value = " + str(value.value) +" action = " + str(value.bestmove) +"]") 
            print("Search completed in %s seconds" % (time.time() - start_time))
            if table[board].value > 0:
                print("First player has a guaranteed win with perfect play")
            elif table[board].value < 0:
                print("Second player has a guaranteed win with perfect play")
            else:
                print("Neither player has a guaranteed win; game will end in tie with perfect play on both sides.")
            
        print("Transposition table has "+ str(len(table))+ " states")
        playing = int(input("Who plays first? 1=human, 2=computer: "))
    
        while(True):
            optimal = 0
            print(board.to_2d_string())

            if runpart == "C":
                table = dict()
                AlphaBetaH(board, -math.inf, math.inf, 0, table)
                print("Transposition table has "+ str(len(table))+ " states")
            
            if board not in table and runpart == "B":
                AlphaBeta(board,-math.inf, math.inf, table)
                
            print("Minimax value for this state: "+ str(table[board].value)+ " Optimal Moves " + str(table[board].bestmove))
        
            if(board.player_to_move == Player.MAX):
                print("It is MAX's turn!")
            else:
                print("It is MIN's turn!")
            
            if playing == 1:
                move = int(input("Enter a move: "))
                board = board.make_move(move)
                playing = 2
            else:
                move = table[board].bestmove
                board = board.make_move(move)
                print("Computer chooses move: "+ str(move))
                playing = 1

            #board.get_winner
            if(board.game_state != GameState.IN_PROGRESS):
                if board.game_state == GameState.MAX_WIN:
                    print("MAX Wins")
                elif board.game_state == GameState.MIN_WIN:
                    print("MIN Wins")
                else:
                    print("Tie")
                print(board.to_2d_string())
                again = input("Play again? (y/n) " )
                break
        if again == "n":
            return False
    
main()
