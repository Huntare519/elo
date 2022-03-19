import sqlite3
from datetime import date
from enum import Enum
import math
import csv
import datetime
from player import Player

enter_string = "enter: "
con_players = sqlite3.connect("test_players.db")
con_games = sqlite3.connect("test_games.db")


class Input(Enum):
    QUICK_ENTER = 1
    FULL_ENTER = 2
    DISPLAY_RANKINGS = 3
    DISPLAY_LAST_GAME = 4
    EXIT = 5


def connect_db(db_name: str):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return cursor, connection


def welcome_message():
    print("1 - quick enter: ")
    print("2 - full enter: ")
    print("3 - display all rankings: ")
    print("4 - display last game: ")
    print("5 - exit: ")

    user_prompt = int(input(enter_string))
    while user_prompt > 5 or user_prompt < 0:
        print("not valid - please enter between 1 and 5")
        user_prompt = int(input("enter: "))
    return user_prompt


def quick_enter(debug=True):
    print("enter in the following format")
    print("winning team players(comma seperated), losing team players, winning score, losing score")

    if debug:
        quick_enter_list = []
        with open('test_quick_enter.csv') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                quick_enter_list.append(row)
        print("entered with csv for debug mode")

    else:
        quick_enter_string = input(enter_string)
        quick_enter_list = quick_enter_string.split(",")
    return quick_enter_list


def full_enter():
    return_list = []
    # gather winnning team
    print("enter the winning team, comma seperated")
    winning_team = input(enter_string)
    winning_team.strip().replace(".", ",").replace(" ", ",")
    return_list.append(winning_team.split(","))
    # todo validate names in database
    # gather losing team
    print("enter the losing team, comma seperated")
    losing_team = input(enter_string)
    losing_team.strip().replace(".", ",").replace(" ", ",")
    return_list.append(losing_team.split(","))
    # gather score
    print("enter the score (Winning Score,Losing Score)")
    score = input(enter_string)
    score.strip().replace("-", ",").replace(" ", ",").replace(".", ",")
    return_list.append(score.split(","))
    # gather plunk
    print("was their a plunk? (yes/no).")
    plunk_list = []
    plunk = (input(enter_string)).lower().strip()
    return_list.append(plunk)
    if plunk == "yes":
        print("how many?")
        i = 0
        plunk_number = input(enter_string)
        while i < int(plunk_number):
            print("who plunked?")
            plunk_list.append(input(enter_string))
            i = i + 1
        return_list.append(plunk_list)

    return return_list


def insert_game_into_database(list_info, debug=True):
    cursor, connection = connect_db("test_games.db")
    today = date.today()
    if debug:
        winner1, winner2 = list_info[0][0], list_info[0][1]
        loser1, loser2 = list_info[0][2], list_info[0][3]
        winning_score, losing_score = list_info[0][4], list_info[0][5]
        plunk, player_plunk = 0, "No"
    else:
        winner1, winner2 = list_info[0], list_info[1]
        loser1, loser2 = list_info[2], list_info[3]
        winning_score, losing_score = list_info[4], list_info[5]
        plunk = 0  # default for quick enter
        player_plunk = "default no"

    cursor.execute("INSERT INTO games VALUES(?,?,?,?,?,?,?,?,?)", (today, winner1,
                                                                   winner2, loser1, loser2, winning_score, losing_score, plunk, player_plunk))
    connection.commit()
    cursor.close()


def check_player_status(quick_enter_list):
    cursor, connection = connect_db("test_players.db")
    today = date.today()
    i = 0
    while (i < 4):
        sql = "SELECT * FROM players WHERE name=?"
        cursor.execute(sql, [quick_enter_list[0][i]])
        result = cursor.fetchone()

        if result:
            print(result)
        else:
            player = quick_enter_list[0][i]
            print(
                f"Looks like {player} didn't previously exist. They have been added with an elo of 1000")
            cursor.execute(
                "INSERT INTO players VALUES (?,?,?,?)", (today, player, 0, 1000))
        i = i + 1
    connection.commit()
    cursor.close()


def display_rankings():
    # query SQL database
    pass


def display_last_game():
    # get last game stats
    pass


def update_elo(list_info, debug=True):
    cursor, connection = connect_db("test_players.db")
    elo_dict = {}
    print()
    if debug:
        cursor.execute("SELECT * FROM players")
        players = cursor.fetchall()
        for row in players:
            elo_dict.update({row[1]: row[3]})

    for k, v in elo_dict.items():
        print(k, v)


def calc_q(winners_elo, losers_elo):
    q = (2.2 / (winners_elo - losers_elo) * 0.001 + 2.2)
    return q


def calc_movm(q, winning_score, losing_score):
    movm = math.log(abs(winning_score - losing_score)+1) * q
    return movm


def init_database():
    cursor_players = con_players.cursor()
    cursor_players.execute(
        "CREATE TABLE IF NOT EXISTS players (date added TEXT, name TEXT, total games INT, elo INT)")
    cursor_games = con_games.cursor()
    cursor_games.execute(
        "CREATE TABLE IF NOT EXISTS games (timestamp TEXT, winner1 TEXT, winner2 TEXT, loser1 TEXT, loser2 TEXT, winner_score INT, loser_score INT, plunk INT, player_plunk TEXT)")
    return cursor_players, cursor_games


def main():
    running = True
    init_database()
    print("----welcome to la casablanca rankings----")

    while(running):
        user_input = welcome_message()
        match user_input:
            case Input.QUICK_ENTER.value:
                quick_enter_list = quick_enter()
            case Input.FULL_ENTER.value:
                winning_team, losing_team, score, plunk, plunk_list = full_enter()
            case Input.DISPLAY_RANKINGS.value:
                display_rankings()
            case Input.DISPLAY_LAST_GAME.value:
                display_last_game()
            case Input.EXIT.value:
                print("thank you for entering the score.")
                running = False

        if (user_input == 1):
            insert_game_into_database(quick_enter_list)
            check_player_status(quick_enter_list)
            update_elo(quick_enter_list)


main()

# TODO
# determine if a new player was entered, create player object
# store players elo
# after every game, calculate new elo
