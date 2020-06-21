import numpy as np


# header info
MAGIC_NUMBER = (ord('H') << 8) + ord('C')
BYTES_M = 2
BYTES_H = 2
BYTES_W = 2


class _CodecBase(object):
    def __init__(self):
        self._histogram = np.ones(256, np.uint64)
        self._histogram_cumulative = np.cumsum(self._histogram)

    def _update_histogram(self, value):
        self._histogram[value] += 1
        self._histogram_cumulative[value:] += 1
