import bot

def run():
    country, coordinates, _ = bot.predict("/screenshot.png")

if __name__ == '__main__':
    run()