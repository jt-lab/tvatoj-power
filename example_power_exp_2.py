# Copyright (c) 2020 Jan Tünnermann. All rights reserved.
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

from tvatojpower import hierarchical_model_noncentered, sim_and_fit

# This example is based on Experiment 2 from
# Tünnermann, Krüger, & Scharlau, (2017).
#

#
# Tünnermann, J., Krüger, A., & Scharlau, I. (2017). 
#      Measuring attention and visual processing 
#      speed by model-based analysis of temporal-order
#      judgments. JoVE, e54856.


'''
This example is based on Experiment 2 from Tünnermann, Krüger, & Scharlau (2017).

The hypothetical experiment is a between-subject design with two conditions
(attention & neutral)

Tünnermann, J., Krüger, A., & Scharlau, I. (2017). 
      Measuring attention and visual processing 
      speed by model-based analysis of temporal-order
      judgments. JoVE, e54856.
'''

# Step 1: Define your hypothetical design:
design = {
  'num_participants'    : 35,                         # Specify the number of participants

    'SOAs'              : [-100.0, -80.0, -60.0,      # Specify the intended SOAs in ms
                           -40.0, -20.0, 0.0, 20.0,
                           40.0, 60.0, 80.0, 100.0],

    'repetitions'       : [24, 24, 32, 32, 48,        # Specify the repetitions of each SOA
                           48, 48, 32, 32, 24, 24],   # (length muss match SOAs)

    'C_n_mu'            : 0.070,                      # Neutral group mean of sim. Cs in 1/ms  
    'C_n_sd_between'    : 0.020,                      # Neutral group standard deviation of C
    'C_a_mu'            : 0.070,                      # Attention group mean of sim. Cs in 1/ms   
    'C_a_sd_between'    : 0.020,                      # Attention group standard deviation of C

    'wp_n_mu'           : 0.50,                       # Neutral group mean of sim. wp
    'wp_n_sd_between'   : 0.005,                      # Neutral group standard deviation of wp
    'wp_a_mu'           : 0.55,                       # Attention group mean of sim. wp
    'wp_a_sd_between'   : 0.02,                       # Neutral group standard deviation of wp
    
    'num_simulation'    : 200,                        # Number of simulations to perform
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
sim_and_fit(setup=design,                                    # The deisgn specified above
            model_func=hierarchical_model_noncentered,        # A function that returns a pymc3 model  
            iterations=200,                                  # How many simulated experiments do we want?
            condition_func=check_rates,                      # A function that checks our goals (defined above)
            goal_var_names=['va_diff_mean',                  # Limit summary stats to the variables used
                            'vp_diff_mean', 'vr_diff_mean',  # in the goal checking and those we would like
                            'C_mu', 'wp_mu','C_sd', 'wp_sd'],# to the printed after each iteration 
            outfile='exp2.csv'
            )

