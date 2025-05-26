from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Unpack

if TYPE_CHECKING:
    from .container import Container

from ..toolkit import Color
from ..errors import ethrow


class EntityKwargs(TypedDict, total=False):
    parent: Container | None
    x: int
    y: int
    width: int
    height: int
    bold: bool
    italic: bool
    color: tuple[int, int, int] | str | None


class Entity:
    """Internal baseclass
    Defines standard for containers, text objects, etc.

    Any object can be stylized with bold, italic and color,
    these properties get inherited by all children.

    Positional data is handled through pos property, 
    which includes all needed checks.

    Interface
        **methods**:
            - constructor
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
    def __init__(self, **kwargs: Unpack[EntityKwargs]):

        parent = kwargs.get("parent", None)
        x = kwargs.get("x", 0)
        y = kwargs.get("y", 0)
        width = kwargs.get("width", 1)
        height = kwargs.get("height", 1)
        bold = kwargs.get("bold", False)
        italic = kwargs.get("italic", False)
        color = kwargs.get("color", None)

        self._parent = parent
        if parent:
            parent.add_child(self, replace=True)
            self._parent = parent

        self._pos = (x, y)
        self._dimension = (width, height)
        self._overlap_check()

        self._abs_pos = self._get_abs_pos()

        self._bold = bold
        self._italic = italic
        self.color = color

    # @protected
    def _overlap_check(self):

        if not self.parent:
            return

        if self.parent.width < self.x + self.width or self.parent.height < self.y + self.height:
            ethrow("ENTY", "edge conflict")

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
                ethrow("ENTY", "child overlap")

    def _get_abs_pos(self) -> tuple[int, int]:

        if self.parent:
            return (self.parent.x_abs +
                    self.x, self.parent.y_abs+self.y)
        else:
            return self.pos

    def _get_display_rgb(self):

        if self.parent and not self.rgb:
            return self.parent.display_rgb
        else:
            return self.rgb

    # @public
    @property
    def pos(self) -> tuple[int, int]:
        return self._pos

    @pos.setter
    def pos(self, pos: tuple[int, int]):
        if self.parent:
            if self.parent.width < self.width + self.x or self.parent.height < self.height + self.y:
                ethrow("ENTY", "edge conflict")

        self._pos = pos
        self._abs_pos = self._get_abs_pos()
        self._overlap_check()

    @property
    def x(self) -> int:
        return self._pos[0]

    @x.setter
    def x(self, x: int):
        self.pos = (x, self.y)

    @property
    def y(self) -> int:
        return self._pos[1]

    @y.setter
    def y(self, y: int):
        self.pos = (self.x, y)

    @property
    def x_abs(self) -> int:
        return self._abs_pos[0]

    @property
    def y_abs(self) -> int:
        return self._abs_pos[1]

    @property
    def abs_pos(self) -> tuple[int, int]:
        return self._abs_pos

    @property
    def width(self) -> int:
        return self._dimension[0]

    @property
    def height(self) -> int:
        return self._dimension[1]

    @property
    def dimensions(self):
        return self._dimension

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

        self._display_rgb = self._get_display_rgb()

    @property
    def rgb(self):
        """for every color there is an rgb but not every rgb defines a color,
        self._rgb = (1,2,3) and self._color = None IS POSSIBLE"""
        return self._rgb

    @property
    def display_rgb(self) -> tuple[int, int, int] | None:
        return self._display_rgb

    @property
    def bold(self):
        return self._bold

    @property
    def italic(self):
        return self._italic

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
            self._abs_pos = self._get_abs_pos()
        else:
            self._parent = None
