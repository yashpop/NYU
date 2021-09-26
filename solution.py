# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a server socket
    serverSocket.bind(("", port))
    # Fill in start
    serverSocket.listen(9)
    # Fill in end

    while True:
        # Establish the connection
        # print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Fill in start      #Fill in end
        try:
            #print("Connection Socket accepted")
            try:
                message = connectionSocket.recv(1024).decode()  # Fill in start    #Fill in end
                #print(message)
                filename = message.split()[1]
                f = open(filename[1:], 'r')
                outputdata = f.readlines()  # Fill in start     #Fill in end
                f.close()
                # Send one HTTP header line into socket.
                # Fill in start
                connectionSocket.send('HTTP/1.0 200 OK\nContent-Type: text/html\n'.encode())
                # Fill in end

                # Send the content of the requested file to the client
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
                # Fill in end
                # Close client socket
                # Fill in start
                connectionSocket.close()
                # Fill in end
            break
        except (ConnectionResetError, BrokenPipeError):
            pass

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":
    webServer(13331)
