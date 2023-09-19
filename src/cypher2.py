def cypher_gen(seed: int) -> int:
    length = len(format(seed, 'b'))
    possible_permutations = 2 ** length
    count = 0
    while count < possible_permutations:
        count += 1
        new_bit = (seed >> 1 ^ seed) & 1
        seed = seed >> 1 | new_bit << (length - 1)
        yield seed & 1

def crypt(key: str, to_crypt: bytes, min_cyphers: int, extra_cyphers: int) -> bytes:
    num_key = int.from_bytes(bytes(key, 'utf-8'))
    cyphers = [cypher_gen(num_key)]
    
    additional_cyphers = int(''.join([str(next(cyphers[-1])) for _ in range(256)]), 2) % (extra_cyphers + 1)
    
    for _ in range(min_cyphers + additional_cyphers):
        new_seed = int(''.join([str(next(cyphers[-1])) for _ in range(256)]), 2)
        cyphers.append(cypher_gen(new_seed))
    
    del cyphers[0]
    print(f'Es werden {len(cyphers)} cyphern verwendet')
    message = b''
    for byte in to_crypt:
        num = ''
        for _ in range(8):
            xor_result = 0
            for cypher in cyphers:
                xor_result ^= next(cypher)
            num += str(xor_result)
        message += int.to_bytes(int(num,2) ^ byte)
    
    return message
