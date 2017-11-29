import mmap as mmap_lib
# be careful here, mmap is already a built-in Python library name
import graded_witness_encryption
#
class NewMultilinearMap:
	def __init__(self, lmda, kappa, n, rho, etap):
		self.mmap = mmap_lib.public_parameters_generate(lmda, kappa, n, rho, etap)
		self.mmap.generate(False)
	#
	def get_n(self):
		return self.mmap.params.n
	#
	def get_lambda(self):
		return self.mmap.params._lambda
	#
	def copy_encoding(self, value):
		return mmap_lib.encoding(value)
	#
	def sample(self):
		samp = mmap_lib.encoding()
		samp.samp(self.mmap, 0)
		return samp
	#
	def encode(self, level, value):
		return self.mmap.enc(value, level)
	#
	def rerandomize(self, level, value):
		assert(level == 1)
		value.rerand()
	#
	def multiply(self, a, b, store_in=None):
		if store_in is None:
			store_in = mmap_lib.encoding()
		#
		store_in.set_to(a)
		store_in.mult_in_place(b)
		return store_in
	#
	def extract(self, value):
		return self.mmap.ext_as_str(value, 0)
	#
#
if __name__=='__main__':
	import ecigen
	import math
	#
	lmda = 200
	n = 10
	#
	lmda_mlm = lmda
	n_mlm = 10
	kappa_mlm = n
	rho_mlm = 52
	etap_mlm = 420
	#
	#T = [[0,2,4], [0,1], [3,5], [2], [1]]
	#W = [0, 2, 4]
	#
	T, W = ecigen.generate(n, math.ceil(n/2), n*3)
	T = [[y-1 for y in x] for x in T]
	#
	print('----------------------')
	#
	pp = NewMultilinearMap(lmda_mlm, kappa_mlm, n_mlm, rho_mlm, etap_mlm)
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
