from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

from ..entity import Entity

if TYPE_CHECKING:
    from ..container import Container


class Element(Entity):
    """only use as abstract class, cannot handle dynamic heigth and width adjustment"""

    def __init__(self,
                 parent: Container | None,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 bold: bool,
                 italic: bool,
                 color: str | tuple[int, int, int] | None):

        super().__init__(parent, x, y, width, height, bold, italic, color)


class Animated(Element):
    def __init__(self,
                 parent: Container | None,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 bold: bool,
                 italic: bool,
                 color: str | tuple[int, int, int] | None,
                 frames: list[str],
                 frametime: float):
        """frametime in ms"""
        self._frames = frames
        self._frametime = frametime / 1000  # frametime in milliseconds
        self._cur = 0
        self._draw = False
        super().__init__(parent, x, y, width, height, bold, italic, color)

    def __str__(self):
        return self._frames[self._cur]

    async def _animation_loop(self) -> None:
        while True:
            await asyncio.sleep(self._frametime)
            self._draw = True

    @property
    def draw_flag(self) -> bool:
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
