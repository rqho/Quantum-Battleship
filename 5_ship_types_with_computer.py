import random
import os
from colorama import Fore, Style

LENGTH_OF_SHIPS = [2, 3, 4]  
PLAYER_BOARD = [[" "] * 8 for i in range(8)]

'''
Dictionary:
- "row" - row associated with other ship in superposition
- "column" - column associated with other ship in superposition
- "prob" - probability of ship being there
'''
PLAYER_SUPERPOSITION_BOARD = [[{"row": 0, "column": 0, "prob": 00}] * 8 for i in range(8)]

COMPUTER_BOARD = [[" "] * 8 for i in range(8)]

'''
Dictionary:
- "row" - row associated with other ship in superposition
- "column" - column associated with other ship in superposition
- "prob" - probability of ship being there
'''
COMPUTER_SUPERPOSITION_BOARD = [[{"row": 0, "column": 0, "prob": 00}] * 8 for i in range(8)]

PLAYER_GUESS_BOARD = [[" "] * 8 for i in range(8)]
COMPUTER_GUESS_BOARD = [[" "] * 8 for i in range(8)]
LETTERS_TO_NUMBERS = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}

def print_board(board):
    if board == PLAYER_BOARD:
        print("Your Board:")
    elif board == COMPUTER_BOARD:
        print("Computer's Board:")
    elif board == PLAYER_GUESS_BOARD:
        print("Your Guesses:")
    elif board == COMPUTER_GUESS_BOARD:
        print("Computer's Guesses:")
    elif board == PLAYER_SUPERPOSITION_BOARD:
        print("Your Superposition Board:")
    elif board == COMPUTER_SUPERPOSITION_BOARD:
        print("Computer's Superposition Board:")
    
    row_number = 1
    if board == COMPUTER_SUPERPOSITION_BOARD or board == PLAYER_SUPERPOSITION_BOARD:
        print("  A  B  C  D  E  F  G  H")
        print(" -+--+--+--+--+--+--+--+-")
        for row in board:
            # print the row number and probabilities, if probability is 0, print "  ", if probability is single digit, add a space
            print("%d|%s|" % (row_number, "|".join(["%2d" % (column["prob"]) if column["prob"] > 0 else "  " for column in row])))
            row_number += 1
    else:
        print("  A B C D E F G H")
        print("  +-+-+-+-+-+-+-+")
        for row in board:
            print("%d|%s|" % (row_number, "|".join(row)))
            row_number += 1
    print("_________________________\n")

