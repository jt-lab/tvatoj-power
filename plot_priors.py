import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import scipy.stats
import numpy as np

f, axs = plt.subplots(2, 3, figsize=(8, 4))

######## C parameters ########

x_min = 0.0
x_max = 0.2

mean = 0.08
std = 0.05

x = np.linspace(x_min, x_max, 100)
y = scipy.stats.norm.pdf(x,mean,std)

axs[0, 0].plot(x,y, color='coral')
axs[0, 0].grid()
axs[0, 0].set_xlim(x_min,x_max)
axs[0, 0].set_ylim(0,15)
axs[0, 0].set_title('Prior on $C$ parameters\n group means in 1/ms\n $\\bf{Normal(\mu = 0.08, \sigma = 0.05):}$',fontsize=10)
axs[0, 0].set_xlabel('$C$')

line_length = 7.5

### Ásgeirsson et al. (2015)
Asgeirsson_Cs = [0.1036, 0.0838, 0.09169, 0.08267]
Asgeirsson_Cs_lines = LineCollection(
    ([[C, 0], [C, line_length]] for C in Asgeirsson_Cs), label='Ásgeirsson et al. (2015)', alpha=0.5, linestyle=':')
axs[0, 0].add_collection(Asgeirsson_Cs_lines)

### McAvinue et al. (2015)
McAvinue_Cs = [0.03206, 0.04035]
McAvinue_Cs_lines = LineCollection(([[C, 0], [C, line_length]] for C in McAvinue_Cs),
                                   label='McAvinue et al. (2015)', alpha=0.5, linestyle=':', color='green')
axs[0, 0].add_collection(McAvinue_Cs_lines)

### Caspersen & Habekost (2013)
Caspersen_Cs = [0.0369, 0.04385]
Caspersen_Cs_lines = LineCollection(([[C, 0], [C, line_length]] for C in Caspersen_Cs),
                                   label='Caspersen & Habekost (2013)', alpha=0.5, linestyle=':', color='blue')
axs[0, 0].add_collection(Caspersen_Cs_lines)

### Wilms et al. (2013)
Wilms_Cs = [0.0702, 0.0605, 0.0539]
Wilms_Cs_lines = LineCollection(([[C, 0], [C, line_length]] for C in Wilms_Cs),
                                   label='Wilms et al. (2013)', alpha=0.5, linestyle=':', color='purple')
axs[0, 0].add_collection(Wilms_Cs_lines)



### McAvinue et al. (2012)
McAvinue2_Cs = [0.046, 0.064, 0.061, 0.057, 0.051, 0.038, 0.038, 0.029]
McAvinue2_Cs_lines = LineCollection(([[C, 0], [C, line_length]] for C in McAvinue2_Cs),
                                   label='Vangkilde et al. (2012)', alpha=0.5, linestyle=':', color='pink')
axs[0, 0].add_collection(McAvinue2_Cs_lines)


### Vangkilde et al. (2011)
Vangkilde_Cs = [0.070, 0.055, 0.051]
Vangkilde_Cs_lines = LineCollection(([[C, 0], [C, line_length]] for C in Vangkilde_Cs),
                                   label='McAvinue et al. (2011)', alpha=0.5, linestyle=':', color='red')
axs[0, 0].add_collection(Vangkilde_Cs_lines)



### Finke et al. (2005)
Finke_Cs = [0.02448, 0.02344]
Finke_Cs_lines = LineCollection(([[C, 0], [C, line_length]] for C in Finke_Cs),
                                   label='Finke et al. (2005)', alpha=0.5, linestyle=':', color='red')
axs[0, 0].add_collection(Finke_Cs_lines)

### Tünnermann et al. (2015)
Tuennermann2015_Cs = [0.05736, 0.05936, 0.06377, 0.06196, 0.05853, 0.06306, 0.05816, 0.05974]
Tuennermann2015_Cs_lines = LineCollection(([[C, 0], [C, line_length]] for C in Tuennermann2015_Cs),
                                   label='Tünnermann et al. (2015)', alpha=0.5, linestyle=':', color='orange')
axs[0, 0].add_collection(Tuennermann2015_Cs_lines)


### Krüger et al. (2016)
Krueger2016_Cs = [0.0497, 0.0476, 0.0552, 0.0603, 0.0407, 0.03869, 0.032, 0.0354]
Krueger2016_Cs_lines = LineCollection(([[C, 0], [C, line_length]] for C in Krueger2016_Cs),
                                   label='Krüger et al. (2016)', alpha=0.5, color='green')
axs[0, 0].add_collection(Krueger2016_Cs_lines)

### Tünnermann & Scharlau (2016)
Tuennermann2016_Cs = [0.07239, 0.08395, 0.13243, 0.05608, 0.12875, 0.09295, 0.07226, 0.06014]
Tuennermann2016_Cs_lines = LineCollection(([[C, 0], [C, line_length]] for C in Tuennermann2016_Cs),
                                   label='Tünnermann & Scharlau (2016)', alpha=0.5, color='blue')
