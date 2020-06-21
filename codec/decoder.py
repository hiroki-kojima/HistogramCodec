import carryless_rangecoder as cr
from io import BytesIO
from imageio import imwrite
import numpy as np
from .common import _CodecBase
from .common import MAGIC_NUMBER
from .common import BYTES_M
from .common import BYTES_H
from .common import BYTES_W


class Decoder(_CodecBase):
    def __init__(self, input, output):
        super(Decoder, self).__init__()
        self.stream = BytesIO(open(input, 'rb').read())
        self._output = output

        assert int.from_bytes(self.stream.read(BYTES_M), 'big') == MAGIC_NUMBER
        self._width = int.from_bytes(self.stream.read(BYTES_W), 'big')
        self._height = int.from_bytes(self.stream.read(BYTES_H), 'big')
        self._image = np.empty((self._height, self._width), np.uint8)

        self._decoder = cr.Decoder(self.stream)
        self.stream.seek(BYTES_M + BYTES_W + BYTES_H)

    def _decode_per_pixel(self):
        return self._decoder.decode(
            self._histogram.tolist(),
            self._histogram_cumulative.tolist()
        )

    def decode(self):
        self._decoder.start()

        for y in range(self._height):
            for x in range(self._width):
                value = self._decode_per_pixel()
                self._update_histogram(value)
                self._image[y, x] = value

        imwrite(self._output, self._image)
