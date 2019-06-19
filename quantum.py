import socket
import os

class Quantum:
    def __init__(self,host=socket.gethostbyname(socket.gethostname()),port=5000,sok=socket.socket(),server=True):
        self.host = host
        self.port = port
        self.sok = sok

        if server==False:
            self.client()
        else:
            self.server()

    def server(self):
        '''server program'''
        print("SERVER MODE ON | HOST ",self.host,' | PORT ',self.port)
        self.sok.bind((self.host,self.port))
        self.sok.listen(10)

        ops = ['help','file','download','upload','dl','up']
        conn,addr = self.sok.accept()
        print('CONNECTED TO CLIENT',addr)

        while True:
            ###communication...
            r = conn.recv(1024).decode() #rx
            print('CLIENT :',r)

            if r in ops:
                if r == 'help':
                    msg = str(ops).encode()
                    conn.send(msg)
                elif r == 'file':
                    top = str(os.getcwd())+'\\store'
                    file_name = ''
                    for root, dirs, files in os.walk(top):
	                    file_name = str(files).encode()
                    conn.send(file_name)
                elif r == 'download' or 'dl':
                    '''download operation'''
                    buffer = 0 #buffer size variable
                    msg = str('dl_ack').encode() #download ack
                    conn.send(msg)               #tx
                    r = conn.recv(1024).decode() #rx file name
                    path_var = str(os.getcwd())+'\\store'+'\\'+r
                    print(path_var)
                    if os.path.exists(path_var):
                        msg = str('OK').encode()
                        conn.send(msg)          #tx 'OK'
                        r = conn.recv(1024).decode() #rx 'OK'
                        size = os.path.getsize(path_var)
                        msg = str(size).encode()
                        conn.send(msg)   #tx
                        r = conn.recv(1024).decode() #rx 'OK'
                        #file sending...
                        file = open(path_var,'rb')
                        file_data = file.read(size)
                        conn.send(file_data) #tx


                    else:
                        msg = "FILE DOES NOT EXIST".encode()
                        conn.send(msg)
                else:
                    print("SERVICE CURRENTLY UNAVAILABLE")


            else:
                conn.send(str('INVALID COMMAND').encode())

    def client(self):
        '''client program'''
        self.sok.connect((self.host,self.port))
        print("CLIENT MODE ON\n CONNECTED...")
        while True:
            msg = input(str('CLIENT :')).encode()
            self.sok.send(msg)                  #tx
            r = self.sok.recv(1024).decode()    #rx

            if r == 'dl_ack':
                '''download operation'''
                print('SERVER: File Name?')
                msg_file = input(str('CLIENT :')).encode()
                self.sok.send(msg_file)          #tx file name
                r = self.sok.recv(1024).decode() #rx  'OK'
                if r == 'OK':
                    msg = str('OK').encode()
                    self.sok.send(msg)  #tx 'OK'
                    r_size = int(self.sok.recv(1024).decode())#rx
                    self.sok.send(msg) #tx ok
                    #file receive
                    path_var = str(os.getcwd())+'\\download'+'\\'+msg_file.decode()
                    file = open(path_var,'wb')
                    file_data = self.sok.recv(r_size+100)  #rx file
                    file.write(file_data)
                    file.close()
                    print('SERVER: SENT!')

                else:
                    pass

            else:
                print('SERVER: ',r)


if __name__ == '__main__':
    ex = Quantum(host='10.24.131.228')
