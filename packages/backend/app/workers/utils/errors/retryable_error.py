from abc import ABC


class RetryableError(Exception, ABC):
    pass
