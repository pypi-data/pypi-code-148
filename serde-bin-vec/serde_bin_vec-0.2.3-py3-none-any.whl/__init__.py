__version__ = '0.2.3'
import struct
import binascii


num_bytes = 16


def save(uuid, vector: list[float], filename='data.bin'):
    f = open(filename, 'ab')
    f.write(struct.pack('B'*num_bytes, *uuid))
    data = [struct.pack('d', f) for f in vector]
    [f.write(d) for d in data]
    f.close()


def read_all(filename='data.bin'):
    f = open(filename, 'rb')
    output = []
    Is = 'B'*num_bytes
    Ds = 'd'*512
    vec_len = 512*8
    while True:
        try:
            tmp = [binascii.hexlify(bytearray(struct.unpack(Is, f.read(16)))),
                   struct.unpack(Ds, f.read(vec_len))]
            output.append(tmp)
        except:
            break
    f.close()
    return output


def save_all(list_of_lists, filename='data.bin'):
    open(filename, 'w').write('')
    for item in list_of_lists:
        save(item[0], item[1], filename)
