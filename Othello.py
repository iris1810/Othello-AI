#######################################
# Name: Khai Tran Nguyen
# Class: CSC 4993 _ Artificial Intelligence
# Date : Nov 1 2025
# Assignment 3 : Othello Game AI
#######################################

# create an 8×8 Othello board with the initial 4 discs (black always moves first)
# show the board after every move (ASCII is fine)
# let a human type a move like d3 or D3
# check if that move is legal (i.e. it outflanks at least one opponent disc)
# flip all outflanked discs in all 8 directions
# handle “no legal moves → pass” rule
# detect game over (neither player can move, or board full)
# count discs and announce winner

import pygame
import random
import copy

# the direction to capture (flip) your opponent’s discs
# That line can go:
    # horizontally (left or right)
    # vertically (up or down)
    # diagonally (up-left, up-right, down-left, down-right)
DIRECTIONS =[
    (-1,0), # up
    (1,0),  # down
    (0,-1), # left
    (0,1),  # right
    (-1,-1),# up-left
    (-1,1), # up-right
    (1,-1), # down-left
    (1,1)   # down-right
]


#### Utility functions ####
def loadImages(path, size):
    """ Load an image into the game, and scale it to the given size """
    img = pygame.image.load(f"{path}").convert_alpha() # keep the transparency of the image
    img = pygame.transform.scale(img,size)
    return img


