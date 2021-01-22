# TVATOJ-power

TVATOJ-power is a Python module plus examples for performing Bayesian power estimation ([Kruschke, 2014](#1)) for TVA-based ([Bundesen, 1998](#2)) TOJ experiments (as introduced in [Tünnermann, Krüger, & Scharlau, 2017](#3)). In particular, it contains a Python+[PyMC3](https://github.com/pymc-devs/pymc3) ([Salvatier et al., 2016](#4)) port of the [Tünnermann, Krüger, & Scharlau's (2017)](#3) R with JAGS examples ([example_power_exp_1.py](./example_power_exp_1.py) & [example_power_exp_2.py](./example_power_exp_2.py) are the python version of the original R scripts). In addition, new examples and functionalities were added.

## Background
In classic statistics power is probability of avoiding type-II errors. Or in other words, it is the probability that a hypothesis test correctly rejects the null-hypothesis, given that the alternative hypothesis is true, which researchers typically want to maximize by using sufficiently large samples. However, the TVATOJ framework uses a Bayesian statsitical framework. In Bayesian statistics, there is no inherent need for binary decision (reject or not ) and consequently no concept of power in the classical sense. However, in broader sense, reasearcher might want to maximize to detect whatever kind of differences they are interested in. Along these lines, Bayesian power simulations can be performed ([Kruschke, 2014](#1)). The idea is to repeatedly simulate data with model (purely hypothetical or based on earlier findings), fit it, and determine for how many simulations the research goal was reached. This type of power anaylsis is highly flexible, as not only the number of participants can be varied to tweap power, but also other experimental parameters, such as, in the present context, the magnitudes and spacing of the SOAs and how their repetitions are distributed. This python module contains the procedure (with simualtion and fitting) to perform such repeated simualtation and convert them in to a Bayesian estimate of power (i.e., it returns the probability of reaching the research goal along with 95 % highest density intervals).

## Dendencies
* [PyMC3](https://github.com/pymc-devs/pymc3) 
* [coloredlogs](https://github.com/xolox/python-coloredlogs) (optional)

## Installation
* Install the dependencies listed above, e.g.: `conda install -c conda-forge pymc3`
* Clone the repositories: `git clone https://github.com/jeti182/tvatoj-power.git`

## Module & Examples
You should then find the following components:
* tvatojpower.py contains the psychometric function, setup of the  PyMC3 model, and the overall simulation and power estimation procedure.
* [example_power_exp_1.py](./example_power_exp_1.py): Example power simulation for a *within*-participants design with an attention and a neutral condition.
* [example_power_exp_2.py](./example_power_exp_2.py): Example power simulation for a *between*-participants design with an attention and a neutral condition.
* [example_power_single_C.py](./example_power_single_C.py) Example power simulation for a within-participants design with an attention and a neutral condition, but both conditions share TVA's C parameter
* [example_power_one_condition.py](./example_power_one_condition.py): Example power simulation for an experiment with a single condition (and attention being directed to the probe stimulus).
* [plot_priors.py](./plot_priors.py): Plot prior visualizations and typical values found in the literature.


## Running the examples
* E.g., `python example_power_exp_1.py`

## Defining and running a new power analysis
Defining and running a new TVATOJ power analysis is a three step procedure.

In the first step, we specify the desired setup for which we want to estimate power. All its details contribute to the resulting power estimate. See below for an example. The first three entries of the `dict` define the experiment's details: how many participants, which SOAs, and how often is each SOA repeated? The following entries specify the parameters of the simulation. In this example, we assume that there is a single *C* for both the attention and the neutral condition. We specify its group mean and the standard deviation. For the attentional weight of the probe, we specify mean and standard deviation separately for both the neutral and the attention condition. The values in the example below are based on typical estimates from the literature. The simulation can also use other versions of the model. For instance, it could use one that has individual *C* group estimates for the neutral and attended condition. Please see the further `example_...` -scripts for the different possibilities. They can be used as templates because the presence or absence of a certain key in the design `dict` selects the simulation and model to be used.

```python
# First some imports:
from tvatojpower import hierarchical_model_noncentered, sim_and_fit

# Step 1: Define your hypothetical design:
design = {
    'num_participants'   : 25,                         # Number of participants
    'SOAs'               : [-100.0, -80.0, -60.0,      # SOAs
                            -40.0, -20.0, 0.0, 20.0,
                            40.0, 60.0, 80.0, 100.0],
    'repetitions'        : [24, 24, 32, 32, 48,        # Repetitions of each SOAs
                            48, 48, 32, 32, 24, 24],

    'C_single_mu'        : 0.070,                      # Group mean of simulted Cs
    'C_single_sd_between': 0.020,                      # Group SD of the Cs
    'wp_a_mu'            : 0.55,                       # Group mean of simultated wp for the attention condition
    'wp_a_sd_between'    : 0.02,                       # SD of wp_attended
    'wp_n_mu'            : 0.50,                       # Group mean of wp_neutral ...
    'wp_n_sd_between'    : 0.005,                      # SD of wp_neutral ...
}
```
In the second step, we define our research goal. When was the experiment successful? For this, we define a function that returns true if the desired outcome was successfully detected. In this example, the function is called `check_rates`, and it checks whether the processing rate difference (of attended and unattended stimuli) is larger than 4 Hz in favor of the attended stimulus. Additionally, either the difference of the probe rates from the neutral and attention condition need to indicate that the probe was accelerated or the reference rate was slowed down. The success function can be based on any desired criterion. For instance, instead of basing it on processing rate estimates, we could want that the attentional weight of the probe in the attention condition is larger 0.5. These criteria are based on the `summary` objects generated by [arviz summary function](https://arviz-devs.github.io/arviz/api/generated/arviz.summary.html), and typically it will consider the 95 % highest density interval (HDI) bounds. For instance, if our goal is that some estimate is above a certain value, we will test for its lower HDI bound bein above the value of interest (see the example below). Further examples are available in this repository. 

```python
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
```
The third and final step is starting the repeated simulation and estimation process. This can be done by calling the sim_and_fit function and passing the design dict defined above as "setup" and the check_rates function as "condition_func" parameters. See the comments below for deThe third and final step is starting the repeated simulation and estimation process. This can be done by calling the `sim_and_fit` function and passing the design `dict` defined above as "`setup`" and the `check_rates` function as "`condition_func`" parameters. See the comments below for descriptions of the further parameters. Again, the other examples included in this repository can be templates for running different versions of the analyses. scriptions of the further parameters. Again, the other examples included in this repository can be templates for running different versions of the analyses. 

```python
# Step 3: Start the simulations and power estimation
sim_and_fit(setup=design,                                   # The deisgn specified above
            model_func=hierarchical_model_noncentered,      # A function that returns a pymc3 model
            single_C=True,                                  # Let the simulator know we want the model with a shared C
            iterations=200,                                 # How many simulated experiments do we want?
            condition_func=check_rates,                     # A function that checks our goals (defined above)
            goal_var_names=['va_diff_mean', 'vp_diff_mean', # Limit summary stats to the variables used
                            'vr_diff_mean', 'C_mu', 'wp_mu',# in the goal checking and those we would like
                            'C_sd', 'wp_sd'],               # to the printed after each iteration 
            outfile='single_C.csv'
            )
```

Depending on your machine (especially on whether or not PyMC3 can use your GPU), the simulations will run for a while. On the CPU, they might take some hours. You can look at the output continuously written into the console, as it shows a current estimate based on the simulations so far. Sometimes it is evident that the final result will be of too low power. Then, the simulations can be aborted (Ctrl+C), and the parameters changed (e.g., the number of repetitions or participants can be increased, or perhaps a more sensitive SOA range could be specified). Of course, it could also be clear early on that the power simulation will converge to a value close to one. This indicates that you would be very likely to detect the desired effect (if it was present as specified in the hypothetical setup). However, if you would want to be more economical, you could consider rerunning the simulation with fewer participants (or repetitions, etc.). The results are also written to disk.

## Priors
Currently, the TVATOJ-power uses hardcoded hyper-priors, which are visualized below in Figure 1. These priors are informed by typical measurements reported in the literature but are sufficiently vague to let new data (empirical or simulated) govern the posteriors. Note that these vaguely informed priors are used mainly to enable efficient sampling (e.g., by avoiding problematic extreme proposal). Currently, there is no interface to modify the priors. If you feel the need to used different priors, you will have to go into the hierarchical_model_noncentered function in [tvatojpower.py](./tvatojpower.py).

![Prior Visualizations](prior-visualizations.svg)

 <em>Figure 1. Visualizations of the hyper-priors. Vertical lines mark values reported in the literature (solid lines are  from experiments that used the TVATOJ paradigm, dashed lines are from experiments using traditional whole reports). Further details and references to the cited literature can be found in [Tünnermann (2016, pp. 153–154)](#5).</em>


## Fitting experimental data
After performing power simulations, optimizing the experimental setup, and collecting real data, you might want to fit the experimental data with the TVATOJ model. This module is not intended to be an easy-to-use TOJ fitting library. However, since the power estimation procedure also fits the data with TVATOJ (and hence has that functionality), and since the other TVATOJ implementations are outdated, it might be a good idea to use `hierarchical_model_noncentered` and `fit` from [tvatojpower.py](./tvatojpower.py) to fit your empirical data. There is currently no proper interface to do so and no documentation, which hopefully will change soon.

## TODOs
* Adding an interface to change priors. Perhaps a pymc3 model stub can be created on the user side with the priors attached. The `hierarchical_model_noncentered` function could then check if priors are already defined and only add the defaults if there are none.
* Adding an interface to load and fit empirical data and visualizing results-



## References

<a id="1">Kruschke, J. (2014)</a> Doing Bayesian data analysis: A tutorial with R, JAGS, and Stan. Academic Press.

<a id="2">Bundesen, C. (1998) </a>. A computational theory of visual attention. Philosophical Transactions of the Royal Society of London. Series B: Biological Sciences, 353(1373), 1271–1281.

<a id="3">Tünnermann, J., Krüger, A., & Scharlau, I. (2017)</a>. Measuring attention and visual processing speed by model-based analysis of temporal-order judgments. JoVE (Journal of Visualized Experiments), (119), e54856.

<a id="4">Salvatier, J., Wiecki, T. V., & Fonnesbeck, C. (2016)</a>. Probabilistic programming in Python using PyMC3. PeerJ Computer Science, 2, e55.

<a id="5">Tünnermann, J. (2016)</a>. On the origin of visual temporal-order perception by means of attentional selection. [(PDF)](https://www.researchgate.net/publication/307560676_On_the_origin_of_visual_temporal-order_perception_by_means_of_attentional_selection)

