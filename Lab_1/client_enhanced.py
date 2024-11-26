import socket
import os
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


def client_program():
    """Enhanced TCP client to send files."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(('localhost', PORT))
        print(f"Connected to server on port {PORT}")
        
        # Input the file to send
        filename = input("Enter the filename to send: ")
        if not os.path.exists(filename):
            print("File not found!")
            return
        
        filesize = os.path.getsize(filename)
        
        # Send file metadata
        file_metadata = f"{filename},{filesize}"
        client_socket.send(file_metadata.encode())
        
        # Send file in chunks
        sent_bytes = 0
        with open(filename, "rb") as f:
            progress = tqdm(total=filesize, unit="B", unit_scale=True, desc="Sending")
            while (chunk := f.read(BUFFER_SIZE)):
                client_socket.send(chunk)
                sent_bytes += len(chunk)
                progress.update(len(chunk))
            progress.close()
        
        # Send checksum
        checksum = calculate_checksum(filename)
        client_socket.send(checksum.encode())
        
        print("File transfer complete.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    client_program()
