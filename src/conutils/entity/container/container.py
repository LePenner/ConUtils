from __future__ import annotations

from conutils.entity.entity import Entity, StructureError


class Container(Entity):
    """ simple container class with child/parent logic"""

    def __init__(self, parent: Container | None = None, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        # initialize object
        self.children = []
        super().__init__(parent, x, y, width, height)
        self.name = [k for k, v in globals().items() if v is self]

        # perform checks

    def add_child(self, child, replace=False):
        if child.parent and not replace:
            raise StructureError('parent double')
        self.children.append(child)
        child.parent = self

    def remove_child(self, child):
        if child not in self.children:
            raise StructureError('child not found')
        self.children.remove(child)
        child.parent = None
