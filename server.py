import socket
import struct
def unpack_packet(conn, header_format):
    # TODO: Implement header unpacking based on received bytes
    # First, we need to figure out the heaer size and read it
    header_size = struct.calcsize(header_format)
    header_bytes = conn.recv(header_size)

    # If there is no data/header bytes then either data was not received or no data was sent
    if not header_bytes:
        return "No data received."
    
    # We need to unpack the header to get our routing info
    version, header_len, service_type, payload_len = struct.unpack(header_format, header_bytes)

    # Read the payload based on the length
    payload_bytes = conn.recv(payload_len)

    # Now we need to decode the payload based on the service type
    if service_type == 1:
        # unpack payload as integers
        payload = struct.unpack('!i', payload_bytes)[0]
    elif service_type == 2:
        # unpack payload as float
        payload = struct.unpack('!f', payload_bytes)[0]
    elif service_type == 3:
        # unpack payload as strings
        payload = payload_bytes.decode('utf-8')
    else:
        # the payload is can't be unpacked because we don't know what it is
        payload = "Unkown Service Type"

    # TODO: Create a string from the header fields
    packet_header_as_string = (
        f"Header [V:{version}, L:{header_len}, T:{service_type}, P_Len:{payload_len}] "
        f"| Payload: {payload}"
    )
    # return the string - this will be the payload
    return packet_header_as_string

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 12345
    # Fixed length header -> Version (1 byte), Header Length (1 byte), Service Type (1 byte), Payload Length (2 bytes)
    header_format = '!BBBH' # TODO: Specify the header format using "struct" 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print(f"Server listening...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by: {addr}")
            while True:
                try:
                    # TODO: Receive and unpack packet using the unpack_packet function
                    payload_string = unpack_packet(conn, header_format)

                    if not payload_string or "No data received" in payload_string:
                        break

                    print(f"Processed: {payload_string}")

                    #TODO: create header
                    response_text = "Message Received"
                    #TODO: add payload
                    payload_bytes = response_text.encode()

                    # Create header fields
                    version = 1
                    header_length = struct.calcsize(header_format)
                    service_type = 3
                    payload_length = len(payload_bytes)

                    # Pack the header
                    header = struct.pack(
                        '!BBBH',
                        version,
                        header_length,
                        service_type,
                        payload_length
                    )
                    #TODO: send to client
                    conn.sendall(header + payload_bytes)
                    pass
                except:
                    print("Connection closed or an error occurred")
                    break
                #TODO: create header
                #TODO: add payload
                #TODO: send to client