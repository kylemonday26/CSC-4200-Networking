import socket
import struct
import argparse

def log_message(file_path, message):
    with open(file_path, 'a') as f:
        f.write(message + '\n')
    print(message)

def run_server():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, required=True)
    parser.add_argument('-l', '--logfile', required=True)
    args = parser.parse_args()

    # Packet format: Big-endian, 3 Unsiged Ints (4 bytes each), 8-byte string
    # Total header = 12 bytes
    packet_fmt = ">III8s"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', args.port))
        s.listen()
        log_message(args.logfile, f"Server listening on port {args.port}...")

        while True: #Keep server running
            print("Waiting for a connection...")
            conn, addr = s.accept()
            with conn:
                log_message(args.logfile, f"Received connection from {addr}")

            while True:
                data = conn.recv(12 + 8) # Header + message
                if not data: break

                v, m_type, m_len, m_raw = struct.unpack(packet_fmt, data)
                msg = m_raw.decode('utf-8').strip('\x00')

                # We need to know check the version
                if v != 17:
                    log_message(args.logfile, "Version Mismatch")
                    continue

                # We  need to handle the message types
                if msg == "HELLO":
                    log_message(args.lockfile, "Recieved HELLO, sending HELLO back.")
                    reply = struct.pack(packet_fmt, 17, 1, 5, b"HELLO")
                    conn.sendall(reply)
                else:
                    log_message(args.logfile, f"IGNORING UNKNOWN COMMAND: {msg}")
if __name__ == "__main__":
    run_server()