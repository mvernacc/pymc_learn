from math import log
def lognormal_params(m, v):
    """ See https://en.wikipedia.org/wiki/Log-normal_distribution#Notation """
    return log(m / (1 + v / m**2)**0.5), log(1 + v / m**2)
