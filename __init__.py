# Encoding: utf-8

from tkinter import Tk, Canvas


class Tetris:

    TITLE = 'Tetris by Rim'
    BODY_W = 240  # 12 стовбців по 20
    BODY_H = 480  # 24 рядків по 20
    BODY_BG = '#000000'

    def __init__(self):
        self._createWindow()

    def _createWindow(self):
        self.root = Tk()
        self.root.title(self.TITLE)

        self.body = Canvas(self.root, width=self.BODY_W,
                           height=self.BODY_H, bg=self.BODY_BG)
        self.body.grid()

    def run(self):
        self.root.mainloop()

    def _createPixel(self, x, y, bg):
        return self.body.create_rectangle(x, y, x)


if __name__ == "__main__":
    Tetris().run()
