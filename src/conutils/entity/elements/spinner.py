from __future__ import annotations
from typing import TYPE_CHECKING
import json
from conutils.entity.entity import Entity
from conutils.entity.elements.animated import Animated

if TYPE_CHECKING:
    from conutils.entity.container.container import Container


class Spinner(Entity, Animated):
    """Spinner class can be used as standalone or in conjunction with a container"""

    def __init__(self, parent: Container | None = None, spn_type: str = 'default', x: int = 0, y: int = 0, frametime: int = 1000):
        """specify a type of spinner to initiate, loads it from dict: spinners
        if no type is specified 'default' type is used
        """
        if spn_type not in Spinner._spinners:
            raise SpinnerTypeError('msng_type', spn_type)

        self._spn_type = spn_type
        self._seq = Spinner._spinners[spn_type]["seq"]
        self._div = Spinner._spinners[spn_type]["div"]
        self._spn_pos = 0

        super().__init__(parent=parent, x=x, y=y,
                         width=self._div, height=1, frames=self._generate_frames(), frametime=frametime)

    _default_spinner = {"seq": '|/-\\',
                        "div": 1}
    _spinners = {"default": _default_spinner.copy()}

    @classmethod
    def get_spinners(cls):
        return cls._spinners.copy()

    @classmethod
    def reg_spn_type(cls, spn_type: str, seq: str, div: int, replace=False):
        if spn_type in cls._spinners and not replace:
            raise SpinnerTypeError('dupl_type', spn_type)
        elif len(seq) % div != 0:
            raise DivisionError(spn_type)

        cls._spinners[spn_type] = {"seq": seq,
                                   "div": div}

    @classmethod
    def del_spn_type(cls, spn_type: str):
        if spn_type not in cls._spinners:
            raise SpinnerTypeError('msng_type', spn_type)

        if spn_type == "default":
            cls._spinners["default"] = cls._default_spinner.copy()
        else:
            del cls._spinners[spn_type]

    @classmethod
    def reset_spinners(cls):
        cls._spinners = {"default": cls._default_spinner.copy()}

    @classmethod
    def load_json(cls, file: str, replace=False):
        """json file format as follows: {spinner_name : {"seq" : str, "div" : int}}

        replace toggles between keeping an already existing spinner or overwriting it.

        if json file contains duplicate keys only the last defined structure will be loaded
        custom json read functionality needed
        """
        with open(file) as json_file:
            loaded_file = json.load(json_file)

        # format check
        for spinner, element_dict in loaded_file.items():
            if "seq" in element_dict and "div" in element_dict:
                if not isinstance(element_dict["seq"], str):
                    raise FormatError('seq', spinner)
                elif not isinstance(element_dict["div"], int):
                    raise FormatError('div', spinner)
            else:
                raise FormatError('keys', spinner)

        # if format is correct
        for spinner, values in loaded_file.items():
            if spinner in cls._spinners and not replace:
                continue  # skip duplicates
            cls.reg_spn_type(
                spinner, values["seq"], values["div"], replace=True)

    def change_spn_to(self, spn_type: str):
        if spn_type not in Spinner._spinners:
            raise SpinnerTypeError('msng_type', spn_type)

        self._spn_type = spn_type
        self._seq = Spinner._spinners[spn_type]["seq"]
        self._div = Spinner._spinners[spn_type]["div"]
        self._frames = Spinner._generate_frames(self)

    def _generate_frames(self):
        return [self._seq[i:i+self._div] for i in range(0, len(self._seq), self._div)]


class SpinnerTypeError(Exception):
    def __init__(self, key, element):
        messages = {'msng_type': 'type does not exist',
                    'dupl_type': 'type already exists, consider: replace=True'}

        if key in messages:
            message = messages[key]
        else:
            message = 'unknown error'

        super().__init__(f'Invalid spinner type\n  ' +
                         message + f'\non: {element}\n')


class FormatError(Exception):
    def __init__(self, key, element):
        messages = {'seq': 'value error for "seq" expected str',
                    'div': 'value error for "div" expected int',
                    'keys': 'key error'}

        if key in messages:
            message = messages[key]
        else:
            message = 'unknown error'

        super().__init__(f'invalid JSON format\n  ' +
                         message + f'\non: {element}\n')


class DivisionError(Exception):
    def __init__(self, element):
        super().__init__(
            f'\n  sequence needs to be divisible by divider\non: {element}')
