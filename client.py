import argparse
import socket
import struct

def create_packet(version, header_length, service_type, payload):
    # TODO: Implement packet creation based on parameters
    # TODO: use the python struct module to create a fixed length header
    # TODO: Fixed length header -> Version (1 byte), Header Length (1 byte), Service Type (1 byte), Payload Length (2 bytes)
    # TODO: payload -> variable length
    # TODO: depending on the service type, handle encoding of the different types of payload.
    # TODO: service_type 1 = payload is int, service_type 2 = payload is float, service_type 3 = payload is string
    # We need to handle the payload based on service type
    if service_type == 1:
        # If service type is 1, pack a 4-byte integer
        payload_bytes = struct.pack('!i', int(payload))
    elif service_type == 2:
        # If service type is 2, pack as a 4 byte float
        payload_bytes = struct.pack('!f', float(payload))
    elif service_type == 3:
        # If service type is 3, encode string to bytes
        payload_bytes = payload.encode('utf-8')
    else:
        # Else default to empty bytes if type is unkown
        payload_bytes = b''

    # Get the length of the processed payload
    payload_len = len((payload_bytes))

    # Create the 5-byte fixed header: Version(B), Header Length(B), Service Type(B), Payload(H)
    header = struct.pack('!BBBH', version, header_length, service_type, payload_len)

    # Combine the header and payload_bytes
    packet = header + payload_bytes

    return packet

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Client for packet creation and sending.")
    parser.add_argument('--version', type=int, required=True, help='Packet version')
    parser.add_argument('--header_length', type=int, required=True, help='Length of the packet header')
    parser.add_argument('--service_type', type=int, required=True, help='Service type of the payload (1 for int, 2 for float, 3 for string)')
    parser.add_argument('--payload', type=str, required=True, help='Payload to be packed into the packet')
    parser.add_argument('--host', type=str, default='10.128.0.5', help='Server Internal IP')
    parser.add_argument('--port', type=int, default=12345, help='Server port')
    args = parser.parse_args()
    # TODO: Create and send packet using the create_packet function
    packet = create_packet(args.version, args.header_length, args.service_type, args.payload)
 
    #TODO: connect to the server
    # I will use try/except blocks as networking can be unpredictable
    try:
        # We use with as that ensures the socket is closed automatically even if an error occurs
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"Connecting to {args.host}:{args.port}...")
            s.connect((args.host, args.port))

    #TODO: send the packet
            s.sendall(packet)
            print("Packet sent successfully.")

    #TODO: receive the packet
            # Receive the response header first
            received_header = s.recv(5)
            if not received_header:
                print("Server closed the connection.")
            else:
                # Unpack the header to understand the incoming payload
                # I am shorting version, header_length, service_type, etc to v, hl, st, etc for readability
                v, hl, st, p_len = struct.unpack('!BBBH', received_header)
    #TODO: prints header
                print(f"\n--- Received Header ---\nVersion {v}\nHeader Length: {hl}\nService Type: {st}\nPayload Length: {p_len}")

                # Receive the payload based on the length specifed in the header
                received_payload_bytes = s.recv(p_len)

                # Convert the bytes back into their original format so that people can read the data
                if st == 1:
                    # Converts bytes back to integers
                    final_payload = struct.unpack('!i', received_payload_bytes)[0]
                elif st == 2:
                    # Converts bytes back to float
                    final_payload = struct.unpack('!f', received_payload_bytes)[0]
                else: 
                    # Convert bytes back to strings
                    final_payload = received_payload_bytes.decode('utf-8')
    #TODO: prints payload
                print(f"--- Received Payload ---\nData: {final_payload}\n")
    
    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Check to see if it is running?")
    except struct.error as e:
        print(f"Error: Data formatting issue - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")