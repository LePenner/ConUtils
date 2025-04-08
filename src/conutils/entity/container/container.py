from __future__ import annotations

from conutils.entity.entity import Entity, StructureError


class Container(Entity):
    """simple container class with child/parent logic"""

    def __init__(self, parent: Container | None = None, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        self._children = []
        super().__init__(parent, x, y, width, height)

    def add_child(self, child, replace=False):
        if child._parent and not replace:
            raise StructureError('parent double')
        self._children.append(child)
        child._parent = self

    def remove_child(self, child):
        if child not in self._children:
            raise StructureError('child not found')
        self._children.remove(child)
        child._parent = None

    def set_parent(self, parent: Container | None = None, replace=False):
        if parent in self._children and not replace:
            raise StructureError('incest')

        if parent in self._children:
            self._children.remove(parent)
        if parent:
            if parent._parent == self:
                parent._parent = None
            self._parent = parent
            parent._children.append(self)

    def get_parent(self):
        return self._parent
