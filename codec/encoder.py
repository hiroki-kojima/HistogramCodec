import carryless_rangecoder as cr
from io import BytesIO
from imageio import imread
from .common import _CodecBase
from .common import MAGIC_NUMBER
from .common import BYTES_M
from .common import BYTES_H
from .common import BYTES_W


class Encoder(_CodecBase):
    def __init__(self, input, output):
        super(Encoder, self).__init__()
        self._stream = BytesIO()
        self._image = imread(input)
        self._output = output
        self._height, self._width = self._image.shape

        self._stream.write(MAGIC_NUMBER.to_bytes(BYTES_M, 'big'))
        self._stream.write(self._width.to_bytes(BYTES_W, 'big'))
        self._stream.write(self._height.to_bytes(BYTES_H, 'big'))

        self._encoder = cr.Encoder(self._stream)

    def _encode_per_pixel(self, value):
        self._encoder.encode(
            self._histogram.tolist(),
            self._histogram_cumulative.tolist(),
            value
        )

    def encode(self):
        for y in range(self._height):
            for x in range(self._width):
                value = self._image[y, x]
                self._encode_per_pixel(value)
                self._update_histogram(value)

        self._encoder.finish()
        decoded = self._stream.getvalue()
        open(self._output, 'wb').write(decoded)

        return len(decoded) * 8 / self._image.size
