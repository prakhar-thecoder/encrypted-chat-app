import random
import socket
from sympy import mod_inverse, isprime, primitive_root


def get_cyclic_group_prime_and_generator():
    p = 509
    while not isprime(p):
        p += 2
    g = primitive_root(p)
    return p, g

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def key_selection(p, g):
    x = random.randint(1, p - 2)
    y = pow(g, x, p)
    return (p, g, y), x

def encrypt(public_key, M):
    p, g, y = public_key
    k = random.randint(1, p - 2)
    C1 = pow(g, k, p)
    C2 = (M * pow(y, k, p)) % p
    return C1, C2

def decrypt(private_key, ciphertext, p):
    C1, C2 = ciphertext
    s = pow(C1, private_key, p)
    s_inverse = mod_inverse(s, p)
    M = (C2 * s_inverse) % p
    return M