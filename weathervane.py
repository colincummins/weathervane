import os

from framed_text import FramedText
from Quote import Quote
from voice_api import VoiceAPI
from forecast_to_quote import forecast_to_quote
from get_forecast import get_forecast
from skrivenerAPI import SkrivenerAPI
from zipfinderAPI import ZipfinderAPI
from poeterAPI import PoeterAPI
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
    "Type (E)nter to hear quote inspired by your local weather (Quote will also print)",
    "Type (L)ocation to set/change/clear your location (required)",
    "Type (A)bout to know more about Weathervane",
    "Type (I) to toggle image mode >>>NEW<<<",
    "Type (P) to toggle poem mode >>>NEW<<<",
    "Type (V) to toggle voice mode",
    "Type (Z) to toggle zipcode display",
    "Type (Q)uit to end program"
]
PROMPT = "[(Enter)/(L)ocation/(A)bout/(I)mage/(P)oem/(V)oice/(Z)ipcode Display/(Q)uit]:"
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
        self.image = True
        self.poem = False
        self.display_zip = True
        self.menu_commands = {
            '': self.display_quote,
            'l': self.input_location,
            'q': self.quit_program,
            'v': self.toggle_voice,
            'i': self.toggle_image,
            'z': self.toggle_zip_display,
            'a': self.display_about,
            'p': self.toggle_poem
        }
        self.voice_api = VoiceAPI()
        self.skrv = SkrivenerAPI()
        self.zipf = ZipfinderAPI()
        self.papi = PoeterAPI()

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
        print('(L)ocation:', self.get_location_display() or "NONE ('L' to set)", "(I)mage Mode:", "ON" if self.image else "OFF","(P)oem Mode:", "ON" if self.poem else "OFF", "(V)oice Mode:", "ON" if self.voice else "OFF")

    def get_quote(self):
        forecast = get_forecast(self.location['zip'])
        if self.poem:
            # Have to strip newlines to avoid issues w/ textwrap later
            body = self.papi.get_poem(forecast).replace('\n', ' ')
            author = "Original Poem by Weathervane"
        else:
            body, author = forecast_to_quote(forecast)
        new_quote = Quote(body, author)
        return new_quote

    def render_quote(self, quote: Quote) -> None:
        # Adapted from the Skrivener readme - https://github.com/bcliden/skrivener?tab=readme-ov-file
        image_bytes = self.skrv.text_to_img(str(quote))
        bytes_buffer = io.BytesIO(image_bytes)
        image = im.open(bytes_buffer)
        image.show()
        image.save("wv.png", format="png")

    def display_quote(self):
        if not self.location:
            print("You must set a location to receive weathervanes. Press (L) to enter.")
            print()
            return
        quote = self.get_quote()
        print()
        FramedText(quote.get_body(), header="Weathervane for " + self.location['placename'], footer=quote.get_author()).display()
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
    os.system("cls||clear||")
    app = App()
    app.mainloop()
