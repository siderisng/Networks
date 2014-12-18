import socket
import sys
from thread import *
listConns = list ()
listFilesConn= list()
listFiles = list()



HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
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
 
#Function for handling connections. This will be used to create threads
def clientthread(conn ):
    #Sending message to connected client
    conn.send('Welcome to the server. \nType nFile <name of file> for uploading file.\nType tFile <name of file> for downloading file. \nType ShowList for showing the current list of files available\nType Q or q to exit') 
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
		
        flag = 0 
        
        #Receiving from client
        
        data = conn.recv(1024)
        
        reply = data
        if not data:
            break
		
		#upload file
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
                        flag =1
                        connToSend.send ("NEED FILE"+str(conn))
                       
                        
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
            conn.send('Syntax Error\nType nFile <name of file> for uploading file.\nType tFile <name of file> for downloading file. \nType ShowList for showing the current list of files available\nType Q or q to exit')
        
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    listConns.append(conn)
    print 'Connected with ' + addr[0] + ':' + str(addr[1]) 
    print 'List of connections:'
    print listConns 
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()