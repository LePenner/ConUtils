from __future__ import annotations
import asyncio
from typing import Unpack

from ..entity import Entity, EntityKwargs
from ...errors.errors import ethrow


class Element(Entity):

    def __init__(self, **kwargs: Unpack[EntityKwargs]):

        super().__init__(**kwargs)

    @property
    def representation(self):
        ret: list[str] = []
        return ret


class Animated(Element):
    def __init__(self,
                 frames: None | list[str] | list[list[str]],
                 frametime: float = 100,
                 **kwargs: Unpack[EntityKwargs]):
        """frametime in ms"""
        self._frames = Animated._get_proper_frames(frames)
        # NOT PRECISE FOR LOW VALUES
        self._frametime = frametime / 1000  # frametime in milliseconds
        self._cur = 0
        self._draw = False

        super().__init__(**kwargs)

    def __str__(self):
        return str(self._frames[self._cur])

    @staticmethod
    def _get_proper_frames(frames: None | list[str] | list[list[str]]) -> list[list[str]]:

        if frames == None:
            return [[]]

        output: list[list[str]] = []

        for frame in frames:
            if isinstance(frame, str):
                try:
                    frame = [frame.strip("\n") for frame in frame.split("\n")]
                except:
                    ethrow("ELMT", "faulty frames")

                output.append(frame)

            # untrusted input
            elif isinstance(frame, list):  # type: ignore

                # untrusted input
                if all(isinstance(line, str) for line in frame):  # type: ignore

                    output.append(frame)

                else:
                    ethrow("ELMT", "faulty frames")

            else:
                ethrow("ELMT", "faulty frames")

        return output

    async def _animation_loop(self) -> None:
        while True:
            await asyncio.sleep(self._frametime)
            self.draw_next()

    @property
    def representation(self):
        return self._frames[self._cur]

    def get_frame(self):
        return self._frames[self._cur]

    def draw_next(self):
        self._cur += 1
        if self._cur >= len(self._frames):
            self._cur = 0

        return self._frames[self._cur]
