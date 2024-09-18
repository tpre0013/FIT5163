import socket
import ssl

# Server certificate and key
SERVER_CERT = 'server.crt'
SERVER_KEY = 'server.key'
CLIENT_CERT = 'client.crt'

def create_server_socket():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8443))
    server_socket.listen(5)
    return server_socket

def secure_server_socket(server_socket):
    # Wrap the socket with SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    context.load_verify_locations(cafile=CLIENT_CERT)
    context.verify_mode = ssl.CERT_REQUIRED

    secure_socket = context.wrap_socket(server_socket, server_side=True)
    return secure_socket

def main():
    server_socket = create_server_socket()
    secure_socket = secure_server_socket(server_socket)
    print("Server listening on port 8443...")

    while True:
        client_socket, addr = secure_socket.accept()
        print(f"Accepted connection from {addr}")
        try:
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Received data: {data}")
            client_socket.send("Hello from server".encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

if __name__ == '__main__':
    main()
