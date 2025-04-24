from __future__ import annotations
from typing import TYPE_CHECKING, Optional, TypedDict, Unpack

if TYPE_CHECKING:
    from .container import Container


class EntityArgs(TypedDict):
    parent: Optional[Container]
    x: int
    y: int
    width: int
    height: int
    bold: bool
    italic: bool
    color: Optional[tuple[int, int, int]]


class Entity:
    """Internal baseclass
    Defines standard for containers, text objects, etc.

    Interface
        methods:
            -
    """

    # @constructor
    def __init__(self, **kwargs: Unpack[EntityArgs]):

        parent = kwargs["parent"]
        self._parent = parent
        self.__set_width(kwargs["width"])
        self.__set_heigth(kwargs["height"])
        self._x = kwargs["x"]
        self._y = kwargs["y"]
        self.bold = kwargs["bold"]
        self.italic = kwargs["italic"]

        # needs checks
        self._color = kwargs["color"]

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
    def color(self):
        return self._color

    @color.setter
    def color(self, color: tuple[int, int, int] | None):
        pass

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
