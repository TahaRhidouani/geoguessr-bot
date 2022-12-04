import web
import bot

def menu():
    choice = input("\n\n1: Play local game\n2: Play multiplayer game\n3: Manual mode\nQ: Quit\n\nPlease enter your choice: ")

    if choice == "1":
        web.play()
        menu()
    elif choice == "2":
        gameUrl = input("Paste the game URL, or press enter to make the bot host: ")
        web.play(gameUrl, True)
        menu()
    elif choice == "3":
        img_dir = input("Paste your image directory: ")
        try:
            country = bot.predict(img_dir)[0]
            print("This seems to be " + country + ".")
        except Exception as e:
            print(e)
        menu()
    elif choice=="Q" or choice=="q":
        exit()
    else:
        print("\nInvalid input. Please try again")
        menu()

if __name__ == '__main__':
    print("\n************ Welcome to the geoguessr AI bot **************")
    menu()