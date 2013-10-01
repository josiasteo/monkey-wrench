'''
@author: Josias Teo
'''

import client, server
import time

'''
@summary: 
Test Case no.: 0001
Source: R-Pi
Target: PC
Scenario: R-Pi sending sensor info to PC
Result: 
'''
def case0001():
    # === Info needed to send a JSON message ===
    # Specify the target IP and port number
    serverIP = 'localhost'
    port = 13373
    # Specifies the identity of the message's source
    sourceID = 'R-Pi'
    
    # === Creating data to send ===
    arrOfReadings = [ "L,1,C,0,R,42", "L,1,C,0,R,42", "L,1,C,1,R,42" ]
    data = { 0:  arrOfReadings }
    
    # === Call send_msg method from client helper class ===
    returnVal = client.send_msg(serverIP, port, sourceID, data)
    
    print 'Return value from target:', returnVal
    
    if returnVal == 0:
        print 'Message successfully sent to:', serverIP
    else:
        print 'Message was not sent to:', serverIP
    

'''
@summary: 
Test Case no.: 0002
Scenario: Initialize socket server
Result: 
'''
def case0002():
    server.initServer('localhost', 13373)

''' ====== Start of main method ======= '''

if __name__ == '__main__':
#     print 'Start of Test Case 0002'
#     case0002()
#     print 'End of Test Case 0002'
#       
#     # Sleep to allow server to startup properly
#     time.sleep(5)
#        
    print 'Start of Test Case 0001'
    case0001()
    print 'End of Test Case 0001'