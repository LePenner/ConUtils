from __future__ import annotations

from typing import Unpack
from ..entity import EntityKwargs


from ...errors import ethrow
from ..elements import Text
from ...errors import ethrow
from ...entity import Entity


class Frame(Entity):
    def __init__(self,
                 vert_edge: str = "|",
                 hori_edge: str = "=",
                 corner: str | list[str] = ["#"],
                 **kwargs: Unpack[EntityKwargs]):

        self._container = kwargs.get("parent")
        self._parts: list[Text] = []
        super().__init__(**kwargs)
        self.representation(vert_edge, hori_edge, corner)

    @property
    def parts(self):
        return self._parts

    @property
    def vertical_edge(self):
        return self._vertical_edge

    @vertical_edge.setter
    def vertical_edge(self, vertical_edge: str):
        self.representation(vertical_edge,
                            self._horrizontal_edge, self._corner)

    @property
    def horrizontal_edge(self):
        return self._horrizontal_edge

    @horrizontal_edge.setter
    def horrizontal_edge(self, horrizontal_edge: str):
        self.representation(self._vertical_edge,
                            horrizontal_edge, self._corner)

    @property
    def corner(self):
        return self._corner

    @corner.setter
    def corner(self, corner: str | list[str]):
        self.representation(self._vertical_edge,
                            self._horrizontal_edge, corner)

    def representation(self, vert_edge: str, hori_edge: str, corner: str | list[str]):
        if type(corner) == str:
            self._corner = [corner]
        if len(corner) == 0:
            self._corner = " "
        else:
            self._corner = corner

        self._vertical_edge = vert_edge
        self._horrizontal_edge = hori_edge

        parent = self.parent
        if parent:
            if set(self.parts).intersection(set(parent.children)):
                parent.remove_child(self)
                parent.add_child(self)
            self._presentation()

    # ----- OVERWRITES -----

    @property
    def pos(self) -> tuple[int, int]:
        return self._pos

    @pos.setter
    def pos(self, pos: tuple[int, int]):
        ethrow("FRAM", "read from Frame")

    # ----- END -----

    def _presentation(self):
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

        corner_parts: list[list[str]] = [[] for _ in range(4)]

        for y in range(height):

            # 0 or 1
            height_mod = (y % 2)
            for x in range(width):

                # counts 0 1 0 1... if heigth_mod = 0
                # and 2 3 2 3... if height_mod = 1
                corner_parts[height_mod*2 + x % 2].append(
                    # applies pattern with matrix scaling
                    self.corner[y//2 % corner_height][x//2 % corner_width])

            # checking if the next line will fit
            # new line every 2 iterations of y
            if y+2 < height:
                # left side corners
                if width > 0:
                    corner_parts[height_mod*2].append("\n")
                # right side corners
                if width > 1:
                    corner_parts[height_mod*2 + 1].append("\n")

        elements = ["".join(parts) for parts in corner_parts]

        pw = self.parent.width
        w = max(width//2, corner_width)
        ph = self.parent.height
        h = max(height//2, corner_height)

        offsets = [
            # corner cords
            (0, 0),
            (pw - w, 0),
            (0, ph - h),
            (pw - w, ph - h)
        ]

        sides_offsets = [
            # top | left | bot | right
            (w, 0),
            (0, h),
            (w, ph-hori_height),
            (pw-vert_width, h)
        ]

        for i in range(2):
            if w < round(pw / 2):
                elements.append("\n".join(tile*(pw-w*2)
                                for tile in self.horrizontal_edge))
                offsets.append(sides_offsets[i*2])

            if h < round(ph/2):
                elements.append("\n".join(self.vertical_edge
                                for _ in range(ph - h*2)))
                offsets.append(sides_offsets[i*2+1])

        self._parts = []
        for i, (x, y) in enumerate(offsets):
            child = (Text(elements[i],
                          x=x,
                          y=y,
                          color=self.color,
                          bold=self.bold,
                          strike_through=self.strike_through,
                          italic=self.italic))
            self.parent.add_child(child)
            self._parts.append(child)
