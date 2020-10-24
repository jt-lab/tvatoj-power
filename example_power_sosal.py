# Copyright (c) 2020 Jan Tünnermann. All rights reserved.
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

from tvatojpower import hierarchical_model_noncentered, sim_and_fit



# Step 1: Define your hypothetical design:
design = {

    'num_participants'   : 35,                         # Specify the number of participants

    'SOAs'               : [-100.0, -80.0, -60.0,      # Specify the intended SOAs in ms
                            -40.0, -20.0, 0.0, 20.0,
                            40.0, 60.0, 80.0, 100.0],

    'repetitions'        : [24, 24, 32, 32, 48,        # Specify the repetitions of each SOA
                            48, 48, 32, 32, 24, 24],   # (length must match SOAs)


    'C_mu'               : 0.100,                      # Group mean of the simulated Cs in 1/ms
    'C_sd_between'       : 0.020,                      # Standard deviation of simulated Cs
    'wp_mu'              : 0.55,                       # Group mean of the simulated wps
    'wp_sd_between'      : 0.05,                       # Standard deviation of similated wps

    'num_simulation'     : 200,                        # Number of simulations to perform
}

# Step 2: Define your research goals. (When was the experiment succesful?)
def check_rates(summary_stats):
    success = summary_stats['hdi_2.5%']['wp_mu[0]'] > 0.5   # All we care about in this example is that
                                                            # that we see an attention effect in the probe weight,
                                                            # meaning that it is larger than .5 (neutral weight)
                                                            # Note that despite having only one condition we have
                                                            # to use the index [0] here.
    return success

# Step 3: Start the simulations and power estimation
sim_and_fit(setup=design,                                # The deisgn specified above
            model_func=hierarchical_model_noncentered,    # A function that returns a pymc3 model (currently only this one) 
            single_C=True,                               # 
            single_wp=True,
            iterations=200,                              # How many simulated experiments do we want?
            condition_func=check_rates,                  # A function that checks our goals (defined above)
            goal_var_names=['C_mu', 'wp_mu'],            # Limit summary stats to the variables used
                                                         # to the printed after each iteration 
            outfile='test100_0.55.csv'               # A file where the log (==final result) will be stored
            )

