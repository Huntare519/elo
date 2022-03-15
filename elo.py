
def welcome_message():
    print("welcome to la casablanca rankings")
    print("1 - quick enter: ")
    print("2 - full enter: ")
    print("3 - display all rankings: ")
    print("4 - display last game: ")

    user_prompt = int(input("enter: "))
    while user_prompt > 4 | | user_prompt < 0:
        print("not valid - please enter between 1 and 4")
        user_prompt = int(input("enter: "))
    return user_prompt


def main():
    user_input = welcome_message()
