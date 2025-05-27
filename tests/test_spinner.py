import unittest
import os
from conutils._internals.entity.elements.spinner import Spinner, FormatError, DivisionError, SpinnerTypeError


class TestSpinner(unittest.TestCase):

    def test_wrong_initialization(self):
        self.assertRaises(SpinnerTypeError, Spinner, "wrong type")

    def test_default_spinner(self):
        spn = Spinner()
        self.assertEqual(spn.seq, '|/-\\')
        self.assertEqual(spn.div, 1)

    def test_spn_change(self):
        Spinner.reg_spn_type("test spnr", ".oOo", 1)
        spn = Spinner()
        self.assertEqual(spn.spinner, ("|/-\\", 1))
        spn.change_spn_to("test spnr")
        self.assertEqual(spn.spinner, (".oOo", 1))

    def test_custom_spinner(self):

        # reg test spinner
        Spinner.reg_spn_type("test type", "test", 1, False)
        self.assertEqual(Spinner.get_spinners()["test type"], {
                         'seq': 'test', 'div': 1})

        # try overwriting spinner with overwrite set to false
        self.assertRaises(SpinnerTypeError, Spinner.reg_spn_type,
                          "test type", "overwrite", 1, False)

        # overwrite set to true
        Spinner.reg_spn_type("test type", "second overwrite", 1, True)

    def test_load_spinners(self):

        PATH = os.path.dirname(__file__)

        Spinner.load_json(PATH+"/json/spinners_1.json")
        self.assertEqual(Spinner.get_spinners()[
                         "default"], {'seq':  '|/-\\', 'div': 1})
        Spinner.load_json(PATH +
                          "/json/spinners_1.json", replace=True)
        self.assertNotEqual(Spinner.get_spinners()[
            "default"], {'seq':  '|/-\\', 'div': 1})

        Spinner.reset_spinners()

        # test for div andseq type
        self.assertRaises(FormatError, Spinner.load_json,
                          PATH+"/json/spinners_2.json")

        # test for keys
        self.assertRaises(FormatError, Spinner.load_json,
                          PATH+"/json/spinners_3.json")

        # test for division
        self.assertRaises(DivisionError, Spinner.load_json,
                          PATH+"/json/spinners_4.json")
