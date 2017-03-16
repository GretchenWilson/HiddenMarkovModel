from math import log, exp


class log_float(object):
    LOGZERO = None

    def __init__(self, value, mode=None):
        if mode:
            self.value = value
        else:

            try:
                self.value = log(value)

            except ValueError:

                if value < 0:
                    raise (ValueError, "Can't take log of negative number")

                self.value = log_float.LOGZERO

    def __mul__(self, other):

        if not isinstance(other, log_float):
            other = log_float(other)

        return self._elnproduct(self.value, other.value)

    def __rmul__(self, other):
        if not isinstance(other, log_float):
            other = log_float(other)
        return self._elnproduct(self.value, other.value)

    def _elnproduct(self, x, y):
        if x is log_float.LOGZERO or y is log_float.LOGZERO:
            return log_float(0)
        else:
            return log_float(x + y, True)

    def __div__(self, other):
        if not isinstance(other, log_float):
            other = log_float(other)
        if other.value is log_float.LOGZERO:
            raise (ZeroDivisionError, "Can't divide by zero!")
        if self.value is log_float.LOGZERO:
            return log_float(0)
        else:
            return log_float((self.value - other.value), True)

    def __rdiv__(self, other):
        if not isinstance(other, log_float):
            other = log_float(other)
        if self.value is log_float.LOGZERO:
            raise (ZeroDivisionError, "Can't divide by zero!")
        if other.value is log_float.LOGZERO:
            return log_float(0)
        else:
            return log_float((other.value - self.value), True)

    def __add__(self, other):
        if not isinstance(other, log_float):
            other = log_float(other)

        return self._elnsum(self.value, other.value)

    def __radd__(self, other):
        if not isinstance(other, log_float):
            other = log_float(other)

        return self._elnsum(self.value, other.value)

    def _elnsum(self, x, y):

        if x is log_float.LOGZERO or y is log_float.LOGZERO:
            if x is log_float.LOGZERO:
                return log_float(y, True)
            else:
                return log_float(x, True)
        else:

            if x > y:
                return log_float(x + log(1 + exp(y - x)), True)
            else:
                return log_float(y + log(1 + exp(x - y)), True)

    def __cmp__(self, other):
        if not isinstance(other, log_float):
            other = log_float(other)

        if other.value is log_float.LOGZERO or self.value is log_float.LOGZERO:
            if other.value is log_float.LOGZERO:
                if self.value is log_float.LOGZERO:
                    return 0
                return 1
            else:
                return -1
        if self.value > other.value:
            return 1
        if other.value > self.value:
            return -1
        else:
            return 0

    def __str__(self):
        if self.value is log_float.LOGZERO:
            return str(0.0)
        return str(exp(self.value))

    def __repr__(self):
        if self.value is log_float.LOGZERO:
            return str(0.0)
        return str(exp(self.value))
if __name__ == "__main__":

    import doctest
    doctest.testmod()

