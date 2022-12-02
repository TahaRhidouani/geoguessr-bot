import web
import bot

def menu():
    choice = input("1: Start local game\n2: Start multiplayer game\n3: Manual mode\nQ: Quit\n\nPlease enter your choice: ")

    if choice == "1":
        web.local()
    elif choice == "2":
        gameUrl = input("Please enter the game URL, or press enter to make the bot host: ")
        web.multiplayer(gameUrl)
    elif choice == "3":
        img_dir = input("Please enter your image directory: ")
        print(bot.predict(img_dir))
    elif choice=="Q" or choice=="q":
        exit()
    else:
        print("\nInvalid input. Please try again")
        menu()

if __name__ == '__main__':
    print("\n************ Welcome to the geoguessr AI bot **************\n")
    menu()