from passlib.context import CryptContext


class EncryptionCls:
    def __init__(self):
        self.crypt_cls = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify(self, password: str, hashed_password: str) -> bool:
        return self.crypt_cls.verify(password, hashed_password)

    def encrypt(self, password: str) -> str:
        return self.crypt_cls.hash(password)


encryption_cls = EncryptionCls()
