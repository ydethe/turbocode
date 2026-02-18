from pyturbocode.TurboCodec import TurboCodec


def test_codec():
    codec = TurboCodec()

    data = b"Hello, world!" * 10
    enc = codec.encode(data)

    data_decoded = codec.decode(enc)

    assert data_decoded == data


if __name__ == "__main__":
    test_codec()
