class Figure:
    def __init__(self, color):
        self.color = color

        @staticmethod
        def create(color, figure):
            return None         #todo


class Point(Figure):
    def __init__(self, color, x, y):
        super().__init__(color)
        self.__x = x
        self.__y = y

    @staticmethod
    def create(color, figure):
        return Point(color, figure['x'], figure['y'])

    def print(self, pict):
        pict.point([(self.__x,self.__y)], self.color)


class Polygon(Figure):
    def __init__(self, color, points):
        super().__init__(color)
        self.__points = points

    @staticmethod
    def create(color, fig):
        return Polygon(color, fig['points'])

    def print(self, pict):
        point_list = []
        for point in self.__points:
            point_list.append(tuple(point))
        pict.polygon(point_list, self.color, self.color)


class Rectangle(Figure):
    def __init__(self, color, x, y, height, width):
        super().__init__(color)
        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y

    @staticmethod
    def create(color, fig):
        return Rectangle(color, fig['x'], fig['y'], fig['height'], fig['width'])

    def print(self, pict):
        pict.rectangle([self.__x, self.__y,
                        self.__x + self.__width, self.__y + self.__height],
                       self.color)


class Square(Figure):
    def __init__(self, color, x, y, size):
        super().__init__(color)
        self.__x = x
        self.__y = y
        self.__size = size

    @staticmethod
    def create(color, fig):
        return Square(color, fig['x'], fig['y'], fig['size'])

    def print(self, pict):
        pict.rectangle([self.__x - self.__size*0.5, self.__y - self.__size*0.5,
                        self.__x + self.__size*0.5, self.__y + self.__size*0.5],
                       self.color)


class Circle(Figure):
    def __init__(self, color, x, y, radius):
        super().__init__(color)
        self.__x = x
        self.__y = y
        self.__radius = radius

    @staticmethod
    def create(color, fig):
        return Circle(color, fig['x'], fig['y'], fig['radius'])

    def print(self, pict):
        pict.ellipse((self.__x - self.__radius, self.__y - self.__radius,
                      self.__x + self.__radius, self.__y + self.__radius), self.color, self.color)

