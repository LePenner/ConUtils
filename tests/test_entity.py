import unittest
from conutils._internals.entity.entity import Entity
from conutils import Container, Color
from conutils._internals.errors.errors import ConUtils_error


class TestEntity(unittest.TestCase):

    def test_default(self):

        ent = Entity()

        expected: list[None | int | bool] = [
            None, 0, 0, 1, 1, False, False, False, None]

        actual: list[Container | int | bool | str | None] = [ent.parent, ent.x, ent.y, ent.width, ent.height,
                                                             ent.bold, ent.italic, ent.strike_through, ent.color]

        self.assertEqual(expected, actual)

    def test_custom(self):

        container = Container(width=10, height=10)
        ent = Entity(parent=container, x=2, y=4, width=2, height=3, bold=True,
                     italic=True, strike_through=True, color="green")

        expected: list[None | int | bool | str] = [
            2, 4, 2, 3, True, True, True, "green"]

        actual: list[int | bool | str | None | Container] = [ent.x, ent.y, ent.width, ent.height,
                                                             ent.bold, ent.italic, ent.strike_through, ent.color]

        self.assertEqual(expected, actual)
        self.assertIsInstance(ent.parent, Container)

    def test_attr_parent(self):
        ent = Entity()

        container = Container()
        ent.parent = container
        self.assertIsInstance(ent.parent, Container)

    def test_attr_pos(self):
        container = Container(x=2, y=3, width=10, height=10)
        ent = Entity(parent=container)

        ent.x = 5
        ent.y = 6
        self.assertEqual(ent.x, 5)
        self.assertEqual(ent.y, 6)
        self.assertEqual(ent.x_abs, 5 + container.x)
        self.assertEqual(ent.y_abs, 6 + container.y)
        self.assertEqual(ent.pos, (5, 6))
        self.assertEqual(ent.abs_pos, (5 + container.x, 6 + container.y))

    def test_attr_form(self):
        ent = Entity()

        form: list[str] = ["bold", "italic", "strike_through"]
        for attribute in form:
            with self.subTest(attribute=attribute):
                setattr(ent, attribute, True)
                self.assertEqual(getattr(ent, attribute), True)

    def test_attr_color(self):
        container = Container(width=10, height=10, color=(30, 30, 30))
        ent = Entity(parent=container)
        self.assertEqual(ent.display_rgb, (30, 30, 30))

        ent.color = (40, 40, 40)
        self.assertIsNone(ent.color)
        self.assertEqual(ent.rgb, (40, 40, 40))
        self.assertEqual(ent.display_rgb, (40, 40, 40))

        Color.add_color("test color", (1, 2, 3))
        ent.color = "test color"

        # edge case testing
        neg_edgecases: list[tuple[int, int, int]] = [(256, 0, 0),
                                                     (0, 256, 0),
                                                     (0, 0, 256),
                                                     (-1, 0, 0),
                                                     (0, -1, 0),
                                                     (0, 0, -1)]

        pos_edgecases: list[tuple[int, int, int]] = [(255, 0, 0),
                                                     (0, 255, 0),
                                                     (0, 0, 255),
                                                     (0, 0, 0)]

        for case in neg_edgecases:
            with self.subTest(case):
                with self.assertRaises(ConUtils_error):
                    ent.color = case

        for case in pos_edgecases:
            with self.subTest(case):
                ent.color = case

    def test_attr_read_only(self):
        ent = Entity()

        read_only: list[str] = ["x_abs",
                                "y_abs",
                                "abs_pos",
                                "height",
                                "width",
                                "dimensions",
                                "rgb",
                                "display_rgb"]

        for attribute in read_only:
            with self.subTest(attribute=attribute):
                with self.assertRaises(AttributeError, msg=f"on {attribute}"):
                    setattr(ent, attribute, 3)
