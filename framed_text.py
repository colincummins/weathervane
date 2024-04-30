import textwrap


class FramedText:
    def __init__(self, quote, author = "", width=70, quote_width = 60):
        self.quote = quote
        self.author = author
        self.width = width
        self.quote_width = quote_width

    def display(self):
        CORNER = "#"
        VERT = "|"
        HORIZ = "="
        wrapped_text = textwrap.TextWrapper(width=self.quote_width)
        lines = wrapped_text.wrap(self.quote)

        padding = (self.width - 2 - self.quote_width) // 2

        print(CORNER + (HORIZ * (self.width - 2) ) + CORNER)
        print(VERT + " " * (self.width - 2) + VERT)
        for line in lines:
            print(VERT + " " * padding + line.ljust(self.width - padding - 2) + VERT)
        print(VERT + " " * (self.width - 2) + VERT)
        print(CORNER + ((self.author + HORIZ * padding).rjust(self.width - 2 - padding, HORIZ)) + HORIZ * padding +  CORNER)
