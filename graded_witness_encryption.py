def _format_key_string(key, bit_length):
	sign_bit = (key[0] == '-')
	if sign_bit:
		key = key[1:]
	#
	key = str(int(sign_bit))+key
	return key.zfill(bit_length)
#
def encrypt(mmap_instance, T):
	n = mmap_instance.get_n()
	lmda = mmap_instance.get_lambda()
	#
	a = [mmap_instance.sample() for x in range(n)]
	a_prime = [mmap_instance.encode(1, a[x]) for x in range(n)]
	ciphertext = []
	#
	for i in range(len(T)):
		for j in range(len(a_prime)):
			mmap_instance.rerandomize(1, a_prime[j])
		#
		this_T = T[i]
		#
		product = mmap_instance.copy_encoding(a_prime[this_T[0]])
		for j in range(1, len(this_T)):
			mmap_instance.multiply(product, a_prime[this_T[j]], store_in=product)
		#
		encoded = mmap_instance.encode(len(this_T), product)
		ciphertext.append(encoded)
	#
	product = mmap_instance.copy_encoding(a_prime[0])
	for i in range(1, n):
		mmap_instance.multiply(product, a_prime[i], store_in=product)
	#
	encoding = mmap_instance.encode(n, product)
	key = mmap_instance.extract(encoding)
	key = _format_key_string(key, lmda)
	#
	return (key, ciphertext)
#
def decrypt(mmap_instance, ciphertext, W):
	lmda = mmap_instance.get_lambda()
	#
	B = mmap_instance.copy_encoding(ciphertext[W[0]])
	for i in range(1, len(W)):
		mmap_instance.multiply(B, ciphertext[W[i]], store_in=B)
	#
	key_recovered = mmap_instance.extract(B)
	key_recovered = _format_key_string(key_recovered, lmda)
	#
	return key_recovered
#
