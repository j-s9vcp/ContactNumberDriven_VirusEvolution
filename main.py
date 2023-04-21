import os
import sys
import math
import joblib
import datetime
import argparse
import numpy as np
from multiprocessing import Pool

from make_pop import calc_contact_history
from calc_r0 import calc_r0
from make_txt import save_txt

def calc_iteration(shape, scale, duration, i_iter, i_r, j_basic, total_vi, data_file):

	print("shape : {}, scale : {}".format(shape, scale))

	total_populations = []
	total_r0 = []

	for i in range(i_iter):

		if i % 100 == 0:
			print("iter {}".format(i))

		ind_populations  = calc_contact_history(shape, scale, duration)
		ind_r0 = calc_r0(i_r, j_basic, ind_populations, total_vi)
		total_populations.append(ind_populations)
		total_r0.append(ind_r0)

	save_joblib(shape, scale, total_populations, total_r0, data_file)
	save_txt(shape, scale, duration, total_r0, data_file)


def save_joblib(shape, scale, total_populations, total_r0, data_file):

	new_dir_path = data_file + '/shape_{}_scale_{}'.format(shape, scale)

	joblib.dump(total_populations, new_dir_path + '/ind_pop.pkl', compress = 3)
	joblib.dump(total_r0, new_dir_path + '/ind_r0.pkl', compress = 3)



def aggregate_info(shape_range, scale_range, duration, i_iter, i_r, j_basic, total_vi, data_file):

	z = []

	# for Fig 2

	for ind_shape, ind_scale in zip(shape_range, scale_range):

		z.append([ind_shape, ind_scale, duration, i_iter, i_r, j_basic, total_vi, data_file])

	# # for Fig 3

	# for ind_shape in shape_range:
	# 	for ind_scale in scale_range:

	# 	z.append([ind_shape, ind_scale, duration, i_iter, i_r, j_basic, total_vi, data_file])

	return z

def make_directory(args):

	data_file = args[-1][-1]

	try:
		os.mkdir(data_file)
	except:
		print('Save dir exist : /data, OK?')
		sys.exit()

	for i in range(len(args)):

		ind_shape = args[i][0]
		ind_scale = args[i][1]


		new_dir_path = data_file + '/shape_{}_scale_{}'.format(ind_shape, ind_scale)

		try:
			os.mkdir(new_dir_path)
		except:
			print('File exist : /shape_{}_scale_{}'.format(ind_shape, ind_scale))
			sys.exit()


def wrapper_calc_iteration(args):
    return calc_iteration(*args)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--iteration', type=int)
	parser.add_argument('-m', '--max_duration', type=int)
	parser.add_argument('-n', '--n_processes', type=int)
	args = parser.parse_args( )

	# parameters
	n_processes = args.n_processes
	i_iter = args.iteration
	max_duration = args.max_duration

	total_vi = joblib.load('pre_data' + '/vi_amount_include_inf_{}d'.format(max_duration))

	i_r = 25
	max_prob = 0.8
	max_vi_for_j_basic = 87746.60599946312
	j_basic = max_prob/(i_r**np.log10(max_vi_for_j_basic))

	dt_now = datetime.datetime.now()

	data_file = 'data_{}{}{}'.format(dt_now.year, dt_now.month, dt_now.day)

	# for Fig 2

	shape_range = np.array([100, 0.12])
	scale_range = np.array([0.03, 10])

	# # for Fig 3

	# shape_range = 10**np.linspace(-1, 1, 21)
	# scale_range = 10**np.linspace(-1, 1, 21)


	args = aggregate_info(shape_range, scale_range, max_duration, i_iter, i_r, j_basic, total_vi, data_file)

	make_directory(args)

	p = Pool(processes=n_processes)
	p.map(wrapper_calc_iteration, args)

