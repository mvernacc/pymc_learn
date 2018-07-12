"""Rod example of Monte Carlo methods for engineering uncertainty"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pymc3 as pm

# Assume the rod strength is normally distributed
strength_mean = 100.
strength_sd = 5.

# Assume the max. load is normally distributed
load_mean = 85.
load_sd = 10.

# Analytic solution
# Compute the parameters of the margin (strength - load) distribution.
m_mean = strength_mean - load_mean
m_sd = (strength_sd**2 + load_sd**2)**0.5

m_rv = stats.norm(loc=m_mean, scale=m_sd)

# Compute the probability of failure from the cdf
p_fail = m_rv.cdf(0)
print('Analytic failure probability: {:.4f}'.format(p_fail))

# Monte Carlo solution
rod_model = pm.Model()
with rod_model:
	# Setup model
	strength = pm.Normal('strength', mu=strength_mean, sd=strength_sd)
	load = pm.Normal('load', mu=load_mean, sd=load_sd)
	margin = pm.Deterministic('margin', strength - load)

	# Sample & fit
	trace = pm.sample(1000)
pm.traceplot(trace)

m_samples = trace['margin']
p_fail_mc = sum(m_samples < 0) / len(m_samples)
print('Monte-Carlo failure probability: {:.4f}'.format(p_fail_mc))

plt.figure()
ax = plt.subplot(111)
pm.plots.kdeplot(trace['margin'], ax=ax,
	label='Monte Carlo, $p_{{fail}}={:.4f}$'.format(p_fail_mc))
x = np.linspace(m_mean - 4 * m_sd, m_mean + 4 * m_sd, 100)
plt.plot(x, m_rv.pdf(x), linestyle='--', color='black',
	label='Analytic, $p_{{fail}}={:.4f}$'.format(p_fail))
plt.fill_between(x[x <= 0], 0, m_rv.pdf(x[x <= 0]), facecolor='red', alpha=0.5)
plt.axvline(x=0, color='red')
plt.title('Margin')
plt.ylabel('Prob. density')
plt.legend()
plt.ylim([0, plt.ylim()[1]])

plt.show()
