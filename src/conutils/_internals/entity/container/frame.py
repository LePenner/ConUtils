from __future__ import annotations
from typing import TYPE_CHECKING

from ...errors import ethrow
from ..elements import Text

if TYPE_CHECKING:
    from .container import Container

from typing import Unpack
from conutils._internals.entity.entity import EntityKwargs
from ...errors import ethrow
from ...entity import Entity


class Frame(Entity):
    def __init__(self,
                 vert_edge: str = "|",
                 hori_edge: str = "=",
                 corner: str | list[str] = ["#"],
                 **kwargs: Unpack[EntityKwargs]):

        self._container = kwargs.get("parent")
        super().__init__(**kwargs)
        self.vertical_edge = vert_edge
        self.horrizontal_edge = hori_edge
        self.corner = corner

    @property
    def corner(self):
        return self._corner

    @corner.setter
    def corner(self, corner: str | list[str]):
        if type(corner) == str:
            self._corner = [corner]
        else:
            self._corner = corner
        self.presentation()

    @property
    def container(self):
        return self.parent

    @container.setter
    def container(self, container: Container | None):
        if container:
            self.parent = container
            self.presentation()
        else:
            self.parent = None

    @property
    def pos(self) -> tuple[int, int]:
        return self._pos

    @pos.setter
    def pos(self, pos: tuple[int, int]):
        ethrow("FRAM", "read from Frame")

    def presentation(self):
        """Process presentation settings.

        Can only be called if a container/parent is set."""
        if not self.parent:
            raise Exception

        corner_height = len(self.corner)
        corner_width = len(max(self.corner))
        hori_height = len(self.horrizontal_edge)
        vert_width = len(self.vertical_edge)

        width = min(max(corner_width, vert_width)*2, self.parent.width)
        height = min(max(corner_height, hori_height)*2, self.parent.height)

        print(width, height)

        corner_parts: list[list[str]] = [[] for _ in range(4)]

        for y in range(height):

            # 0 or 1
            height_mod = (y % 2)
            for x in range(width):

                # counts 0 1 0 1... if heigth_mod = 0
                # and 2 3 2 3... if height_mod = 1
                corner_parts[height_mod*2 + x % 2].append(
                    # applies pattern with matrix scaling
                    self.corner[y % corner_height][x % corner_width])

                # print(corner_parts)

            # checking if the next line will fit
            # new line every 2 iterations of y
            if y+2 < height:
                # left side corners
                if width > 0:
                    corner_parts[height_mod*2].append("\n")
                # right side corners
                if width > 1:
                    corner_parts[height_mod*2 + 1].append("\n")

        corners = ["".join(parts) for parts in corner_parts]

        pw = self.parent.width
        w = min(width//2, corner_width)
        ph = self.parent.height
        h = min(height//2, corner_height)

        offsets = [
            (0, 0),
            (pw - w, 0),
            (0, ph - h),
            (pw - w, ph - h),
        ]

        print(corners, offsets)

        for i, (x, y) in enumerate(offsets):
            self.parent.add_child(Text(corners[i], x=x, y=y))
