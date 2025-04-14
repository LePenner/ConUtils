from __future__ import annotations
from typing import TYPE_CHECKING

from .element import Element

if TYPE_CHECKING:
    from ..container import Container


class StaticText(Element):
    def __init__(self, representation: list[str] | None = None,
                 parent: Container | None = None,
                 x: int = 0, y: int = 0):
        """representation in format ["First Line","Second Line", "Third Line"]"""
        self._str = ""

        width = 0

        if representation:
            for l in representation:
                if not l.isprintable():
                    raise Exception()
                if self._str == "":
                    self._str = l
                else:
                    self._str += '\n\033[{x}{direction}'+l

                if len(l) > width:
                    width = len(l)
            height = len(representation)
        else:
            width = 1
            height = 1

        super().__init__(parent, x, y, width, height)

    def __str__(self):
        # for right indentation on every line
        if self.x_abs > 0:
            return self._str.format(x=self.x_abs, direction="C")
        else:
            return self._str.format(x=self.x_abs, direction="D")
