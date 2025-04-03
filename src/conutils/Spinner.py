import json

class Spinner():
    def __init__(self, spn_type = str):
        if spn_type not in Spinner.spinners:
            raise Exception('Invalid spinner type')

        self.spn_type = spn_type
        self.seq = Spinner.spinners[spn_type]["seq"]
        self.div = Spinner.spinners[spn_type]["div"]
        self.seq_list = Spinner._generate_sequence_list(self)

    
    spinners = {"default" : {"seq" : '|/-\\',
                             "div" : 1}}
 
    @classmethod
    def reg_spn(cls, name = str, seq = str, div = int):
        if name in cls.spinners:
            raise Exception('This type of spinner already exists, please choose another name')
        elif len(seq) % div != 0:
            raise Exception('Sequence needs to be divisible by divider')
        
        cls.spinners[name] = {"seq" : seq, 
                              "div" : div }
    
    """json format as follows: {<spinner_name> : {"seq" : <str>, "div" : <int>}}"""
    @classmethod
    def load_json(cls, file_ = str, replace = False):
        with open(file_) as json_file:
            loaded_file = json.load(json_file)

        # format check
        for spinner in loaded_file.items():
            # get dict as tuple out of tuple
            # e = (key, value)
            for e in spinner[1].items():
                match e[0]: 
                    case "seq":
                        if type(e[1]) != str:
                            raise JsonFromatError('seq', spinner[0])
                    case "div":
                        if type(e[1]) != int:
                            raise JsonFromatError('div', spinner[0])
                    case _:
                        raise JsonFromatError('keys', spinner[0])
        
        # if format is correct
        # -- code goes here --
   
    def change_spn_to(self, spn_type = str):
        if spn_type not in Spinner.spinners:
            raise Exception('Invalid spinner type')
        
        self.spn_type = spn_type
        self.seq = Spinner.spinners[spn_type]["seq"]
        self.div = Spinner.spinners[spn_type]["div"]
        self.seq_list = Spinner._generate_sequence_list(self)


    def _generate_sequence_list(self):
        return [self.seq[i:i+self.div] for i in range(0, len(self.seq), self.div)]


class JsonFromatError(Exception):
    def __init__(self, key, element):
        messages = { 'seq' : 'value error for "seq" expected str',
                     'div' : 'value error for "div" expected int',
                     'key' : 'key error'}
        
        if key in messages:
            self.message = messages[key]
        else:
            self.message = 'unknown error'

        super().__init__('Invalid json format\n  ' + self.message + f' on: {element}\n')


        
spn = Spinner("default")

Spinner.load_json("test.json")
