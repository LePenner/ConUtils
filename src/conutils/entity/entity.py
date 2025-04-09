from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from conutils.entity.container.container import Container


class Entity:
    """standard class for containers, text objects, etc."""

    def __init__(self, parent: Container | None,
                 x: int, y: int, width: int, height: int):
        self._parent = parent
        self.set_x(x)
        self.set_y(y)
        self._set_width(width)
        self._set_heigth(height)

        if parent:
            parent.add_child(self, replace=True)
            self._parent = parent

    # ----- setter: position -----

    def set_x(self, x: int):
        if self._parent and hasattr(self, '_width'):
            if self._parent.get_width() < self._width + x:
                raise StructureError('edge conflict')
        self._x = x

    def set_y(self, y: int):
        if self._parent and hasattr(self, '_height'):
            if self._parent.get_height() < self._height + self._y:
                raise StructureError('edge conflict')
        self._y = y

    def move(self, x: int, y: int):
        self.set_x(x)
        self.set_y(y)

    # ----- getter: position -----

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_pos(self) -> tuple[int, int]:
        return ((self._x, self._y))

    def get_x_abs(self) -> int:
        if self._parent:
            return self._parent.get_x_abs() + self._x
        else:
            return self._x

    def get_y_abs(self) -> int:
        if self._parent:
            return self._parent.get_y_abs() + self._y
        else:
            return self._y

    def get_abs_pos(self) -> tuple[int, int]:
        return ((self.get_x_abs(), self.get_y_abs()))

    # ----- setter: dimension -----

    def _set_width(self, width: int):
        if self._parent and hasattr(self, '_x'):
            if self._parent.get_width() < self._x + width:
                raise StructureError('edge conflict')
        self._width = width

    def _set_heigth(self, height: int):
        if self._parent and hasattr(self, '_y'):
            if self._parent.get_height() < self._y + height:
                raise StructureError('edge conflict')
        self._height = height

    def _set_dimensions(self, width: int, height: int):
        self._set_width(width)
        self._set_heigth(height)

    # ----- getter: dimension -----

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_dimensions(self):
        return ((self._width, self._height))

    # ----- misc -----

    def get_parent(self):
        return self._parent


class StructureError(Exception):
    def __init__(self, key: str):
        messages = {'parent double': "specified child already has parent associated, try 'replace=True'",
                    'child not found': "not a child of given container",
                    'edge conflict': "specified displacement conflicts with size of container,\nmake sure to set appropriate width and height",
                    'incest': "specified parent is already child of entity",
                    'child overlap': "positions of children conflict/overlap with each other\nto disable: overlap=True in your container"
                    }

        if key in messages:
            message = messages[key]
        else:
            message = 'unknown error'

        super().__init__(f'invalid structure\n  ' + message)
