# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", port))
    serverSocket.listen(9)
    while True:
        connectionSocket, addr = serverSocket.accept()
        try:
            try:
                message = connectionSocket.recv(1024).decode()
                print(message)
                filename = message.split()[1]
                f = open(filename[1:], 'r')
                outputdata = f.read()
                f.close()
                # Send one HTTP header line into socket.
                connectionSocket.send('HTTP/1.0 200 OK\nContent-Type: text/html\n\n'.encode())
                for i in range(0, len(outputdata)):
                    connectionSocket.send(outputdata[i].encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.close()
            except IOError:
                # Send response message for file not found (404)
                # Fill in start
                outputdata = 'HTTP/1.0 404 NOT FOUND\nContent-Type: text/html\n\n<html><p><b>Not Found</b></p>'
                connectionSocket.send(outputdata.encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.close()
            # break
        except (ConnectionResetError, BrokenPipeError):
            print("shitty code")
            pass

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":
    webServer(13331)
