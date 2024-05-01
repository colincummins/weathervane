import pynput


class InputHandler:
    def __init__(self):
        self.message_displayed = False
        self.listener = pynput.keyboard.Listener(on_press=self.on_press, suppress=True)
        self.listener.start()

    def on_press(self,key):
        if not self.message_displayed:
            self.message_displayed = True
            print('Please Wait...\n')

    def input(self, prompt):
        self.listener.stop()
        captured = input(prompt)
        self.__init__()
        return captured
