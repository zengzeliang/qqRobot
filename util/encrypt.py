import base64

class Encrypt:
    @staticmethod
    def decrypt(enStr):
        deStr = base64.b64decode(enStr).decode('utf-8')
        return deStr