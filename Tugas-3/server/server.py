import socket
import threading
import os

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socks.bind((SERVER_IP, SERVER_PORT))
socks.listen(5)

print "Server start"

def FileAsk(name, socks):
    while True:
        namafile = socks.recv(1024)
        #if namafile[:4] == 'list':
        #    print "print directory list"
        #    print "directory path: " + namafile[5:]
        #    fl = os.listdir(namafile[5:])
        #    print fl
        #    socks.send(str(fl))

        if os.path.isfile(namafile):
            socks.send("ADA " + str(os.path.getsize(namafile)))
            resp = socks.recv(1024)
            if resp.startswith("OK"):
                with open(namafile, 'rb') as fp:
                    k = fp.read(1024)
                    socks.send(k)
                    while k != "":
                        k = fp.read(1024)
                        socks.send(k)
        else:
            socks.send("ERR ")
        #socks.close()

def Receive(name, socks):
    namafile = socks.recv(1024)
    print "Uploading File to Server"
    uploadResponse = socks.recv(1024)
    if uploadResponse[:7] == "SENDING":
        fp = open('server_' + namafile, 'wb')
        data = socks.recv(1024)
        filesize = long(uploadResponse[8:])
        totalRecv = len(data)
        fp.write(data)
        while totalRecv < filesize:
            data = socks.recv(1024)
            totalRecv += len(data)
            fp.write(data)
            print "Upload {0:.2f}".format((totalRecv / float(filesize)) * 100) + "%"

        print "Upload Complete!"
        fp.close()
    else:
        socks.send("ERR")

while True:
    conn, addr = socks.accept()
    print "Client connect " + str(addr)
    #print conn
    #con = socks.recv(1024)
    #if con[:0]=='1':
    thread = threading.Thread(target=FileAsk, args=("thread", conn))
    thread.start()
    #elif con[:0]=='2':
    #   thread = threading.Thread(target=Receive, args=("thread", conn))
    #    thread.start()

#socks.close()

