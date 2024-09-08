import random

def key_selection(p: int, g: int):
    # Choose a private key x (1 < x < p-1)
    x = random.randint(1, p - 2)
    
    # Compute the public key component y = g^x mod p
    y = pow(g, x, p)
    
    # Return public key (p, g, y) and private key x
    return (p, g, y), x


if __name__ == "__main__":
    print(key_selection(211, 5))