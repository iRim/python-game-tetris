# Encoding: utf-8

from tkinter import Tk, Canvas
from random import choice, randint

TITLE = 'Tetris by Rim'
PIXEL = 30
COLUMNS = 12
ROWS = 24
BODY_W = PIXEL * COLUMNS
BODY_H = PIXEL * ROWS
BODY_BG = '#000000'

POINT_ROW = 0
POINT_COLUMN = (BODY_W / PIXEL) // 2

TEXT_NORMAL = 'Почати гру'
TEXT_NORMAL_FONT = ('Tahoma', 24)
TEXT_NORMAL_COLOR = '#ffffff'

TEXT_ERROR = 'Ви програли'
TEXT_ERROR_FONT = ('Verdana', 18)
TEXT_ERROR_COLOR = '#cc0000'

TEXT_SCORE = '0'
TEXT_SCORE_FONT = ('Tahoma', 12)
TEXT_SCORE_COLOR = '#cccccc'

DEFAULT_SPEED = 500


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
    FIGURE_INDEX = 0
    FIGURE_PIXELS = []
    MOVE_LEFT = True
    MOVE_RIGHT = True
    ALL_PIXELS = []
    ROW_PIXELS = dict()
    SPEED = DEFAULT_SPEED

    def __init__(self):
        self._endGame = True
        self.score = 0
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
        self.FIGURE_INDEX = 0
        self.FIGURE_PIXELS = self._getFigure().get()
        self.ALL_PIXELS += self.FIGURE_PIXELS
        self.MOVE_LEFT = True
        self.MOVE_RIGHT = True

        figure = self._getFigure()
        if len(figure.PIXELS) - 2 > 0:
            rand = randint(0, len(figure.PIXELS) - 2)
            for i in range(rand):
                self._rotate90Deg()

    def _keypress(self, e):
        if e.keysym in ['Left', 'Right']:
            position = 1
            if e.keysym == 'Left':
                position = -1
            self._moveFigure('x', position)
        elif e.keysym == 'Up':
            self._rotate90Deg()
        else:
            self._moveFigure()

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

    def _moveFigureCheckX(self, x, position=1):
        if (position < 0 and int(x) > 0) or (position > 0 and int(x) + PIXEL < BODY_W):
            return True
        return False

    def _moveFigure(self, xy='y', position=1):
        if (xy == 'x' and ((self.MOVE_LEFT and position == -1) or (self.MOVE_RIGHT and position == 1))) or xy == 'y':
            checkX = checkY = []

            for pix in self.FIGURE_PIXELS:
                x, y, x1, y1 = self.body.coords(pix)
                x_new = x
                y_new = y
                if xy == 'x' and ((position < 0 and int(x) > 0) or (position > 0 and int(x) + PIXEL < BODY_W)):
                    x_new = int(x + position * PIXEL)
                elif xy == 'y' and int(y) + PIXEL < BODY_H:
                    y_new = int(y + PIXEL)

                self.body.coords(pix, x_new, y_new, x_new +
                                 PIXEL, y_new + PIXEL)
                if xy == 'x':
                    checkX.append(int(x_new))
                else:
                    checkY.append(int(y_new))

            if xy == 'x':
                checkX.sort()
                if (len(checkX) > 0 and checkX[0] == 0) or self._checkEmptyLeftColumn():
                    self.MOVE_LEFT = False
                else:
                    self.MOVE_LEFT = True

                if (len(checkX) > 0 and checkX[-1] + PIXEL == BODY_W) or self._checkEmptyRightColumn():
                    self.MOVE_RIGHT = False
                else:
                    self.MOVE_RIGHT = True
            else:
                checkY.sort()
                if (len(checkY) > 0 and checkY[-1] + PIXEL == BODY_H) or self._checkEmptyNextRow():
                    self._figureInsertToRow()

    def _checkEmptyNextRow(self):
        for pix in self.FIGURE_PIXELS:
            x, y, x1, y1 = self.body.coords(pix)
            coords = '{0}x{1}'.format(int(x), int(y + PIXEL))
            if len(self.ROW_PIXELS) > 0 and coords in self.ROW_PIXELS.keys():
                return True
        return False

    def _checkEmptyLeftColumn(self):
        for pix in self.FIGURE_PIXELS:
            x, y, x1, y1 = self.body.coords(pix)
            x_new = int(x - PIXEL)
            if x_new < 0:
                x_new = 0
            coords = '{0}x{1}'.format(x_new, int(y))

            if coords in self.ROW_PIXELS.keys():
                return True
        return False

    def _checkEmptyRightColumn(self):
        for pix in self.FIGURE_PIXELS:
            x, y, x1, y1 = self.body.coords(pix)
            x_new = int(x + PIXEL)
            if x_new > BODY_W:
                x_new = BODY_W
            coords = '{0}x{1}'.format(x_new, int(y))

            if coords in self.ROW_PIXELS.keys():
                return True
        return False

    def _figureInsertToRow(self):
        for pix in self.FIGURE_PIXELS:
            x, y, x1, y1 = self.body.coords(pix)
            key = '{x}x{y}'.format(x=int(x), y=int(y))
            self.ROW_PIXELS[key] = pix
        self.FIGURE_PIXELS.clear()
        self._checkFullRows()
        self._randomFigure()

    def _checkFullRows(self):
        rows = dict()
        # Збираємо інформацію по конкретних лініях
        for key, pix in self.ROW_PIXELS.items():
            column, row, x1, y1 = self.body.coords(pix)
            row = int(row)
            column = int(column)
            if row not in rows.keys():
                rows[row] = dict()

            if column not in rows[row].keys():
                rows[row][column] = key

        ####
        # проблема в self.ROW_PIXELS, залишаються старі ключі через які фігура не може опуститися нижче
        ####

        bonus = 0
        for row in sorted(rows):
            if len(rows.get(row)) == COLUMNS:
                bonus += 1
                for keypix in rows.get(row).values():
                    self.body.delete(self.ROW_PIXELS.get(keypix))
                    del self.ROW_PIXELS[keypix]
                del rows[row]
                self._moveRowsDown(row)
                self._updateScore(COLUMNS)

        if bonus > 1:
            self._updateScore(bonus * COLUMNS)

    def _updateScore(self, score):
        self.score += int(score)
        self.body.itemconfig(self.text_score, text='%s' % self.score)

    def _moveRowsDown(self, toRowNum=ROWS):
        rows = dict(self.ROW_PIXELS)
        self.ROW_PIXELS.clear()
        for pix in rows.values():
            x, y, x1, y1 = self.body.coords(pix)
            self.ROW_PIXELS['{0}x{1}'.format(int(x), int(y))] = pix
            if int(y) < toRowNum:
                self.body.coords(pix, x, y + PIXEL, x1, y1 + PIXEL)
        del rows

    def _move(self):
        self._moveFigure()
        if self._endGame != True:
            self.root.after(self.SPEED, self._move)

    def _start(self, e):
        self._endGame = False
        self.body.itemconfig(self.text_error, state='hidden')
        self.body.itemconfig(self.text_start, state='hidden')
        self.score = 0
        self.body.itemconfig(self.text_score, state='normal')

        self._randomFigure()
        self.body.bind("<KeyPress>", self._keypress)
        self._move()

    def _end(self):
        self.body.itemconfig(self.text_error, state='normal')
        self.body.itemconfig(self.text_start, state='normal')

        for pix in self.ALL_PIXELS:
            self.body.delete(pix)
        self.ALL_PIXELS.clear()

    def _createGame(self):
        X = BODY_W // 2
        Y = BODY_H // 2.2
        self.text_score = self.body.create_text(
            15, 15, text=TEXT_SCORE, fill=TEXT_SCORE_COLOR, font=TEXT_SCORE_FONT, state='hidden')
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
                {'x': -2, 'y': 2},
            ],
            [
                {'x': -1, 'y': 1},
                {'x': 0, 'y': 0},
                {'x': 1, 'y': -1},
                {'x': 2, 'y': -2},
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
