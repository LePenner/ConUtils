import __main__
import os
import asyncio
from typing import Unpack
from .entity.container import Container
from .entity.elements import Animated
from .toolkit.screen_compiler import Output
from .entity.entity import EntityKwargs


class Console(Container):
    """Console handles the output of any child screens and lines to the terminal.

    define an `update` function to configure runtime behavior. 
    """

    def __init__(self, overlap: bool = False, fps: int = 100, **kwargs: Unpack[EntityKwargs]):
        self._stop_flag = False
        self.fps = fps

        # set default length and height to terminal
        kwargs["width"] = kwargs.get("width", os.get_terminal_size()[0])
        kwargs["height"] = kwargs.get("height", os.get_terminal_size()[1])

        super().__init__(overlap=overlap, **kwargs)

        self._otp = Output(self)

    def _cleanup(self):
        self.show_cursor()
        self.clear_console()
        self.reset_format()

    @staticmethod
    def hide_cursor():
        print('\033[?25l', end="")

    @staticmethod
    def show_cursor():
        print('\033[?25h', end="")

    @staticmethod
    def clear_console():
        match os.name:
            case "nt":
                os.system("cls")
            case "posix":
                os.system("clear")
            case _:
                print("\033[H\033[J", end="")

    @staticmethod
    def reset_format():
        print("\033[0m", end="")

    def stop(self):
        self._stop_flag = True

    def run(self):
        self.clear_console()
        self.hide_cursor()
        print("\033[s", end="")
        try:
            asyncio.run(self._run_async())
            self._cleanup()
        except KeyboardInterrupt:
            self._cleanup()

    async def _run_async(self):

        children = self._collect_children()

        # start all animation loops
        for child in children:
            if hasattr(child, "_animation_loop"):
                # _animation_loop() is protected
                asyncio.create_task(child._animation_loop())  # type: ignore

        # check for updates
        while self._stop_flag == False:
            await asyncio.sleep(1/self.fps)
            for child in children:
                if isinstance(child, Animated):
                    if child.draw_flag == True:
                        child.reset_drawflag()
                        child.draw_next()

                self._otp.add(child)

            print(self._otp.compile(), end="\r")
            self._otp.clear()

            # lets user add custom functionality on runtime
            # checks for function update() in main file
            if getattr(__main__, "update", None):
                __main__.update()
