import socket
import threading
from utils import *


def receive_messages(client_socket, private_key, p):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            encrypted_message = eval(data)
            decrypted_message = ''.join(chr(decrypt(private_key, (C1, C2), p)) for C1, C2 in encrypted_message)
            print(f"\nClient1: {decrypted_message}")
        except Exception as e:
            print(f"Error: {e}")
            break


if __name__ == '__main__':
    p, g = get_cyclic_group_prime_and_generator()
    public_key, private_key = key_selection(p, g)

    ip = input("Enter IP Address to connect: ")
    client_socket = socket.create_connection((ip, 8888))
    print(f"Connected to Client1\nPublic key: {public_key}")

    data = client_socket.recv(1024).decode('utf-8')
    client1_public_key = eval(data)
    print(f"Received public key from Client1: {client1_public_key}")

    client_socket.send(f"{public_key}".encode('utf-8'))
    threading.Thread(target=receive_messages, args=(client_socket, private_key, p)).start()

    while True:
        message = input("You (Client2): ")
        encrypted_message = [encrypt(client1_public_key, ord(char)) for char in message]
        client_socket.send(f"{encrypted_message}".encode('utf-8'))
        if message.lower() == 'exit':
            client_socket.close()
            break