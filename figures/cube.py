# Encoding: utf-8

from figures.Figure import Figure


class figureCube(Figure):

    def __init__(self):
        super().__init__()

    def _createFigure(self):
        self._createPixel()
