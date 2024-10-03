# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    
    serverSocket.bind(("", port))
    serverSocket.listen(1)  # Start listening to incoming connections
    
    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Accept the connection from the client
        
        try:
            message = connectionSocket.recv(1024)  # Receive the message from the client
            filename = message.split()[1]
            
            # Open the client requested file
            f = open(filename[1:], "rb")  # Open file in binary read mode
            
            # Create a response header for 200 OK
            header = "HTTP/1.1 200 OK\r\n"
            header += "Content-Type: text/html; charset=UTF-8\r\n"
            header += "Server: SimpleWebServer/1.0\r\n"  # Add Server header
            header += "Connection: close\r\n"  # Add Connection header
            header += "\r\n"  # End of headers
            
            # Read the contents of the file and prepare the full response
            outputdata = f.read()
            response = header.encode() + outputdata  # Combine header and body
            
            connectionSocket.sendall(response)  # Send the complete response
            
            connectionSocket.close()  # Closing the connection socket
            
        except Exception as e:
            # Send response message for invalid request due to the file not being found (404)
            header = "HTTP/1.1 404 Not Found\r\n"
            header += "Content-Type: text/html; charset=UTF-8\r\n"
            header += "Server: SimpleWebServer/1.0\r\n"  # Add Server header
            header += "Connection: close\r\n"  # Add Connection header
            header += "\r\n"
            body = "<html><body><h1>404 Not Found</h1></body></html>"
            response = header.encode() + body.encode()  # Combine header and body
            
            connectionSocket.sendall(response)  # Send the complete response
            
            connectionSocket.close()  # Close client socket

if __name__ == "__main__":
    webServer(13331)
