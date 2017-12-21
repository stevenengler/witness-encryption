import json
import time
import math
#
import mmap_ges
import graded_witness_encryption
import trivial_ges
import ecigen
#
def save_data_newmultimaps(filename, name, pp, arguments, mmap_arguments, T, W, C, K, K_recovered, time_to_generate_map, time_to_encrypt, time_to_decrypt):
	data = {}
	data['name'] = name
	data['public_parameters'] = mmap_ges.get_public_params(pp, 16)
	data['arguments'] = arguments
	data['mmap_arguments'] = mmap_arguments
	data['T'] = T
	data['W'] = W
	data['C'] = [x.get_value_str(16) for x in C]
	data['K'] = K
	data['K_recovered'] = K_recovered
	data['time_to_generate_map'] = time_to_generate_map
	data['time_to_encrypt'] = time_to_encrypt
	data['time_to_decrypt'] = time_to_decrypt
	#
	with open(filename, 'w') as out_file:
		json.dump(data, out_file)
	#
#
def save_data_trivial_ges(filename, name, pp, arguments, mmap_arguments, T, W, C, K, K_recovered, time_to_generate_map, time_to_encrypt, time_to_decrypt):
	data = {}
	data['name'] = name
	data['public_parameters'] = {'n':arguments['n'], 'lbda':arguments['lmda']}
	data['arguments'] = arguments
	data['mmap_arguments'] = mmap_arguments
	data['T'] = T
	data['W'] = W
	data['C'] = C
	data['K'] = K
	data['K_recovered'] = K_recovered
	data['time_to_generate_map'] = time_to_generate_map
	data['time_to_encrypt'] = time_to_encrypt
	data['time_to_decrypt'] = time_to_decrypt
	#
	with open(filename, 'w') as out_file:
		json.dump(data, out_file)
	#
#
def load_experiment(name):
	with open(name) as f:
		return json.load(f)
#
def calc_transfer_data_size_trivial_ges(data):
	size = 0
	#
	# T:
	for x in data['T']:
		for y in x:
			size += 4
		#
	#
	# C:
	for x in data['C']:
		size += 8
	#
	# parameters:
	size += 4*len(data['public_parameters'])
	#
	return size
#
def calc_transfer_data_size_newmultimaps(data):
	size = 0
	#
	# T:
	for x in data['T']:
		for y in x:
			size += 4
		#
	#
	# C:
	for x in data['C']:
		size += math.ceil(len(x)/2)
	#
	# small public parameters (integers):
	size += 4*len(data['public_parameters']['small_values'])
	#
	# large public parameters (strings):
	for x in data['public_parameters']['large_values']:
		if isinstance(x, list):
			for y in x:
				size += math.ceil(len(y)/2)
			#
		else:
			size += math.ceil(len(x)/2)
		#
	#
	return size
#
def run_experiment(name, lmda, n, l, t, mmap_generator, mmap_args, save_data_func):
	T, W = ecigen.generate(n, l, t)
	T = [[y-1 for y in x] for x in T]
	#
	print('*** {} ***'.format(name))
	print('#'*(len(name)+8))
	#
	start_time = time.clock()
	pp = mmap_generator(*mmap_args)
	time_to_generate_map = time.clock()-start_time
	print('time_to_generate_map: {0}'.format(time_to_generate_map))
	#
	print('----------------------')
	#
	start_time = time.clock()
	(K, C) = graded_witness_encryption.encrypt(pp, T)
	time_to_encrypt = time.clock()-start_time
	print('time_to_encrypt: {0}'.format(time_to_encrypt))
	#
	print('K (first 20 bits): {0}...'.format(K[0:20]))
	print('K length: {0}'.format(len(K)))
	print('Num of 1 bits: {0}'.format(K.count('1')))
	#
	print('----------------------')
	#
	start_time = time.clock()
	K_recovered = graded_witness_encryption.decrypt(pp, C, W)
	time_to_decrypt = time.clock()-start_time
	print('time_to_decrypt: {0}'.format(time_to_decrypt))
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
	args = {'lmda':lmda, 'n':n, 'l':l, 't':t}
	save_data_func('results/'+name+'.json', name, pp, args, mmap_args, T, W, C, K, K_recovered, time_to_generate_map, time_to_encrypt, time_to_decrypt)
#
if __name__=='__main__':
	lmda = 52
	n = 20
	#
	lmda_mlm = lmda
	n_mlm = n
	kappa_mlm = n
	rho_mlm = 52
	etap_mlm = 420
	#
	l = math.ceil(n/2)
	t = n*3
	#
	name1 = 'newmultimaps_lmda-{0}_n-{1}_l-{2}_t-{3}'.format(lmda, n, l, t)
	run_experiment(name1, lmda, n, l, t, mmap_ges.MMapGES, (lmda_mlm, n_mlm, kappa_mlm, rho_mlm, etap_mlm), save_data_newmultimaps)
	#
	name2 = 'trivial_lmda-{0}_n-{1}_l-{2}_t-{3}'.format(lmda, n, l, t)
	run_experiment(name2, lmda, n, l, t, trivial_ges.TrivialGES, (lmda, n), save_data_trivial_ges)
	#
	print('newmultimaps bytes: {}'.format(calc_transfer_data_size_newmultimaps(load_experiment('results/'+name1+'.json'))))
	print('trivial_ges bytes: {}'.format(calc_transfer_data_size_trivial_ges(load_experiment('results/'+name2+'.json'))))
#
