class Spinner():
    def __init__(self, spn_type):
        if spn_type not in Spinner.spinners:
            raise Exception('Invalid spinner type')

        self.spn_type = spn_type
        self.seq = Spinner.spinners[spn_type]["seq"]
        self.div = Spinner.spinners[spn_type]["div"]
        self.seq_list = Spinner._generate_sequence_list(self)

    

    spinners = {"default" : {"seq" : '|/-\\',
                             "div" : 1}}
 
    @classmethod
    def reg_spn(cls, name, seq, div):
        if name in cls.spinners:
            raise Exception('This type of spinner already exists, please choose another name')
        elif len(seq) % div != 0:
            raise Exception('Sequence needs to be divisible by divider')
        
        cls.spinners[name] = {"seq" : seq, 
                              "div" : div }
        

    def change_spn_to(self, spn_type):
        if spn_type not in Spinner.spinners:
            raise Exception('Invalid spinner type')
        
        self.spn_type = spn_type
        self.seq = Spinner.spinners[spn_type]["seq"]
        self.div = Spinner.spinners[spn_type]["div"]
        self.seq_list = Spinner._generate_sequence_list(self)


    def _generate_sequence_list(self):
        return [self.seq[i:i+self.div] for i in range(0, len(self.seq), self.div)]
    def load_json(self):
        pass