import socket
import threading
import random
from sympy import mod_inverse


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
            print(f"\nClient1: {decrypted_message}")
        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == '__main__':
    p = 211
    g = 5
    # Generate key pair for client2
    public_key, private_key = key_selection(p, g)

    client_socket = socket.create_connection(("127.0.0.1", 8888))
    print(f"Connected to Client1\nPublic key: {public_key}")

    # Receive public key from client1 (server)
    data = client_socket.recv(1024).decode('utf-8')
    client1_public_key = eval(data)
    print(f"Received public key from Client1: {client1_public_key}")

    # Send public key to client1 (server)
    client_socket.send(f"{public_key}".encode('utf-8'))

    # Create a separate thread to receive messages
    threading.Thread(target=receive_messages, args=(client_socket, private_key, p)).start()

    # Chat loop
    while True:
        message = input("You (Client2): ")
        encrypted_message = [encrypt(client1_public_key, ord(char)) for char in message]

        # Send the encrypted message
        client_socket.send(f"{encrypted_message}".encode('utf-8'))

        if message.lower() == 'exit':
            client_socket.close()
            break
