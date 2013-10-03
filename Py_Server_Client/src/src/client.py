'''
@author: Josias Teo
@summary: Responsible for sending, then receiving a response from the server.
Just testing
'''

import socket
import json
import sys

'''
@summary: 
Sends a JSON encoded message to a socket server, specified in the socket object.
The JSON message is in the following format:
{ 'source' : sourceID , 'data' : (data) }

@param serverIP: IP address of target server
@param port: Port number of target server
@param sourceID: A simplified authentication string to state where the message is coming from. Eg. 'Algo', 'Arduino'
@param data: Can be any arbitrary data. Will be encapsulated in a tuple.

@return: A Json object for further processing. None is returned
if the sending / receiving process failed.
'''
def send_msg(serverIP, port, sourceID, data):
    try:
        
        print 'Connecting to server:', serverIP, 'port:', port
        socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketObj.connect((serverIP, port))
        print 'Success - Connected to server:', serverIP, 'port:', port
        
        # Specify data to be sent
        msg = { 'source':sourceID, 'data': data }
        
        # Encode msg in JSON
        msg_json = json.dumps(msg) + '\n'
        
        # Send JSON encoded message, in a resilient manner
        totalsent = 0
        while totalsent < len(msg_json):
            print 'Sending:', msg_json[totalsent:]
            sent = socketObj.send( msg_json[totalsent:] )
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            totalsent = totalsent + sent
            
        if totalsent <> len(msg_json):
            print 'Error: Message was not completely sent.'
        else:
            print 'Bytes sent:', totalsent
            
        # Receive response from server
        print 'Start rcv response'
        responseStr = socketObj.recv(4096)
        print 'String received from server:', responseStr
        response = json.loads(responseStr)
        print 'Finish rcv response'
        
        return response['data']
        
    except socket.error as se:
        print "Socket error:", se
    except Exception as e:
        print "Unexpected error:", e
    
    return None