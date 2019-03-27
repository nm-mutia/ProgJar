import socket
import os

TARGET_IP = '127.0.0.1'
TARGET_PORT = 5000

sock = socket.socket()
sock.connect((TARGET_IP, TARGET_PORT))

def minta():
    namafile = raw_input("File name? -> ")
    if namafile[:4] == 'list':  # digunakan untuk list isi directory / folder
        datas = sock.recv(1024)
        print "directory: \n" + str(datas)
    elif namafile != 'q':
        sock.send(namafile)
        data = sock.recv(1024)
        if data.startswith("ADA"):
            sizes = long(data[3:])
            msg = raw_input("File exists, " + str(sizes) + " bytes, download? (Y/N)? -> ")
            if msg == 'Y':
                print namafile
                sock.send("OK")
                fp = open('new_'+namafile, 'wb')
                #os.makedirs(os.path.dirname('new_'+namafile), exist_ok=True)
                data = sock.recv(1024)
                total = len(data)
                fp.write(data)
                while total < sizes:
                    data = sock.recv(1024)
                    total += len(data)
                    fp.write(data)
                    print "Download {0:.2f}".format((total/float(sizes))*100) + "%"
                print "Download finished!"
                fp.close()
            else:
                print "tidak ada"
        else:
            print "File tidak ada!"

    #sock.close()

def kirim():
    namafile = raw_input("File name? -> ")
    print "Uploading File to Server"
    upload_name = namafile
    sock.send("SENDING " + str(os.path.getsize(upload_name)))
    with open(upload_name, 'rb') as fp:
        sizes2 = fp.read(1024)
        sock.send(sizes2)
        while sizes2 != "":
            sizes2 = fp.read(1024)
            sock.send(sizes2)
    fp.close()


if __name__ == '__main__':
    while True:
        inp = raw_input("1.Download file 2.Upload File \n")
        sock.sendto(inp, (TARGET_IP, TARGET_PORT))
        if int(inp) == 1:
            minta()
        elif int(inp) == 2:
            kirim()
