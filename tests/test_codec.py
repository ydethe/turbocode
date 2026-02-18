import random

from pyturbocode.TurboCodec import TurboCodec


def test_codec():
    random.seed(4651354)

    codec = TurboCodec()

    data = b"Hello, world! " * 10
    enc = codec.encode(data)

    mod_enc = enc[:15] + random.randbytes(5) + enc[20:]
    data_decoded = codec.decode(mod_enc)

    assert data_decoded == data


if __name__ == "__main__":
    test_codec()
