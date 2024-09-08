import random

# Encryption by Bob (Sender)
def encrypt(public_key: tuple, M: int):
    p, g, y = public_key
    
    # Choose a random ephemeral key k (1 < k < p-1)
    k = random.randint(1, p - 2)
    
    # Compute C1 = g^k mod p
    C1 = pow(g, k, p)
    
    # Compute C2 = M * y^k mod p
    C2 = (M * pow(y, k, p)) % p
    
    # Return ciphertext (C1, C2)
    return (C1, C2)


def encrypt_msg(public_key: tuple, M: str):
    ciphertext = []
    for char in M:
        ciphertext.append(encrypt(public_key, ord(char)))

    return ciphertext

# Example usage
if __name__ == '__main__':
    public_key = (211, 5, 109)

    M = "Hello"
    ciphertext = []
    for char in M:
        ciphertext.append(encrypt(public_key, ord(char)))

    print(ciphertext)
