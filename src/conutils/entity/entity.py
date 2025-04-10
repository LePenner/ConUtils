from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from conutils.entity.container.container import Container


class Entity:
    """standard class for containers, text objects, etc."""

    def __init__(self, parent: Container | None,
                 x: int, y: int, width: int, height: int):
        self._parent = parent
        self._x = x
        self._y = y
        self.__set_width(width)
        self.__set_heigth(height)

        if parent:
            parent.add_child(self, replace=True)
            self._parent = parent

    def __set_width(self, width: int):
        if self.parent and hasattr(self, '_x'):
            if self.parent.width < self._x + width:
                raise StructureError('edge conflict')
        self._width = width

    def __set_heigth(self, height: int):
        if self.parent and hasattr(self, '_y'):
            if self.parent.height < self._y + height:
                raise StructureError('edge conflict')
        self._height = height

    # ----- position -----

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def pos(self) -> tuple[int, int]:
        return ((self._x, self._y))

    @property
    def x_abs(self) -> int:
        if self.parent:
            return self.parent.x_abs + self._x
        else:
            return self._x

    @property
    def y_abs(self) -> int:
        if self.parent:
            return self.parent.y_abs + self.y
        else:
            return self.y

    @property
    def abs_pos(self) -> tuple[int, int]:
        return ((self.x_abs, self.y_abs))

    # ----- setter: position -----

    @x.setter
    def x(self, x: int):
        if self.parent and hasattr(self, 'width'):
            if self._parent.width < self.width + x:
                raise StructureError('edge conflict')
        self._x = x

    @y.setter
    def y(self, y: int):
        if self.parent and hasattr(self, 'height'):
            if self.parent.height < self.height + self.y:
                raise StructureError('edge conflict')
        self._y = y

    @pos.setter
    def pos(self, x: int, y: int):
        self.x = x
        self.y = y

    # ----- dimension -----

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def dimensions(self):
        return ((self.width, self.height))

    # ----- misc -----

    @property
    def parent(self):
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
