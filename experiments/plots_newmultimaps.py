import plot_tools
import experiment_1
import experiment_2
import experiment_3
import experiment_4
import experiment_tools
#
if __name__=='__main__':
	keys1 = ['time_to_generate_map','time_to_encrypt','time_to_decrypt']
	keys1_readable = ['Map Generation', 'Encryption', 'Decryption']
	keys2 = ['transfer_data_size']
	keys2_readable = [None]
	#
	print('Loading data.')
	experiment_1 = experiment_1.import_results('exp1_newmultimaps', experiment_tools.calc_transfer_data_size_newmultimaps, 'sec', 'seconds', 'MiB', 'mebibytes')
	print('Finished loading data.')
	#
	plot_tools.plot_experiment(experiment_1, 'Experiment 1 Time', keys1, keys1_readable, 'Exact Cover Problem Size (n)', 'Time', 0, False, color_index=0)
	plot_tools.plot_experiment(experiment_1, 'Experiment 1 Data', keys2, keys2_readable, 'Exact Cover Problem Size (n)', 'Data Size', 0, False, color_index=3)
	#
	print('Loading data.')
	experiment_2 = experiment_2.import_results('exp2_newmultimaps', experiment_tools.calc_transfer_data_size_newmultimaps, 'sec', 'seconds', 'MiB', 'mebibytes')
	print('Finished loading data.')
	#
	plot_tools.plot_experiment(experiment_2, 'Experiment 2 Time', keys1, keys1_readable, 'Security Parameter (λ)', 'Time', 0, False, color_index=0)
	plot_tools.plot_experiment(experiment_2, 'Experiment 2 Data', keys2, keys2_readable, 'Security Parameter (λ)', 'Data Size', 0, False, color_index=3)
	#
	print('Loading data.')
	experiment_3 = experiment_3.import_results('exp3_newmultimaps', experiment_tools.calc_transfer_data_size_newmultimaps, 'sec', 'seconds', 'MiB', 'mebibytes')
	print('Finished loading data.')
	#
	plot_tools.plot_experiment(experiment_3, 'Experiment 3 Time', keys1, keys1_readable, 'Witness Length (|I|)', 'Time', 0, False, color_index=0)
	plot_tools.plot_experiment(experiment_3, 'Experiment 3 Data', keys2, keys2_readable, 'Witness Length (|I|)', 'Data Size', 0, False, ymax=4, color_index=3)
	#
	print('Loading data.')
	experiment_4 = experiment_4.import_results('exp4_newmultimaps', experiment_tools.calc_transfer_data_size_newmultimaps, 'sec', 'seconds', 'MiB', 'mebibytes')
	print('Finished loading data.')
	#
	plot_tools.plot_experiment(experiment_4, 'Experiment 4 Time', keys1, keys1_readable, 'Number of Subsets (|T|)', 'Time', 0, False, color_index=0)
	plot_tools.plot_experiment(experiment_4, 'Experiment 4 Data', keys2, keys2_readable, 'Number of Subsets (|T|)', 'Data Size', 0, False, color_index=3)
#
