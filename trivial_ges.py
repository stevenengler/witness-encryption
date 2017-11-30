from graded_witness_encryption import GradedEncodingSchemeBase
from random import *
import copy
import pickle

class TrivialGES(GradedEncodingSchemeBase):
    def __init__(self, l, n):
        self.l = l
        self.n = n

    def get_n(self):
        return self.n

    def get_lambda(self):
        return self.l

    def copy_encoding(self, value):
        return copy.deepcopy(value)

    def sample(self):
        return [0, randint(1, self.n)]

    def encode(self, level, value):
        return [level, value[1]]

    def rerandomize(self, level, value):
        value[0] = level

    def multiply(self, a, b, store_in=None):
        if store_in is None:
            store_in = [0,0]
        store_in[0] = a[0]+b[0]
        store_in[1] = a[1]*b[1]
        return store_in

    def extract(self, value):
        b = pickle.dumps(value)
        if len(b) < self.l:
            b = bytes([0])*(self.l - len(b)) + b
        return b

