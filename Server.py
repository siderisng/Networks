import socket #for sockets
import sys  #for exit
from thread import * #for thread creation

listNames = list ()
listConns = list () # list of sockets used for chat
listFilesConn= list() # list of sockets used for chat and files associated with them
listFiles = list() #list of files
listAllConns = list() #list of chat and file exchange sockets

clientID=0
PORTB = 9000
HOST = ''    # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port

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
listFiles.append ("List of files:\n") 
 
#function for sharing files 
def clientExchange(conn, connToSend, nofFile ):
    
    global PORTB
    #find socket for file exchange associated with socket that has file
    for anyConn in listAllConns:
        if anyConn[0] == connToSend:
            
            connRcv = anyConn[1]
            break
	#find socket for file exchange associated with socket that wants file	
    for anyConn in listAllConns:
        if anyConn[0] == conn:
            
            connSEND = anyConn[1]
            break
  	
  	#Sent that you want a file
    msg = "wFILE"
    connToSend.send (msg)
    
    #wait for reply
    data = connRcv.recv(1024)
    #if it asks you for the name of file respond
    if data == "NAME":
        connRcv.send (nofFile)	
    
    #if it's ok receive the size of file 
    data = connRcv.recv(1024)
    
    if data != "NOT":    
        
        size = int (data)
        #send it to client that wants the file
        msg = str (size)       
        connSEND.send (msg)
        #wait for acknowledgment
        data = connSEND.recv(1024)
        
        #send a unused port
        PORTB +=1
        
        #send it to sender
        connRcv.send (str(PORTB))
        #acknowledgment
        data = connRcv.recv(1024)
        
        #send it to client
        connSEND.send (str(PORTB))      
        
        
        print "Finished Transaction"
    #else send client error message    
    else:
        msg = "NOT"
        connSEND.send (msg)
        
        
#Function for handling connections. This will be used to create threads
def clientthread(conn ):
    #Sending message to connected client/ Instruction for using server
    
    global clientID
    cName = "Client"+str (clientID)
    clientID+=1
    conn.send('Welcome to the server '+cName+'.\nType Chat: <msg> to share a message with other clients\nType nFile< ><name of file> for uploading file.\nType tFile< ><name of file> for downloading file. \nType ShowList for showing the current list of files available\nType Q or q to exit') 
     
    
    
    #infinite loop so that function do not terminate and thread do not end.
    while True:
		
        flag = 0 #used for checking if file exists
        
        #Receiving from client
        
        data = conn.recv(1024)
        
        reply = data
        if not data:
            break
		
		#Chat
        elif data[0:5] == "Chat:":
			#Send to all except this client
            for sendTo in listConns:
                if conn == sendTo:
                    continue 
                sendTo.send (cName+ ':' + data[5:])
                
        #upload        
        elif data[0:5] == "nFile":
			
			#read name of file and add it
            tupleFiles = (data[6:],conn)
            listFilesConn.append (tupleFiles) 
            listFiles.append (cName+ ":" + data[6:] + ", ")
            #send list of files
            for sendTo in listConns:
                
                
                for fileName in listFiles:
                    
                    sendTo.sendall(fileName)
                    
        #ask permission to take file
        elif data[0:5] == "tFile":
            
            #find if file exists
            for aFile in listFilesConn:
                
                if data[6:] == aFile[0]:
					
                     
                    if aFile[1] == conn:
                        conn.send ("You already have this file, don't be silly")
                        flag =1
                        continue
                    else:
                        #if it does call clientExchange function
                        connToSend = aFile[1]
                        nofFile = data[6:]
                        #Send client to get ready
                        conn.send ("GET READY")
                        start_new_thread (clientExchange, (conn,connToSend,nofFile) )
                        flag =1
                        
            if flag == 0:
                conn.send ("Sorry no such File uploaded.  Maybe the client log out")
                
            else:
                flag=0
       
       #show file list
        elif data [0:] == "ShowList":
            #sends list back to the client that asks for it
            
            for fileName in listFiles:
                    
                    conn.sendall(fileName)
                    
        #QUIT
        elif (data  == "Q" or data =='q'):
            
            #delete from lists
            #close sockets
            for deleteCon in listAllConns:
                if deleteCon[0] == conn:
                    connDel = deleteCon[1]
                    listAllConns.remove (deleteCon)
                    break
				
            listConns.remove (conn)
            for toDel in listFilesConn: 
                if toDel[1]== conn:
                    listFilesConn.remove(toDel)
                    
            break
		
       #not a valid command             
        else:
            conn.send('Syntax Error\nType Chat: <msg> to share a message with other clients\nType nFile< ><name of file> for uploading file.\nType tFile< ><name of file> for downloading file. \nType ShowList for showing the current list of files available\nType Q or q to exit')
        
    #came out of loop
    conn.send ("Time to die")
    print "Closing socket " + str(conn)
    conn.close()
    connDel.close()
    
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    
    
    print 'Connected with ' + addr[0] + ':' + str(addr[1]) 
    
    data = conn.recv(1024)
    reply = data
    print data
    #iif it's a chat socket add it to the appropriate list and wait for the file socket to connect it
    if reply == "CSHOC":
        listConns.append(conn)
        
        print 'List of connections:'
        print listConns 
        toLink = str (conn) #used later for finding the right socket
        conn.send (toLink) #sends back socket name
        
    #if it's a file socket    
    elif reply == "FSHOC":
        conn.send (" OK ")
        #wait to aquire the name of the chat socket to link it with
        data = conn.recv(1024)
        #find its pair         
        for toLink in listConns:
            
            toCMP = str (toLink)
            #if you find it, link them and start clientthread function     
            if toCMP == data: 
                
                tupleLinked = (toLink, conn)
                listAllConns.append (tupleLinked)
                print "Finihsed Connection For "
                print toLink
                start_new_thread(clientthread ,(toLink,))
                break
			
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    
 
s.close()