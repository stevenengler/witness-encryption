import experiment_tools
import math
from unitconvert.timeunits import TimeUnit
from unitconvert.digitalunits import DigitalUnit
#
def import_results(name_prefix, transfer_size_func, time_unit, time_unit_display, data_unit, data_unit_display):
	n = 40
	lmda = 30
	#
	experiments = []
	t_vals = [40, 200, 400, 800, 1200, 1600, 2000, 2400, 2800]
	repeat_vals = list(range(5))
	for t in t_vals:
		temp = []
		for rep in repeat_vals:
			l = math.ceil(n/2)
			name = '{}_lmda-{}_n-{}_l-{}_t-{}_repeat-{}'.format(name_prefix, lmda, n, l, t, rep)
			#
			raw_data = experiment_tools.load_experiment('results/{}.json'.format(name))
			#
			data = {}
			data['name'] = raw_data['name']
			data['time_to_generate_map'] = {'data':TimeUnit(raw_data['time_to_generate_map'], 'sec', time_unit).doconvert(),
			                                'unit':time_unit_display}
			data['time_to_encrypt'] = {'data':TimeUnit(raw_data['time_to_encrypt'], 'sec', time_unit).doconvert(),
			                           'unit':time_unit_display}
			data['time_to_decrypt'] = {'data':TimeUnit(raw_data['time_to_decrypt'], 'sec', time_unit).doconvert(),
			                           'unit':time_unit_display}
			data['transfer_data_size'] = {'data':DigitalUnit(transfer_size_func(raw_data), 'B', data_unit).doconvert(),
			                              'unit':data_unit_display}
			temp.append(data)
		#
		experiments.append(temp)
	#
	return {'x':t_vals, 'y':experiments}
#
if __name__=='__main__':
	import mmap_ges
	import trivial_ges
	#
	for mult in [1, 5, 10, 20, 30, 40, 50, 60, 70]:
		for repeat_count in range(5):
			lmda = 30
			n = 40
			l = math.ceil(n/2)
			t = n*mult
			#
			lmda_mlm = lmda
			kappa_mlm = n
			n_mlm = n
			rho_mlm = 52
			etap_mlm = 420
			#
			name_newmultimaps = 'exp4_newmultimaps_lmda-{0}_n-{1}_l-{2}_t-{3}_repeat-{4}'.format(lmda, n, l, t, repeat_count)
			#
			experiment_tools.run_experiment(name_newmultimaps, lmda, n, l, t, mmap_ges.MMapGES, (lmda_mlm, n_mlm, kappa_mlm, rho_mlm, etap_mlm), experiment_tools.save_data_newmultimaps)
			#
			name_trivial_ges = 'exp4_trivial_ges_lmda-{0}_n-{1}_l-{2}_t-{3}_repeat-{4}'.format(lmda, n, l, t, repeat_count)
			#
			experiment_tools.run_experiment(name_trivial_ges, lmda, n, l, t, trivial_ges.TrivialGES, (lmda, n), experiment_tools.save_data_trivial_ges)
		#
	#
#
