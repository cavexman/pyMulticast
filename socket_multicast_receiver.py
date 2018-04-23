# socket_multicast_receiver.py
import socket
import struct
import sys
import pyaudio
import wave

CHUNK = 1024

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

df = open('/tmp/beep.wav', 'wb')

print('\nwaiting to receive message')
# Receive/respond loop
while True:
    data, address = sock.recvfrom(1024)

    if( data == b'done'):
        print('download complete')
        break
    df.write(data)


wf = wave.open('/tmp/beep.wav', 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

snddata = wf.readframes(CHUNK)

while snddata != '':
    stream.write(snddata)
    snddata = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()
