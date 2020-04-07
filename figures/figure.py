# Encoding: utf-8


class Figure():

    PIXEL = 20
    PIXEL_BG = '#ffffff'

    def __init__(self, body):
        self.body = body

    def createPixel(self, x, y, bg=self.PIXEL_BG):
        return self.body.create_rectangle(x, y, x + self.PIXEL, y + self.PIXEL, fill=bg)
