import re
from figures import *
from PIL import Image, ImageDraw


class Parser:
    types_of_figures = {
        'point': Point,
        'polygon': Polygon,
        'rectangle': Rectangle,
        'square': Square,
        'circle': Circle
    }

    def __init__(self, json_content):
        self._palette = json_content["Palette"]
        self._screen = json_content["Screen"]
        self._figures = []

        for elem in json_content["Figures"]:
            self._figures.append(self.parse_figure(elem))

        self.parse_screen()

    def parse_screen(self):
        self._screen['fg_color'] = self.get_color(self._screen['fg_color'])
        self._screen['bg_color'] = self.get_color(self._screen['bg_color'])

    def parse_figure(self, elem):

        elem_type = elem['type']

        if 'color' in elem:
            processed_color = self.get_color(elem['color'])
        else:
            processed_color = self._screen['fg_color']

        if elem_type in self.types_of_figures:
            return self.types_of_figures[elem_type].create(processed_color, elem)
        else:
            raise KeyError("invalid figure type")

    def get_color(self, color):

        if re.match('\(\\d{1,2}|2[0-4][0-9]|25[0-5],\
                    \\d{1,2}|2[0-4][0-9]|25[0-5],\
                    \\d{1,2}|2[0-4][0-9]|25[0-5]\)', color):
            to_ret = 'rgb' + color
        elif re.match('^#[0-9a-f]{6}$', color):
            to_ret = color
        elif color in self._palette.keys():
            return self.get_color(self._palette[color])
        else:
            raise SyntaxError("invalid color format")

        return to_ret

    def process_to_picture(self):

        screen_size = (self._screen['width'], self._screen['height'])
        to_ret = Image.new('RGB', screen_size, self._screen['bg_color'])

        picture = ImageDraw.Draw(to_ret)

        for elem in self._figures:
            elem.print(picture)

        return to_ret
