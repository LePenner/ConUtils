import asyncio


class Animated:
    def __init__(self, frames: list, frametime: int, **kwargs):
        """frametime in ms"""
        self._frames = frames
        self._frametime = frametime / 1000  # frametime in milliseconds
        self._cur = 0
        self._draw = False
        super().__init__(**kwargs)

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
