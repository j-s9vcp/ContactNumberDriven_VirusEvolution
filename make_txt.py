import joblib
import numpy as np

def save_best_txt(best_list, save_path):

    best_p = best_list[0]
    best_e = best_list[1]
    best_i_d = best_list[2]
    best_r0 = best_list[3]

    text = 'contact\np\tepsilon\ti_d\tr0\n'

    for i in range(len(best_p)):
        text = '{}{}\t{}\t{}\t{}\n'.format(text,best_p[i],best_e[i],best_i_d[i], best_r0[i])

    with open(save_path + '/best_param.txt','w') as f:
        f.write(text)

def aggregate_data(shape, scale, iter_r0, Vi_values, data_file):

    print("shape : {}, scale : {}".format(shape, scale))

    save_path = data_file + '/shape_{}_scale_{}'.format(shape, scale)


    z = []
    for i in range(0, 10000, 100):
        for j in np.arange(0, 1, 0.01):
            z.append([i, j])

    best_p = []
    best_e = []
    best_id = []
    best_r0 = []

    for i in range(len(iter_r0)):
        ind_r0 = iter_r0[i]

        best_r = [j for j, v in enumerate(ind_r0) if v == max(ind_r0)]
    

        for b in best_r:
            best_p.append(z[b][0])
            best_e.append(z[b][1])
            best_id.append(Vi_values[b])
            best_r0.append(max(ind_r0))

    best_list = [best_p, best_e, best_id, best_r0]

    return best_list, save_path


def save_txt(shape, scale, max_duration, iter_r0, data_file):

    Vi_values = joblib.load('pre_data' + '/inf_id_{}d'.format(max_duration))

    best_list, save_path = aggregate_data(shape, scale, iter_r0, Vi_values, data_file)

    save_best_txt(best_list, save_path)	