class Othello:
    ############# INITIALIZE THE GAME #############
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100,800)) # In turple, the pixel dimensions of the window
        pygame.display.set_caption("Othello Game AI")

        self.rows = 8
        self.colums = 8 

        self.board = Board(self.rows, self.colums,(80,80),self)

        self.RUN = True
        self.current_player = 1 # 1 = black starts first
        self.game_over = False
        self.font = pygame.font.SysFont("Arial", 24, bold=True)

        ## AI setting 
        self.ai_color = None # let user choose 1 for black, 2 white, 0 - 2 people no AI
        self.search_depth = 3 # limited depth for minimax search
        self.use_alpha_beta = True # toggle on/off per move
        self.debug_mode = False # toggle per move 

        # for ai take turn store the last result
        self.last_nodes = 0
        self.last_evaluate  = 0
        self.last_ai_move = None

        # for Player want computer help to decided 
        self.hint_move = None  # store a suggested move to draw on the board



    def run(self):
        while self.RUN == True :
            self.input()
            self.update()
            self.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False
            
            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # block human clicks if it's AI's turn or game over
                if self.game_over or self.current_player == self.ai_color:
                    return
                
                if event.button == 3: # right click
                    self.board.printGameLogicBoard()
                if event.button == 1: # left click
                    row,col = self.board.mouse_to_cell(event.pos) # get the current position of mouse 
                  
                  
                    # check for valid cell => yes then check another condition
                    if row is not None: 
                        # check for this move have flips -> flips -> swith player
                        moved = self.board.make_move(row,col,self.current_player)

                        if moved == True: # if true
                            # switch the player 
                            if self.current_player == 1:
                                self.current_player = 2
                            else:
                                self.current_player = 1

                            ## Check for automatic check before switch turn,
                            #  if next player will not have move, skip next player's turn 
                            if self.board.has_move(self.current_player) == False:
                                #switch back to the other player
                                if self.current_player == 1:
                                    self.current_player = 2
                                else:
                                    self.current_player = 1
                                
                                print("There are no valid move for next player, skip next player's turn")

            # Check for key press SPACE for reset, Q for Quit the game   
            if event.type == pygame.KEYDOWN:

                #Quit if Q
                if event.key == pygame.K_q:
                    self.RUN = False

                # Hotkeys to toggle AI settings
                # 1 black or 2 white for AI color
                if event.key == pygame.K_1:
                    self.ai_color = 1 # black
                    print("AI color set to BLACK")
                if event.key == pygame.K_2:
                    self.ai_color = 2 # white
                    print("AI color set to WHITE")

                # '[' to decrease or ']' to increase search depth
                if event.key == pygame.K_LEFTBRACKET:
                    if self.search_depth >1:
                        self.search_depth -= 1
                        print(f"Search depth decreased to {self.search_depth}")
                if event.key == pygame.K_RIGHTBRACKET:
                    self.search_depth += 1
                    print(f"Search depth increased to {self.search_depth}")
                
                # p toggle alpha-beta pruning
                if event.key == pygame.K_p:
                    self.use_alpha_beta = not self.use_alpha_beta  # if it uses alpha => change to not use alpha, vice versa
                    print(f"Alpha-Beta Pruning is set to {self.use_alpha_beta}")

                # d toggle debug mode
                if event.key == pygame.K_d:
                    self.debug_mode = not self.debug_mode # change to the opposite state for debug mode
                    print(f"Debug mode is: {self.debug_mode} ")

                # a Force AI move if it's AI's turn
                if event.key == pygame.K_a:
                    if not self.game_over and self.current_player == self.ai_color:
                        self._ai_take_turn()
                
                if event.key == pygame.K_1:
                    self.ai_color = 1  # black
                    print("AI color set to BLACK")

                if event.key == pygame.K_2:
                    self.ai_color = 2  # white
                    print("AI color set to WHITE")

                # 0 key = turn off AI completely (2-player mode)
                if event.key == pygame.K_0:
                    self.ai_color = None
                    print("AI disabled (2-player mode)")

                # H = show a hint (best move for the current player)
                if event.key == pygame.K_h:
                    if not self.game_over:
                        move, score, nodes, _ = self._compute_best_move_for(self.current_player)
                        self.hint_move = move  # could be None if pass
                        if self.debug_mode:
                            print(f"HINT for {'BLACK' if self.current_player==1 else 'WHITE'}: {move} (score={score})")

                # M = let the computer make a move for the current player (human or AI)
                if event.key == pygame.K_m:
                    if not self.game_over:
                        self._make_move_for(self.current_player)

                # Reset if SPACE
                if event.key == pygame.K_SPACE:
                    self.board = Board(self.rows, self.colums, (80,80),self) # new board
                    self.current_player = 1 # black starts first
                    self.game_over = False
                    self.last_nodes = 0
                    self.last_evaluate = 0
                    self.last_ai_move = None
                    print("Game Reset!")
                

    def update (self):
        """check for game over condition"""
        if self.game_over == True:
            return # no need to check anymore
        
        if not self.board.has_move(self.current_player):
            # switch to the other player
            self.current_player = 2 if self.current_player == 1 else 1

        # if the other player ALSO has no move -> game over
        if not self.board.has_move(self.current_player):
            self.game_over = True
            return  # stop this frame; let the next frame handle AI/human normally   
        
        # Force AI to move as soon as it’s their turn
        if self.current_player == self.ai_color:
            self._ai_take_turn()
        
        # check if both player have no move => True, 
        # means has_move => false => not False is true, True for no move 
        no_move_player1 = not self.board.has_move(1) # return not false = true
        no_move_player2 = not self.board.has_move(2) 
        full = self.board.board_full() # make sure the board is full

        if full == True or (no_move_player1 and no_move_player2)==True:
            self.game_over = True


    def draw (self):
        self.screen.fill((0,0,0)) # fill with black color in turple

        # let the board draw by itself 
        self.board.draw(self.screen)

        # Draw for the score
        black_score, white_score = self.board.score()
        score_text = self.font.render(f"BLACK - {black_score}   |   WHITE - {white_score}", True, (255,250,250))
        self.screen.blit(score_text,(765,370))

        # Draw for the current player
        if self.game_over == False:
            if self.current_player == 1:
                who = "BLACK"
            else:
                who = "WHITE"
            turn_text = self.font.render(f"T U R N : {who}", True, (255,250,250))
            self.screen.blit(turn_text,(80,35))

        else:
            #game over text, it can be tie
            winner = "T I E"
            if black_score > white_score:
                winner = "B L A C K   W I N S !"
            elif white_score > black_score:
                winner = "W H I T E   W I N S !"
            else:
                winner = "T I E"

            end_text = self.font.render(f"G A M E  O V E R !     {winner}", True, (179,27,27))
            self.screen.blit(end_text,(345,750))

        ## draw for ON/OFF alpha_beta, and show the nodes
        information = self.font.render(
            f"AI depth = {self.search_depth}  |  αβ = {'ON' if self.use_alpha_beta else 'OFF'}  "
            f"|  Nodes = {self.last_nodes}  |  Evaluate = {self.last_evaluate}",
            True, (255,250,250)
        )
        self.screen.blit(information, (400,35))

        mode = "2-PLAYER" if self.ai_color is None else f"VS AI ({'BLACK' if self.ai_color==1 else 'WHITE'})"
        mode_text = self.font.render(f"Mode   {mode}", True, (255,250,250))
        self.screen.blit(mode_text, (793,430))


        pygame.display.update()

    ## terminal test( gameover for search )
    def _is_terminal (self):
        # True if is have no more move for BOTH color or full board 
        return self.board.board_full() or (not self.board.has_move(1)) and (not self.board.has_move(2))

