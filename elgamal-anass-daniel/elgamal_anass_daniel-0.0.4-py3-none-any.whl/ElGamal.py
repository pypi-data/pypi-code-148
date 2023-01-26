import random
import math
from time import time

CHECK_PRIMIRIVE_ROOTS = False

def timer(func):
    # A simple decorator for benchmarking/performance purposes
    def wrapper(*args, **kwargs):
        init_t = time()
        func_return = func(*args, **kwargs)
        end_t  = time()

        print(f'[Timer] ( {func.__qualname__} ) > {end_t - init_t} seconds')
        return func_return
    
    return wrapper


class ElGamal(object):
    def __init__(self) -> None:
        pass
    
    def FastModExp(self, g: int , e: int, p: int) -> int:
        """Returns the value of g^e (mod p)

        Args:
            g (int): Primitive root (mod p)
            e (int): Power
            p (int): Prime number

        Returns:
            int: g^e (mod p)
        """

        result = 1 # Output value
        y = g % p  # Sequence y_i, initializing y_0 = g % p

        while e: # While e > 0
            if e & 1: # Bit '1' and not '0'
                result = (result * y) % p # Pel productori
            y = (y ** 2) % p # y_i+1 = (y_i)^2 Quadrat de l'anterior
            e >>= 1          # Right-Shift 
        
        return result

    @timer
    def getPrimitiveRoots(self, p: int) -> list:
        """Returns the primitive roots of p

        Args:
            p (int): Prime number

        Returns:
            list: Primitive roots of p
        """
        
        # NOTE: range(1, p) returns a sequence {1, ..., p-1}

        # coprimes = {num for num in range(1, p) if math.gcd(num, p) == 1}
        # primitive_roots = []
        # for g in range(1, p):

        #     if coprimes == {self.FastModExp(g, e, p) for e in range(1, p)}:
        #         primitive_roots.append(g)
        
        # return primitive_roots

        primitive_roots = []
        for g in range(2, p):
            for e in range(1, p):
                if self.FastModExp(g, e, p) == 1:
                    if e != p-1:
                        break # Provem la seguent arrel
                    else:
                        primitive_roots.append(g)

        return primitive_roots

    @timer
    def getFirstPrimitiveRoot(self, p: int) -> int:
        for g in range(2, p): # De {2, ..., p-1}
            for e in range(1, p): # De {1, ..., p-1}
                # print((g, e), '->', self.FastModExp(g, e, p))
                
                if self.FastModExp(g, e, p) == 1:
                    if e != p-1:
                        break # Provem la seguent arrel
                    else:
                        return g

        return None
    
    @timer
    def getFirstPrimitiveRoot_v2(self, p: int) -> int:
        """Returns the primitive roots of p

        Args:
            p (int): Prime number

        Returns:
            int: The first primitive root of p, None if there is no such primitive root
        """

        g = 2
        while g < p:
            e = 1
            while e < p:
                if self.FastModExp(g, e, p) == 1:
                    if e != p-1:
                        break # Not a primitive root, we test the next one
                    else:
                        return g
                e += 1
            g += 1
        
        return None

    def isPrimitive(self, g: int, p: int) -> bool:
        """Checks whether g is a primitive root (mod p)

        Args:
            g (int): Primitive root (mod p) to be checked
            p (int): Prime number

        Returns:
            bool: True if g is a primitive root (mod p), False otherwise
        """

        for e in range(1, p): # De {1, ..., p-1}                
            if self.FastModExp(g, e, p) == 1:
                if e != p-1:
                    return False
                else:
                    return True

        return False



class Message(ElGamal):
    def __init__(self, msg:str = None, encrypted_msg: list = []) -> None:
        super().__init__()
        self.msg = msg
        self.encrypted_msg = encrypted_msg

    def __repr__(self) -> str:
        return f'Message({self.msg})'
    
    def encrypt(self, g: int, g_x: int, p: int) -> str:
        """Encrypts the message following the ElGamal encryption

        Args:
            g (int): Primitive root of p
            g_x (int): Primitive root of p to the x (secret power)
            p (int): Prime number

        Raises:
            ValueError: 
                If there is no such message to be encrypted
                If prime [p] is minor than 128 (ASCII encoding)
                iF [g] is not a primitive root of [p]

        Returns:
            msg: The encrypted message -> 'g_y-k1|g_y-k2|...|g_y-kn'
        """

        if p < 128:
            raise ValueError('Please, the modular prime has to be major than 127 (ASCII encoding)')

        else:
            if self.msg:
                if CHECK_PRIMIRIVE_ROOTS and not self.isPrimitive(g, p):
                    raise ValueError('Please, set a valid [g] primitive root of [p]')

                else:
                    encrypted_msg = []

                    y   = random.randint(2, p-1)
                    g_y = self.FastModExp(g, y, p)
                    for char in self.msg:
                        k   = (ord(char) * self.FastModExp(g_x, y, p)) % p
                        encrypted_msg.append((g_y, k))
                    
                    encrypted_msg = '|'.join([ f'{g_y}-{k}' for g_y, k in encrypted_msg])
                    self.encrypted_msg = encrypted_msg
                    return encrypted_msg
            
            raise ValueError('Please, set a message to be encrypted')

    def decrypt(self, x: int, p: int, msg:str = None) -> str:
        """Returns the decrypted message following the ElGamal encryption

        Args:
            x (int): Private key
            p (int): Prime number
            msg (str): Message to be decrypted -> 'g_y-k1|g_y-k2|...|g_y-kn'

        Raises:
            ValueError: If there is no such encrypted message

        Returns:
            str: The decrypted message
        """

        if self.encrypted_msg or msg:
            msg = msg if msg else self.encrypted_msg

            msg = [encrypted_char.split('-') for encrypted_char in msg.split('|')] # Decoding of the message
            msg = [(int(g_y), int(k)) for g_y, k in msg]
    
            decrypted_msg = []
            for g_y, k in msg:
                msg_char = (self.FastModExp(g_y, p-1-x, p) * k) % p
                decrypted_msg.append(chr(msg_char))

            self.msg = ''.join(decrypted_msg)
            return self.msg
        
        else:
            raise ValueError('Please, set an encrypted message to be decrypted')


if __name__ == '__main__':

    msg1 = Message("[Msg-1] Hola que tal estas! :D")
    msg1.encrypt(g=2, g_x=1024, p=8820220609)
    # print(msg1.encrypted_msg)
    print(msg1.decrypt(x=10, p=8820220609))
    
    msg2 = Message("[Msg-2] És un bon exemple per demostrar la codificació ASCII, accents, caràcters i signes especials *[]-~ç) 😂😂🥶🥶🔥")
    msg2.encrypt(g=2, g_x=1024, p=8820220609)
    # print(msg2.encrypted_msg)
    print(msg2.decrypt(x=10, p=8820220609))

    msg3 = Message("[Msg-3] És un bon exemple per demostrar la codificació ASCII, accents, caràcters i signes especials *[]-~ç) 😂😂🥶🥶🔥")
    msg3.encrypt(g=115, g_x=4, p=173)
    # print(msg3.encrypted_msg)
    print(msg3.decrypt(x=70, p=173))