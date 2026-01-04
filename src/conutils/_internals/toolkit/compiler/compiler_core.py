from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict
import __main__

if TYPE_CHECKING:
    from ...entity.elements import Element
    from ...console import Console

# screen>line>obj(pos, rep, tuple[bold, italic, strike_through], rgb(r,g,b)|None)


class ObjDict(TypedDict):
    pos: int
    rep: str
    format: tuple[bool, bool, bool]
    color: tuple[int, int, int] | None


line_type = list[ObjDict]
screen_type = list[line_type]


class PreComp:
    def __init__(self, output: Output) -> None:
        self._otp = output

    @staticmethod
    def _binsert_algo(obj: ObjDict, lst: line_type) -> int:
        """Searches for index recursively."""

        x = obj["pos"]
        piv = len(lst)//2

        if len(lst) > 1:

            if x > lst[piv]["pos"]:
                return piv+PreComp._binsert_algo(obj, lst[piv:])+1
            else:
                return PreComp._binsert_algo(obj, lst[:piv])
        elif len(lst) == 1:
            if x > lst[piv]["pos"]:
                return 1
            else:
                return 0
        else:
            return 0

    def to_screen(self, screen_index: int, obj: ObjDict, line: line_type):
        """Places """

        line_index = PreComp._binsert_algo(obj, line)

        line.insert(
            line_index, obj)

        self._otp.screen[screen_index] = line


class Comp:
    def __init__(self, output: Output) -> None:
        self._otp = output
        self._screen = output.screen
        self._console = output.console

    @staticmethod
    def _get_color(color: tuple[int, int, int] | None):
        if color:
            r, g, b = color
            return f"\033[38;2;{r};{g};{b}m"
        else:
            return "\033[39;49m"

    @property
    def screen(self):
        return self._screen

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

    def compile(self):
        """Converts the gathered objects into a single string.

        The objects in `_screen` are converted and formated accordingly. `_screen` is processed on a per line basis.
        """

        if self._otp.console.overlap == True:
            self._overlap_handler()

        out = ""
        #
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
                    out += Comp._get_color(obj["color"])
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


class Output:

    def __init__(self, console: Console, processes: int):

        self._console = console
        self._screen: screen_type = [[] for _ in range(self._console.height)]

        self._comp = Comp(self)
        self._precomp = PreComp(self)

    def __str__(self):
        return self._comp.compile()

    @staticmethod
    def _get_color(color: tuple[int, int, int] | None):
        if color:
            r, g, b = color
            return f"\033[38;2;{r};{g};{b}m"
        else:
            return "\033[39;49m"

    @property
    def console(self):
        return self._console

    @property
    def screen(self):
        return self._screen

    def clear(self):
        self._screen: screen_type = [[] for _ in range(self._console.height)]

    def collect(self, element: Element):
        """Add an Element to a `line` in `_screen`.

        For every line of an elements representation, insert it into the right spot of the line.
        Contains logic to handle single/multiprocessing.
        """

        for i, rep in enumerate(element.representation):

            obj: ObjDict = {"pos": element.x_abs,
                            "rep": rep,
                            "format": (element.bold, element.italic, element.strike_through),
                            "color": element.display_rgb}
            index = element.y_abs+i
            line = self._screen[index]

            '''
            if self._processor:
                # for multiprocessing
                self._processor.queue.put((obj, index))
            else:'''
            self._precomp.to_screen(index, obj, line)
