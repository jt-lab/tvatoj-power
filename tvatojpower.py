# MIT License

# Copyright (c) 2020 Jan Tünnermann

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from numpy import random, exp, array, zeros, log, clip
from theano.tensor import mean, cast
from theano.tensor import exp as ttexp
from math import floor
from numpy.random import random as runif
from tqdm import tqdm
import pymc3
import pandas as pd
from scipy.optimize import fmin
from scipy.stats import *
from tqdm import tqdm
from scipy.stats import beta
import sys, logging
import warnings

logger = logging.getLogger(__name__)
try: 
    import coloredlogs
    coloredlogs.install(level='DEBUG')
except ImportError:
    logging.info('If you like the terminal output colored.' + 
                 'Install colored coloredlogs (e.g., pip install coloredlogs)')

# The TVAOJ psychometric function, see Tünnermann, Petersen, & Scharlau (2015):
def tvatoj_psychometric_function(SOA, C, wp, vp=None, vr=None):
    """ Takes SOAs in ms and either C in 1/ms and w or vp and vr in 1/ms """
    if vp is None or vr is None:
        vp = C * wp
        vr = C * (1 - wp)
    SOA = array(SOA)
    left = (1-exp(-vp*abs(SOA))) + exp(-vp*abs(SOA)) * vp/(vp+vr)
    right = exp(-vr*abs(SOA))*vp/(vp+vr)
    return ((SOA<=0)*left  + (SOA>0)*right)

# A generative simulation of the process
def simulate_subject_toj(SOA, reps, C, wp):
    v1 = C * wp                             # attentional weights and overall rate C ...
    v2 = C * (1 -wp)                        # ... determine the individual rates
    probe_first_count = 0                   # Our counter each SOA starts with zero
    for i in range(0, reps):                # For every repetition
        tS = -log(1 - runif(1)) / v2        # let stimulus 2 race and record its VSTM arrival
        tC =  SOA - log(1 - runif(1)) / v1  # sane for stimulus 1, offset by the SOA
        if tC < tS:                         # Did 1 arrive before 2?
            probe_first_count += 1          # Count as a "probe first judment"
    return probe_first_count                # Return the result across all SOAs


# Simulate TOJs for a group of participants, by drawing 
# their individual parameters from distributions
def simulate_tojs(simulation_setup): 

    s = simulation_setup # For convenient access ...
    single_wp=False

    # Get the paras per individual
    if 'C_sd_within' in s: # within subject design
        logging.info('[SIM] Simulating two different (but correlated) C parameters.')
        C_sub_mu = clip(random.normal(s['C_mu'], s['C_sd_between'], size=s['num_participants']), 0, None)
        C_a_sub =  clip(random.normal(C_sub_mu, s['C_sd_within'], size=s['num_participants']), 0, None)
        C_n_sub =  clip(random.normal(C_sub_mu, s['C_sd_within'], size=s['num_participants']), 0,None)
        wp_a_sub =  clip(random.normal(s['wp_a_mu'], s['wp_a_sd_between'], size=s['num_participants']), 0, None)
        wp_n_sub =  clip(random.normal(s['wp_n_mu'], s['wp_n_sd_between'], size=s['num_participants']), 0, None)
    elif 'C_a_mu' in s: # between design
        logging.info('[SIM] Simulating two independent C parameters.')
        C_a_sub =  clip(random.normal(s['C_a_mu'], s['C_a_sd_between'], size=s['num_participants']), 0, None)
        C_n_sub =  clip(random.normal(s['C_n_mu'], s['C_n_sd_between'], size=s['num_participants']), 0,None)
        wp_a_sub =  clip(random.normal(s['wp_a_mu'], s['wp_a_sd_between'], size=s['num_participants']), 0, None)
        wp_n_sub =  clip(random.normal(s['wp_n_mu'], s['wp_n_sd_between'], size=s['num_participants']), 0, None)
    elif 'C_single_mu' in s:
        logging.info('[SIM] Simulating a single C parameter for both conditions.')
        C_a_sub =  clip(random.normal(s['C_single_mu'], s['C_single_sd_between'], size=s['num_participants']), 0, None)
        C_n_sub = C_a_sub
        wp_a_sub =  clip(random.normal(s['wp_a_mu'], s['wp_a_sd_between'], size=s['num_participants']), 0, None)
        wp_n_sub =  clip(random.normal(s['wp_n_mu'], s['wp_n_sd_between'], size=s['num_participants']), 0, None)
    elif 'wp_mu' in s: # A single wp ==> Single condition experient
        logging.info('[SIM] Simulating a single condition.')
        C_sub =  clip(random.normal(s['C_mu'], s['C_sd_between'], size=s['num_participants']), 0, None)
        wp_sub =  clip(random.normal(s['wp_mu'], s['wp_sd_between'], size=s['num_participants']), 0, None)
        single_wp=True
    else:
        logger.error('Could not infer the design from the simulation parameters provided. Please refer to the exmaples')
        sys.exit('Aborting')


    # Get the TOJs
    participant_id = []
    condition_id = []
    probe_first_count = []
    repetitions = []
    SOA = []

    if single_wp:
        condition_nums = [0]
    else:
        condition_nums = [0, 1]

    for p in range(0, s['num_participants']):
        for i,soa in enumerate(s['SOAs']):
            for c in condition_nums:
                participant_id.append(p)
                condition_id.append(c)
                SOA.append(soa)
                repetitions.append(s['repetitions'][i])
                if c == 0 and not single_wp: # simulate a neutral condition TOJ
                    probe_first_count.append(simulate_subject_toj(soa, s['repetitions'][i], C_n_sub[p], wp_n_sub[p]))
                if c == 1 and not single_wp: # simulate an attention condition TOJ
                    probe_first_count.append(simulate_subject_toj(soa, s['repetitions'][i], C_a_sub[p], wp_a_sub[p]))
                if c == 0 and single_wp:
                    probe_first_count.append(simulate_subject_toj(soa, s['repetitions'][i], C_sub[p], wp_sub[p]))

    df = pd.DataFrame()
    df['participant_id'] = participant_id
    df['condition_id'] = condition_id
    df['SOA'] = SOA
    df['repetitions'] = repetitions
    df['probe_first_count'] = probe_first_count
                
        
    return df



