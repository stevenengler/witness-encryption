import abc
#
class GradedEncodingSchemeBase(abc.ABC):
	@abc.abstractmethod
	def get_n(self):
		pass
	#
	@abc.abstractmethod
	def get_lambda(self):
		pass
	#
	@abc.abstractmethod
	def copy_encoding(self, value):
		pass
	#
	@abc.abstractmethod
	def sample(self):
		pass
	#
	@abc.abstractmethod
	def encode(self, level, value):
		pass
	#
	@abc.abstractmethod
	def rerandomize(self, level, value):
		pass
	#
	@abc.abstractmethod
	def multiply(self, a, b, store_in=None):
		pass
	#
	@abc.abstractmethod
	def extract(self, value):
		pass
	#
#
def _format_key_string(key, bit_length):
	sign_bit = (key[0] == '-')
	if sign_bit:
		key = key[1:]
	#
	key = str(int(sign_bit))+key
	return key.zfill(bit_length)
#
def encrypt(mmap_instance, exact_cover_collection):
	'''
	The mmap instance should be a subclass of the abstract base class 'GradedEncodingSchemeBase'.
	'''
	#
	n = mmap_instance.get_n()
	lmda = mmap_instance.get_lambda()
	#
	a = [mmap_instance.sample() for x in range(n)]
	a_prime = [mmap_instance.encode(1, a[x]) for x in range(n)]
	ciphertext = []
	#
	for exact_cover_subset in exact_cover_collection:
		for x in a_prime:
			mmap_instance.rerandomize(1, x)
		#
		product = mmap_instance.copy_encoding(a_prime[exact_cover_subset[0]])
		for x in exact_cover_subset[1:]:
			mmap_instance.multiply(product, a_prime[x], store_in=product)
		#
		encoded = mmap_instance.encode(len(exact_cover_subset), product)
		ciphertext.append(encoded)
	#
	product = mmap_instance.copy_encoding(a_prime[0])
	for x in a_prime[1:]:
		mmap_instance.multiply(product, x, store_in=product)
	#
	encoding = mmap_instance.encode(n, product)
	key = mmap_instance.extract(encoding)
	key = _format_key_string(key, lmda)
	#
	return (key, ciphertext)
#
def decrypt(mmap_instance, ciphertext, witness):
	'''
	The mmap instance should be a subclass of the abstract base class 'GradedEncodingSchemeBase'.
	'''
	#
	lmda = mmap_instance.get_lambda()
	#
	product = mmap_instance.copy_encoding(ciphertext[witness[0]])
	for x in witness[1:]:
		mmap_instance.multiply(product, ciphertext[x], store_in=product)
	#
	key_recovered = mmap_instance.extract(product)
	key_recovered = _format_key_string(key_recovered, lmda)
	#
	return key_recovered
#
