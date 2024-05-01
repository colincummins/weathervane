import os
from framed_text import FramedText
from Quote import Quote
from voice_api import VoiceAPI

# Constants
TITLE = """
 _    _            _   _
| |  | |          | | | |
| |  | | ___  __ _| |_| |__   ___ _ ____   ____ _ _ __   ___
| |/\| |/ _ \/ _` | __| '_ \ / _ \ '__\ \ / / _` | '_ \ / _ \\
\  /\  /  __/ (_| | |_| | | |  __/ |   \ V / (_| | | | |  __/
 \/  \/ \___|\__,_|\__|_| |_|\___|_|    \_/ \__,_|_| |_|\___|"""

TAGLINE = "Weathervane - Get a quote inspired by today's weather!"
PRIVACY_NOTE = "NOTE: This app requires you enter your zipcode \nwhich may be considered private information"
MENU = [
    "Type (E)nter to hear quote inspired by your local weather (Quote will also print)",
    "Type (Z)ip to set/change/clear your zipcode (required)",
    "Type (A)bout to know more about Weathervane",
    "Type (V) to toggle voice mode >>>NEW<<<",
    "Type (Q)uit to end program"
]
PROMPT = "[(Enter)/(z)ipcode/(a)bout/(v)oice/(q)uit]:"
ABOUT = ("I wrote Weathervane to inspire and inform users by displaying a random quote based on the weather forecast for\
 their zip code. You can set your zipcode by pressing 'z'. You can change the zipcode by pressing 'z'. You can also\
  just hit enter at the zipcode prompt to clear it. I would like to add the ability to save your zipcode, save\
   favorite quotes, and email quotes to others")
DUMMY_QUOTE = 'Into each life some rain must fall, but too much is falling in mine.'
DUMMY_AUTHOR = 'Ralph Waldo Emerson'


class App:
    def __init__(self):
        self.title = TITLE
        self.tagline = TAGLINE
        self.privacy_note = PRIVACY_NOTE
        self.menu = MENU
        self.about = ABOUT
        self.zip = None
        self.prompt = PROMPT
        self.voice = False
        self.commands = {
            '': self.display_quote,
            'z': self.get_zipcode,
            'q': self.quit_program,
            'v': self.toggle_voice,
            'a': self.display_about
        }
        self.voice_api = VoiceAPI()

    def display_title(self):
        print(self.title)

    def display_tagline(self):
        print(self.tagline)
        print()

    def display_privacy_note(self):
        print(self.privacy_note)
        print()

    def display_menu(self):
        print("MENU:")
        print(*self.menu,sep="\n")
        print()

    def display_status(self):
        print('(Z)ipcode:',self.zip or "NONE (z to set)", "(V)oice Mode:", "ON" if self.voice else "OFF")

    def get_quote(self):
        return Quote(DUMMY_QUOTE,DUMMY_AUTHOR)

    def display_quote(self):
        if not self.zip:
            print("You must set a zipcode to receive weathervanes. Press (z) to enter.")
            print()
            return
        quote = self.get_quote()
        print()
        FramedText(quote.get_body(), header="Weathervane for " + self.zip, footer=quote.get_author()).display()
        print()
        if self.voice:
            self.voice_api.say_quote(quote.get_body(),quote.get_author())

    def toggle_voice(self):
        self.voice = ~self.voice

    def quit_program(self):
        exit(0)

    def process_command(self):
        valid = False
        command = None
        while not valid:
            command = input(PROMPT)
            command = command.lower() if command.isalpha() else command
            if command in self.commands:
                valid = True
                self.commands[command]()

    def validate_zip(self, zipcode):
        return zipcode == "" or zipcode.isnumeric()

    def get_zipcode(self):
        valid = False
        while not valid:
            zipcode = input('Enter Zipcode (XXXXX) or hit [enter] to reset: ')
            if zipcode == "c":
                return
            if zipcode == "" or self.validate_zip(zipcode):
                self.zip = zipcode
                valid = True
                print()
            else:
                print('Invalid Zipcode. Please re-enter zip or hit [c] to cancel.')

    def display_about(self):
        print()
        framed_text = FramedText(self.about, "About Weathervane")
        framed_text.display()
        print()

    def mainloop(self):
        self.display_title()
        self.display_tagline()
        self.display_privacy_note()
        self.display_menu()
        while True:
            self.display_status()
            self.process_command()


if __name__ == "__main__":
    os.system("cls||clear||")
    app = App()
    app.mainloop()