import matplotlib.pylab as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FormatStrFormatter
from matplotlib import transforms
from matplotlib import lines
from matplotlib.ticker import ScalarFormatter
#
import statistics
import math
import numpy as np
#
CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
				  '#984ea3', '#a65628', '#f781bf',
				  '#999999', '#e41a1c', '#dede00']
#
def graph(data, keys_to_graph, keys_readable, xlabel, ylabel, color_index=0, x_log=False, ymin=None, ymax=None):
	plt.xlabel(xlabel)
	#
	if not all([data['y'][0][0][key]['unit']==data['y'][0][0][keys_to_graph[0]]['unit'] for key in keys_to_graph]):
		raise Exception('Not all units were the same.')
	#
	unit = data['y'][0][0][keys_to_graph[0]]['unit']
	#
	if unit != None:
		plt.ylabel('{} ({})'.format(ylabel, unit))
	else:
		plt.ylabel(ylabel)
	#
	plt.minorticks_on()
	plt.grid(color='lightgrey')
	#
	if x_log:
		plt.gca().set_xscale('log', basex=2)
		plt.gca().set_xticks([0.5, 1, 2, 4, 8, 16])
		plt.gca().xaxis.set_major_formatter(ScalarFormatter())
	#
	markers = ['o', 's', '^', 'v', 'D']
	#
	for i in range(len(keys_to_graph)):
		key = keys_to_graph[i]
		values = [[repeat[key]['data'] for repeat in data['y'][j]] for j in range(len(data['y']))]
		#
		x = data['x']
		y = [statistics.mean(i) for i in values]
		#
		import numpy as np, scipy.stats as st
		conf_intervals = np.array([st.t.interval(0.95, len(repeat_vals)-1, loc=np.mean(repeat_vals), scale=st.sem(repeat_vals)) for repeat_vals in values])
		yerr_up = conf_intervals[:,0]-y
		yerr_down = -(conf_intervals[:,1]-y)
		#
		plt.errorbar(x, y, fmt='.-', label=keys_readable[i], color=CB_color_cycle[i+color_index], marker=markers[i+color_index], markersize=5, ecolor='#333333', yerr=[yerr_up, yerr_down], capsize=3)
	#
	if ymax is not None:
		plt.ylim(ymax=ymax)
	#
	if plt.gca().get_ylim()[0]>0:
		plt.ylim(ymin=ymin)
	#
#
def plot_experiment(data, title, keys_to_graph, keys_readable, xlabel, ylabel, ymin=None, x_log=False, ymax=None, special_legend=0, color_index=0):
	plt.figure(figsize=(4, 3))
	#
	graph(data, keys_to_graph, keys_readable, xlabel, ylabel, color_index, x_log, ymin, ymax)
	#
	if not all([x==None for x in keys_readable]):
		# get handles
		handles, labels = plt.gca().get_legend_handles_labels()
		# remove the errorbars
		handles = [h[0] for h in handles]
		if special_legend == 1:
			plt.legend(handles, labels, markerscale=1.5, bbox_to_anchor=(0, 0.3), loc='center left')
		else:
			plt.legend(handles, labels, markerscale=1.5)
		#
	#
	plt.tight_layout()
	plt.savefig('figures/'+title.replace(' ', '_')+'.pdf', format='pdf', bbox_inches='tight')
	plt.show()
#
