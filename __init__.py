# Encoding: utf-8

from tkinter import Tk, Canvas
from random import choice, randint

TITLE = 'Tetris by Rim'
PIXEL = 30
BODY_W = PIXEL * 12
BODY_H = BODY_W * 2
BODY_BG = '#000000'


class Figure:

    POINT_ROW = 5
    POINT_COLUMN = 0
    FIGURE_PIXELS = []

    def __init__(self):
        super().__init__()

    def _generate(self):
        index = 0
        if len(self.PIXELS) > 1:
            index = randint(0, len(self.PIXELS) - 1)
        self.FIGURE_INDEX = index

        for pix in self.PIXELS[index]:
            x = pix['x'] * PIXEL + self.POINT_ROW * PIXEL
            y = pix['y'] * PIXEL + self.POINT_COLUMN * PIXEL
            self.FIGURE_PIXELS.append(
                self._createPixel(x, y, self.PIXEL_COLOR))

    def _createPixel(self, x, y, bg='#ffffff'):
        return self.body.create_rectangle(
            x, y, x + PIXEL, y + PIXEL, fill=bg)

    def random(self):
        self._generate()
        return self.FIGURE_PIXELS, self.FIGURE_INDEX


class Tetris:

    FIGURES = [
        # 'Cube',
        # 'Line',
        'HorseL',
        # 'HorseR',
        # 'LetterSL',
        # 'LetterSR',
        # 'LetterT'
    ]
    FIGURE = None
    FIGURE_PIXELS = []
    FIGURE_INDEX = 0
    MOVE_RIGHT = True
    MOVE_LEFT = True

    def __init__(self):
        self._createWindow()

    def _createWindow(self):
        self.root = Tk()
        self.root.title(TITLE)

        self.body = Canvas(self.root, width=BODY_W,
                           height=BODY_H, bg=BODY_BG)
        self.body.grid()
        self.body.focus_set()

    def _randomFigure(self):
        self.FIGURE = choice(self.FIGURES)
        self.FIGURE_PIXELS, self.FIGURE_INDEX = getattr(
            self, self.FIGURE)(self.body).random()

    def _keypress(self, e):
        if e.keysym in ['Left', 'Right']:
            self._moveFigure(e.keysym)
        elif e.keysym == 'Up':
            self._rotateFigure()
        else:
            print('Fast move to Down')

    def _rotateFigure(self):
        print(self.FIGURE, self.FIGURE_PIXELS, self.FIGURE_INDEX)

    def _moveFigure(self, move):
        if (self.MOVE_LEFT and move == 'Left') or (self.MOVE_RIGHT and move != 'Left'):
            if move == 'Left':
                move = -1
            else:
                move = 1

            check_pix = []

            for pix in self.FIGURE_PIXELS:
                x, y, x1, y1 = self.body.coords(pix)
                if (move < 0 and int(x) > 0) or (move > 0 and int(x) + PIXEL < BODY_W):
                    x_new = int(x + move * PIXEL)
                    self.body.coords(pix, x_new, y, x_new + PIXEL, y + PIXEL)
                    check_pix.append(x_new)

            check_pix.sort()
            if check_pix[-1] + PIXEL == BODY_W:
                self.MOVE_RIGHT = False
            elif check_pix[0] == 0:
                self.MOVE_LEFT = False
            else:
                self.MOVE_LEFT = True
                self.MOVE_RIGHT = True

    def _start(self):
        self._randomFigure()
        self.body.bind("<KeyPress>", self._keypress)

    def run(self):
        self._start()
        self.root.mainloop()

    class Cube(Figure):

        PIXELS = [
            [
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 1},
            ]
        ]
        PIXEL_COLOR = 'gray'

        def __init__(self, body):
            self.body = body

    class Line(Figure):

        PIXELS = [
            [
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
                {'x': 2, 'y': 0},
                {'x': 3, 'y': 0},
            ],
            [
                {'x': 0, 'y': 0},
                {'x': 0, 'y': 1},
                {'x': 0, 'y': 2},
                {'x': 0, 'y': 3},
            ]
        ]
        PIXEL_COLOR = 'red'

        def __init__(self, body):
            self.body = body

    class HorseL(Figure):

        PIXELS = [
            [
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
                {'x': 2, 'y': 0},
                {'x': 0, 'y': 1},
            ], [
                {'x': 1, 'y': 0},
                {'x': 1, 'y': 1},
                {'x': 1, 'y': 2},
                {'x': 0, 'y': 0},
            ], [
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 1},
                {'x': 2, 'y': 1},
                {'x': 2, 'y': 0},
            ], [
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 1},
                {'x': 2, 'y': 1},
                {'x': 2, 'y': 0},
            ]
        ]
        PIXEL_COLOR = 'violet'

        def __init__(self, body):
            self.body = body

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


if __name__ == "__main__":
    Tetris().run()
