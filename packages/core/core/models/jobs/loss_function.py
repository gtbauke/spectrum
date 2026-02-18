from enum import StrEnum


class LossFunction(StrEnum):
    MSE = "MSE"
    GAUSSIAN = "Gaussian"
    BERNOULLI = "Bernoulli"
    POISSON = "Poisson"
