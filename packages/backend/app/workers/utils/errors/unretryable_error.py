from abc import ABC


class UnretryableError(Exception, ABC):
    pass
