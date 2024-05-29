import textwrap


class FramedText:
    def __init__(self, text, header = "", footer = "", width=70, text_width = 60):
        self.header = header
        self.text = text
        self.footer = footer
        self.width = width
        self.text_width = text_width

    def line_length_ok(self):
        return all([len(line) <= self.text_width for line in self.text.splitlines()])

    def display(self):
        CORNER = "#"
        VERT = "|"
        HORIZ = "="
        wrapped_text = textwrap.TextWrapper(width=self.text_width, replace_whitespace=False)
        if self.line_length_ok():
            lines = self.text.splitlines()
        else:
            lines = wrapped_text.wrap(self.text)

        padding = (self.width - 2 - self.text_width) // 2

        print(CORNER + HORIZ * padding + ((self.header + HORIZ * padding).ljust(self.width - 2 - padding, HORIZ)) +  CORNER)
        print(VERT + " " * (self.width - 2) + VERT)
        for line in lines:
            print(VERT + " " * padding + line.ljust(self.width - padding - 2) + VERT)
        print(VERT + " " * (self.width - 2) + VERT)
        print(CORNER + ((self.footer + HORIZ * padding).rjust(self.width - 2 - padding, HORIZ)) + HORIZ * padding +  CORNER)
