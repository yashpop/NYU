from socket import *
import time

def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope

    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    # Fill in start
    server = (mailserver, port)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(server)
    # Fill in end

    recv = clientSocket.recv(1024).decode()
    # print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    # Fill in start
    mailFrom = "MAIL FROM:yp2203@nyu.edu\r\n"
    clientSocket.send(mailFrom.encode())
    recv2 = clientSocket.recv(1024)
    recv2 = recv2.decode()
    # Fill in end

    # Send RCPT TO command and print server response.
    rcptTo = "RCPT TO:<xxxxxxxxxx>\r\n"
    clientSocket.send(rcptTo.encode())
    recv3 = clientSocket.recv(1024)
    recv3 = recv3.decode()

    # Send DATA command and print server response.
    data = "DATA\r\n"
    clientSocket.send(data.encode())
    recv4 = clientSocket.recv(1024)
    recv4 = recv4.decode()

    # Send message data.
    # Fill in start
    subject = "Subject: testing my client with clientsocket\r\n\r\n"
    clientSocket.send(subject.encode())
    clientSocket.send(msg.encode())
    # Fill in end

    # Message ends with a single period.
    clientSocket.send(endmsg.encode())
    recv_msg = clientSocket.recv(1024)

    # Send QUIT command and get server response.
    quit = "QUIT\r\n"
    clientSocket.send(quit.encode())
    recv5 = clientSocket.recv(1024)
    clientSocket.close()


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
