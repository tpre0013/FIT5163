import socket
import ssl

# Client certificate and key
CLIENT_CERT = 'client.crt'
CLIENT_KEY = 'client.key'
SERVER_CERT = 'server.crt'

def secure_client_socket():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the socket with SSL
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    context.load_verify_locations(cafile=SERVER_CERT)

    secure_socket = context.wrap_socket(client_socket, server_hostname='localhost')
    return secure_socket

def main():
    secure_socket = secure_client_socket()
    secure_socket.connect(('localhost', 8443))
    print("Connected to the server...")

    try:
        secure_socket.send("Hello from client".encode('utf-8'))
        data = secure_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {data}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        secure_socket.close()

if __name__ == '__main__':
    main()
