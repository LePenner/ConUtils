from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

from conutils.entity.entity import Entity

if TYPE_CHECKING:
    from conutils.entity.container.container import Container


class Element(Entity):

    def __init__(self, representation: list[str] | None, parent: Container | None = None, x: int = 0, y: int = 0):

        self._str = ''  # no error if representation is empty

        width = 0

        if representation:
            for l in representation:
                if not l.isprintable():
                    raise Exception()
                if not self._str:
                    self._str = l
                else:
                    self._str += '\n'+l

                if len(l) > width:
                    width = len(l)
            height = len(representation)
        else:
            width = 0
            height = 0

        super().__init__(parent, x, y, width, height)

    def __str__(self):
        return self._str


class Animated(Element):
    def __init__(self, parent: Container | None = None, x: int = 0, y: int = 0, frames: list[str] = [], frametime: int = 100):
        """frametime in ms"""
        self._frames = frames
        self._frametime = frametime / 1000  # frametime in milliseconds
        self._cur = 0
        self._draw = False
        super().__init__(None, parent, x, y)

    def __str__(self):
        return self._frames[self._cur]

    async def _animation_loop(self):
        while True:
            await asyncio.sleep(self._frametime)
            self._draw = True

    def get_draw_flag(self):
        return self._draw

    def reset_drawflag(self):
        self._draw = False

    def get_frame(self):
        return self._frames[self._cur]

    def draw_next(self):
        self._cur += 1
        if self._cur >= len(self._frames):
            self._cur = 0

        return self._frames[self._cur]
