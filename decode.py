from codec import Decoder
from sys import argv

# ex) python decode.py encoded decoded.png
dec = Decoder(argv[1], argv[2])
dec.decode()
