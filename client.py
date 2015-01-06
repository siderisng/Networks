import socket   #for sockets
import sys  #for exit
import os.path #for file handling

from thread import *  #for thread handling

#this function sends a requested file to server
def giveFile():
    
    #if it is given a file request it asks server which one
    msg = "NAME"
    sendSoc.sendto(msg , (host, port))   
   
    #acquire name of file   
    d = sendSoc.recvfrom(1024)
    fname = d[0]   
    
    #check if there is such a file
    if os.path.isfile(fname) == True: 
        
        #if it does exist find the size of it
        size = os.path.getsize (fname)
        
        #send message to server with the size of it
        msg = str (size)
        sendSoc.sendto(msg , (host, port))
        
        #open file
        sFile=open (fname, "rb")
        #read all and send
        l = sFile.read(size)
        sendSoc.send(l)
        #close file and print appropriate message   
        sFile.close ()
        print "Just Sent a File"
    
    #if file doesn't exist send negative message
    else:
		
        msg = "NOT"
        sendSoc.sendto(msg , (host, port))


#used for getting info from server
def ListenToTheServer():
    i=0
    while(1):
        
        # receive data from server
        d = s.recvfrom(1024)
        reply = d[0]
            
        #if the message is time to die then it's time to end the programm
        if reply == "Time to die":
            print "BB!!!"
            sys.exit()
        
        #if there is a file request start giveFile function
        elif reply[:5]=="wFILE":
            start_new_thread(giveFile ,())
        
        #if GET READY is the answer then client must wait till he gets back the file he asked for
        elif reply == "GET READY":
            print "Starting Sending procedures. Please do not send anything till it's over"
            #get size of file from server
            d = s.recvfrom(1024)
            reply = d[0]   
            
			#if everything's ok get file
            if reply != "NOT":
                
                size = int(reply) 
                #create new file with unique name
                nfile = open ("nFile_"+ str(i)+ str(s),'wb')
                i= i+1
                
                #receive file
                l = s.recv(size)
                #write it to file then close it
                nfile.write(l)
                nfile.close ()
                   
                print "OK... FILE OBTAINED"
 
            #else say that something went wrong    
            else:
                print "Something went wrong. Please try again. It's possible that client doesn't have file anymore.."
                
        #if answer does not match any other just print the reply        
        else: 
            print reply	
            
            
            
host = "localhost" 
port = 8888

#socket for sending file   

try:
    #create an AF_INET, STREAM socket (TCP)
    sendSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Socket Created'


#socket chat socket
try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Socket Created'
 
#end of socket creation

#find ip of host
try:
    remote_ip = socket.gethostbyname( host )
 
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
     
print 'Ip address of ' + host + ' is ' + remote_ip
 

#Connect chat socket to remote server
s.connect((remote_ip , port))
print 'Socket for Chat Connected to ' + host + ' on ip ' + remote_ip

#send type of socket
msg = "CSHOC"
s.sendto(msg , (host, port))

#acquire name of socket in server
d = s.recvfrom(1024)
reply = d[0]


#Connect file exchange socket to remote server
sendSoc.connect((remote_ip , port))
print 'Socket for file exchange connected to ' + host + ' on ip ' + remote_ip

#send type of socket
msg = "FSHOC"
sendSoc.sendto(msg , (host, port))
#send socket to link it with
sendSoc.sendto(reply , (host, port))


#start new thread for listening to the server
start_new_thread(ListenToTheServer ,())

#this is used for sending messages to the server
while(1) :
       
    try:
		
        msg = raw_input()
        s.sendto(msg , (host, port))     
       
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()