#place Ships
def place_ships(board):
    #loop through length of ships
    for ship_length in LENGTH_OF_SHIPS:
        #loop until ship fits and doesn't overlap
        first_ship_placed = False
        superpos_ship_placed = False
        ship_info = [{} for _ in range(ship_length)]
        ship_info_s = [{} for _ in range(ship_length)]
        prob = 0
        while not (first_ship_placed and superpos_ship_placed):
            if board == COMPUTER_BOARD:
                orientation, row, column, prob = random.choice(["H", "V"]), random.randint(0,7), random.randint(0,7), random.randint(1,99)
                orientation_s, row_s, column_s, prob_s = random.choice(["H", "V"]), random.randint(0,7), random.randint(0,7), (100-prob) #superposition ship
                if (first_ship_placed == False):
                    if check_ship_fit(ship_length, row, column, orientation):
                        #check if ship overlaps
                        if ship_overlaps(board, row, column, orientation, ship_length) == False:
                            #place ship
                            if orientation == "H":
                                for i in range(ship_length):
                                    board[row][i + column] = "X"
                                    ship_info[i] = {"row": row, "column": i + column, "prob": prob}
                            else:
                                for i in range(ship_length):
                                    board[i + row][column] = "X"
                                    ship_info[i] = {"row": i + row, "column": column, "prob": prob}
                            first_ship_placed = True
                # place superposition ship only if original ship is placed
                if (first_ship_placed == True):
                    if check_ship_fit(ship_length, row_s, column_s, orientation_s):
                        #check if ship overlaps
                        if ship_overlaps(board, row_s, column_s, orientation_s, ship_length) == False:
                            #place ship
                            if orientation_s == "H":
                                for i in range(ship_length):
                                    board[row_s][i + column_s] = "X"
                                    ship_info_s[i] = {"row": row_s, "column": i + column_s, "prob": prob_s}
                            else:
                                for i in range(ship_length):
                                    board[i + row_s][column_s] = "X"
                                    ship_info_s[i] = {"row": i + row_s, "column": column_s, "prob": prob_s}
                            # Update SUPERPOSITION_BOARD
                            # Add first ship, which stores row and column of superposition ship and its own probability
                            # Add superposition ship, which stores row and column of first ship and its own probability
                            for i in range(ship_length):
                                COMPUTER_SUPERPOSITION_BOARD[ship_info[i]["row"]][ship_info[i]["column"]] = {
                                    "row": ship_info_s[i]["row"],
                                    "column": ship_info_s[i]["column"],
                                    "prob": prob
                                }
                                COMPUTER_SUPERPOSITION_BOARD[ship_info_s[i]["row"]][ship_info_s[i]["column"]] = {
                                    "row": ship_info[i]["row"],
                                    "column": ship_info[i]["column"],
                                    "prob": prob_s
                                }
                            superpos_ship_placed = True
            else:
                if (first_ship_placed == False):
                    print('Place the ship with a length of ' + str(ship_length))
                    row, column, orientation, prob = user_input(True)
                    if check_ship_fit(ship_length, row, column, orientation):
                        #check if ship overlaps
                        if ship_overlaps(board, row, column, orientation, ship_length) == False:
                            #place ship
                            if orientation == "H":
                                for i in range(ship_length):
                                    board[row][i + column] = "X"
                                    ship_info[i] = {"row": row, "column": i + column, "prob": prob}
                            else:
                                for i in range(ship_length):
                                    board[i + row][column] = "X"
                                    ship_info[i] = {"row": i + row, "column": column, "prob": prob}
                            clear_terminal()
                            print_board(PLAYER_BOARD)
                            # print_board(PLAYER_SUPERPOSITION_BOARD)
                            first_ship_placed = True
            
                if (first_ship_placed == True):
                    print('Place the superposition ship with a length of ' + str(ship_length))
                    row_s, column_s, orientation_s = user_input(False)
                    prob_s = 100 - prob
                    if check_ship_fit(ship_length, row_s, column_s, orientation_s):
                        #check if ship overlaps
                        if ship_overlaps(board, row_s, column_s, orientation_s, ship_length) == False:
                            #place ship
                            if orientation_s == "H":
                                for i in range(ship_length):
                                    board[row_s][i + column_s] = "X"
                                    ship_info_s[i] = {"row": row_s, "column": i + column_s, "prob": prob_s}
                            else:
                                for i in range(ship_length):
                                    board[i + row_s][column_s] = "X"
                                    ship_info_s[i] = {"row": i + row_s, "column": column_s, "prob": prob_s}
                            for i in range(ship_length):
                                PLAYER_SUPERPOSITION_BOARD[ship_info[i]["row"]][ship_info[i]["column"]] = {
                                    "row": ship_info_s[i]["row"],
                                    "column": ship_info_s[i]["column"],
                                    "prob": prob
                                }
                                PLAYER_SUPERPOSITION_BOARD[ship_info_s[i]["row"]][ship_info_s[i]["column"]] = {
                                    "row": ship_info[i]["row"],
                                    "column": ship_info[i]["column"],
                                    "prob": prob_s
                                }
                            clear_terminal()
                            print_board(PLAYER_BOARD)
                            print_board(PLAYER_SUPERPOSITION_BOARD)
                            superpos_ship_placed = True
                        
    clear_terminal()

