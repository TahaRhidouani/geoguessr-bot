import sys
import web
import bot

def menu():
    choice = input("A: Run local session\nB: Run multiplayer session\nC: Manual mode\nQ: Quit\n\nPlease enter your choice: ")

    if choice == "A" or choice =="a":
        web.local()
    elif choice == "B" or choice =="b":
        web.multiplayer()
    elif choice == "C" or choice =="c":
        img_dir = input("Please enter your image directory: ")
        bot.predict(img_dir)
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select either A or B")
        print("\nPlease try again")
        menu()

if __name__ == '__main__':
    print("\n************ Welcome to the geoguessr AI bot **************\n")
    menu()