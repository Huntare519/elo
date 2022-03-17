import sqlite3
from enum import Enum
import datetime

enter_string = "enter: "
con_players = sqlite3.connect("test_players.db")
con_games = sqlite3.connect("test_games.db")


class Input(Enum):
    QUICK_ENTER = 1
    FULL_ENTER = 2
    DISPLAY_RANKINGS = 3
    DISPLAY_LAST_GAME = 4
    EXIT = 5


def welcome_message():
    print("welcome to la casablanca rankings")
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


def quick_enter():
    print("enter in the following format")
    print("winning team players(comma seperated), losing team players, winning score, losing score")
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


def insert_players_into_database(cursor_players, cursor_games, winner_1, winner_2, loser_1, loser_2, winner_score, loser_score, plunk, player_plunk):
    pass


def insert_games_into_database(cursor_games, list_info):
    winner1 = list_info[0]
    winner2 = list_info[1]
    loser1 = list_info[2]
    loser2 = list_info[3]
    winning_score = list_info[4]
    losing_score = list_info[5]
    plunk = 0
    player_plunk = "default no"

    cursor_games.execute("INSERT INTO games VALUES(?,?,?,?,?,?,?,?)", (winner1,
                         winner2, loser1, loser2, winning_score, losing_score, plunk, player_plunk))
    con_games.commit()
    cursor_games.close()


def display_rankings():
    # query SQL database
    pass


def display_last_game():
    # get last game stats
    pass


def init_database():
    cursor_players = con_players.cursor()
    cursor_players .execute(
        "CREATE TABLE IF NOT EXISTS players (name TEXT, total games INT, elo INT)")
    cursor_games = con_games.cursor()
    cursor_games.execute(
        "CREATE TABLE IF NOT EXISTS games (winner1 TEXT, winner2 TEXT, loser1 TEXT, loser2 TEXT, winner_score INT, loser_score INT, plunk INT, player_plunk TEXT)")
    return cursor_players, cursor_games


def main():
    running = True

    while(running):
        cursor_players, cursor_games = init_database()
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
            insert_games_into_database(cursor_games, quick_enter_list)


main()
