import socket   #for sockets
import sys  #for exit
import os.path #for file

from thread import *
i = 0

def giveFile():
    
    msg = "NAME"
    sendSoc.sendto(msg , (host, port))   
   
    d = sendSoc.recvfrom(1024)
  
    fname = d[0]   
    
    if os.path.isfile(fname) == True: 
        size = os.path.getsize (fname)
        
        msg = str (size)
        sendSoc.sendto(msg , (host, port))
        
        sFile=open (fname, "rb") 
  
        l = sFile.read(1024)
        
        while (l):
            sendSoc.send(l)
            l = sFile.read(1024)
        print "Done"
        sFile.close ()
    else:
        msg = "NOT"
        sendSoc.sendto(msg , (host, port))


def ListenToTheServer():
    i=0
    while(1):

        #Set the whole string
        
        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        reply = d[0]
            
      
        if reply == "Time to die":
            break
        elif reply[:5]=="wFILE":
            start_new_thread(giveFile ,())
        elif reply == "GET READY":
            print "Starting Sending procedures. Please do not send anything till it's over"
            
            d = s.recvfrom(1024)
            reply = d[0]   
            
			
            if reply[:2] != "NOT":
               
                size = int(reply) 
                nfile = open ("nFile_"+ str(i),'wb')
                i= i+1
                print size
                l = s.recv(size)
                nfile.write(l)
                nfile.close ()
                   
                    
                print "OK... FILE OBTAINED"
                
            else:
                print "Something went wrong. Please try again. It's possible that client doesn't have file anymore.."
                
                
        else: 
            print reply 		
            
            
            
host = "localhost"
port = 8887

#socket for sending file   

try:
    #create an AF_INET, STREAM socket (TCP)
    sendSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
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
 
#end of socket creation


try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
     
print 'Ip address of ' + host + ' is ' + remote_ip
 

#Connect to remote server
s.connect((remote_ip , port))


 
print 'Socket for Chat Connected to ' + host + ' on ip ' + remote_ip

msg = "CSHOC"
s.sendto(msg , (host, port))

d = s.recvfrom(1024)
reply = d[0]
print reply

sendSoc.connect((remote_ip , port))

print 'Socket for file exchange connected to ' + host + ' on ip ' + remote_ip

msg = "FSHOC"
sendSoc.sendto(msg , (host, port))
sendSoc.sendto(reply , (host, port))


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