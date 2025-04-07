class Entity():
    """standard class for containers, text objects, etc."""

    def __init__(self, parent, x, y, width, height):
        self.parent = None
        self._width = width
        self._height = height
        self.set_x(x)
        self.set_y(y)

        if parent:
            parent.add_child(self)
            self.parent = parent

    def set_x(self, x):
        if self.parent:
            if self.parent.get_width() < self._width + x:
                raise StructureError('edge conflict')
        self._x = x

    def get_x(self):
        return self._x

    def set_y(self, y):

        if self.parent:
            if self.parent.get_height() < self._height + self._y:
                raise StructureError('edge conflict')
        self._y = y

    def get_y(self):
        return self._y

    def move(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def get_x_abs(self):
        if self.parent:
            return self.parent.get_x_abs() + self._x
        else:
            return self._x

    def get_y_abs(self):
        if self.parent:
            return self.parent.get_y_abs() + self._y
        else:
            return self._y

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height


class StructureError(Exception):
    def __init__(self, key):
        messages = {'parent double': "specified child already has parent associated, try 'replace=True'",
                    'child not found': "not a child of given container",
                    'edge conflict': "specified movement conflicts with size of container"
                    }

        if key in messages:
            message = messages[key]
        else:
            message = 'unknown error'

        super().__init__(f'invalid structure\n  ' + message)
