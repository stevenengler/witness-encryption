import graded_witness_encryption
from random import *
import copy
import pickle

class TrivialGES(graded_witness_encryption.GradedEncodingSchemeBase):
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
        return str(b)

if __name__=='__main__':
    import ecigen
    import math
    #
    lmda = 400
    n = 200
    #
    #T = [[0,2,4], [0,1], [3,5], [2], [1]]
    #W = [0, 2, 4]
    #
    T, W = ecigen.generate(n, math.ceil(n/2), n*3)
    T = [[y-1 for y in x] for x in T]
    #
    print('----------------------')
    #
    pp = TrivialGES(lmda, n)
    #
    print('----------------------')
    #
    (K, C) = graded_witness_encryption.encrypt(pp, T)
    #
    print('K (first 20 bits): {0}...'.format(K[0:20]))
    print('K length: {0}'.format(len(K)))
    print('Num of 1 bits: {0}'.format(K.count('1')))
    #
    print('----------------------')
    #
    K_recovered = graded_witness_encryption.decrypt(pp, C, W)
    #
    print('K_recovered (first 20 bits): {0}...'.format(K_recovered[0:20]))
    print('K_recovered length: {0}'.format(len(K_recovered)))
    print('Num of 1 bits: {0}'.format(K_recovered.count('1')))
    #
    print('----------------------')
    #
    print('Keys are the same?: {0}'.format(K_recovered == K))
    #
    print('----------------------')
    print()