# Using the non-centered reparamtrization to reduce divergenses
# See here for the rationale: https://twiecki.io/blog/2017/02/08/bayesian-hierchical-non-centered/
def hierarchical_model_noncentered(data, single_C=False, single_wp=False):
    '''Sets up a pymc3 model based on TVATOJ.

    :param data: A TOJ dataframe as return by the simulations
    :param single_C: Whether to use single C (for both conditions)
    :param single_wp: Whether to use a single wp (implies single C and produces a model for a single condition only)

    :returns: Model
    :rtype: pymc3.Model
    '''
 
    model = pymc3.Model()
    with model: 

        p_id = data['participant_id']
        c_id = data['condition_id']

        if single_wp:        
            wp_c_id = len(data['condition_id']) * [0]
            single_C = True
        else:
            wp_c_id = c_id

        if single_C:        
            C_c_id = len(data['condition_id']) * [0]
        else:
            C_c_id = c_id

            
        pfc =  pymc3.Data('probe_first_count',data['probe_first_count'])

        C_mu = pymc3.Normal('C_mu', 0.080, 0.050, shape=len(set(C_c_id)))
        C_sd = pymc3.HalfCauchy('C_sd', 0.1, shape=len(set(C_c_id)))
        
        wp_mu = pymc3.Normal('wp_mu', 0.5,0.2, shape=len(set(wp_c_id)))
        wp_sd = pymc3.HalfCauchy('wp_sd', 0.2, shape=len(set(wp_c_id)))

        wp_e = pymc3.Normal('wp_e', 0,1, shape=(len(set(p_id)), len(set(wp_c_id))))
        C_e = pymc3.Normal('C_e', 0,1, shape=(len(set(p_id)), len(set(C_c_id))))

        C = pymc3.Deterministic('C', (C_mu + C_e * C_sd).clip(0, 1))
        wp = pymc3.Deterministic('wp',  (wp_mu + wp_e * wp_sd).clip(0, 1))
    
        theta = pymc3.Deterministic('theta', tvatoj_psychometric_function(
            data['SOA'], C[(p_id, C_c_id)], wp[(p_id, wp_c_id)]))

        y = pymc3.Binomial('y', n=cast(data['repetitions'], 'int64'),
                                p=theta, observed=pfc,
                                dtype='int64')  

        # The deterministic transformation could probably be externalized
        # However, here the calculation is most safe to produce prober within subject estimates
        vp = pymc3.Deterministic('vp', wp * C)
        vr = pymc3.Deterministic('vr', (1 - wp) * C)
        
        
        vp_mean = pymc3.Deterministic('vp_mean', mean(vp, axis=0)) 
        vr_mean = pymc3.Deterministic('vr_mean', mean(vr, axis=0)) 
        if not single_wp:
            va_diff_mean = pymc3.Deterministic('va_diff_mean', mean(vp[:,1] - vr[:,1])) # Diff of probe and ref rate in the attention cond
            vp_diff_mean = pymc3.Deterministic('vp_diff_mean', mean(vp[:,1] - vp[:,0])) # Diff of attention and neutral condition probe rates
            vr_diff_mean = pymc3.Deterministic('vr_diff_mean', mean(vr[:,1] - vr[:,0])) # Diff of attention and neutral condition probe rates
            wpa_mean = pymc3.Deterministic('wpa_mean', mean(wp[:,1])) 
            wp_diff_mean = pymc3.Deterministic('wp_diff_mean', mean(wp[:,1] - wp[:,0])) 
        else:
            wp_vs_point5_mean = pymc3.Deterministic('wp_mean', mean(wp)) 
        return(model)

 
