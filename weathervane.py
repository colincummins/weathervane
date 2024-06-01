import os

from framed_text import FramedText
from Quote import Quote
from voice_api import VoiceAPI
from forecast_to_quote import forecast_to_quote
from get_forecast import get_forecast
from skrivenerAPI import SkrivenerAPI
from zipfinderAPI import ZipfinderAPI
from poeterAPI import PoeterAPI
from quoteArchiveAPI import QuoteArchiveAPI
from PIL import Image as im
import io

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
    "Type [Enter] to hear quote inspired by your local weather (Quote will also print)",
    "Type (S) to save current quote to your archive",
    "Type (R) to retrieve a random quote from your archive",
    "Type (L) set/change/clear your Location (required)",
    "Type (A) to know more about Weathervane",
    "Type (I) to toggle image mode >>>NEW<<<",
    "Type (P) to toggle poem mode >>>NEW<<<",
    "Type (V) to toggle voice mode",
    "Type (Z) to toggle zipcode display >>>NEW<<<",
    "Type (Q)uit to end program"
]
PROMPT = "[(Enter)/(L)ocation/(A)bout/(I)mage/(P)oem/(V)oice/(Z)ipcode Display/(S)ave Current Quote/(R)andom Archive Quote/(Q)uit]:"
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
        self.location = None
        self.prompt = PROMPT
        self.voice = True
        self.image = False
        self.poem = False
        self.display_zip = True
        self.current_quote = None
        self.menu_commands = {
            '': self.display_quote,
            'l': self.input_location,
            'q': self.quit_program,
            'v': self.toggle_voice,
            'i': self.toggle_image,
            'z': self.toggle_zip_display,
            'a': self.display_about,
            's': self.save_quote,
            'r': self.random_quote,
            'p': self.toggle_poem
        }
        self.voice_api = VoiceAPI()
        self.skrv = SkrivenerAPI()
        self.zipf = ZipfinderAPI()
        self.papi = PoeterAPI()
        self.qarch = QuoteArchiveAPI()

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
        print(*self.menu, sep="\n")
        print()

    def get_location_display(self):
        if self.location is None:
            return None
        if self.display_zip:
            return self.location['zip']
        return self.location['placename']

    def display_status(self):
        print()
        FramedText(self.get_location_display() or "None",header="Location",footer="(L) to set/reset").display()
        print()
        print("(I)mage Mode:",
              "ON" if self.image else "OFF", "(P)oem Mode:", "ON" if self.poem else "OFF", "(V)oice Mode:",
              "ON" if self.voice else "OFF")

    def get_quote(self):
        forecast = get_forecast(self.location['zip'])
        if self.poem:
            body = self.papi.get_poem(forecast)
            author = "Original Poem by Weathervane"
        else:
            body, author = forecast_to_quote(forecast)
        new_quote = Quote(body, author)
        return new_quote

    def render_quote(self, quote: Quote) -> None:
        # Adapted from the Skrivener readme - https://github.com/bcliden/skrivener?tab=readme-ov-file

        # We have to strip newlines out because Skrivener can't currently handle them
        image_bytes = self.skrv.text_to_img(str(quote).replace('\n', ' '))
        bytes_buffer = io.BytesIO(image_bytes)
        image = im.open(bytes_buffer)
        image.show()
        image.save("wv.png", format="png")

    def display_quote(self):
        if not self.location:
            print("You must set a location to receive weathervanes. Press (L) to enter.\n")
            return
        quote = self.get_quote()
        self.current_quote = quote
        print()
        FramedText(quote.get_body(), header="Weathervane for " + self.location['placename'],
                   footer=quote.get_author()).display()
        print()
        if self.voice:
            self.voice_api.say_quote(quote.get_body(), quote.get_author())
        if self.image:
            self.render_quote(quote)

    def toggle_voice(self):
        self.voice = not self.voice

    def toggle_image(self):
        self.image = not self.image

    def toggle_zip_display(self):
        self.display_zip = not self.display_zip

    def toggle_poem(self):
        self.poem = not self.poem

    def save_quote(self):
        if not self.current_quote:
            print('You have not displayed a quote yet')
        else:
            self.qarch.archive_quote(self.current_quote)
            print()
            FramedText("Your quote has been archived").display()
            print()

    def random_quote(self):
        quote = self.qarch.get_random()
        print()
        FramedText(quote.get_body(), header="From Your Archives", footer=quote.get_author()).display()
        print()
        if self.voice:
            self.voice_api.say_quote(quote.get_body(), quote.get_author())
        if self.image:
            self.render_quote(quote)

    @staticmethod
    def quit_program():
        exit(0)

    def process_command(self):
        valid = False
        command = None
        while not valid:
            command = input(PROMPT)
            command = command.lower() if command.isalpha() else command
            if command in self.menu_commands:
                valid = True
                print()
                self.menu_commands[command]()

    def input_location(self):
        valid = False
        while not valid:
            user_input = input('Enter location or press [enter] to reset: ')
            if user_input == "c":
                return
            if user_input == "":
                self.location = None
                return
            try:
                self.location = self.zipf.get_location(user_input)
                valid = True
            except Exception as e:
                print(e)

    def display_about(self):
        print()
        framed_text = FramedText(self.about, "About Weathervane")
        framed_text.display()
        print()

    def mainloop(self):
        self.display_title()
        self.display_tagline()
        self.display_privacy_note()
        while True:
            self.display_menu()
            self.display_status()
            self.process_command()


if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    app = App()
    app.mainloop()
