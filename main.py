import sys
import web
import bot

def menu():
    choice = input("1: Run local session\n2: Run multiplayer session\n3: Manual mode\nQ: Quit\n\nPlease enter your choice: ")

    if choice == "1":
        web.local()
    elif choice == "2":
        web.multiplayer()
    elif choice == "3":
        img_dir = input("Please enter your image directory: ")
        print(bot.predict(img_dir))
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select either A or B")
        print("\nPlease try again")
        menu()

if __name__ == '__main__':
    print("\n************ Welcome to the geoguessr AI bot **************\n")
    menu()