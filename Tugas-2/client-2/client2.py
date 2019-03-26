import socket

TARGET_IP = "127.0.0.1"
TARGET_PORT = 9000

sockcli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockcli.connect((TARGET_IP, TARGET_PORT))

sockcli.sendto("READY", (TARGET_IP, TARGET_PORT))
while True:
    data, addr = sockcli.recvfrom(1024)
    txt = str(data)
    if data.startswith("SEND"):
        tmp = txt.split()
        basename = tmp[1]
        rcv = 0
        fp = open(basename, 'wb+')
        print 'got filename ' + basename

    elif data.startswith("END"):
        fp.close()
        print "End of file : " + basename

    elif data.startswith("CLOSE"):
        print "\nClosing connection"
        break

    else:
        fp.write(data)
        rcv += len(data)
        print 'Received ' + str(rcv)
