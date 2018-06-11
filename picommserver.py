import socket
import sys
import RPi.GPIO as GPIO

stateCH1 = 'OFF'
stateCH2 = 'OFF'

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, GPIO.LOW)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
# Bind the socket to the port
server_address = ('', 50000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    try:
        #print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
	    connection, client_address = sock.accept()
	    print >>sys.stderr, 'connection from', client_address
            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            if data:
		if data == 'State1':
			connection.sendall(stateCH1+';Pilz')
		elif data == 'State2':
			connection.sendall(stateCH2+';Heiz')
		elif data == 'ON1':
			stateCH1 = 'ON'
			GPIO.output(3, GPIO.HIGH)
			connection.sendall('ACK')
		elif data == 'OFF1':
			stateCH1 = 'OFF'
			GPIO.output(3, GPIO.LOW)
			connection.sendall('ACK')
		elif data == 'ON2':
			stateCH2 = 'ON'
			GPIO.output(5, GPIO.HIGH)
			connection.sendall('ACK')
		elif data == 'OFF2':
			stateCH2 = 'OFF'
			GPIO.output(5, GPIO.LOW)
			connection.sendall('ACK')	
                print >>sys.stderr, 'sending data back to the client'
		
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
	    connection.close()
    finally:
        # Clean up the connection
        connection.close()
