from __future__ import annotations
from xmlrpc.client import boolean

from ..entity import Entity, StructureError
from ..elements import Element


class Container(Entity):
    """simple container class with child/parent logic"""

    def __init__(self, parent: Container | None = None,
                 x: int = 0, y: int = 0, width: int = 1, height: int = 1,
                 overlap: bool = False):
        self._children: list[Entity] = []
        self._overlap = overlap
        super().__init__(parent, x, y, width, height)

    # ----- make dimension setter public -----

    @Entity.width.setter
    def width(self, width: int) -> int | None:
        if self.parent and hasattr(self, 'x'):
            if self.parent.width < self.x + width:
                raise StructureError('edge conflict')
        self._width = width
        self._overlap_check()

    @Entity.height.setter
    def height(self, height: int) -> int | None:
        if self.parent and hasattr(self, 'y'):
            if self.parent.height < self.y + height:
                raise StructureError('edge conflict')
        self._height = height
        self._overlap_check()

    @Entity.dimensions.setter
    def dimensions(self, cords: tuple[int, int]):
        self._width = cords[0]
        self._height = cords[1]

    # ----- properties -----

    @property
    def children(self) -> list[Entity]:
        return self._children

    @property
    def overlap(self) -> boolean:
        return self._overlap

    # ----- child logic -----

    def _collect_children(self) -> list[Element]:
        result: list[Element] = []

        for child in self._children:
            if isinstance(child, Container):
                result.extend(child._collect_children())
            else:
                if isinstance(child, Element):
                    result.append(child)
        return result

    def add_child(self, child: Entity, replace: bool = False):
        self._overlap_check()
        if child._parent and not replace:
            raise StructureError('parent double')
        self._children.append(child)
        child._parent = self

    def remove_child(self, child: Entity):
        if child not in self._children:
            raise StructureError('child not found')
        self._children.remove(child)
        child._parent = None

    # ----- parent logic -----

    def set_parent(self, parent: Container | None = None, replace: bool = False):
        if parent in self._children and not replace:
            raise StructureError('incest')

        if parent in self._children:
            self._children.remove(parent)
        if parent:
            if parent._parent == self:
                parent._parent = None
            self._parent = parent
            parent._children.append(self)
