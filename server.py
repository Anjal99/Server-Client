
import socket
from socket import *
import _thread
import time 
import requests

def multi_thread(connectionSocket, addr):
    try:

        # Extract the path of the requested object from the message
        message = connectionSocket.recv(1024).decode('utf-8')
        t1 = time.time()
        print('Connection Established!')
        filename = message.split()[1]
        print(filename[1:])
        f = open(filename[1:],'r')
    
        # Store the entire contenet of the requested file in a temporary buffer
        outputdata = f.read()
        print(outputdata)
        # Send the HTTP response header line to the connection socket
        connectionSocket.sendall('HTTP/1.1 200 OK\r\n\r\n'.encode('utf-8'))
        t2 = time.time()
        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
        RTT = (t2 - t1)
        print('RTT is :',RTT)

    except:
        print('No such File found ')
        connectionSocket.send('HTTP/1.1 404 File not Found\r\n\r\n'.encode('utf-8'))
        # Close the socket in case of some issues 
        connectionSocket.close()

# Create a TCP server socket

serverSocket = socket(AF_INET, SOCK_STREAM)  

# Assign a port number
serverPort = 8000

# Bind the socket to server address and server port

serverSocket.bind(('',serverPort))

# Listen to at most 5 connection at a time

serverSocket.listen(10)

# Server should be up and running and listening to the incoming connections    

while True:
    '''This part is for multi threading'''
    print ('Ready to serve')
    connectionSocket, addr = serverSocket.accept()
    try:
        '''Start the new thread'''
        _thread.start_new_thread(multi_thread, (connectionSocket,addr))
    except:
        print("Unable to start a new thread")
serverSocket.close()







