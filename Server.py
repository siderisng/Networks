import socket
import sys
from thread import *
listConns = list ()
listFilesConn= list()
listFiles = list()
listAllConns = list()


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8887# Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
 
#function for sharing files 
def clientExchange(conn, connToSend, nofFile ):
    
    for anyConn in listAllConns:
        if anyConn[0] == connToSend:
            
            connRcv = anyConn[1]
            break
  	
    msg = "wFILE" + str(conn)
    connToSend.send (msg)
    
    data = connRcv.recv(1024)
    if data == "NAME":
        connRcv.send (nofFile)	
    
    data = connRcv.recv(1024)
    if data != "NOT":    
        size = int (data)
        print size
        
        msg = str (size)       
        conn.send (msg)
        
        l = connRcv.recv(size)
      
        conn.send (l)
        print "File Sent"
        
    else:
        msg = "NOT"
        conn.send (msg)
        
        
#Function for handling connections. This will be used to create threads
def clientthread(conn ):
    #Sending message to connected client
    conn.send('Welcome to the server.\nType Chat: <msg> to share a message with other clients\nType nFile <name of file> for uploading file.\nType tFile <name of file> for downloading file. \nType ShowList for showing the current list of files available\nType Q or q to exit') 
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
		
        flag = 0 
        
        #Receiving from client
        
        data = conn.recv(1024)
        
        reply = data
        if not data:
            break
		
		#Chat
        elif data[0:5] == "Chat:":
			
            for sendTo in listConns:
                if conn == sendTo:
                    continue 
                sendTo.send (data[5:])
                
        #upload        
        elif data[0:5] == "nFile":
			
            tupleFiles = (data[6:],conn)
            listFilesConn.append (tupleFiles) 
            listFiles.append (data[6:]+"\n")
            for sendTo in listConns:
                
                if conn == sendTo:
                    continue 
                sendTo.send ("List of files:\n")
                for fileName in listFiles:
                    
                    sendTo.sendall(fileName)
                    
        #ask permission to take file
        elif data[0:5] == "tFile":
            
            for aFile in listFilesConn:
                
                if data[6:] == aFile[0]:
					
                     
                    if aFile[1] == conn:
                        print "You already have this file, don't be silly"
                        flag =1
                        continue
                    else:
                        connToSend = aFile[1]
                        nofFile = data[6:]
                        conn.send ("GET READY")
                        start_new_thread (clientExchange, (conn,connToSend,nofFile) )
                        flag =1
                        
            if flag == 0:
                conn.send ("No such File uploaded")
                
            else:
                flag=0
       
        elif data[0:2] == "OK":
            toSend = data[3:]     
            print data
       
       #show file list
        elif data [0:] == "ShowList":
            sendTo.send ("List of files:")
            for fileName in listFiles:
                    
                    conn.sendall(fileName)
                    
        #QUIT
        elif (data  == "Q" or data =='q'):
			conn.send ("Time to die")
			break
		
       #not a valid command             
        else:
            conn.send('Syntax Error\nType Chat: <msg> to share a message with other clients\nType nFile <name of file> for uploading file.\nType tFile <name of file> for downloading file. \nType ShowList for showing the current list of files available\nType Q or q to exit')
        
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    
    print 'Connected with ' + addr[0] + ':' + str(addr[1]) 
    
    data = conn.recv(1024)
    reply = data
    
    if reply == "CSHOC":
        listConns.append(conn)
        
        print 'List of connections:'
        print listConns 
        toLink = str (conn)
        conn.send (toLink)
        
    elif reply == "FSHOC":
        
        data = conn.recv(1024)
        
        for toLink in listConns:
            
            toCMP = str (toLink)
           
            if toCMP == data: 
                
                tupleLinked = (toLink, conn)
                listAllConns.append (tupleLinked)
                print "Finihsed Connection For "
                print toLink
                start_new_thread(clientthread ,(toLink,))
                break
			
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    
 
s.close()