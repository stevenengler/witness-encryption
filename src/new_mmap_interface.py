import newmultimaps
import graded_witness_encryption
#
class NewMultilinearMap(graded_witness_encryption.GradedEncodingSchemeBase):
	def __init__(self, lmda, kappa, n, rho, etap):
		self.mmap = newmultimaps.public_parameters_generate(lmda, kappa, n, rho, etap)
		self.mmap.generate(False)
	#
	def get_n(self):
		return self.mmap.params.n
	#
	def get_lambda(self):
		return self.mmap.params._lambda
	#
	def copy_encoding(self, value):
		return newmultimaps.encoding(value)
	#
	def sample(self):
		samp = newmultimaps.encoding()
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
		store_in.assign(a)
		store_in.multiply_assign(b)
		return store_in
	#
	def extract(self, value):
		return self.mmap.ext_str(value, 0, 2)
	#
#
def get_public_params(pp, base=16):
	"""
	Returns a dictionary of small values (integers) and large
	values (strings).
	"""
	#
	small_values = {}
	small_values['n'] = pp.mmap.params.n
	small_values['rhof'] = pp.mmap.params.rhof
	small_values['eta'] = pp.mmap.params.eta
	small_values['etaq'] = pp.mmap.params.etaq
	small_values['rho'] = pp.mmap.params.rho
	small_values['alpha'] = pp.mmap.params.alpha
	small_values['xi'] = pp.mmap.params.xi
	small_values['beta'] = pp.mmap.params.beta
	small_values['nu'] = pp.mmap.params.nu
	small_values['ne'] = pp.mmap.params.ne
	#
	large_values = {}
	large_values['x0p'] = pp.mmap.get_str_x0p(base)
	large_values['x'] = pp.mmap.get_str_x(base)
	large_values['pi0'] = pp.mmap.get_str_pi0(base)
	large_values['pi1'] = pp.mmap.get_str_pi1(base)
	large_values['y'] = pp.mmap.get_str_y(base)
	large_values['N'] = pp.mmap.get_str_N(base)
	large_values['yp'] = pp.mmap.get_str_yp(base)
	large_values['p_zt'] = pp.mmap.get_str_p_zt(base)
	#
	for x in large_values:
		large_values[x] = {'data':large_values[x], 'base':base}
	#
	return {'small_values':small_values, 'large_values':large_values}
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
