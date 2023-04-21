import joblib
import datetime
import argparse
import numpy as np
from multiprocessing import Pool

def inf_duration(AUC50, a_value, vi, max_duration):

    return max_duration*(AUC50**a_value/(vi**a_value+AUC50**a_value))

def wrapper_inf_duration(args):
    return inf_duration(*args)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d50', '--d50', type=int)
    parser.add_argument('-dk', '--dk', type=float)
    parser.add_argument('-m', '--max_duration', type=int)
    parser.add_argument('-n', '--n_processes', type=int)
    args = parser.parse_args( )

    # parameters
    n_processes = args.n_processes
    d50 = args.d50
    dk = args.dk
    max_duration = args.max_duration

    vi_amount = joblib.load('pre_data' + '/vi_amount_{}d'.format(max_duration))

    print('started at ', datetime.datetime.now())

    print('D50 {:.1f}, Dk {:.1f}'.format(d50, dk))

    args = []

    for vi_i in vi_amount:
        args.append([d50, dk, vi_i, max_duration])

    p = Pool(processes=n_processes)
    vi_value = p.map(wrapper_inf_duration, args)

    joblib.dump(vi_value, 'pre_data' + '/inf_id_{}d'.format(max_duration), compress = 3)

    print('finish at ', datetime.datetime.now())
