import socket
import maskpass 
import time
import os
import random

class FTPClient:
    def __init__(self):
        self.isLoggedIn = False
        self.isConnect = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mode = 'A'
        self.serverIP = ""
        self.dataPort = random.randint(1024,65535)
        self.clientIP = "127.0.0.1"

    def send(self, cmd):
        # Sending commands to server
        cmd += '\r\n'
        self.socket.send(cmd.encode()) 

    def recvSocket(self):
        return self.socket.recv(8192).decode()
    
    def status(self):
        return self.isConnect

    def connectFTP(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self.serverIP = ip
        self.isConnect = True
        resp = self.recvSocket()
        print(resp, end="")

    def open(self,ip, port):
        if self.isConnect:
            print("Already connected to 127.0.0.1, use disconnect first.")
            return
        try:
            #connect to ftp server
            self.connectFTP(ip, port)
            self.serverIP = ip
            self.send("OPTS UTF8 ON")
            resp = self.recvSocket()
            print(resp, end="")

            #user
            username = input(f'User ({ip}:(none)): ')
            cmd = f'USER {username}'
            self.send(cmd)
            resp = self.recvSocket()
            print(resp, end="")

            #password
            password = maskpass.askpass(prompt="Password:", mask="")
            cmd = f'PASS {password}'
            self.send(cmd)
            resp = self.recvSocket()
            isSuccess = resp.split()
            if "230" in isSuccess:
                self.isLoggedIn = True
                print('\n'+resp, end="")
                self.username = username
            else:
                self.isLoggedIn = False
                print('\n'+resp, end="")
                print("Login failed.")
  
        except Exception as e:
            print("Error:", e)

    def disconnect(self):
        if not self.isConnect:
            print("Not connected.")
            return
        self.send("QUIT")
        resp = self.recvSocket()
        print(resp) 
        self.isLoggedIn = False 
        self.isConnect = False
        self.socket.close()

    def quit(self):
        if self.isConnect:
            self.disconnect()
        else:
            print("\n", end="")
    
    def socketData(self):
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.bind((self.clientIP, self.dataPort))
        dataSocket.listen(1)
        return dataSocket
    
    def PORT(self):
        port = str(self.dataPort//256) + "," + str(self.dataPort%256)
        ip = self.clientIP.replace(".", ",")
        serverAddr = ip + "," + port 
        self.send(f'PORT {serverAddr}')
        resp = self.recvSocket()
        print(resp, end="")

    def ls(self):
        if not self.isConnect:
            print("Not connected.")
            return
        #ip port
        self.dataPort = random.randint(1024,65535)
        # self.clientIP = socket.gethostbyname(socket.gethostname())
        print(self.clientIP, self.dataPort)

        #PORT method
        self.PORT()

        self.send("NLST")
        resp = self.recvSocket()
        print(resp, end="")

        startTime = time.time()
        size = 0
        
        #data transfer
        dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSocket.bind((self.clientIP, self.dataPort))
        dataSocket.listen(1)
        connectionSocket,addr = dataSocket.accept()
        while True:
            print("a")
            data = connectionSocket.recv(8196).decode()
            if not data:
                break
            print(data, end="")
            size += len(data)
        
        dataSocket.close()
        
        stopTime = time.time()

        resp = self.recvSocket()
        print(resp, end="")
        
        eTime = stopTime-startTime
        speed = 0
        if eTime == 0:
            speed = size/1024
        else:
            speed = size/eTime/1024
        if size > 0:
            print(f'ftp:{size} bytes received in {eTime:.2f}Seconds {speed:.2f}KBytes/sec.')
        
    def pwd(self):
        if not self.isConnect:
            print("Not connected.")
            return
        self.send("XPWD")
        resp = self.recvSocket()
        print(resp, end="")

    def cd(self, path):
        if not self.isConnect:
            print("Not connected.")
            return
        self.send(f'CWD {path}')
        resp = self.recvSocket()
        print(resp, end="")
        
    def rename(self, name, newName):
        #check is exist
        self.send(f'RNFR {name}')
        isExist = self.recvSocket()

        if isExist.startswith("350"):
            self.send(f'RNTO {newName}')
            resp = self.recvSocket()
            print(isExist, end="")
            print(resp, end="")
        else:
            print(isExist, end="")

    def ascii(self):
        if not self.isConnect:
            print("Not connected.")
            return
        self.send(f'TYPE A')
        resp = self.recvSocket()
        print(resp, end="")
        self.mode = 'A'

    def binary(self):
        if not self.isConnect:
            print("Not connected.")
            return
        self.send(f'TYPE I')
        resp = self.recvSocket()
        print(resp, end="")
        self.mode = 'I'

    def get(self, rName, lName):
        #PORT
        self.PORT()
        #data transfer
        dataSocket = self.socketData()
        # send cmd
        self.send(f'RETR {rName}')
        resp = self.recvSocket()
        print(resp, end="")
        #folder that keep file
        folder = "data"
        # create file
        if self.mode == 'I':
            localFile = open(folder+ "/" + lName, "wb")
        else:
            localFile = open(folder+ "/" + lName, "w")
        # data transfer and write file
        startTime = time.time()
        size = 0

        connectionSocket,addr = dataSocket.accept()
        while True:   
            data = connectionSocket.recv(8196).decode()
            if not data:
                break
            localFile.write(data)
            size += len(data)

        dataSocket.close()    
        localFile.close()

        stopTime = time.time()

        resp = self.recvSocket()
        print(resp, end="")
        
        eTime = stopTime-startTime
        speed = 0
        if eTime == 0:
            speed = size/1024
        else:
            speed = size/eTime/1024
        if size > 0:
            print(f'ftp:{size} bytes received in {eTime:.2f}Seconds {speed:.2f}KBytes/sec.')

    def put(self, lPath, rPath):
        # Check if the local file exists
        if os.path.exists(lPath):
            try:
                # PORT command
                self.PORT()

                dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dataSocket.bind((self.clientIP, self.dataPort))
                dataSocket.listen(1)

                self.send(f'STOR {rPath}')
                resp = self.recvSocket()
                print(resp, end="")

                # Open local file for reading
                if self.mode == 'I':
                    localFile = open(lPath, "rb")
                else:
                    localFile = open(lPath, "r")

                startTime = time.time()

                connectionSocket,addr = dataSocket.accept()
                data = localFile.read(8192)
                while data:
                    if self.mode == 'I':
                        connectionSocket.send(data)
                    else:
                        connectionSocket.send(data.encode())
                    data = localFile.read(8192)

                localFile.close()
                dataSocket.close()

                print("unrecieve")
                resp = self.recvSocket()
                print(resp, end="")
                print("recieve")

                if not "/" in lPath:
                    eTime = time.time() - startTime
                    size = os.path.getsize(lPath)
                    speed = size / (eTime * 1024)
                    print(f'ftp: {size} bytes transferred in {eTime:.2f} seconds ({speed:.2f} KBytes/sec).')

            except Exception as e:
                print("Error:", e)
        else:
            print(f'{lPath}: File not found')

    def user(self, username):
        self.send(f'USER {username}')
        resp = self.recvSocket()
        print(resp, end="")

        if resp.startswith("503"):
            print("Login failed.")
        else:
            password = maskpass.askpass(prompt="Password:", mask="")
            self.send(f'PASS {password}')
            resp = self.recvSocket()
            if resp.startswith("230"):
                self.isLoggedIn = True
                print('\n'+resp, end="")
                self.username = username
            else:
                self.isLoggedIn = False
                print('\n'+resp, end="")
                print("Login failed.")
    
    def delete(self, fileName):
        self.send(f'DELE {fileName}')
        resp = self.recvSocket()
        print(resp, end="")