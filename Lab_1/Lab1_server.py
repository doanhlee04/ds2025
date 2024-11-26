import socket

def server_program():
    host = 'localhost'  
    port = 8080         

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    # Accept a connection
    conn, address = server_socket.accept()
    print(f"Connection from {address}")

    # Receive file metadata
    file_info = conn.recv(1024).decode()
    filename, filesize = file_info.split(",")
    filesize = int(filesize)
    print(f"Receiving file: {filename} ({filesize} bytes)")

    # Receive the file in chunks
    with open(f"received_{filename}", "wb") as f:
        received_bytes = 0
        while received_bytes < filesize:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
            received_bytes += len(data)


    print(f"File {filename} received successfully.")
    conn.close()
    server_socket.close()

server_program()