axs[0, 0].add_collection(Tuennermann2016_Cs_lines)

### Tünnermann et al. (2017)
Tuennermann2017_Cs = [0.06711, 0.08579, 0.06494, 0.06232, 0.06507, 0.06079]
Tuennermann2017_Cs_lines = LineCollection(([[C, 0], [C, line_length]] for C in Tuennermann2017_Cs),
                                   label='Tünnermann et al. (2017)', alpha=0.5, color='purple')
axs[0, 0].add_collection(Tuennermann2017_Cs_lines)


handles, labels = axs[0, 0].get_legend_handles_labels()

axs[0, 2].set_axis_off()
axs[1, 2].set_axis_off()
axs[0, 2].legend(handles, labels, loc='upper left',
          fancybox=True, shadow=True, ncol=1, fontsize=7)

#f.subplots_adjust(bottom=0.5)

x_min = 0.0
x_max = 0.2
scale = 0.1
x = np.linspace(x_min, x_max, 100)
y = scipy.stats.halfcauchy.pdf(x,0, scale)

axs[0, 1].plot(x,y, color='coral', linestyle=':')
axs[0, 1].grid()
axs[0, 1].set_xlim(x_min,x_max)
axs[0, 1].set_ylim(0,10)
axs[0, 1].set_title('Prior on $C$ parameter\n group standard deviations in 1/ms\n $\\bf{HalfCauchy(scale = 0.01):}$',fontsize=10)
axs[0, 1].set_xlabel('$C$')

######## w parameters ########


x_min = 0.0
x_max = 1

mean = 0.5
std = 0.2

x = np.linspace(x_min, x_max, 100)
y = scipy.stats.norm.pdf(x,mean,std)

axs[1, 0].plot(x,y, color='teal')
axs[1, 0].grid()
axs[1, 0].set_xlim(x_min,x_max)
axs[1, 0].set_ylim(0,2.5)
axs[1, 0].set_title('Prior on $w_p$ parameter\n group means\n $\\bf{Normal(\mu = 0.5, \sigma = 0.2):}$',fontsize=10)
axs[1, 0].set_xlabel('$w_p$')

line_length = 1.5

### Tünnermann et al. (2015)
Tuennermann2015_wps = [0.6, 0.52, 0.61, 0.59]
Tuennermann2015_wps_lines = LineCollection(
    ([[C, 0], [C, line_length]] for C in Tuennermann2015_wps), label='Tünnermann et al. (2015)', alpha=0.5, color='orange', linestyle=':')
axs[1, 0].add_collection(Tuennermann2015_wps_lines)


### Krüger et al. (2016)
Krueger2016_wps = [0.49, 0.51, 0.39, 0.64, 0.58]
Krueger2016_wps_lines = LineCollection(
    ([[C, 0], [C, line_length]] for C in Krueger2016_wps), label='Krüger et al. (2016)', alpha=0.5, color='green')
axs[1, 0].add_collection(Krueger2016_wps_lines)


### Tünnermann & Scharlau (2016)
Tuennermann2016_wps = [0.51, 0.67, 0.25, 0.77, 0.64, 0.5]
Tuennermann2016_wps_lines = LineCollection(
    ([[C, 0], [C, line_length]] for C in Tuennermann2016_wps), label='Tünnermann & Scharlau (2016)', alpha=0.5, color='blue')
axs[1, 0].add_collection(Tuennermann2016_wps_lines)


### Tünnermann et al. (2017)
Tuennermann2017_wps = [0.59, 0.52, 0.54, 0.42]
Tuennermann2017_wps_lines = LineCollection(
    ([[C, 0], [C, line_length]] for C in Tuennermann2017_wps), label=' Tünnermann et al. (2017)', alpha=0.5, color='purple')
axs[1, 0].add_collection(Tuennermann2017_wps_lines)

handles, labels = axs[1, 0].get_legend_handles_labels()

axs[1, 2].legend(handles, labels, loc='upper left',
          fancybox=True, shadow=True, ncol=1, fontsize=7)



x_min = 0.0
x_max = 0.5
scale = 0.2
x = np.linspace(x_min, x_max, 100)
y = scipy.stats.halfcauchy.pdf(x,0, scale)

axs[1, 1].plot(x,y, color='teal', linestyle=':')
axs[1, 1].grid()
axs[1, 1].set_xlim(x_min,x_max)
axs[1, 1].set_ylim(0,5)
axs[1, 1].set_title('Prior on $w_p$ parameter\n group standard deviations\n $\\bf{HalfCauchy(scale = 0.02):}$',fontsize=10)
axs[1, 1].set_xlabel('$w_p$')

plt.tight_layout()
plt.savefig("prior-visualizaions.svg")
plt.show()
