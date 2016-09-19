from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
from urllib import quote, unquote
import requests
import socket
import time

class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)
        self.session = requests.Session()
        self.wait = kwargs.get('wait', 2.0)

    def oracle(self, data, **kwargs):
        somecookie = b64encode(data)
        payload = {'matrix-id': somecookie}
        #self.session.data['matrix_id'] = somecookie

        while 1:
            try:
                response = self.session.post('http://crypto.chal.csaw.io:8001/',
                        stream=False, timeout=5, verify=False, data=payload)
                break
            except (socket.error, requests.exceptions.RequestException):
                logging.exception('Retrying request in %.2f seconds...',
                                  self.wait)
                time.sleep(self.wait)
                continue

        self.history.append(response)

        if not 'exception during AES decryption' in response.text:
            logging.debug('No padding exception raised on %r', somecookie)
            return

        # An HTTP 500 error was returned, likely due to incorrect padding
        raise BadPaddingException

if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)
    matrix_id = 'g61doGe6z0Qh9J7G4SMun9pBJXYiqnw5/PVfQGwf3W9Oj/f1hyEaoIW11aR6eK8PRj8nlG6GpPOlETaZRhbreDg9pnM31T9LCuUc+SQCHao='
    encrypted_cookie = b64decode(matrix_id)

    padbuster = PadBuster()
    bz = 16
    cookie = padbuster.decrypt(encrypted_cookie, block_size=bz, iv=bytearray(bz))

    print('Decrypted somecookie: %s => %r' % (matrix_id, cookie))
#g61doGe6z0Qh9J7G4SMun9pBJXYiqnw5/PVfQGwf3W9Oj/f1hyEaoIW11aR6eK8PRj8nlG6GpPOlETaZRhbreDg9pnM31T9LCuUc+SQCHao= 
#=> bytearray(b'\x12\x96\x82\xbbW!\x0e\xd8\xf6\xd0\xd6\xf3I\xa22\xccflag{what_if_i_told_you_you_solved_the_challenge}\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f')
