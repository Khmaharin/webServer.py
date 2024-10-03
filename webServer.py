# import socket module
from socket import *
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
            message = connectionSocket.recv(1024).decode()  # Receive the message from the client
            filename = message.split()[1]
            
            # Open the client requested file
            f = open(filename[1:], "rb")  # Open file in binary read mode
            
            # Create a response header for 200 OK
            header = "HTTP/1.1 200 OK\r\n"
            header += "Content-Type: text/html; charset=UTF-8\r\n"
            header += "\r\n"  # End of headers
            
            connectionSocket.send(header.encode())  # Send header
            
            # Read the contents of the file and send it to the client
            outputdata = f.read()
            connectionSocket.send(outputdata)  # Send the content of the file

            f.close()  # Close the file after sending it
            
            connectionSocket.close()  # Closing the connection socket
            
        except Exception as e:
            # Send response message for invalid request due to the file not being found (404)
            header = "HTTP/1.1 404 Not Found\r\n"
            header += "Content-Type: text/html; charset=UTF-8\r\n"
            header += "\r\n"
            connectionSocket.send(header.encode())  # Send header
            connectionSocket.send(b"<html><body><h1>404 Not Found</h1></body></html>")  # Send body
            
            connectionSocket.close()  # Close client socket

if __name__ == "__main__":
    webServer(13331)
