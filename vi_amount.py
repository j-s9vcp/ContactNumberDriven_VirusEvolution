import joblib
import datetime
import argparse
import numpy as np
from multiprocessing import Pool

def simulator(tau_max, p, epsilon):

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

    return sum(Vi_range)/1000

def wrapper_simulator(args):
    return simulator(*args)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--max_duration', type=int)
    parser.add_argument('-n', '--n_processes', type=int)
    args = parser.parse_args( )

    # parameters
    n_processes = args.n_processes
    max_duration = args.max_duration

    print('started at ', datetime.datetime.now())

    print('max_duration {}'.format(max_duration))

    args = []

    for i in range(0, 10000, 100):
        for j in np.arange(0, 1, 0.01):
            args.append([max_duration, i, j])

    p = Pool(processes=n_processes)
    vi_amount = p.map(wrapper_simulator, args)

    joblib.dump(vi_amount, 'pre_data' + '/vi_amount_{}d'.format(max_duration), compress = 3)

    print('finish at ', datetime.datetime.now())
