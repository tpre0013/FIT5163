import socket
import ssl

# Server certificate and key
SERVER_CERT = 'server.crt'
SERVER_KEY = 'server.key'

def secure_server_socket():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8443))
    server_socket.listen(5)
    
    # Wrap the socket with SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    
    # Comment out these lines if not requiring client certificates
    # context.load_verify_locations(cafile=CLIENT_CERT)
    # context.verify_mode = ssl.CERT_REQUIRED  # This line enforces client certificates

    secure_socket = context.wrap_socket(server_socket, server_side=True)
    return secure_socket

def main():
    secure_socket = secure_server_socket()
    print("Server listening on port 8443...")

    while True:
        try:
            client_socket, addr = secure_socket.accept()
            print(f"Connection accepted from {addr}")
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Received from client: {data}")
            client_socket.send("Hello from server".encode('utf-8'))
        except ssl.SSLError as e:
            print(f"SSL error: {e}")
        except Exception as e:
            print(f"General error: {e}")
        finally:
            client_socket.close()

if __name__ == '__main__':
    main()
