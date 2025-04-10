from __future__ import annotations

from conutils.entity.elements.element import Element
from conutils.entity.entity import Entity, StructureError


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
    def width(self, width: int):
        if self._parent and hasattr(self, '_x'):
            if self._parent.width < self._x + width:
                raise StructureError('edge conflict')
        self._width = width

    @Entity.height.setter
    def height(self, height: int):
        if self._parent and hasattr(self, '_y'):
            if self._parent.height < self._y + height:
                raise StructureError('edge conflict')
        self._height = height

    @Entity.dimensions.setter
    def dimensions(self, width: int, height: int):
        self.width = width
        self.heigth = height

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

    def _overlap_check(self, add_child: Entity):

        r1_x = range(
            add_child._x, add_child._x+add_child._width)
        r1_y = range(
            add_child._y, add_child._y+add_child._height)

        for child in self._children:
            r2_x = range(
                child._x, child._x+child._width)
            r2_y = range(
                child._y, child._y+child._height)

            if not self._overlap\
                    and r1_x.start < r2_x.stop and r2_x.start < r1_x.stop\
                    and r1_y.start < r2_y.stop and r2_y.start < r1_y.stop:
                raise StructureError('child overlap')

    def add_child(self, child: Entity, replace: bool = False):
        self._overlap_check(child)
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
