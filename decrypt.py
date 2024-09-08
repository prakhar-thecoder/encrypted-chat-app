from sympy import mod_inverse

# Decryption by Jack (Receiver)
def decrypt(private_key: int, ciphertext: tuple, p: int):
    C1, C2 = ciphertext
    x = private_key
    
    # Compute the shared secret s = C1^x mod p
    s = pow(C1, x, p)
    
    # Compute the inverse of s modulo p
    s_inverse = mod_inverse(s, p)
    
    # Recover the original message M = C2 * s_inverse mod p
    M = (C2 * s_inverse) % p
    
    # Return the original message
    return M


def decrypt_msg(private_key: int, ciphertext: list, p: int):
    decrypted_message = ""
    for t in ciphertext:
        decrypted_message += chr(decrypt(private_key, t, p))


# Example usage
if __name__ == '__main__':
    private_key = 9
    p = 211

    # Bob's Message (ciphertext)
    ciphertext = [(125, 133), (121, 176), (203, 118), (13, 141), (96, 162)]

    decrypted_message = ""
    for t in ciphertext:
        decrypted_message += chr(decrypt(private_key, t, p))

    print(decrypted_message)
