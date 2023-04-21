import numpy as np

def calc_r0(i_r, j_basic, ind_populations, total_vi):
    
    total_r_values = []
    
    for i in range(len(total_vi)):

        r_value = []

        temporal_vi = total_vi[i]
        
        for u in range(len(temporal_vi)):            
                
            viral_load = i_r**np.log10(temporal_vi[u])
            prob = viral_load * j_basic

            secondary_infected = ind_populations[u]*prob
            
            r_value.append(secondary_infected)
                
            
        total_r_values.append(sum(r_value))

    return total_r_values