################ MIN MAX WITH OPTION ALPHA BETA  ###########
    def minimax (self,depth, player_to_move, alpha, beta, use_ab, ai_color, indent = "" ):
        """ Return (best_score, best_move, nodes_explored, debug_lines)
        score:      backed-up heuristic value from this node
        best_move:  (row, col) chosen at this node (None at leaves or pass)
        nodes:      number of nodes visited in this subtree 
        debug_lines: list[str] human-readable trace (only filled if debug on)

        Args:
        depth:           remaining ply to search (0 => evaluate now)
        player_to_move:  whose turn at this node (1 = BLACK, 2 = WHITE)
        alpha, beta:     current pruning bounds for max/min windows
        ai_color:        which color the AI controls (1 or 2)
        use_ab:          whether to apply alpha, beta pruning
        indent:          indentation prefix for pretty debug printing"""

        nodes = 1 # total number of nodes (game states) explored under this branch.
        debug_log = []

        # terminal or depth limit check
        # if we reach the depth limit or game is over then (terminal), return a leaf evaluation
        if self._is_terminal() or depth ==0:
            score = self.board.evaluate(ai_color)
            if self.debug_mode: # True
                debug_log.append(f"{indent}Evaluate d={depth} score={score}")
            return score, None, nodes, debug_log
        
        # generate a ldegal move for ....
        moves = self.board.valid_move(player_to_move)

        # PASS rule (not terminal): switch player and reduce depth
        # player dont have move => pass that move to another player
        if not moves:
            if self.debug_mode:
                if player_to_move == ai_color:
                    role = "MAX"
                else: 
                    role = "MIN"
                # then recursive to opponent with depth - 1
                debug_log.append(f"{indent}{role} PASS")

            # in the children node we dont care about child best move, so just "_" ignore it 
            if player_to_move == 1:
                next_mover = 2
            else:
                next_mover = 1

            score, _, child_node, child_db_log = self.minimax(
                depth -1,
                next_mover,
                alpha, beta, use_ab, ai_color,
                indent + " " ) # indent deeper in the tree
            
            nodes += child_node
            debug_log += child_db_log

            # no move at this node since it pass
            return score, None, nodes, debug_log
        
        #### Decided whether this node is MAX or MIN
        # if it's AI turn, maximize, otherwise minimize
        is_maximize = (player_to_move == ai_color)

        if is_maximize:
            # MAX mode - AI try to maximize score
            best_score = -float("inf")
            best_move = None 

            for (r,c) in moves:
                # for each candiate, get the flip then we can undo 
                flips = self.board.apply_move(r,c, player_to_move)
                if not flips:  # safety guard, valid_move should ensure this though
                    continue

                # in the children node we dont care about child best move, so just "_" ignore it 
                if player_to_move == 1:
                    next_mover = 2
                else:
                    next_mover = 1

                # recursive to the oponent 
                child_score, _, child_node, child_db_log = self.minimax(
                    depth -1,
                    next_mover,
                    alpha,beta,use_ab,ai_color,
                    indent + " "
                )
                # undo the board state, ready for the next cadinate
                self.board.undo_move(r,c, flips, player_to_move)
                # accumulate node count and debug log
                nodes += child_node

                # if it is in debug mode
                if self.debug_mode:
                    # add this move in the MAX
                    debug_log.append(f"{indent}MAX d={depth} move={(r,c)} -> {child_score}")
                    # add the child explore in
                    debug_log += child_db_log

                # keep the larges value for MAX
                if child_score > best_score:
                    best_score = child_score
                    best_move = (r,c) 

                # if it is in the alpha-beta update and possible prune
                if use_ab:
                    alpha = max(alpha,best_score)
                    if beta <= alpha:
                        if self.debug_mode:
                            debug_log.append(f"{indent}PRUNE beta <= alpha (α={alpha:.2f}, β={beta:.2f})")
                        break
                    
            return best_score, best_move, nodes, debug_log
        
        else:
            ####### MIN node (opponent tries to minimize the score)
            best_score = float("inf")
            best_move = None 

            for (r,c) in moves:
                flips = self.board.apply_move(r,c,player_to_move)
                if not flips:  # safety guard
                    continue
                
                # in the children node we dont care about child best move, so just "_" ignore it 
                if player_to_move == 1:
                    next_mover = 2
                else:
                    next_mover = 1

                # dont care best move in child -> '_'
                child_score,_,child_node, child_db_log = self.minimax(
                    depth -1,
                    next_mover,
                    alpha,beta,use_ab,ai_color,
                    indent + " "
                )
                # undo the flips (correct args)
                self.board.undo_move(r, c, flips, player_to_move)
                nodes += child_node

                # if it is in the debug mode
                if self.debug_mode:
                    debug_log.append(f"{indent}MIN  d={depth} move={(r,c)} -> {child_score} ")
                    debug_log += child_db_log

                # Min keep the smallest score
                if child_score <= best_score:
                    best_score = child_score
                    best_move = (r,c)

                #If it in alpha-beta mode
                if use_ab:
                    beta = min(beta, best_score)
                    if beta <= alpha: # prune, because alpha is the current maximize, 
                        #if it smaller the current max, no need future find any smaller => prun
                        if self.debug_mode:
                            debug_log.append (f"{indent} PRUNE beta <= alpha (α={alpha:.2f}, β={beta:.2f})")
                        break 
            return best_score, best_move, nodes, debug_log


    def _ai_take_turn(self):
        # Ensure: do nothing if game ended or not AI's turn
        if self.game_over or self.current_player != self.ai_color:
            return
        
        if not self.board.has_move(self.current_player):
            self.current_player = 2 if self.current_player == 1 else 1
            return
        
        # ask minimax for the best move for the current position
        #    Returns: score (heuristic), best move (r,c) or None (pass),
        #             nodes (visited states), debug_log (debug lines for printing)
        score,move,nodes,db_log = self.minimax(self.search_depth,
                                               self.current_player,
                                               -float("inf"),float("inf"),
                                               self.use_alpha_beta,
                                               self.ai_color,indent ="")
        # save nodes, score, move after the move
        self.last_nodes = nodes     # total explored nodes for this decision
        self.last_evaluate = score  # backed-up evaluation returned by minimax
        self.last_ai_move = move    # the move chosen by minimax (or None if pass)

        # print full decision trace
        if self.debug_mode:
            print("=== DEBUG (one AI turn) ===")
            for line in db_log:
                 print(line)

        # if no legal move : pass rule
        if move is None :
            if self.current_player ==1:
                self.current_player =2
            else:
                self.current_player =1 

        # It has Move, make that chosen move, then swtich turn
        r,c = move
        self.board.make_move(r,c,self.current_player)

        if self.current_player ==1:
            self.current_player =2
        else:
            self.current_player =1 

    def _compute_best_move_for(self, player):
        """Return (move, score, nodes, db_log) 
        for the given player using current search settings.
        ai_color in minimax is set to 'player' so that side is maximized."""
        if not self.board.has_move(player):
            return None, None, 0, []

        score, move, nodes, db_log = self.minimax(
            depth=self.search_depth,
            player_to_move=player,
            alpha=-float("inf"),
            beta=float("inf"),
            use_ab=self.use_alpha_beta,
            ai_color=player,      
            indent=""
        )
        # record diagnostics 
        self.last_nodes = nodes
        self.last_evaluate = score
        self.last_ai_move = move

        return move, score, nodes, db_log


    def _make_move_for(self, player):
        """Have the computer actually play one move for 'player'.
        Returns True if a move was played, False if pass/no move."""
        move, score, nodes, db_log = self._compute_best_move_for(player)

        if self.debug_mode:
            role = "BLACK" if player == 1 else "WHITE"
            print(f"=== DEBUG (computer plays for {role}) ===")
            for line in db_log:
                print(line)

        if move is None:
            # PASS: if it's currently this player's turn, switch; also check double-pass -> game over
            if self.current_player == player:
                self.current_player = 2 if player == 1 else 1
                if not self.board.has_move(self.current_player):
                    self.game_over = True
            return False

        r, c = move
        self.board.make_move(r, c, player)

        # if we just played for the side whose turn it is, switch the turn
        if self.current_player == player:
            self.current_player = 2 if player == 1 else 1

        # clear hint once we make a move
        self.hint_move = None
        return True