# This function is borrowed from @aloctavodia, who ported it from John Kruschke's scripts
# https://github.com/aloctavodia/Doing_bayesian_data_analysis/blob/master/HDIofICDF.py
def HDIofICDF(dist_name, credMass=0.95, **args):
    # freeze distribution with given arguments
    distri = dist_name(**args)
    # initial guess for HDIlowTailPr
    incredMass =  1.0 - credMass

    def intervalWidth(lowTailPr):
        return distri.ppf(credMass + lowTailPr) - distri.ppf(lowTailPr)

    # find lowTailPr that minimizes intervalWidth
    HDIlowTailPr = fmin(intervalWidth, incredMass, ftol=1e-8, disp=False)[0]
    # return interval as array([low, high])
    return distri.ppf([HDIlowTailPr, credMass + HDIlowTailPr])

def sim_and_fit(setup, model_func, iterations, condition_func, 
                goal_var_names=None, log_var_names=['C_mu', 'wp_mu'],
                single_C=False, single_wp=False, outfile='out.csv',
                turn_off_warnings=True):

    if (turn_off_warnings):
        warnings.filterwarnings("ignore")
        logging.warning('Attention: Warnings turned off. ') # There is so much from pymc3 and theano ..

    if log_var_names==None or len(log_var_names) < 1:
        sys.exit('log_var_names should not be empty or None! Log at least one variable!')
    num_success=0
    model = None
    for i in tqdm(range(iterations), desc='Overall progress'):
        data = simulate_tojs(setup)
        if model is None:
            model = model_func(data, single_C=single_C, single_wp=single_wp)
        with model:
            pymc3.set_data({'probe_first_count': data['probe_first_count']})
            trace = pymc3.sample(2000, tune=1000, cores=4, init='adapt_diag', target_accept=0.85)
            summary_stats = pymc3.summary(trace, var_names=goal_var_names, hdi_prob=0.95)
            print(summary_stats)
        success = condition_func(summary_stats) * 1 # Either 0 or 1, depending on reaching our goals.
        num_success += success
        attempts = (i+1)
        success_rate = num_success / attempts
        hdi = HDIofICDF(beta,a=1+num_success, b=1+(attempts-num_success))
        logging.info(('[ESTIMATE] Success rate: %.2f' % success_rate +
                     ' [95 %% HDI: %.2f to %.2f]' % (hdi[0],hdi[1]) + 
                     '\n' + '-'* 20))

        out_df = pymc3.summary(trace, var_names=log_var_names, hdi_prob=0.95)
        out_df.insert(0, 'iteration', attempts)
        out_df.insert(1, 'success', success)
        out_df.insert(2, 'power_est', success_rate)
        out_df.insert(3, 'power_hdi_2.5%', hdi[0])
        out_df.insert(4, 'power_hdi_97.5%', hdi[1])
        if attempts == 1:
            out_df.to_csv(outfile)
        else:
            out_df.to_csv(outfile, mode='a', header=False)

def fit(model_func, condition_func, outfile='fit.csv'):
    trace = pymc3.sample(2000, tune=1000, cores=4, init='adapt_diag') #, target_accept=.85)
    summary_stats = pymc3.summary(trace, hdi_prob=0.95)
    summary_stats.to_csv(outfile)
    logger.info('The model was fitted and a summary was written to: ' + outfile)
    logger.info('You can analyze the returned trace with help of the Arviz library (https://arviz-devs.github.io/arviz/)')
    logger.info('For instance, plot parameter posteriors with arviz.plot_posterior(trace, var_names=["C", "wp"])')
    return trace
