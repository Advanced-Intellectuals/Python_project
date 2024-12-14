import bcrypt


class PasswordHasher():
    def hash(self, password: str):
        salt = bcrypt.gensalt(10)
        bytepw = password.encode('utf-8')
        return bcrypt.hashpw(bytepw, salt).decode('utf-8')

    def compare(self, password: str, hash: str):
        bytepw = password.encode('utf-8')
        bytehash = hash.encode('utf-8')
        return bcrypt.checkpw(bytepw, bytehash)
