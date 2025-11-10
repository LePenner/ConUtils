from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Callable, Any, Protocol, cast
import multiprocessing as mp
import __main__

if TYPE_CHECKING:
    from ..entity.elements import Element
    from ..console import Console

# screen>line>obj(pos, rep, tuple[bold, italic, strike_through], rgb(r,g,b)|None)


class ObjDict(TypedDict):
    pos: int
    rep: str
    format: tuple[bool, bool, bool]
    color: tuple[int, int, int] | None


line_type = list[ObjDict]
screen_type = list[line_type]


class LockProtocol(Protocol):
    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool: ...
    def release(self) -> None: ...
    def locked(self) -> bool: ...


class QueueProtocol(Protocol):
    def put(self, item: Any) -> None: ...
    def get(self) -> Any: ...
    def get_nowait(self) -> Any: ...


class ValueProtocol(Protocol):
    @property
    def value(self) -> bool: ...
    @value.setter
    def value(self) -> None: ...


class PlateType(TypedDict):
    queue: QueueProtocol
    locks: list[LockProtocol]
    stop: ValueProtocol


class MultiProcessing:
    def __init__(self, otp: Output, processes: int, add_processor: Callable[[ObjDict, line_type], line_type]) -> None:
        manager = mp.Manager()
        self._manager = manager
        self._otp = otp
        self._add_processor = add_processor
        self._screen = manager.list()
        self._queue = manager.Queue()
        self._pool = mp.Pool(processes)
        self._line_locks = [manager.Lock() for _ in range(otp.console.height)]
        self._stop_flag = manager.Value("b", False)
        self._plate = cast(PlateType, {"queue": self._queue,
                                       "locks": self._line_locks,
                                       "stop": self._stop_flag})

    @staticmethod
    def _add_multiprocessing(q: QueueProtocol,
                             locks: list[LockProtocol],
                             stop: ValueProtocol,
                             add_processor: Callable[[ObjDict, line_type], line_type],
                             screen: screen_type):

        while not stop.value:

            try:
                obj, index = cast(
                    tuple[ObjDict, int], q.get_nowait())

            except:
                # no object in queue
                return

            lock = locks[index]

            if lock.acquire(blocking=False):
                try:
                    screen[index] = add_processor(obj, screen[index])

                finally:
                    lock.release()
            else:
                q.put((obj, index))

    @property
    def pool(self):
        return self._pool

    @property
    def queue(self):
        return self._queue

    @property
    def plate(self):
        return self._plate

    @property
    def screen(self):
        return self._screen

    def start_processor(self):
        p = self._plate
        self._screen = self._manager.list(
            [self._manager.list(line) for line in self._otp.screen]
        )
        self._stop_flag = False
        self._process = self.pool_work(self._add_multiprocessing,
                                       p["queue"], p["locks"], p["stop"], self._add_processor, self._screen)

    def end_processor(self):
        self._stop_flag = True
        self._process.wait()

    def pool_work(self, f: Callable[..., Any], *args: Any):
        if not self._pool:
            raise RuntimeError

        return self._pool.apply_async(f, args)


