from typing import TypedDict


class ObjDict(TypedDict):
    pos: int
    rep: str
    format: tuple[bool, bool, bool]
    color: tuple[int, int, int] | None


line_type = list[ObjDict]
frame_type = list[line_type]
