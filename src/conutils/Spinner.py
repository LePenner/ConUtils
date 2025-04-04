import json

class Spinner():
    def __init__(self, spn_type = 'default'):
        """specify a type of spinner to initiate, loads it from dict: spinners
        if no type is specified 'default' type is used
        """
        if spn_type not in Spinner._spinners:
            raise SpinnerTypeError('msng_type', spn_type)

        self.spn_type = spn_type
        self.seq = Spinner._spinners[spn_type]["seq"]
        self.div = Spinner._spinners[spn_type]["div"]
        self.seq_list = self._generate_sequence_list()

    _default_spinner = {"seq" : '|/-\\',
                        "div" : 1}
    _spinners = {"default" : _default_spinner.copy()}


    @classmethod
    def get_spinners(cls):
        return cls._spinners.copy()

    @classmethod
    def reg_spn_type(cls, spn_type: str, seq: str, div: int, replace=False):
        if spn_type in cls._spinners and not replace:
            raise SpinnerTypeError('dupl_type', spn_type)
        elif len(seq) % div != 0:
            raise DivisionError(spn_type)
        
        cls._spinners[spn_type] = {"seq" : seq, 
                                  "div" : div }
    
    @classmethod
    def del_spn_type(cls, spn_type: str):
        if spn_type not in cls._spinners:
            raise SpinnerTypeError('msng_type', spn_type)
        
        if spn_type == "default":
            cls._spinners["default"] = cls._default_spinner.copy()
        else:
            del cls._spinners[spn_type]

    @classmethod
    def load_json(cls, file: str, replace = False):
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
            cls.reg_spn_type(spinner, values["seq"], values["div"], replace=True)

    def change_spn_to(self, spn_type: str):
        if spn_type not in Spinner._spinners:
            raise SpinnerTypeError('msng_type', spn_type)

        self.spn_type = spn_type
        self.seq = Spinner._spinners[spn_type]["seq"]
        self.div = Spinner._spinners[spn_type]["div"]
        self.seq_list = Spinner._generate_sequence_list(self)

    def _generate_sequence_list(self):
        return [self.seq[i:i+self.div] for i in range(0, len(self.seq), self.div)]


class SpinnerTypeError(Exception):
    def __init__(self, key, element):
        messages = { 'msng_type' : 'type does not exist',
                     'dupl_type' : 'type already exists, consider: replace=True'}

        if key in messages:
            message = messages[key]
        else:
            message = 'unknown error'

        super().__init__(f'Invalid spinner type\n  ' + message + f'\non: {element}\n')

class FormatError(Exception):
    def __init__(self, key, element):
        messages = { 'seq'  : 'value error for "seq" expected str',
                     'div'  : 'value error for "div" expected int',
                     'keys' : 'key error'}

        if key in messages:
            message = messages[key]
        else:
            message = 'unknown error'

        super().__init__(f'invalid JSON format\n  ' + message + f'\non: {element}\n')

class DivisionError(Exception):
    def __init__(self, element):
        super().__init__(f'\n  sequence needs to be divisible by divider\non: {element}')

Spinner.load_json("src/conutils/test.json")