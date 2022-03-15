enter_string = "enter: "


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
    print("winning team players (comma seperated), losing team players, winning score, losing score, yes/no for plunk, if yes, who plunked.")
    quick_enter_string = input(enter_string)
    quick_enter_list = quick_enter_string.split(",")
    winner_1 = quick_enter_list[0]
    winner_2 = quick_enter_list[1]
    loser_1 = quick_enter_list[2]
    loser_2 = quick_enter_list[3]
    winner_score = quick_enter_list[4]
    loser_score = quick_enter_list[5]

    plunk = quick_enter_list[6].lower().strip()
    if plunk == "yes":
        plunk = True
        player_plunk = quick_enter_list[7]
    else:
        plunk = False
        player_plunk = ""

    return winner_1, winner_2, loser_1, loser_2, winner_score, loser_score, plunk, player_plunk


def full_enter():
    # gather winnning team
    print("enter the winning team, comma seperated")
    winning_team = input(enter_string)
    winning_team.strip().replace(".", ",").replace(" ", ",")
    winning_team = winning_team.split(",")
    # todo validate names in database
    # gather losing team
    print("enter the losing team, comma seperated")
    losing_team = input(enter_string)
    losing_team.strip().replace(".", ",").replace(" ", ",")
    losing_team = losing_team.split(",")
    # gather score
    print("enter the score (Winning Score,Losing Score)")
    score = input(enter_string)
    score.strip().replace("-", ",").replace(" ", ",").replace(".", ",")
    score = score.split(",")
    # gather plunk
    print("was their a plunk? (yes/no).")
    plunk_list = []
    plunk = (input(enter_string)).lower().strip()
    if plunk == "yes":
        print("how many?")
        i = 0
        plunk_number = input(enter_string)
        while i < int(plunk_number):
            print("who plunked?")
            plunk_list.append(input(enter_string))
            i = i + 1

    return winning_team, losing_team, score, plunk, plunk_list


def display_rankings():
    # query SQL database
    pass


def display_last_game():
    # get last game stats
    pass


def main():
    running = True

    while(running):
        user_input = welcome_message()
        match user_input:
            case 1:
                winner_1, winner_2, loser_1, loser_2, winner_score, loser_score, plunk, player_plunk = quick_enter()
            case 2:
                winning_team, losing_team, score, plunk, plunk_list = full_enter()
            case 3:
                display_rankings()
            case 4:
                display_last_game()
            case 5:
                print("thank you for entering the score.")
                running = False


main()
