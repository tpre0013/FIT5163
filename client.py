import socket
import ssl

def main():
    # Create SSL context and disable certificate verification
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Wrap socket with the SSL context
    secure_socket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname='localhost')

    try:
        # Connect to server
        secure_socket.connect(('localhost', 8443))
        print("Connected to server")

        # Send and receive data
        secure_socket.send("Hello from client".encode('utf-8'))
        response = secure_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {response}")

    except ssl.SSLError as e:
        print(f"SSL error: {e}")
    except Exception as e:
        print(f"General error: {e}")
    finally:
        # Ensure the connection is properly closed
        secure_socket.close()

if __name__ == "__main__":
    main()

