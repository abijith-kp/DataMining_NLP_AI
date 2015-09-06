import os

NEG = "neg"
POS = "pos"

class IMDB_DS:
    def __init__(self, path):
        self.dataset_path = path
        self.negative = None
        self.positive = None
        self.bow = { NEG: None,
                     POS: None }

    # return the neagtive dataset in the path
    # as a list
    def neg(self):
        if self.negative != None:
            return self.negative

        p = os.path.join(self.dataset_path, NEG)
        file_list = os.listdir(p)
        result = []
        for fl in file_list:
            rate = fl.split(".")[0].split("_")[1]
            with open(os.path.join(p, fl)) as f:
                result.append([f.read(), rate])

        self.negative = result
        return result

    # return the positive dataset in the path
    # as a list
    def pos(self):
        if self.positive != None:
            return self.positive

        p = os.path.join(self.dataset_path, POS)
        file_list = os.listdir(p)
        result = []
        for fl in file_list:
            rate = fl.split(".")[0].split("_")[1]
            with open(os.path.join(p, fl)) as f:
                result.append([f.read(), rate])

        self.positive = result
        return result

    def get_BOW(self, polarity):
        if self.bow[polarity] != None:
            return self.bow[polarity]

        if polarity == NEG:
            dataset = self.neg()
        elif polarity == POS:
            dataset = self.pos()
        else:
            print "Invalid value.\n"
            return

        bow = list()
        for (c, r) in dataset:
            bow.extend(c.lower().split())

        self.bow[polarity] = bow
        return bow
