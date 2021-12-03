from socket import *
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = string[count + 1] * 256 + string[count]
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += ord(string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Fill in start

        # Fetch the ICMP header from the IP packet
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        # icmph = recPacket[176:184]
        icmph = recPacket[20:28]
        type, code, checksum, pID, sq = struct.unpack("bbHHh", icmph)
        # icmp Type, code, checksum, packetID, sequence

        # print("ICMP Header: ", type, code, checksum, pID, sq)
        if pID == ID:
            bytesinDbl = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesinDbl])[0]
            rtt = timeReceived - timeSent

            # print(f"Round-Trip Time: {rtt}")
            return rtt

        # Fill in end
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    # print(header)
    data = struct.pack("d", time.time())
    # print(data)
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)
    # Get the right checksum, and put in the header

    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network  byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    # print(header)
    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str

    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    # print(f"icmp: {icmp}")
    # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

def avg(elems):
    size=len(elems)
    val=0
    for i in elems:
        val+=i
    return val/size

def std_dev(elems):
    sum=0
    mean=avg(elems)
    for elem in elems:
        sum+=(elem-mean)**2
    return (sum/len(elems))**(1/2)


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,  	# the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    # print("Pinging " + dest + " using Python:")
    # print("")
    delay=[]
    # Send ping requests to a server separated by approximately one second
    for i in range(0, 4):
        output=doOnePing(dest, timeout)
        if output=="Request timed out.":
            return ['0', '0.0', '0', '0.0']
        delay.append(output)
        # print(delay)
        time.sleep(1)  # one second
    # Calculate vars values and return them
    packet_min = min(delay)
    packet_max = max(delay)
    packet_avg = avg(delay)
    stdev_var = std_dev(delay)
    vars = [packet_min, packet_avg,packet_max,stdev_var]
    # print(vars)
    return vars


if __name__ == '__main__':
    ping("google.co.il")
    # ping("amazon.in")

