# Copyright (c) 2020 Jan Tünnermann. All rights reserved.
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

from tvatojpower import hierachical_model_noncentered, sim_and_fit

'''
This is an example of a power estimation for a TOJ experiment with two conditions
(neutral & attention). While the relative attentional weight can be different
between the conditions (e.g., wp > 0.5 due to attetnion in the attention condition),
the C parameter is assumed to be the same in both conditions.
'''

# Step 1: Define your hypothetical design:
design = {
    'num_participants'   : 25,                         # Anzahl der Probanden
    'SOAs'               : [-100.0, -80.0, -60.0,      # Die SOAs
                            -40.0, -20.0, 0.0, 20.0,
                            40.0, 60.0, 80.0, 100.0],

    'repetitions'        : [24, 24, 32, 32, 48,        # Die Wdhs in den SOAs
                            48, 48, 32, 32, 24, 24],
    'C_single_mu'        : 0.070,                      # Mittelwert der simulierten Cs
    'C_single_sd_between': 0.020,                      # SD mit der die Cs zwischen Probanden varieieren
    'wp_a_mu'            : 0.55,                       # Mittelwert simulierten wps in der attended Bed. 
    'wp_a_sd_between'    : 0.02,                       # SD von wp_attended zw. Probanden
    'wp_n_mu'            : 0.50,                       # Mittelwert wp_neutral ...
    'wp_n_sd_between'    : 0.005,                      # SD wp_neutral ...
    'num_simulation'     : 200,                        # Anzahl der sims. Kann so bleiben 
}

# Step 2: Define your research goals. (When was the experiment succesful?)
def check_rates(summary_stats):
    success = (
        summary_stats['hdi_2.5%']['va_diff_mean'] > 0.004   # We want: a 4 Hz (or larger) difference
                                                            # between the probe and ref rate in the attention cond ...
            and (                                           # ... and ...
            summary_stats['hdi_2.5%']['vp_diff_mean'] > 0   # either the probe should be faster in the attenion condition than in neutral condition
            or                                              # or
            summary_stats['hdi_97.5%']['vr_diff_mean'] < 0  # the reference should be slower. 
            )
    )
    return success

# Step 3: Start the simulations and power estimation
sim_and_fit(setup=design,                                   # The deisgn specified above
            model_func=hierachical_model_noncentered,       # A function that returns a pymc3 model  
            single_C=True,                                  # Let the simulator know we want the model with a shared C
            iterations=200,                                 # How many simulated experiments do we want?
            condition_func=check_rates,                     # A function that checks our goals (defined above)
            goal_var_names=['va_diff_mean', 'vp_diff_mean', # Limit summary stats to the variables used
                            'vr_diff_mean', 'C_mu', 'wp_mu',# in the goal checking and those we would like
                            'C_sd', 'wp_sd'],               # to the printed after each iteration 
            outfile='single_C.csv'
            )

