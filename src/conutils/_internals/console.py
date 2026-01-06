import __main__
import os
import asyncio
import time
import datetime
from multiprocessing import cpu_count, freeze_support, current_process, set_start_method
from typing import Unpack
from .entity.elements import Animated
from .entity.container import Container
from .toolkit.compiler.compiler_core import Frame
from .entity.entity import EntityKwargs
from .errors import ethrow


class Console(Container):
    """Console handles the output of any child screens and lines to the terminal.

    Define an `update` function to configure runtime behavior.

    Setting `debug` to `True` will disable the console output.
    """

    _instance = None

    def __init__(self,
                 overlap: bool = False,
                 fps: int = 0,
                 multiprocessing: bool | int = False,
                 debug: bool = False,
                 **kwargs: Unpack[EntityKwargs]):
        self._stop_flag = False
        self.fps = fps

        if multiprocessing == True:
            multiprocessing = cpu_count()
        elif multiprocessing != False:
            if multiprocessing > cpu_count():
                ethrow("CONS", "too many processes")

        self._processes = multiprocessing
        self.debug = debug

        # set default length and height to terminal
        kwargs["width"] = kwargs.get("width") or\
            os.get_terminal_size()[0]
        kwargs["height"] = kwargs.get("height") or\
            os.get_terminal_size()[1]

        super().__init__(overlap=overlap, **kwargs)

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

        freeze_support()
        if current_process().name != "MainProcess":
            return

        set_start_method("spawn", force=True)
        self.clear_console()
        self.hide_cursor()

        try:
            asyncio.run(self._run_async())
            self._cleanup()
        except KeyboardInterrupt:
            self._cleanup()

    async def _run_async(self):

        children = self._collect_children()

        # start all animation loops
        for child in children:
            if isinstance(child, Animated):
                # _animation_loop() is protected
                asyncio.create_task(child._animation_loop())  # type: ignore

        last_loop_time = time.perf_counter()
        last_render_time = last_loop_time
        # keeps track of sync
        accumulator = 0
        dt_fixed = 1/self.fps

        while self._stop_flag == False:

            now = time.perf_counter()
            dt = now - last_loop_time
            last_loop_time = now

            accumulator += dt
            while accumulator >= dt_fixed:
                # lets user add custom functionality on runtime
                # checks for function update() in main file
                if getattr(__main__, "update", None):
                    __main__.update()  # type:  ignore
                accumulator -= dt_fixed

            if now - last_render_time >= dt_fixed:
                frame = Frame(self, self._processes)
                for child in children:
                    frame.collect(child)

                if not self.debug:
                    print(frame.compile(), end="\r")
                else:
                    with open("out.txt", "a") as f:
                        frametime = now - last_render_time
                        f.write(
                            f"[{datetime.datetime.now()}] frametime: "
                            f"{frametime*1000:.2f} ms || {1/frametime:.2f} fps\n"
                        )

                last_render_time = now

            await asyncio.sleep(0)