class Board:
    def __init__(self,rows, cols, size, main):
        self.GAME = main
        self.y = rows
        self.x = cols
        self.size = size

        self.whitetoken = loadImages("tokens/white_token.png",size)
        self.blacktoken = loadImages("tokens/black_token.png",size)
        self.transitionWhiteToBlack= [loadImages(f"tokens/BlackToWhite{i}.png",self.size) for i in range (1,4)]
        self.transitionBlackToWhite= [loadImages(f"tokens/WhiteToBlack{i}.png",self.size) for i in range (1,4)]

        # 2D list represent the state of the board - what piece is on each square 
        self.boardLogic = self.regenBoard(self.y, self.x)

    def regenBoard(self, rows, cols): # regenerate the board with all value for each cell 
        """ generate an empty board for logic use """
        board = []
        for y in range (rows):
            line = []
            for x in range (cols):
                line.append(0)
            board.append(line)

        # Put the 4 starting disks
        mid1 = rows // 2-1 # 3
        mid2 = rows // 2   # 4
        board[mid1][mid1] = 2 # D4 White
        board[mid1][mid2] = 1 # E4 Black
        board[mid2][mid1] = 1 # D5 Black
        board[mid2][mid2] = 2 # E5 White

        return board
    
    def printGameLogicBoard(self):
        print('  | A | B | C | D | E | F | G | H |')
        for i, row in enumerate(self.boardLogic): # enumerate to get the index and the item in the list
            line = f"{i} |".ljust(3, " ") # 3 is the length of string we want, fill up with " " space, start from left
            for item in row:
                line += f"{item}".center(3," ") + "|" # center the item, with the width = 3
            print(line)
        print() # print a new line

    def draw(self,surface):
        #1. draw the background squares
        board_color = (237,232,208) # olive green color
        line_color = (120,117,105) # light green color
        tile_w, tile_h = self.size # 80,80
        offset_x = 80 # so board is not at the edge of the window, at the center 
        offset_y = 80

        for row in range(self.y):
            for col in range(self.x):
                # compute each square position
                x = offset_x + col * tile_w
                y = offset_y + row * tile_h
                # create the rectangle for 1 cell with that information
                rectangle = pygame.Rect(x,y,tile_w,tile_h)
                #draw the square and the outline
                pygame.draw.rect(surface, board_color, rectangle)
                pygame.draw.rect(surface, line_color, rectangle, 2) # 2 is the 2 pixel border thickness

        #2. Draw pieces according to boardLogic
        for row in range (self.y):
            for col in range (self.x):
                value = self.boardLogic [row][col]

                if value == 0: # empty cell
                    continue # skip that cell
                
                # for cell not equal 0 , then calculate the screen coordinates of that square.
                x = offset_x + col * tile_w
                y = offset_y + row * tile_h

                if value == 1: # black piece 
                    surface.blit(self.blacktoken, (x,y))
                elif value == 2: # white piece
                    surface.blit(self.whitetoken, (x,y)) #draw this image at this position

        # Draw hightlight legal moves for current player
        next_moves = self.valid_move(self.GAME.current_player)
        highlight_color = (179,27,27) 
        tile_w, tile_h = self.size
        offset_x = 120
        offset_y = 120
        for r,c in next_moves:
            x = offset_x + c*tile_w
            y = offset_y + r*tile_h
            pygame.draw.circle(surface,highlight_color,(x,y),5)
        
        ## draw for Hint
        # draw a hint marker if present (for the current player)
        if self.GAME.hint_move is not None:
            hr, hc = self.GAME.hint_move
            tile_w, tile_h = self.size
            # use the SAME offsets you used to draw the grid, so marker aligns!
            offset_x = 80
            offset_y = 80
            # center of the cell
            cx = offset_x + hc * tile_w + tile_w // 2
            cy = offset_y + hr * tile_h + tile_h // 2
            pygame.draw.circle(surface, (155, 19, 19), (cx, cy), 15, 4)  # simple white ring

    
    def mouse_to_cell(self,mouse_position):
        """ Convert mouse position to board cell coordinates """
        mx, my = mouse_position
        tile_w, tile_h = self.size
        offset_x = 80
        offset_y = 80

        #shift back the offset
        mx = mx - offset_x
        my = my - offset_y

        if mx < 0 or my < 0 :
            return None, None # outside the board
        col = mx // tile_w  # b/c before that we have x = offset_x + col * tile_w
        row = my // tile_h 

        if 0 <= row < self.y and 0 <= col < self.x:
            return row,col
        return None,None # outside the board    
    
    ## Find flip positions
    def on_board(self, row, col):
        """ Check if the given position is on the board """
        return 0 <= row < self.y and 0 <= col < self.x
    
    def find_flips(self,row,col,player):
        """ Return a list of (r,c) to flip if player plays at (row,col).
            player 1 = black, 2 = white"""
        if self.boardLogic[row][col] !=0: # the square already have a piece, =0 is empty
            return [] # no flips possible
        if player == 1 :
            opponent = 2 
        else :
            opponent = 1
        flips = [] # list of positions to fli

        # loop through all 8 direction 
        for direction_r, direction_c in DIRECTIONS:
            r = row + direction_r # take 1 step in that direction 
            c = col + direction_c
            line = [] # temporary list to store potential flips in this direction

            # collect token in this direction, collect all opponent
            while self.on_board(r,c) and self.boardLogic[r][c] == opponent:
                line.append((r,c))
                r += direction_r
                c += direction_c
            
            # if it is the player piece
            if self.on_board(r,c) and self.boardLogic[r][c] == player:
                flips.extend(line) # add to flips all the opponent in that direction, 
                                    #then loop another direction
            else:
                # empty square on the board => so the line still keep line [] -> empty for this direction
                line = []

        return flips
    
    def make_move(self,row,col,player):
        """when player make a move, check the board for flips and modyfied the board"""
        flips = self.find_flips(row,col,player)

        if not flips: # mean flips == [] empty
            return False
        
        # that move have flips
        self.boardLogic[row][col] = player
        for (r,c) in flips:
            self.boardLogic[r][c] = player

        # After do turn , clear hint it
        self.GAME.hint_move = None
        
        return True
    
    #### Helper function: check valid move #####
    def valid_move(self,player):
        """check if (r,c) is valid for player"""
        moves = []
        for r in range (self.y):
            for c in range (self.x):
                # on board and have flips mean it is the valid move
                if self.on_board(r,c) and self.find_flips(r,c,player):
                    moves.append((r,c))
        return moves
    
    def has_move(self,player):
        """return True is player has move, move > 0"""
        return len(self.valid_move(player)) >0 
    
    def board_full(self):
        """return True if all squares are filled"""
        for r in range (self.y):
            for c in range (self.x):
                if self.boardLogic[r][c] == 0: # not full yet
                    return False
        return True
    
    def score (self):
        """Count the amount of pieces for each player"""
        black_score =0
        white_score =0
        for r in range (self.y):
            for c in range (self.x):
                if self.boardLogic[r][c] == 1:
                    black_score +=1
                elif self.boardLogic[r][c] ==2:
                    white_score += 1
        return black_score, white_score
    
    def evaluate (self, ai_color):
        """Return a heuristic score from ai_color perspective.
        Higher score better for ai_color"""
        # the difference betwwen 2 disc color + small mobility term + bigger corner term
        # Count for disc , 1 value
        if ai_color == 1  :
            opponent_color = 2
        else: 
            opponent_color = 1

        ai_disc =0
        opp_disc =0
        for r in range (self.y):
            for c in range (self.x):
                if self.boardLogic[r][c] == ai_color:
                    ai_disc += 1
                elif self.boardLogic[r][c] == opponent_color:
                    opp_disc += 1
        disc_term = ai_disc - opp_disc

        # count mobility for both sides , 2 value
        ai_moves = len(self.valid_move(ai_color))
        opp_moves = len(self.valid_move(opponent_color))
        mobility_term = ai_moves - opp_moves
    
        # count corners for both sides using, 25 value 
        corners = [(0,0), (0,self.x-1), (self.y-1,0), (self.y-1,self.x-1)]
        ai_corner = 0
        opp_corner = 0
        for (r,c) in corners:
            if self.boardLogic[r][c] == ai_color:
                ai_corner += 1
            if self.boardLogic[r][c] == opponent_color:
                opp_corner +=1
        
        corner_term = ai_corner - opp_corner 

        # return the weight by multiple with value and sum all of that
        return (1 * disc_term) + (2 * mobility_term) + (25 * corner_term)
        
    ### Apply/ Undo helpers 
    def apply_move(self, row, col, player):
        """Apply move, return list of flipped squares so we can undo"""
        flips = self.find_flips(row,col,player)

        if not flips: # the list is empty 
            return None
        
        self.boardLogic[row][col] = player
        for (r,c) in flips:
            self.boardLogic[r][c]= player
        
        return flips # for undo move
    
    def undo_move (self,row,col,flips,player):
        if not flips: # no list of flip
            return None
        
        if player == 1:
            opponent = 2
        else:
            opponent = 1

        self.boardLogic[row][col] = 0 # for empty 
        for (r,c) in flips:
            self.boardLogic[r][c] = opponent

        
############# MAIN ##############
if __name__ == "__main__":
    print("Welcome to Othello!")
    print("You can play:")
    print(" - Human vs Human (default)")
    print(" - Human vs AI (press 1 - Black or 2 - White to choose AI color)")
    print(" - Press 0 to disable AI (return to 2-player mode)")
    print(" - Press SPACE to reset, Q to quit\n")
    game = Othello()
    game.run()
    pygame.quit()
