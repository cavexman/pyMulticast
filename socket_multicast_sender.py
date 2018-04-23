# socket_multicast_sender.py
import socket
import struct
import sys

CHUNK = 1024

#message = b'very important data'
wf = open('/Users/caveman/Desktop/beep-01a.wav', 'rb')
#message = wf.read() 
  

#message = wf.readframes(CHUNK)

multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not
# go past the local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:
    while True:
            message = wf.read(CHUNK) 
            if not message:
                message = b'done'
                sent = sock.sendto(message, multicast_group)
                break           
            sent = sock.sendto(message, multicast_group)
    
 

finally:
    print('closing socket')
    sock.close()
