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


class Output:

    def __init__(self, console: Console, processes: int):

        self._console = console
        manager = mp.Manager()
        self._queue: QueueProtocol | None = manager.Queue()
        self._pool = mp.Pool(processes) if processes > 0 else None
        self._line_locks: list[LockProtocol] = [manager.Lock()
                                                for _ in range(self._console.height)]
        self.clear()

        self.stop_processor = False

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

    def _add_processor(self, obj: ObjDict, line: line_type):

        index = self._binsert_algo(obj, line)

        line.insert(
            index, obj)

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

    def _add_multiprocessing(self):

        while not self.stop_processor:
            if not self._queue:
                raise RuntimeError

            try:
                obj, index = cast(
                    tuple[ObjDict, int], self._queue.get_nowait())
            except:
                return

            lock = self._line_locks[index]

            if not lock.locked():
                lock.acquire()
                line = self._screen[obj["pos"] + index]
                self._add_processor(obj, line)
                lock.release()
            else:
                self._queue.put((obj, index))

    @property
    def pool(self):
        return self._pool

    def start_processor(self):
        self.stop_processor = False
        self.pool_work(self._add_multiprocessing)

    def pool_work(self, f: Callable[..., Any], *args: Any):
        if not self._pool:
            raise RuntimeError

        return self._pool.apply_async(f, *args)

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

            if self._pool and self._queue:
                # for multiprocessing
                self._queue.put((obj, i))
            else:
                line = self._screen[element.y_abs+i]
                self._add_processor(obj, line)

    def compile(self):
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