#check if ship fits in board
def check_ship_fit(SHIP_LENGTH, row, column, orientation):
    if orientation == "H":
        if column + SHIP_LENGTH > 8:
            return False
        else:
            return True
    else:
        if row + SHIP_LENGTH > 8:
            return False
        else:
            return True

#check each position for overlap
def ship_overlaps(board, row, column, orientation, ship_length):
    if orientation == "H":
        for i in range(column, column + ship_length):
            if board[row][i] == "X":
                return True
    else:
        for i in range(row, row + ship_length):
            if board[i][column] == "X":
                return True
    return False


def user_input(place_ship):
    # place_ship = True for first ship
    # place_ship = False for superposition ship
    if place_ship == True:
        while True:
            try: 
                orientation = input("Enter orientation (H or V): ").upper()
                if orientation == "H" or orientation == "V":
                    break
            except TypeError:
                print('Enter a valid orientation H or V')
        while True:
            try: 
                row = input("Enter the row 1-8 of the ship: ")
                if row in '12345678':
                    row = int(row) - 1
                    break
            except ValueError:
                print('Enter a valid number between 1-8')
        while True:
            try: 
                column = input("Enter the column of the ship: ").upper()
                if column in 'ABCDEFGH':
                    column = LETTERS_TO_NUMBERS[column]
                    break
            except KeyError:
                print('Enter a valid letter between A-H')
        while True:
            try: 
                prob = input("Enter the probability of the ship being there (1-99): ")
                # check if prob is a number from 1-99
                if prob.isdigit() and 1 <= int(prob) <= 99:
                    prob = int(prob)
                    break
            except ValueError:
                print('Enter a valid number between 1-99')
        return row, column, orientation, prob 
    else:
        while True:
            try: 
                orientation = input("Enter orientation (H or V): ").upper()
                if orientation == "H" or orientation == "V":
                    break
            except TypeError:
                print('Enter a valid orientation H or V')
        while True:
            try: 
                row = input("Enter the row 1-8 of the ship: ")
                if row in '12345678':
                    row = int(row) - 1
                    break
            except ValueError:
                print('Enter a valid number between 1-8')
        while True:
            try: 
                column = input("Enter the column of the ship: ").upper()
                if column in 'ABCDEFGH':
                    column = LETTERS_TO_NUMBERS[column]
                    break
            except KeyError:
                print('Enter a valid letter between A-H')
        return row, column, orientation

#check if all ships are hit
def count_hit_ships(board):
    count = 0
    for row in board:
        for column in row:
            if column == "X":
                count += 1
    return count

#user and computer turn
def turn(board):
    if board == PLAYER_GUESS_BOARD:
        row, column = user_input(PLAYER_GUESS_BOARD)
        if board[row][column] == "-":
            turn(board)
        elif board[row][column] == "X":
            turn(board)
        elif COMPUTER_BOARD[row][column] == "X":
            board[row][column] = "X"
        else:
            board[row][column] = "-"
    else:
        row, column = random.randint(0,7), random.randint(0,7)
        if board[row][column] == "-":
            turn(board)
        elif board[row][column] == "X":
            turn(board)
        elif PLAYER_BOARD[row][column] == "X":
            board[row][column] = "X"
        else:
            board[row][column] = "-"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

place_ships(COMPUTER_BOARD)
print_board(COMPUTER_BOARD)
print_board(PLAYER_BOARD)
place_ships(PLAYER_BOARD)
        
while True:
    #player turn
    while True:
        print('Guess a battleship location')
        print_board(PLAYER_GUESS_BOARD)
        turn(PLAYER_GUESS_BOARD)
        break
    if count_hit_ships(PLAYER_GUESS_BOARD) == 17:
        print("You win!")
        break   
    #computer turn
    while True:
        turn(COMPUTER_GUESS_BOARD)
        break
    clear_terminal()           
    print_board(COMPUTER_GUESS_BOARD)   
    if count_hit_ships(COMPUTER_GUESS_BOARD) == 17:
        print("Sorry, the computer won.")
        break