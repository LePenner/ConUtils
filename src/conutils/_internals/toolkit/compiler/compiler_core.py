from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
import __main__
from errors import ethrow

if TYPE_CHECKING:
    from ...entity.elements import Element
    from ...console import Console

# frame>line>obj(pos, rep, tuple[bold, italic, strike_through], rgb(r,g,b)|None)


class ObjDict(TypedDict):
    pos: int
    rep: str
    format: tuple[bool, bool, bool]
    color: tuple[int, int, int] | None


line_type = list[ObjDict]
frame_type = list[line_type]


class PreComp:

    @staticmethod
    def _binsert_index(obj: ObjDict, line: line_type) -> int:
        x = obj["pos"]
        lo = 0
        hi = len(line)

        while lo < hi:
            mid = (lo + hi) // 2
            if line[mid]["pos"] < x:
                lo = mid + 1
            else:
                hi = mid

        return lo

    @staticmethod
    def to_frame(obj: ObjDict, line: line_type):
        """Calculates position for `obj` and places it in its location."""

        line_index = PreComp._binsert_index(obj, line)

        line.insert(
            line_index, obj)


class Comp:
    """Contains all logic to compile `Frame`."""

    @staticmethod
    def _overlap_handler(frame: frame_type):

        for line in frame:

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

    @staticmethod
    def _get_color(color: tuple[int, int, int] | None):
        if color:
            r, g, b = color
            return f"\033[38;2;{r};{g};{b}m"
        else:
            return "\033[39;49m"

    @staticmethod
    def compile(frame: frame_type, console: Console):
        """Converts the gathered objects into a single string.

        The objects in a frame are converted and formated accordingly. The frame is processed on a per line basis.
        """

        if console.overlap == True:
            Comp._overlap_handler(frame)

        out = ""
        #
        for i, line in enumerate(frame):
            # fill line with spaces if empty
            if len(line) == 0:
                out += " "*console.width
                continue

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
                    out += Comp._get_color(obj["color"])
                else:
                    # reset color
                    out += "\033[39m"

                # add representation
                out += obj["rep"]

                # if last object in line:
                if len(line) == j+1:
                    # fill rest of line with spaces
                    out += " "*(console.width -
                                obj["pos"] - len(obj["rep"]))

            # add new line at end of line
            if len(frame) != i+1:
                out += "\n"
            # if last line: return to top left
            else:
                out += "\033[u"
        return out


class Frame:
    """Holds a frame to be operated on.

        Collected elements are placed onto the Frame.
        Frame can be compiled after. 

    Uses one instance each frame.
    Frame is consumed after compilation.
    """

    def __init__(self, console: Console, processes: int):

        self._console = console
        self._frame: frame_type = [[] for _ in range(self._console.height)]
        self._cached_frame: str | None = None

    def get_cached(self):
        if self._cached_frame:
            return self._cached_frame
        else:
            ethrow("COMP", "not compiled")

    def compile(self):
        if not self._cached_frame:
            out = Comp.compile(self._frame, self._console)
            self._cached_frame = out
            return out
        else:
            ethrow("COMP", "cached frame")

    def collect(self, element: Element):
        """Add an Element to a `line` in `_frame`.

        For every line of an elements representation, insert it into the right spot of the line.
        Contains logic to handle single/multiprocessing.
        """

        for i, rep in enumerate(element.representation):

            obj: ObjDict = {"pos": element.x_abs,
                            "rep": rep,
                            "format": (element.bold, element.italic, element.strike_through),
                            "color": element.display_rgb}
            index = element.y_abs+i
            line = self._frame[index]

            '''
            if self._processor:
                # for multiprocessing
                self._processor.queue.put((obj, index))
            else:'''

            PreComp.to_frame(obj, line)
