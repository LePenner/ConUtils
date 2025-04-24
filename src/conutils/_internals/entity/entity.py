from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .container import Container

from ..toolkit import Color


class Entity:
    """Internal baseclass
    Defines standard for containers, text objects, etc.

    Interface
        methods:
            -
    """

    # @constructor
    def __init__(self,
                 parent: Container | None,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 bold: bool,
                 italic: bool,
                 color: str | tuple[int, int, int] | None):

        self._parent = parent

        # define positioning
        self.__set_width(width)
        self.__set_heigth(height)
        self._x = x
        self._y = y

        self.bold = bold
        self.italic = italic

        # needs checks
        self.color = color

        if parent:
            parent.add_child(self, replace=True)
            self._parent = parent

        self._overlap_check()

    def __set_width(self, width: int):
        if self.parent and hasattr(self, 'x'):
            if self.parent.width < self.x + width:
                raise StructureError('edge conflict')
        self._width = width

    def __set_heigth(self, height: int):
        if self.parent and hasattr(self, 'y'):
            if self.parent.height < self.y + height:
                raise StructureError('edge conflict')
        self._height = height

    # @protected
    def _overlap_check(self):

        if self.parent:
            r1_x = range(
                self.x, self.x+self._width)
            r1_y = range(
                self.y, self.y+self._height)

            comp: list[Entity] = self.parent.children.copy()
            comp.remove(self)

            for child in comp:
                r2_x = range(
                    child.x, child.x+child._width)
                r2_y = range(
                    child.y, child.y+child._height)

                if not self.parent.overlap\
                        and r1_x.start < r2_x.stop and r2_x.start < r1_x.stop\
                        and r1_y.start < r2_y.stop and r2_y.start < r1_y.stop:
                    raise Exception('child overlap')

    # @public
    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int):
        if self.parent and hasattr(self, 'width'):
            if self.parent.width < self.width + x:
                raise StructureError('edge conflict')
        self._x = x
        self._overlap_check()

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        if self.parent and hasattr(self, 'height'):
            if self.parent.height < self.height + self.y:
                raise StructureError('edge conflict')
        self._y = y
        self._overlap_check()

    @property
    def pos(self) -> tuple[int, int]:
        return ((self._x, self._y))

    @pos.setter
    def pos(self, x: int, y: int):
        self.x = x
        self.y = y

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

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def dimensions(self):
        return ((self.width, self.height))

    @property
    def color(self) -> str | None:
        return self._color

    @color.setter
    def color(self, color: str | tuple[int, int, int] | None):
        """a color name and explicit rgb values can be passed

        color effects both 
        the properties color AND rgb"""

        if type(color) == str:
            if color not in Color.colors:
                raise Exception(
                    'color does not exist, add it as a color or use rgb values')

            self._color = color
            self._rgb = Color[color]

        elif type(color) == tuple:
            for i in color:
                if 0 > i > 255:
                    raise Exception('rgb values need to be between 0 and 255')

                self._color = None
                self._rgb = color

        elif not color:
            self._color = None
            self._rgb = None

        else:
            raise Exception(
                'wrong color specification, need either keyword or rgb')

    @property
    def rgb(self):
        """for every color there is an rgb but not every rgb defines a color,
        self._rgb = (1,2,3) and self._color = None IS POSSIBLE"""
        return self._rgb

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
