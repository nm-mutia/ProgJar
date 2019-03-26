import socket
import os
from threading import Thread

SERVER_IP = '127.0.0.1'
SERVER_PORT = 9000
NAMAFILE = ["doraemon.jpg", "monster.jpg", "sponge.jpg"]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

def sendPic(ip, port):
    addr = (ip, port)

    for x in NAMAFILE:
        imgsize = os.stat(x).st_size
        sock.sendto("SEND {}".format(x), (addr))

        fp = open(x, 'rb')
        k = fp.read()
        sizes = 0

        for y in k:
            sock.sendto(y, (addr))
            sizes = sizes + 1
            print "Sent {} of {} " . format(sizes, imgsize)

        print "Image %s successfully send to client" % x
        sock.sendto("END", (addr))
        fp.close()

    sock.sendto("CLOSE", (addr))

while True:
    data, addr = sock.recvfrom(1024)
    print "Request : " + str(data)

    if str(data) == "READY":
        thread = Thread(target=sendPic, args=(addr))
        thread.start()