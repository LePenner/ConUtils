from typing import TypedDict


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
