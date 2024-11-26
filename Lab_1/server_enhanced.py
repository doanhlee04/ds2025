import socket
import hashlib
from tqdm import tqdm

BUFFER_SIZE = 1024  # Size of data chunks
PORT = 8080


def calculate_checksum(filepath):
    """Calculate MD5 checksum of the file."""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(BUFFER_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()


def server_program():
    """Enhanced TCP server to receive files."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('localhost', PORT))
        server_socket.listen(5)
        print(f"Server is listening on port {PORT}...")
        
        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")
        
        # Receive file metadata
        file_metadata = conn.recv(BUFFER_SIZE).decode()
        filename, filesize = file_metadata.split(",")
        filesize = int(filesize)
        print(f"Receiving file: {filename} ({filesize} bytes)")
        
        # Receive file in chunks
        received_bytes = 0
        with open(f"received_{filename}", "wb") as f:
            progress = tqdm(total=filesize, unit="B", unit_scale=True, desc="Receiving")
            while received_bytes < filesize:
                chunk = conn.recv(BUFFER_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                received_bytes += len(chunk)
                progress.update(len(chunk))
            progress.close()
        
        # Verify checksum
        received_checksum = conn.recv(BUFFER_SIZE).decode()
        calculated_checksum = calculate_checksum(f"received_{filename}")
        if received_checksum == calculated_checksum:
            print("File integrity verified.")
        else:
            print("File integrity check failed!")
        
        print("File transfer complete.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()


if __name__ == "__main__":
    server_program()
