import mmap
import ecigen
import math
#
def generate_mmap(lmda, kappa, n, rho, etap):
	pp = mmap.public_parameters_generate(lmda, kappa, n, rho, etap)
	pp.generate(False)
	#
	return pp
#
def format_key_string(key, bit_length):
	sign_bit = (key[0] == '-')
	if sign_bit:
		key = key[1:]
	#
	key = str(int(sign_bit))+key
	return key.zfill(bit_length)
#
def encrypt(lmda, n, T, pp):
	a = []
	#
	for i in range(n):
		samp = mmap.encoding()
		samp.samp(pp, 0)
		a.append(samp)
	#
	C = []
	#
	
	
	a_prime = []
	#
	for j in range(n):
		samp = mmap.encoding()
		samp.set_to(a[j])
		samp = pp.enc(samp, 1)
		#samp.rerand()
		a_prime.append(samp)
	#
	
	
	
	
	for i in range(len(T)):
		#
		'''
		a_prime = []
		#
		for j in range(n):
			samp = mmap.encoding()
			samp.set_to(a[j])
			samp = pp.enc(samp, 1)
			samp.rerand()
			a_prime.append(samp)
		#
		'''
		#
		
		for j in range(len(a_prime)):
			a_prime[j].rerand()
		
		
		#
		product = mmap.encoding()
		product.set_to(a_prime[T[i][0]])
		for j in range(1, len(T[i])):
			'''
			print(j)
			print(j)
			print(len(T))
			print(T[i])
			print(len(T[i]))
			print(T[i][j])
			print(len(a_prime))
			print('--------')
			'''
			product.mult_in_place(a_prime[T[i][j]])
		#
		encoded = pp.enc(product, len(T[i]))
		C.append(encoded)
	#
	product = mmap.encoding()
	product.set_to(a[0])
	#
	for i in range(1, n):
		product.mult_in_place(a[i])
	#
	encoding = pp.enc(product, n)
	K = pp.ext_as_str(encoding, 0)
	K = format_key_string(K, lmda)
	#
	return (K, C)
#
def decrypt(lmda, n, C, pp, W):
	B = mmap.encoding()
	B.set_to(C[W[0]])
	#
	for i in range(1, len(W)):
		B.mult_in_place(C[W[i]])
	#
	K_recovered = pp.ext_as_str(B, 0)
	K_recovered = format_key_string(K_recovered, lmda)
	#
	return K_recovered
#
if __name__ == '__main__':
	#
	# FIX KEY LENGTH sometimes 201
	#
	lmda = 200
	n = 44
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
	pp = generate_mmap(lmda_mlm, kappa_mlm, n_mlm, rho_mlm, etap_mlm)
	#
	print('----------------------')
	#
	(K, C) = encrypt(lmda, n, T, pp)
	#
	print('K (first 20 bits): {0}...'.format(K[0:20]))
	print('K length: {0}'.format(len(K)))
	print('Num of 1 bits: {0}'.format(K.count('1')))
	#
	print('----------------------')
	#
	K_recovered = decrypt(lmda, n, C, pp, W)
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
#
