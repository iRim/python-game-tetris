# Encoding: utf-8

from tkinter import Tk, Canvas
from random import choice, randint
from time import sleep

TITLE = 'Tetris by Rim'
PIXEL = 30
BODY_W = PIXEL * 12
BODY_H = BODY_W * 2
BODY_BG = '#000000'

POINT_ROW = 0
POINT_COLUMN = (BODY_W / PIXEL) // 2

TEXT_NORMAL = 'Почати гру'
TEXT_NORMAL_FONT = ('Tahoma', 24)
TEXT_NORMAL_COLOR = '#ffffff'

TEXT_ERROR = 'Ви програли'
TEXT_ERROR_FONT = ('Verdana', 18)
TEXT_ERROR_COLOR = '#cc0000'

DEFAULT_SPEED = 100


class Figure:

    FIGURE_PIXELS = []

    def __init__(self):
        super().__init__()

    def _generate(self):
        for pix in self.PIXELS[0]:
            x = pix['x'] * PIXEL + POINT_COLUMN * PIXEL
            y = pix['y'] * PIXEL + POINT_ROW * PIXEL
            self.FIGURE_PIXELS.append(
                self._createPixel(x, y, self.PIXEL_COLOR))

    def _createPixel(self, x, y, bg='#ffffff'):
        return self.body.create_rectangle(
            x, y, x + PIXEL, y + PIXEL, fill=bg)

    def get(self):
        self._generate()
        return self.FIGURE_PIXELS


