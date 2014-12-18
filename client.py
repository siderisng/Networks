import socket   #for sockets
import sys  #for exit
from thread import *



   
 
 
 
 
def ListenToTheServer():
    while(1) :

        #Set the whole string
        
        # receive data from client (data, addr)
            d = s.recvfrom(1024)
            reply = d[0]
            
            print reply
            if reply == "Time to die":`
                break
            elif reply=='NEED FILE':
                
               s.sendto("OK" + d[7:] , (host, port))   
               
               
#socket for sending file    
try:
    #create an AF_INET, STREAM socket (TCP)
    send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Socket Created'
#main socket
try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Socket Created'
 
host = '192.168.1.5'
port = 8888
 
try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
     
print 'Ip address of ' + host + ' is ' + remote_ip
 

#Connect to remote server
s.connect((remote_ip , port))
 
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

d = s.recvfrom(1024)
reply = d[0]
addr = d[1]
print 'Server reply : ' + reply

start_new_thread(ListenToTheServer ,())

while(1) :
       
    try:
		
        msg = raw_input()
        s.sendto(msg , (host, port))     
       
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()