class Output:

    def __init__(self, console: Console, processes: int):

        self._console = console
        self.clear()  # initilazes self._screen

        if processes:
            self._processor = MultiProcessing(
                self, processes, self._add_processor)
        else:
            self._processor = None

    @staticmethod
    def _get_color(color: tuple[int, int, int] | None):
        if color:
            r, g, b = color
            return f"\033[38;2;{r};{g};{b}m"
        else:
            return "\033[39;49m"

    @staticmethod
    def _binsert_algo(obj: ObjDict, lst: line_type) -> int:
        """Searches for index recursively."""

        x = obj["pos"]
        piv = len(lst)//2

        if len(lst) > 1:

            if x > lst[piv]["pos"]:
                return piv+Output._binsert_algo(obj, lst[piv:])+1
            else:
                return Output._binsert_algo(obj, lst[:piv])
        elif len(lst) == 1:
            if x > lst[piv]["pos"]:
                return 1
            else:
                return 0
        else:
            return 0

    @staticmethod
    def _add_processor(obj: ObjDict, line: line_type):

        index = Output._binsert_algo(obj, line)

        line.insert(
            index, obj)

        return line

    def _overlap_handler(self):

        for line in self._screen:

            # j as line index
            j: int = 1
            while True:

                if len(line) <= j:
                    break

                # previous object in list
                prev_obj = line[j-1]
                prev_obj_pos = prev_obj["pos"]
                prev_obj_width = len(prev_obj["rep"])

                # point of reference
                obj = line[j]
                obj_pos = obj["pos"]
                obj_width = len(obj["rep"])

                # check objects for overlap
                if prev_obj_pos <= obj_pos + obj_width and \
                        prev_obj_pos + prev_obj_width >= obj_pos:

                    split: ObjDict = {
                        "pos": prev_obj_pos,
                        "rep": "",
                        "format": prev_obj["format"],
                        "color": prev_obj["color"]
                    }

                    # remove prev_obj from line
                    line.pop(j-1)

                    # calculate left side of split
                    # how much is visible
                    if prev_obj_pos < obj_pos:
                        l_split = split.copy()
                        l_split["rep"] = prev_obj["rep"][:obj_pos - prev_obj_pos]
                        line.insert(j-1, l_split)
                        # increment j because we added an element to the left
                        j += 1

                    # calculate right side of split
                    # how much is visible
                    if prev_obj_pos + prev_obj_width > obj_pos + obj_width:
                        r_split = split.copy()
                        r_split["rep"] = prev_obj["rep"][(
                            obj_pos + obj_width) - prev_obj_pos:]
                        r_split["pos"] += obj_width
                        line.insert(j+1, r_split)

                # if objects dont overlap go to next object
                # Note: WE DO NOT INCREMENT IF THERE IS OVERLAP!
                else:
                    j += 1

    @property
    def console(self):
        return self._console

    @property
    def screen(self):
        return self._screen

    @property
    def processor(self):
        return self._processor

    def clear(self):
        self._screen: screen_type = [[] for _ in range(self._console.height)]

    def add(self, element: Element):
        """Add an Element to a line in screen.

        For every line of an elements representation, insert it into the right spot of the line.
        """

        for i, rep in enumerate(element.representation):

            obj: ObjDict = {"pos": element.x_abs,
                            "rep": rep,
                            "format": (element.bold, element.italic, element.strike_through),
                            "color": element.display_rgb}
            index = element.y_abs+i
            line = self._screen[index]

            if self._processor:
                # for multiprocessing
                self._processor.queue.put((obj, index))
            else:
                self._screen[index] = self._add_processor(obj, line)

    def compile(self):
        if self._processor:
            self._screen = [
                list(line) for line in self._processor.screen]

        if self._console.overlap == True:
            self._overlap_handler()

        out = ""
        for i, line in enumerate(self._screen):
            # fill line with spaces if empty
            if len(line) == 0:
                out += " "*self._console.width

            for j, obj in enumerate(line):
                if j > 0:
                    # add spacing
                    # starting position - prev starting position - len(obj)
                    out += " "*(obj["pos"] - line[j-1]
                                ["pos"] - len(line[j-1]["rep"]))
                else:
                    out += " "*obj["pos"]

                # check for color
                if obj["color"]:
                    out += Output._get_color(obj["color"])
                else:
                    # reset color
                    out += "\033[39m"

                # add representation
                out += obj["rep"]

                # if last object in line:
                if len(line) == j+1:
                    # fill rest of line with spaces
                    out += " "*(self._console.width -
                                obj["pos"] - len(obj["rep"]))

            # add new line at end of line
            if len(self._screen) != i+1:
                out += "\n"
            # if last line: return to top left
            else:
                out += "\033[u"
        return out
