""" Example of Monte Carlo method applied to solid rocket motor chamber pressure uncertainty.

We are trying to predict the expected chamber pressure of a new solid rocket motor design,
and to understand the uncertainty of this estimate. We assume that distributions for the
input factors (e.g. propellant properties) have been estimated from small-scale experiments.
We wish to determine how uncertainty in these inputs propagates into uncertainty
in the (time-average) chamber pressure.

We use the STAR-27 Apogee Motor as an example - nominal values are taken from Rocket Propulsion
Elements, 8th Edition, table 12-3; distributions are my wild guesses. 


"""

import numpy as np
import matplotlib.pyplot as plt
import pymc3 as pm

# Define the model
solid_rocket_model = pm.Model()
with solid_rocket_model:
    # Distributions on the input variables
    # Burning area, time averaged [units: meter**2]
    A_b = pm.Normal('A_b', mu=0.899, sd=0.01)
    # A_b = 0.899
    # Throat area [units: meter**2]
    A_t_scaled = pm.Normal('A_t_scaled', mu=3.81, sd=0.03)
    A_t = A_t_scaled * 1e-3
    # A_t = 3.81e-3
    # Propellant solid density [units: kilogram meter**-3]
    rho_b = pm.Normal('rho_b', mu=1774, sd=20)
    # rho_b = 1774.
    # Characteristic velocity [units: meter second**-1]
    c_star = 1579.
    # Burn rate coefficient [units: meter second**-1 pascal**-n]
    a_scaled = pm.Lognormal('a_scaled', mu=2.16, sd=0.058)
    a = a_scaled * 1e-5
    # Burn rate exponent [units: dimensionless]
    n = pm.Beta('n', mu=0.28, sd=0.01)

    # Chamber pressure model
    # Chamber pressure [units: megapascal]
    p_c = pm.Deterministic('p_c', ((A_b / A_t) * rho_b * c_star * a)**(1 / (1-n)) * 1e-6)

    # Sample from the model
    trace = pm.sample(1000)
    pm.backends.ndarray.save_trace(trace, 'solid_rocket_example_traces', overwrite=True)
pm.traceplot(trace)
plt.show()
