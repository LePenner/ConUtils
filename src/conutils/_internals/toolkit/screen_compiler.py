from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from ..entity.elements import Element
    from ..console import Console

#             screen>line>obj(pos, rep, tuple[bold, italic, strike_through], rgb(r,g,b)|None)


class ObjDict(TypedDict):
    pos: int
    rep: str
    format: tuple[bool, bool, bool]
    color: tuple[int, int, int] | None


line_type = list[ObjDict]
screen_type = list[line_type]


class Output:

    def __init__(self, console: Console):

        self.console = console
        self.clear()

    @staticmethod
    def get_color(color: tuple[int, int, int] | None):
        if color:
            r, g, b = color
            return f"\033[38;2;{r};{g};{b}m"
        else:
            return "\033[39;49m"

    @staticmethod
    def binsert_algo(obj: Element, lst: line_type) -> int:
        """Searches for index recursively."""

        x = obj.x_abs
        piv = len(lst)//2

        if len(lst) > 1:

            if x > lst[piv]["pos"]:
                return piv+Output.binsert_algo(obj, lst[piv:])+1
            else:
                return Output.binsert_algo(obj, lst[:piv])
        elif len(lst) == 1:
            if x > lst[piv]["pos"]:
                return 1
            else:
                return 0
        else:
            return 0

    def clear(self):
        self._screen: screen_type = [[] for _ in range(self.console.height)]

    def add(self, element: Element):
        """Add an Element to a line in screen.

        For every line of an elements representation, insert it into the right spot of the line.
        """

        for i, rep in enumerate(element.representation):

            line = self._screen[element.y_abs+i]
            index = self.binsert_algo(element, line)

            line.insert(
                index, {"pos": element.x_abs,
                        "rep": rep,
                        "format": (element.bold, element.italic, element.strike_through),
                        "color": element.display_rgb})

    def compile(self):
        if self.console.overlap == True:
            for i, line in enumerate(self._screen):

                for j, obj in enumerate(line):

                    if j > 0:

                        prev_obj = line[j-1]
                        prev_obj_pos = prev_obj["pos"]
                        prev_obj_width = len(prev_obj["rep"])

                        obj_pos = obj["pos"]
                        obj_width = len(obj["rep"])

                        # check with neighboring objects for overlaps
                        if prev_obj_pos <= obj_pos + obj_width or \
                                prev_obj_pos + prev_obj_width >= obj_pos:

                            to_split = line.pop(j-1)

                            # calculate left split
                            if to_split["pos"] < obj_pos:
                                l_split: ObjDict = {
                                    "pos": to_split["pos"],
                                    "rep": to_split["rep"][:obj_pos - to_split["pos"]],
                                    "format": to_split["format"],
                                    "color": to_split["color"]
                                }
                                line.insert(j-1, l_split)
                                j += 1

                            # calculate right split
                            if to_split["pos"] + len(to_split["rep"]) > obj_pos + obj_width:
                                r_split: ObjDict = {
                                    "pos": obj_pos + obj_width,
                                    "rep": to_split["rep"][(obj_pos + obj_width) - to_split["pos"]:],
                                    "format": to_split["format"],
                                    "color": to_split["color"]
                                }
                                line.insert(j, r_split)

        out = ""
        for i, line in enumerate(self._screen):
            # fill line with spaces if empty
            if len(line) == 0:
                out += " "*self.console.width

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
                    out += Output.get_color(obj["color"])
                else:
                    # reset color
                    out += "\033[39m"

                # add representation
                out += obj["rep"]

                # if last object in line:
                if len(line) == j+1:
                    # fill rest of line with spaces
                    out += " "*(self.console.width -
                                obj["pos"] - len(obj["rep"]))

            # add new line at end of line
            if len(self._screen) != i+1:
                out += "\n"
            # if last line: return to top left
            else:
                out += "\033[u"
        return out
