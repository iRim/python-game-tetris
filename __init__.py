# Encoding: utf-8

from tkinter import Tk, Canvas
from random import choice


class Figure:

    PIXEL = 20
    POINT_ROW = 5
    POINT_COLUMN = 0
    FIGURE_PIXELS = []

    def __init__(self):
        super().__init__()

    def _generate(self):
        for pix in self.PIXELS:
            x = pix['x'] * self.PIXEL + self.POINT_ROW * self.PIXEL
            y = pix['y'] * self.PIXEL + self.POINT_COLUMN * self.PIXEL
            self.FIGURE_PIXELS.append(
                self._createPixel(x, y, self.PIXEL_COLOR))

    def _createPixel(self, x, y, bg='#ffffff'):
        return self.body.create_rectangle(
            x, y, x + self.PIXEL, y + self.PIXEL, fill=bg)

    def getFigure(self):
        self._generate()
        return self.FIGURE_PIXELS


class Tetris:

    TITLE = 'Tetris by Rim'
    BODY_W = 240  # 12 стовбців по 20
    BODY_H = 480  # 24 рядків по 20
    BODY_BG = '#000000'

    FIGURES = [
        'Cube',
        'Line',
        'HorseL',
        'HorseR',
        'LetterSL',
        'LetterSR',
        'LetterT'
    ]

    def __init__(self):
        self._createWindow()

    def _createWindow(self):
        self.root = Tk()
        self.root.title(self.TITLE)

        self.body = Canvas(self.root, width=self.BODY_W,
                           height=self.BODY_H, bg=self.BODY_BG)
        self.body.grid()

    def _randomFigure(self):
        figure = choice(self.FIGURES)
        getattr(self, figure)(self.body)

    def _moveFigure(self, e):
        print(e)
        # if e.keysym in ['Left', 'Right']:
        #     pass  # move left-right
        # elif e.keysym == 'Up':
        #     self._rotateFigure()
        # else:
        #     pass  # fast move to down

    def _rotateFigure(self):
        print('ROTATE')

    def _start(self):
        self._randomFigure()
        self.body.bind("<KeyPress>", self._moveFigure)

    def run(self):
        self._start()
        self.root.mainloop()

    class Cube(Figure):

        PIXELS = [
            {'x': 0, 'y': 0},
            {'x': 1, 'y': 0},
            {'x': 0, 'y': 1},
            {'x': 1, 'y': 1},
        ]
        PIXEL_COLOR = 'gray'

        def __init__(self, body):
            self.body = body
            self.getFigure()
            print(self.FIGURE_PIXELS)

    class Line(Figure):

        PIXELS = [
            {'x': 0, 'y': 0},
            {'x': 1, 'y': 0},
            {'x': 2, 'y': 0},
            {'x': 3, 'y': 0},
        ]
        PIXEL_COLOR = 'red'

        def __init__(self, body):
            self.body = body
            self.getFigure()

    class HorseL(Figure):

        PIXELS = [
            {'x': 0, 'y': 0},
            {'x': 1, 'y': 0},
            {'x': 2, 'y': 0},
            {'x': 0, 'y': 1},
        ]
        PIXEL_COLOR = 'violet'

        def __init__(self, body):
            self.body = body
            self.getFigure()

    class HorseR(Figure):

        PIXELS = [
            {'x': 0, 'y': 0},
            {'x': 1, 'y': 0},
            {'x': 2, 'y': 0},
            {'x': 2, 'y': 1},
        ]
        PIXEL_COLOR = 'dodgerblue'

        def __init__(self, body):
            self.body = body
            self.getFigure()

    class LetterSL(Figure):

        PIXELS = [
            {'x': 0, 'y': 0},
            {'x': 1, 'y': 0},
            {'x': 1, 'y': 1},
            {'x': 2, 'y': 1},
        ]
        PIXEL_COLOR = 'orange'

        def __init__(self, body):
            self.body = body
            self.getFigure()

    class LetterSR(Figure):

        PIXELS = [
            {'x': 1, 'y': 0},
            {'x': 2, 'y': 0},
            {'x': 1, 'y': 1},
            {'x': 0, 'y': 1},
        ]
        PIXEL_COLOR = 'orangered'

        def __init__(self, body):
            self.body = body
            self.getFigure()

    class LetterT(Figure):

        PIXELS = [
            {'x': 0, 'y': 0},
            {'x': 1, 'y': 0},
            {'x': 2, 'y': 0},
            {'x': 1, 'y': 1},
        ]
        PIXEL_COLOR = 'green'

        def __init__(self, body):
            self.body = body
            self.getFigure()


if __name__ == "__main__":
    Tetris().run()