class Tetris:

    FIGURES = [
        'Cube',
        'Line',
        'HorseL',
        'HorseR',
        'LetterSL',
        'LetterSR',
        'LetterT'
    ]
    FIGURE = None
    FIGURE_PIXELS = []
    FIGURE_INDEX = 0
    MOVE_RIGHT = True
    MOVE_LEFT = True
    ALL_PIXELS = []
    SPEED = DEFAULT_SPEED

    def __init__(self):
        self._endGame = True
        self._createWindow()

    def _createWindow(self):
        self.root = Tk()
        self.root.title(TITLE)

        self.body = Canvas(self.root, width=BODY_W,
                           height=BODY_H, bg=BODY_BG)
        self.body.grid()
        self.body.focus_set()

    def _getFigure(self):
        return getattr(self, self.FIGURE)(self.body)

    def _randomFigure(self):
        self.FIGURE = choice(self.FIGURES)
        self.FIGURE_PIXELS = self._getFigure().get()
        self.ALL_PIXELS += self.FIGURE_PIXELS

    def _keypress(self, e):
        if e.keysym in ['Left', 'Right']:
            position = 1
            if e.keysym == 'Left':
                position = -1
            self._moveFigure('x', position)
        elif e.keysym == 'Up':
            self._rotate90Deg()
        else:
            print('Fast move to Down')

    def _rotate90Deg(self):
        figure = self._getFigure()
        f_len = len(figure.PIXELS)
        if f_len > 1:
            self.FIGURE_INDEX += 1
            if self.FIGURE_INDEX >= f_len:
                self.FIGURE_INDEX = 1

            f_next = figure.PIXELS[self.FIGURE_INDEX]

            for key, pix in enumerate(self.FIGURE_PIXELS):
                x, y, x1, y1 = self.body.coords(pix)
                new_x = x + f_next[key]['x'] * PIXEL
                new_y = y + f_next[key]['y'] * PIXEL
                self.body.coords(pix, new_x, new_y, new_x +
                                 PIXEL, new_y + PIXEL)

    def _checkBorder(self):
        arr = []
        for pix in self.FIGURE_PIXELS:
            x, y, x1, y1 = self.body.coords(pix)
            if int(x) < 0:
                arr.append(int(x))

        arr.sort()
        if len(arr) > 0:
            for pix in self.FIGURE_PIXELS:
                x, y, x1, y1 = self.body.coords(pix)

    def _moveFigureCheckX(self, x, position=1):
        return (position < 0 and int(x) > 0) or (position > 0 and int(x) + PIXEL < BODY_W)

    def _moveFigure(self, xy='y', position=1):
        if (self.MOVE_LEFT and position == -1) or (self.MOVE_RIGHT and position == 1):
            check_pix = []

            for pix in self.FIGURE_PIXELS:
                x, y, x1, y1 = self.body.coords(pix)
                if self._moveFigureCheckX(x, position):
                    x_new = int(x + position * PIXEL)
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

    def _moveDown(self):
        while True:

            sleep(self.SPEED)

    def _start(self, e):
        self._endGame = False
        self.body.itemconfig(self.text_error, state='hidden')
        self.body.itemconfig(self.text_start, state='hidden')

        self._randomFigure()
        self._moveDown()
        self.body.bind("<KeyPress>", self._keypress)

    def _end(self):
        self.body.itemconfig(self.text_error, state='normal')
        self.body.itemconfig(self.text_start, state='normal')

        for pix in self.ALL_PIXELS:
            self.body.delete(pix)
        self.ALL_PIXELS = []

    def _createGame(self):
        X = BODY_W // 2
        Y = BODY_H // 2.2
        self.text_error = self.body.create_text(
            X, Y - PIXEL * 2, fill=TEXT_ERROR_COLOR, font=TEXT_ERROR_FONT, text=TEXT_ERROR, state='hidden')
        self.text_start = self.body.create_text(
            X, Y, fill=TEXT_NORMAL_COLOR, font=TEXT_NORMAL_FONT, text=TEXT_NORMAL)
        self.body.tag_bind(self.text_start, '<Button>', self._start)

    def run(self):
        self._createGame()
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
                {'x': -1, 'y': 0},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
                {'x': 2, 'y': 0},
            ],
            [
                {'x': 1, 'y': -1},
                {'x': 0, 'y': 0},
                {'x': -1, 'y': 1},
                {'x': -2, 'y': 1},
            ],
            [
                {'x': -1, 'y': 1},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': -1},
                {'x': 2, 'y': -1},
            ]
        ]
        PIXEL_COLOR = 'red'

        def __init__(self, body):
            self.body = body

    class HorseL(Figure):
        PIXELS = [
            # дефолтне значення
            [
                {'x': -1, 'y': 0},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
                {'x': -1, 'y': 1},
            ],
            # на 90
            [
                {'x': 1, 'y': -1},
                {'x': 0, 'y': 0},
                {'x': -1, 'y': 1},
                {'x': 0, 'y': -2},
            ],
            # на 180
            [
                {'x': 1, 'y': 1},
                {'x': 0, 'y': 0},
                {'x': -1, 'y': -1},
                {'x': 2, 'y': 0},
            ],
            # на 270
            [
                {'x': -1, 'y': 1},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': -1},
                {'x': 0, 'y': 2},
            ],
            # на 360
            [
                {'x': -1, 'y': -1},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 1},
                {'x': -2, 'y': 0},
            ],
        ]
        PIXEL_COLOR = 'violet'

        def __init__(self, body):
            self.body = body

    class HorseR(Figure):

        PIXELS = [
            # дефолтне значення
            [
                {'x': -1, 'y': 0},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
                {'x': 1, 'y': 1},
            ],
            # на 90
            [
                {'x': 1, 'y': -1},
                {'x': 0, 'y': 0},
                {'x': -1, 'y': 1},
                {'x': -2, 'y': 0},
            ],
            # на 180
            [
                {'x': 1, 'y': 1},
                {'x': 0, 'y': 0},
                {'x': -1, 'y': -1},
                {'x': 0, 'y': -2},
            ],
            # на 270
            [
                {'x': -1, 'y': 1},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': -1},
                {'x': 2, 'y': 0},
            ],
            # на 360
            [
                {'x': -1, 'y': -1},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 1},
                {'x': 0, 'y': 2},
            ],
        ]
        PIXEL_COLOR = 'dodgerblue'

        def __init__(self, body):
            self.body = body

    class LetterSL(Figure):

        PIXELS = [
            [
                {'x': -1, 'y': 0},
                {'x': 0, 'y': 0},
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 1},
            ],
            [
                {'x': 1, 'y': -1},
                {'x': 0, 'y': 0},
                {'x': -1, 'y': -1},
                {'x': -2, 'y': 0},
            ],
            [
                {'x': -1, 'y': 1},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 1},
                {'x': 2, 'y': 0},
            ]
        ]
        PIXEL_COLOR = 'orange'

        def __init__(self, body):
            self.body = body

    class LetterSR(Figure):

        PIXELS = [
            [
                {'x': -1, 'y': 0},
                {'x': 0, 'y': 0},
                {'x': 0, 'y': -1},
                {'x': 1, 'y': -1},
            ],
            [
                {'x': 1, 'y': -1},
                {'x': 0, 'y': 0},
                {'x': -1, 'y': -1},
                {'x': -2, 'y': 0},
            ],
            [
                {'x': -1, 'y': 1},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 1},
                {'x': 2, 'y': 0},
            ]
        ]
        PIXEL_COLOR = 'orangered'

        def __init__(self, body):
            self.body = body

    class LetterT(Figure):

        PIXELS = [
            [
                {'x': -1, 'y': 0},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
                {'x': 0, 'y': -1},
            ],
            [
                {'x': 1, 'y': -1},
                {'x': 0, 'y': 0},
                {'x': -1, 'y': 1},
                {'x': 1, 'y': 1},
            ],
            [
                {'x': 1, 'y': 1},
                {'x': 0, 'y': 0},
                {'x': -1, 'y': -1},
                {'x': -1, 'y': 1},
            ],
            [
                {'x': -1, 'y': 1},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': -1},
                {'x': -1, 'y': -1},
            ],
            [
                {'x': -1, 'y': -1},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 1},
                {'x': 1, 'y': -1},
            ],
        ]
        PIXEL_COLOR = 'green'

        def __init__(self, body):
            self.body = body


if __name__ == "__main__":
    Tetris().run()
