import socket
import os

def client_program():
    host = 'localhost'
    port = 8080         

    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    # Specify the file to send
    filename = "text_01.txt"
    filesize = os.path.getsize(filename)

    # Send file metadata
    file_info = f"{filename},{filesize}"
    client_socket.send(file_info.encode())

    # Send the file in chunks
    with open(filename, "rb") as f:
        while (chunk := f.read(1024)):
            client_socket.send(chunk)

    print(f"File {filename} sent successfully.")
    client_socket.close()

client_program()
