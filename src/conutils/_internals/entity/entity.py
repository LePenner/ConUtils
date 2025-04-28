from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .container import Container

from ..toolkit import Color


class Entity:
    """Internal baseclass
    Defines standard for containers, text objects, etc.

    Any object can be stylized with bold, itlac and color,
    these properties get inherited by all children.

    Interface
        **methods**:
            - constructor
            - 
        **attributes**:
            - x
            - y
            - pos
            - color
            - parent
        read only:
            - x_abs
            - y_abs
            - abs_pos
            - height
            - width
            - dimension
            - rgb
            - display_rgb
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
        if parent:
            parent.add_child(self, replace=True)
            self._parent = parent

        # define positioning
        self._x = x
        self._y = y

        # get initial absolute position recursively
        # further handled in x and y setter by parent
        self._set_x_abs(x)
        self._set_y_abs(y)

        # built in conflict checks
        self.__set_width(width)
        self.__set_height(height)

        self._overlap_check()

        self.bold = bold
        self.italic = italic

        self.color = color
        self._set_display_rgb(self.rgb)

    def __set_width(self, width: int) -> int | None:
        if self._parent:
            if self._parent.width < self.x + width:
                raise StructureError('edge conflict')
        self._width = width

    def __set_height(self, height: int) -> int | None:
        if self._parent:
            if self._parent.height < self.y + height:
                raise StructureError('edge conflict')
        self._height = height

    # @protected
    def _overlap_check(self):

        if self.parent:
            r1_x = range(
                self.x, self.x+self.width)
            r1_y = range(
                self.y, self.y+self.height)

            comp: list[Entity] = self.parent.children.copy()
            comp.remove(self)

            for child in comp:
                r2_x = range(
                    child.x, child.x+child.width)
                r2_y = range(
                    child.y, child.y+child.height)

                if not self.parent.overlap\
                        and r1_x.start < r2_x.stop and r2_x.start < r1_x.stop\
                        and r1_y.start < r2_y.stop and r2_y.start < r1_y.stop:
                    raise Exception('child overlap')

    def _set_x_abs(self, x: int = 0):

        # initialisation and failsafe if no parrent
        if x:
            self._x_abs = x
        else:
            self._x_abs = self.x

        if self.parent:
            self._x_abs = self.parent.x_abs + self.x
        else:
            return self.x

    def _set_y_abs(self, y: int = 0):

        # initialisation and failsafe if no parrent
        if y:
            self._y_abs = y
        else:
            self._y_abs = self.y

        if self.parent:
            self._y_abs = self.parent.y_abs + self.y
        else:
            return self.y

    def _set_display_rgb(self, rgb: tuple[int, int, int] | None = None):

        # initialisation and failsafe if no parrent
        if rgb:
            self._display_rgb = rgb
        else:
            self._display_rgb = self.rgb

        if self.parent and not self.rgb:
            self._display_rgb = self.parent.display_rgb
        else:
            return self.rgb

    # @public
    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int):
        if self.parent and hasattr(self, 'width') and\
                self.parent.width < self.width + x:
            raise StructureError('edge conflict')
        self._x = x
        self._overlap_check()
        self._set_x_abs()

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        if self.parent and hasattr(self, 'height') and\
                self.parent.height < self.height + self.y:
            raise StructureError('edge conflict')
        self._y = y
        self._overlap_check()
        self._set_y_abs()

    @property
    def pos(self) -> tuple[int, int]:
        return ((self._x, self._y))

    @pos.setter
    def pos(self, pos: tuple[int, int]):
        self.x = pos[0]
        self.y = pos[1]

    @property
    def x_abs(self) -> int:
        return self._x_abs

    @property
    def y_abs(self) -> int:
        return self._y_abs

    @property
    def abs_pos(self) -> tuple[int, int]:
        return ((self._x_abs, self._y_abs))

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
            self._set_display_rgb(Color[color])

        elif type(color) == tuple:
            for i in color:
                if 0 > i > 255:
                    raise Exception('rgb values need to be between 0 and 255')

            self._color = None
            self._rgb = color
            self._set_display_rgb(color)

        elif not color:
            self._color = None
            self._rgb = None
            self._set_display_rgb()

        else:
            raise Exception(
                'wrong color specification, need either keyword or rgb')

    @property
    def rgb(self):
        """for every color there is an rgb but not every rgb defines a color,
        self._rgb = (1,2,3) and self._color = None IS POSSIBLE"""
        return self._rgb

    @property
    def display_rgb(self) -> tuple[int, int, int] | None:
        return self._display_rgb

    @property
    def parent(self) -> Container | None:
        return self._parent

    @parent.setter
    def parent(self, parent: Container | None):
        if self.parent:
            self.parent.remove_child(self)

        if parent:
            parent.add_child(self, replace=True)
            self._parent = parent
            self._set_x_abs()
            self._set_y_abs()
        else:
            self._parent = None


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
