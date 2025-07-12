import socket
import cv2
import pickle
import struct

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('SERVER_IP', 5000))  # Replace SERVER_IP with the server's IP address

data = b""
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        data += client_socket.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize the frame
    frame = pickle.loads(frame_data)

    # Display the frame
    cv2.imshow("Received Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
cv2.destroyAllWindows()



