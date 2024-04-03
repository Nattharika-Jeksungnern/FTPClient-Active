import socket
import ftpclient

client = ftpclient.FTPClient()

while True:
    line = input("ftp> ").strip()
    args = line.split()
    command = args[0]

    if command == "open":
        try:
            client.open(args[1], int(args[2]))
        except:
            client.open(args[1], 21)
    elif command == "disconnect" or command == "close":
        client.disconnect()
    elif command == "bye" or command == "quit":
        client.quit()
        break
    elif command == "ls":
        client.ls()
        
    elif command == "pwd":
        client.pwd()
    elif command == "cd":
        try:
            client.cd(args[1])
        except:
            path = input("Remote directory ")
            client.cd(path)
    elif command == "rename":
        if not client.status():
            print("Not connected.")
            continue
        if len(args) == 3:
            client.rename(args[1], args[2])
        elif len(args) == 2:
            newName = input("To name ")
            client.rename(args[1], newName)
        else:
            name = input("From name ")
            newName = input("To name ")
            client.rename(name, newName)
    elif command == "ascii":
        client.ascii()
    elif command == "binary":
        client.binary()
    elif command == "get":
        if not client.status():
            print("Not connected.")
            continue
        if len(args) == 1:
            rName = input("Remote file ")
            lName = input("Local file ")
            client.get(rName, lName)
        elif len(args) == 2:
            client.get(args[1], args[1])
        else:
            client.get(args[1], args[2])
    elif command == "put":
        if not client.status():
            print("Not connected.")
            continue
        if len(args) == 1:
            lName = input("Local file ")
            rName = input("Remote file ")
            client.put(lName, rName)
        elif len(args) == 2:
            client.put(args[1], args[1])
        else:
            client.put(args[1], args[2])
    elif command == "user":
        if not client.status():
            print("Not connected.")
            continue
        try:
            client.user(args[1])
        except:
            username = input("Username ")
            client.user(username)
    elif command == "delete":
        if not client.status():
            print("Not connected.")
            continue
        try:
            client.delete(args[1])
        except:
            fileName = input("Remote file ")
            client.delete(fileName)
    else:
        print("Invalid command.")
    