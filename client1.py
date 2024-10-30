import os
import socket
import threading
import random
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

def receive_messages(client_socket, private_key, p):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            encrypted_message = eval(data)
            decrypted_message = ''.join(chr(decrypt(private_key, (C1, C2), p)) for C1, C2 in encrypted_message)
            print(f"\nClient2: {decrypted_message}")
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == '__main__':
    p, g = get_cyclic_group_prime_and_generator()
    public_key, private_key = key_selection(p, g)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8888))
    server.listen(1)
    print(f"\nClient1 started...\nPublic key: {public_key}")
    print(f"IP Address: {get_local_ip()}")
    client_socket, client_address = server.accept()
    client_socket.send(f"{public_key}".encode('utf-8'))
    data = client_socket.recv(1024).decode('utf-8')
    client2_public_key = eval(data)
    print(f"Received public key from Client2: {client2_public_key}")
    threading.Thread(target=receive_messages, args=(client_socket, private_key, p)).start()
    while True:
        message = input("You (Client1): ")
        encrypted_message = [encrypt(client2_public_key, ord(char)) for char in message]
        client_socket.send(f"{encrypted_message}".encode('utf-8'))
        if message.lower() == 'exit':
            client_socket.close()
            break
    server.close()
