import hashlib
import struct
import codecs
import random

ver = 0x20400000
prev_block = "00000000000000000006a4a234288a44e715275f1775b77b2fddb6c02eb6b72f"
mrkl_root = "2dc60c563da5368e0668b81bc4d8dd369639a1134f68e425a9a74e428801e5b8"
time_ = 0x5DB8AB5E
bits = 0x17148EDF

def get_nonce(start_value, end_value, target_str):
    nonce = start_value
    loop = 0

    while nonce < end_value:
        header = (struct.pack("<L", ver) + codecs.decode(prev_block, "hex")[::-1] +
                codecs.decode(mrkl_root, "hex")[::-1] + struct.pack("<LLL", time_, bits, nonce))
        hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()

        if loop < 5:
            print(nonce, codecs.encode(hash[::-1], "hex"))
        
        if hash[::-1] < target_str:
            print('success')
            return [nonce, hash[::-1], True, loop]
        
        nonce += 1
        loop += 1
    
    return [nonce, hash[::-1], False, loop]

def get_random_start(nonce1):
    random.seed()
    return random.randint(nonce1 + 1, nonce1 + 1800000000)

def main():
    exp = bits >> 24
    mant = bits & 0xffffff
    target_hexstr = '%064x' % (mant * (1 << (8*(exp - 3))))
    target_str = codecs.decode(target_hexstr, "hex")

    result = get_nonce(3000000000, 3100000000, target_str)
    success = result[2]

    if success:
        nonce1 = result[0]
        hash = result[1]
        print('Nonce1: ', nonce1)
        print('Hash: ', codecs.encode(hash[::-1], "hex"))
    else:
        print('Nonce1 not found')
        return

    new_start = get_random_start(nonce1)
    result = get_nonce(new_start, new_start + 100000000, target_str)
    success = result[2]
    no_tests = result[3]
    
    print()
    print()
    
    if success:
        nonce2 = result[0]
        hash = result[1]
        print('Nonce2: ', nonce2)
        print('Hash: ', codecs.encode(hash[::-1], "hex"))
        print('Number of tests: ', no_tests)
    else:
        print('Nonce2 not found')
        print('Number of tests: ', no_tests)

    print()

if __name__ == '__main__':
    main()