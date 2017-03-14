import socket
import sys
import datetime

# Create a TCP/IP socket
sock = socket.socket()

# Bind the socket to the port
server_address = ('', 333)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(5)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'Time "%s"' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print >>sys.stderr, 'received "%s"' % data
            if data:
                print >>sys.stderr, 'Saving Data'

                filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".txt"
                fileData = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "," + data + "\n"

                file = open(filename,"a")
                file.write(fileData)
                file.close()



    finally:
        # Clean up the connection
        print >> sys.stderr, 'Error!'
        connection.close()
