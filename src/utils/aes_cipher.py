from base64 import b64decode, b64encode
from hashlib import md5
from typing import Union

from Crypto import Random
from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key: str) -> None:
        self.bs = AES.block_size
        self.key = key.encode()

    def encrypt(self, message: str) -> bytes:
        salt = Random.new().read(8)
        key_iv = self._bytes_to_key(self.key, salt, 32 + 16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return b64encode(b"Salted__" + salt + aes.encrypt(self._pad(message.encode())))

    def decrypt(self, encrypted: str) -> bytes:
        encrypted_decoded = b64decode(encrypted)
        assert encrypted_decoded[0:8] == b"Salted__"
        salt = encrypted_decoded[8:16]
        key_iv = self._bytes_to_key(self.key, salt, 32 + 16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return self._unpad(aes.decrypt(encrypted_decoded[16:]))

    def _pad(self, data: bytes) -> bytes:
        length = self.bs - (len(data) % self.bs)
        return data + (chr(length) * length).encode()

    @staticmethod
    def _unpad(data: bytes) -> bytes:
        return data[
            : -(data[-1] if type(data[-1]) == int else ord(Union[str, bytes](data[-1])))
        ]

    @staticmethod
    def _bytes_to_key(data: bytes, salt: bytes, output: int = 48) -> bytes:
        assert len(salt) == 8, len(salt)
        data += salt
        key = md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = md5(key + data).digest()
            final_key += key
        return final_key[:output]
