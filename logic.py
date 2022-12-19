import random
import sys
import pandas as pd
import uuid


class Database:
    def __init__(self):

        # CSV integration
        self.path = "game_data.csv"
        try:
            with open("game_data.csv"):

                self.games = pd.read_csv(self.path,index_col=0)
        except FileNotFoundError:

            self.games = pd.DataFrame(
                columns=[
                    "move1",
                    "move2",
                    "move3",
                    "move4",
                    "move5",
                    "move6",
                    "move7",
                    "move8",
                    "move9", #max 9 moves total
                    "game_id",
                    "winner",
                    "winner_char",
                    "playerX",
                    "playerO",
                    
                ]
            )

    #New Game Initialization
    def insert_game(self, game_id, playerX, playerO):

        self.games = self.games.append(

            {"game_id": game_id, "playerX": playerX, "playerO": playerO},
            
            ignore_index=True,
        )
        self.save()

    # Insert a move into a game
    def insert_move(self, game_id, move_number, coordinates):

        game = self.games[self.games["game_id"] == game_id]
        if len(game) == 0:

            return False
        move_column = "move" + str(move_number)
        self.games.loc[self.games["game_id"] ==
                       game_id, move_column] = coordinates
        self.save()
        return True

    # Update the winner of a game
    def update_winner(self, game_id, winner, win_char):

        game = self.games[self.games["game_id"] == game_id]
        if len(game) == 0:

            return False
        self.games.loc[self.games["game_id"] == game_id, "winner"] = winner
        self.games.loc[self.games["game_id"] ==
                       game_id, "winner_char"] = win_char
        self.save()
        return True

    # Get all games in the database
    def get_all_games(self):

        return self.games


    # Get a specific game by game_id
    def get_game_by_id(self, game_id):

        return self.games[self.games["game_id"] == game_id]

    def get_stats(self):

        games = self.games
        combined_matches = len(games)
        if combined_matches == 0:

            return {
                "human_wins": 0,
                "robot_wins": 0,
                "win_percentages": {"human": 0, "bot": 0},
                "combined_matches": 0,
            }
        # Win record Calibration
        human_wins = len(games[games["winner"] == "Human"])
        robot_wins = len(games[games["winner"] == "Bot"])
        # Statistics % Calibration
        robot_win_percentage = robot_wins/combined_matches * 100
        human_win_percentage = human_wins/combined_matches * 100

        return {
            "combined_matches": combined_matches,
            "human_wins": human_wins,
            "robot_wins": robot_wins,
            "win_percentages":{
                "human": human_win_percentage,
                "robot": robot_win_percentage,
            },
        }
    # get the most played first choice from statistics - get_most_common_first_move
    def most_frequent_first_choice(self):

        games = self.games
        if len(games)==0:

            return None
        first_moves = games["move1"]
        first_move_counter = first_moves.value_counter()
        if len(first_move_counter)==0:

            return None
        most_frequent_first_pick=first_move_counter.index[0]
        return most_frequent_first_pick

    def least_frequent_first_choice(self):

        games=self.games
        if len(games)==0:

            return None
        first_moves=games["move1"]
        first_move_counter=first_moves.value_counter()
        if len(first_move_counter)==0:

            return None
        least_frequent_first_pick = first_move_counter.index[len(first_move_counter) - 1]
        return least_frequent_first_pick

    # Save to the CSV file
    def save(self):

        self.games.to_csv(self.path)


class Board:

    def __init__(self) -> None:

        self._rows = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def __str__(self) -> str:

        s="-------\n"
        for row in self._rows:

            for cell in row:
                s=s+"|"
                if cell==None:

                    s=s+" "
                else:
                    s=s+cell
            s=s+"|\n-------\n"
        return s
    # assigning and returning values
    def get(self,x,y):

        return self._rows[x][y]

    def set(self,x,y,value):

        self._rows[x][y]=value

    #check if board state has a legal winner
    def _check_winners(self,winning_symbol):

        board=self._rows

        if board[0][0]==board[0][1]==board[0][2]==winning_symbol:

            return winning_symbol

        elif board[1][0]==board[1][1]==board[1][2]==winning_symbol:

            return winning_symbol

        elif board[2][0]==board[2][1]==board[2][2]==winning_symbol:

            return winning_symbol
            
        elif board[0][0]==board[1][0]==board[2][0]==winning_symbol:

            return winning_symbol

        elif board[0][1]==board[1][1]==board[2][1]==winning_symbol:

            return winning_symbol

        elif board[0][2]==board[1][2]==board[2][2]==winning_symbol:

            return winning_symbol

        elif board[1][1]==board[2][2]==board[0][0]==winning_symbol:

            return winning_symbol

        elif board[0][2]==board[1][1]==board[2][0]==winning_symbol:

            return winning_symbol
        else:

            return None

#keeps track of all back-end statistics,csv, etc.
class Game:

    def __init__(self, playerX, playerO):

        self._board=Board()
        self._playerX=playerX
        self._playerO=playerO
        self.current_player=self._playerX
        self.current_char="X" #switch this to O for consistency testing
        self.db=Database()
        self.game_id=uuid.uuid4().hex
        self.db.insert_game(
            self.game_id, self._playerX.type, self._playerO.type)

    #player toggling
    def switch_player(self):

        if self.current_player==self._playerX:

            self.current_player=self._playerO
            self.current_char="O"
            return

        self.current_player=self._playerX
        self.current_char="X"

    def run(self):

        move_number=1
        while move_number<=9:#Board will be filled up if it reaches this number

            print(f"Please choose Player {self.current_char}")
            row, column=self.current_player.get_move(
                self._board, self.current_char)
            coordinates=str(row)+'-'+str(column)
            self.db.insert_move(self.game_id,move_number,coordinates)
            if self._board._check_winners(self.current_char):

                print(f"{self.current_char} is victorious")
                self.db.update_winner(
                    self.game_id, self.current_player.type,self.current_char)
                print(self.db.get_stats())
                print('Most chosen first move->',
                      self.db.most_frequent_first_choice())
                print('Least chosen first move->',
                      self.db.least_frequent_first_choice())
                # self.db.save()
                sys.exit("Match Fin")

            move_number+=1
            self.switch_player() 

        print("Stalemate")
        self.db.update_winner(self.game_id, "Draw", "NONE")
        print(self.db.get_stats())#checking if data tracks with input/results

#Human Class
class Human:
    def __init__(self) -> None:
        
        self.type="Human"

    def get_move(self,board,char):

        # reveal board state
        print(board)

        # accept input from user(s)
        row=int(input("Please input the row coordinate you wish to change [0-2]> "))
        column=int(input("Please input the column coordinate you wish to change [0-2]> "))

        # check if spot is already filled 
        if board.get(row,column)!=None:
            print("Square already contains symbol :( ")
            self.get_move(board,char)

        board.set(row,column,char)
        print(board) #comment out to not receive board state after submitting a selection
        return (row,column)
        

#To call this a simple AI class is an insult to real AI
class Bot:
    def __init__(self) -> None:

        self.type="Bot"

    def get_move(self,board,char):

        row=random.randint(0,2)
        column=random.randint(0,2)
        if board.get(row,column)!=None:

            self.get_move(board,char)
        else:

            board.set(row,column,char)
            print(board)
        return (row,column)