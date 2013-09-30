'''
@author: Josias Teo
@summary: 
Server is called to launch within the Caller's code. Launch the server
as a separate thread by instantiating the ThreadedSocketServer class.
Otherwise, simply call the initServer method to run the server within
the same process.

Responsible for receiving, then sending a reply back to client.
'''

import SocketServer
import json
import threading

class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            # Receive instruction from PC, forward to Arduino
            msg_json = self.request.recv(4096).strip()
            msg = json.loads(msg_json)
             
            print 'From client:', msg
            
            # Process received Json object
            processJsonObj(msg)
             
            # Respond to the client
            respondToClient(self.request, len(msg_json))
             
            if 'shutdown' == msg['source']:
                print 'Shutting down server...'
                self.server.shutdown()
             
        except Exception as e:
            print "Exception while receiving message: ", e

'''
@summary: This class initializes a socket server in
a separate thread.
@note: May not work well on the Raspberry Pi, due to multi-threading issues.
Instead, call initServer() to initialize a server.
'''
class ThreadedSocketServer (threading.Thread):
    def __init__(self, threadID, name, ip, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ip = ip
        self.port = port
    def run(self):
        print 'Running thread:', self.name
        initServer(self.ip, self.port)
'''
@summary: 
Initializes a socket server in a separate thread, on the specified IP address and port.

@param ip: IP address on which the server should be bound to.
@param port: Port number on which the server should listen to.
'''
def initServer(ip, port):
    print 'Starting up server at:', ip, 'port:', port
    
    try:
        server = MyTCPServer((ip, port), MyTCPServerHandler)
    
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        print 'Listening on:', ip, port
        server.serve_forever()
        
    except Exception as e:
        print 'Unexpected error:', e
        print 'Server will be shutdown.'

'''
TODO: Insert code here to handle Json Object after receiving it.
@summary: This method specifies how the received Json object is handled
by this application.
@note:
For Algo, it will pass this info to Mapping to update map.
For R-Pi, it will forward the received instructions to Arduino.
'''    
def processJsonObj(msg):
    print 'Processing Json Object:'
    
    instrString = msg['data']
    
    # Put all instructions into one string
#     for instr in msg['data']:
#         print 'Action to Arduino:', instr
#         instrString = instrString + ',' + instr
        
    # Send to action over serial
    print instrString
    
'''
Insert code here to create the response to be sent to the client.
@summary: Create the response to be sent to the client.
@param request: The Request object to send the response.
@note:
For Algo, it will send instructions in response to data from R-Pi.
For R-Pi, it will send an ACK to PC for the received instructions.
'''  
def respondToClient(request, msg_len):
    print 'Responding to client'
    
    # Send back an ACK, with the number of bytes received
    ack = json.dumps({'return':msg_len})
    print 'Sending ACK:', ack
    # sent can be used to check the no of bytes sent, error checking 
    request.send(ack)
    
        
'''
=== Start of main method ===
'''
if __name__ == '__main__':
    print 'Running server.py as main method'
    srv = ThreadedSocketServer(1, 'SockServer-1', 'localhost', 13373)
    srv.start()