from __future__ import annotations

from conutils.entity.entity import Entity, StructureError


class Container(Entity):
    """simple container class with child/parent logic"""

    def __init__(self, parent: Container | None = None, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        # initialize object
        self.children = []
        super().__init__(parent, x, y, width, height)

    def add_child(self, child, replace=False):
        if child._parent and not replace:
            raise StructureError('parent double')
        self.children.append(child)
        child._parent = self

    def remove_child(self, child):
        if child not in self.children:
            raise StructureError('child not found')
        self.children.remove(child)
        child._parent = None

    def set_parent(self, parent: Container | None = None, replace=False):
        if parent in self.children and not replace:
            raise StructureError('incest')

        if parent in self.children:
            self.children.remove(parent)
        if parent:
            if parent._parent == self:
                parent._parent = None
            self._parent = parent
            parent.children.append(self)

    def get_parent(self):
        return self._parent
