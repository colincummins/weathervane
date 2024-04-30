
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
    "Type (Q)uit to end program"
]
PROMPT = "[Enter/(z)ipcode/(a)bout/(q)uit]:"
ABOUT = ""


class App:
    def __init__(self):
        self.title = TITLE
        self.tagline = TAGLINE
        self.privacy_note = PRIVACY_NOTE
        self.menu = MENU
        self.zip = None
        self.quote = None
        self.prompt = PROMPT
        self.commands = {
            '': self.display_quote,
            'z': self.get_zipcode,
            'q': self.quit_program
        }

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

    def display_zip(self):
        print('Zipcode:',self.zip or "NONE (Press 'z' to set)")

    def display_quote(self):
        print('A quote')

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
            else:
                print('Invalid Zipcode. Please re-enter zip or hit [c] to cancel.')

    def mainloop(self):
        self.display_title()
        self.display_tagline()
        self.display_privacy_note()
        while True:
            self.display_menu()
            self.display_zip()
            self.process_command()


if __name__ == "__main__":
    app = App()
    app.mainloop()