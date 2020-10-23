# TVATOJ-power

TVATOJ-power is a Python module plus examples for performing Bayesian power estimation ([Kruschke, 2014](#1)) for TVA-based ([Bundesen, 1998](#2)) TOJ experiments (as introduced in [Tünnermann, Krüger, & Scharlau, 2017](#3)). In particular, it contains a Python with [PyMC3](https://github.com/pymc-devs/pymc3) ([Salvatier et al., 2016](#4)) port of the [Tünnermann, Krüger, & Scharlau's (2017)](#3) R with JAGS examples (example_power_exp_1.py, example_power_exp_2.py). In addition, two new examples were added.

## Background
In classic statistics power is probability of avoiding type-II errors. Or in other words, it is the probability that a hypothesis test correctly rejects the null-hypothesis, given that the alternative hypothesis is true, which researchers typically want to maximize by using sufficiently large samples. However, the TVATOJ framework uses a Bayesian statsitical framework. In Bayesian statistics, there is no inherent need for binary decision (reject or not ) and consequently no concept of power in the classical sense. However, in broader sense, reasearcher might want to maximize to detect whatever kind of differences they are interested in. Along these lines, Bayesian power simulations can be performed [Kruschke, 2014](#1). The idea is to repeatedly simulate data with model (purely hypothetical or based on earlier findings), fit it, and determine for how many simulations the research goal was reached. This type of power anaylsis is highly flexible, as not only the number of participants can be varied to tweap power, but also other experimental parameters, such as, in the present context, the magnitudes and spacing of the SOAs and how their repetitions are distributed. This python module contains the procedure (with simualtion and fitting) to perform such repeated simualtation and convert them in to a Bayesian estimate of powet (i.e., it returns the probability of reaching the research goal along with 95 % highest density intervals).

## Dendencies
* [PyMC3](https://github.com/pymc-devs/pymc3) 
* [coloredlogs](https://github.com/xolox/python-coloredlogs) (optional)

## Installation
* Install the dependencies listed above, e.g.: `conda install -c conda-forge pymc3`
* Clone the repositors: `git clone https://github.com/jeti182/tvatoj-power.git`

## Module & Examples
You should then find the following components:
* tvatojpower.py contains the psychometric function, setup of the  PyMC3 model, and the overall simulation and power estimation procedure.
* example_power_exp_1.py: Example power simulation for a *within*-participants design with an attention and a neutral condition.
* example_power_exp_2.py: Example power simulation for a *between*-participants design with an attention and a neutral condition.
* example_power_single_C.py Example power simulation for a within-participants design with an attention and a neutral condition, but both conditions share TVA's C parameter
* example_power_one_condition.py: xample power simulation for an experiment with a single condition (and attention being directed to the probe stimulus).


## Running the examples
* e.g., python example_power_exp_1.py
* Detailed instructions coming soon.

## Setting up custom power simulations
* See examples, detailed instructions coming soon.

## Priors
Currently, the tvattoj-power uses hardcoded hyper-priors, which are visualized belwo in Figure 1. These priors are informed by typical measurements reported in the literature but are sufficiently vague to let new data (empirical or simulated) govern the posteriors. Note that these vaguely informed priors are used mainly to enable efficient sampling (e.g., by avoiding problematic extreme proposal). Currently, there is no interface to modify the priors. If you feel the need to used different priors, you will have to go into the hierarchical_model_noncentered function in [tvatojpower.py](./tvatojpower.py).

![Prior Visualizations](prior-visualization.svg)
 <em>Figure 1. Visualizations of the hyper-priors. Vertical lines mark values reported in the literature (solid lines are  from experiments that used the TVATOJ paradigm, dashed lines are from experiments using traditional whole repors). Further details and references to the cited literature can be found in [Tünnermann (2016, pp.153--154)](#5).  </em>



## References

<a id="1">Kruschke, J. (2014)</a> Doing Bayesian data analysis: A tutorial with R, JAGS, and Stan. Academic Press.

<a id="2"> Bundesen, C. (1998) </a>. A computational theory of visual attention. Philosophical Transactions of the Royal Society of London. Series B: Biological Sciences, 353(1373), 1271-1281.

<a id="3">Tünnermann, J., Krüger, A., & Scharlau, I. (2017)</a>. Measuring attention and visual processing speed by model-based analysis of temporal-order judgments. JoVE (Journal of Visualized Experiments), (119), e54856.

<a id="4">Salvatier, J., Wiecki, T. V., & Fonnesbeck, C. (2016)</a>. Probabilistic programming in Python using PyMC3. PeerJ Computer Science, 2, e55.

<a id="5">Tünnermann, J. (2016)</a>. On the origin of visual temporal-order perception by means of attentional selection. [(PDF)](https://www.researchgate.net/publication/307560676_On_the_origin_of_visual_temporal-order_perception_by_means_of_attentional_selection)

