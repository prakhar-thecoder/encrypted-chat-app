import os
import socket
import threading
import random
from sympy import mod_inverse


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't need to connect, just triggers route discovery
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

# Key generation for ElGamal
def key_selection(p: int, g: int):
    x = random.randint(1, p - 2)  # Private key
    y = pow(g, x, p)  # Public key component
    return (p, g, y), x  # Return public key and private key


# Encryption using the other party's public key
def encrypt(public_key: tuple, M: int):
    p, g, y = public_key
    k = random.randint(1, p - 2)  # Ephemeral key
    C1 = pow(g, k, p)
    C2 = (M * pow(y, k, p)) % p
    return (C1, C2)


# Decryption using your own private key
def decrypt(private_key: int, ciphertext: tuple, p: int):
    C1, C2 = ciphertext
    s = pow(C1, private_key, p)  # Shared secret
    s_inverse = mod_inverse(s, p)
    M = (C2 * s_inverse) % p
    return M


def receive_messages(client_socket, private_key, p):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            # Split the encrypted pairs (C1, C2)
            encrypted_message = eval(data)
            decrypted_message = ""
            for C1, C2 in encrypted_message:
                decrypted_message += chr(decrypt(private_key, (C1, C2), p))
            print(f"\nClient2: {decrypted_message}")
        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == '__main__':
    p = 211
    g = 5
    # Generate key pair for client1 (server)
    public_key, private_key = key_selection(p, g)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8888))
    server.listen(1)
    print(f"\nClient1 started...\nPublic key: {public_key}")
    print(f"IP Address: {get_local_ip()}")

    client_socket, client_address = server.accept()

    # Send public key to client2
    client_socket.send(f"{public_key}".encode('utf-8'))

    # Receive public key from client2
    data = client_socket.recv(1024).decode('utf-8')
    client2_public_key = eval(data)
    print(f"Received public key from Client2: {client2_public_key}")

    # Create a separate thread to receive messages
    threading.Thread(target=receive_messages, args=(client_socket, private_key, p)).start()

    # Chat loop
    while True:
        message = input("You (Client1): ")
        encrypted_message = [encrypt(client2_public_key, ord(char)) for char in message]

        # Send the encrypted message
        client_socket.send(f"{encrypted_message}".encode('utf-8'))

        if message.lower() == 'exit':
            client_socket.close()
            break

    server.close()
