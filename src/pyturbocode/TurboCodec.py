"""
API simple et facile à utiliser pour les Turbo Codes
Wrapper autour de CommPy avec interface bytes → bytes
"""

import numpy as np
from commpy.channelcoding import Trellis, turbo_encode, turbo_decode
from commpy.channelcoding.interleavers import RandInterlv


class TurboCodec:
    """
    Codec Turbo simple avec interface bytes → bytes

    Exemple d'utilisation:
    >>> codec = TurboCodec()
    >>> message = b"Hello World!"
    >>> encoded = codec.encode(message)
    >>> decoded = codec.decode(encoded, snr_db=3.0)
    >>> assert message == decoded
    """

    def __init__(self, constraint_length: int = 3, num_iterations: int = 8):
        """
        Initialise le codec turbo

        Args:
            constraint_length: Longueur de contrainte (K), par défaut 3
            num_iterations: Nombre d'itérations pour le décodage
        """
        self.K = constraint_length
        self.num_iterations = num_iterations

        # Configuration du treillis pour code RSC
        memory = np.array([constraint_length - 1])
        g_matrix = np.array([[0o7, 0o5]])  # Générateurs polynomiaux

        self.trellis1 = Trellis(memory, g_matrix, feedback=0o7, code_type="rsc")
        self.trellis2 = Trellis(memory, g_matrix, feedback=0o7, code_type="rsc")

    def encode(self, data: bytes) -> bytes:
        """
        Encode des données avec le turbo code

        Args:
            data: Données à encoder (bytes)

        Returns:
            Données encodées (bytes) avec métadonnées
        """
        # Convertir en bits
        message_bits = self._bytes_to_bits(data)
        original_length = len(message_bits)

        # Créer un entrelaceur
        interleaver = RandInterlv(length=original_length, seed=1346)

        # Encoder
        sys_stream, non_sys_stream_1, non_sys_stream_2 = turbo_encode(
            msg_bits=message_bits,
            trellis1=self.trellis1,
            trellis2=self.trellis2,
            interleaver=interleaver,
        )

        # Créer un paquet avec métadonnées
        # Format: [longueur_originale N: 4 bytes][interleaver: N*4 bytes][données encodées]
        packet = bytearray()

        # Longueur originale (32 bits)
        packet.extend(original_length.to_bytes(4, "big"))  # len: 4

        # Données encodées
        packet.extend(self._bits_to_bytes(sys_stream))  # len: 13
        packet.extend(self._bits_to_bytes(non_sys_stream_1))  # len: 13
        packet.extend(self._bits_to_bytes(non_sys_stream_2))  # len: 27

        return bytes(packet)

    def decode(self, encoded_data: bytes) -> bytes:
        """
        Décode des données encodées avec le turbo code

        Args:
            encoded_data: Données encodées (bytes) avec métadonnées

        Returns:
            Données décodées (bytes)
        """
        # Extraire les métadonnées
        offset = 0

        # Longueur originale
        original_length = int.from_bytes(encoded_data[offset : offset + 4], "big")
        offset += 4

        # Créer un entrelaceur
        interleaver = RandInterlv(length=original_length, seed=1346)

        # Données encodées
        encoded_bytes = encoded_data[offset:]
        encoded_bits = self._bytes_to_bits(encoded_bytes)

        sys_symbols = encoded_bits[:original_length]
        non_sys_symbols_1 = encoded_bits[original_length : 2 * original_length]
        non_sys_symbols_2 = encoded_bits[2 * original_length : original_length * 3]

        # Décodage
        decoded_bits = turbo_decode(
            sys_symbols,
            non_sys_symbols_1,
            non_sys_symbols_2,
            self.trellis1,
            1,
            self.num_iterations,
            interleaver,
        )

        # Tronquer à la longueur originale
        decoded_bits = decoded_bits[:original_length]

        # Convertir en bytes
        return self._bits_to_bytes(decoded_bits)

    @staticmethod
    def _bytes_to_bits(data: bytes) -> np.ndarray:
        """Convertit bytes en bits"""
        bits: list[int] = []
        for byte in data:
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return np.array(bits, dtype=int)

    @staticmethod
    def _bits_to_bytes(bits: np.ndarray) -> bytes:
        """Convertit bits en bytes"""
        remainder = len(bits) % 8
        if remainder != 0:
            bits = np.append(bits, np.zeros(8 - remainder, dtype=int))

        byte_array = bytearray()
        for i in range(0, len(bits), 8):
            byte_val = 0
            for j in range(8):
                byte_val = (byte_val << 1) | int(bits[i + j])
            byte_array.append(byte_val)

        return bytes(byte_array)
