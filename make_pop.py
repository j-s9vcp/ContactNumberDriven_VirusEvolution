import random
import numpy as np

def Uniform():
    return abs(random.random())

def rand_gamma(kappa, theta):
    uni_num = 0

    int_kappa  = int(kappa)
    frac_kappa = kappa - int_kappa
    x_int = 0
    for i in range(int_kappa):
        x_int += -np.log(Uniform())#+無限大から0までとることができる


    if( abs(frac_kappa) < 0.01 ):
        x_frac = 0

    else:

        b=(np.exp(1.0) + frac_kappa)/np.exp(1.0)
        while 1 :
            u=Uniform()
            p = b * u
            uu = Uniform()
            if p <= 1.0:
                    x_frac = p**(1.0/frac_kappa)
                    if(uu <= np.exp(-x_frac)):
                        break
                
            else:
                x_frac =- np.log((b - p)/frac_kappa)
                if (uu <= x_frac**(frac_kappa - 1.0)):
                        break


            uni_num += 1

    return (x_int + x_frac) * theta


def porand(x):
    k = 0
    uni_num = 0
    a = Uniform()
    b = np.exp(-x)
    a_i = 0
    while(a >= b):
        a *= Uniform()
        #a はだんだん下がっていく
        k += 1
        uni_num += 1

    return k


def calc(shape, scale):
    return porand(rand_gamma(shape, scale))


def calc_contact_history(shape, scale, duration):
    p_list = []
    
    for i in range(duration):
        day_contact = calc(shape, scale)
        p_list.append(day_contact)

    
    return p_list


