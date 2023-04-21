import joblib
import datetime
import argparse
import numpy as np
from multiprocessing import Pool


output_dir = '/Users/sunagawajunya/Documents/2020/Dr_Yamaguchi/borna/others/20210802/search_details'


def inf_simulator(tau_max, p, epsilon):

    gamma = 10
    c = 10
    beta = 0.0001
    micro = 0.01
    dt = 0.001


    cc = p/(p + 1000)

    Ta = 1000
    Ia = 0
    Vi = 1
    Vni = 0

    Ta_range = [Ta]
    Ia_range = [Ia]
    Vi_range = [Vi]
    Vni_range = [Vni]

    for i in range(1, int(tau_max*1000)):

        Taa = Ta + (gamma-beta*Ta*Vi-micro*Ta)*dt

        Iaa = Ia + (beta*Ta*Vi-cc*Ia)*dt

        Vii = Vi + (epsilon*p*Ia-c*Vi)*dt

        Vnii = Vni + ((1-epsilon)*p*Ia-c*Vni)*dt

        Ia = Iaa
        Ta = Taa
        Vi = Vii
        Vni = Vnii

        Ta_range.append(Ta)
        Ia_range.append(Ia)
        Vi_range.append(Vi)
        Vni_range.append(Vni)

    return Vi_range, Vni_range
    # return Vi_range


def pre_calc_prob(tau_max, p, epsilon):

    vi, vni = inf_simulator(tau_max, p, epsilon)

    total_VL = []

    ave_VL = []

    for u in range(len(vi)):

        ave_VL.append(vi[u])

        if u % 1000 == 0:
            total_VL.append(sum(ave_VL)/1000)

            ave_VL = []

    return total_VL


def wrapper_pre_calc_prob(args):
    return pre_calc_prob(*args)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--max_duration', type=int)
    parser.add_argument('-n', '--n_processes', type=int)
    args = parser.parse_args( )

    # parameters
    n_processes = args.n_processes
    max_duration = args.max_duration


    print('started at ', datetime.datetime.now())

    inf_ = joblib.load('pre_data' + '/inf_id_{}d'.format(max_duration))

    args = []

    t_o = 0

    for ii in range(0, 10000, 100):
        for jj in np.arange(0, 1, 0.01):
            k = inf_[t_o]
            args.append([k, ii, jj])
            t_o += 1

    p = Pool(processes=n_processes)
    vi_value_include_inf = p.map(wrapper_pre_calc_prob, args)

    joblib.dump(vi_value_include_inf, 'pre_data' + '/vi_amount_include_inf_{}d'.format(max_duration), compress = 3)

    print('finish at ', datetime.datetime.now())
