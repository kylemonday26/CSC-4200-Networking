import socket
import struct
import argparse
import sys

def log_client(file_path, message):
    with open(file_path, 'a') as f:
        f.write(message + '\n')
    print(message)

def run_client():
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('-p', '--port', type=int, required=True)
    parser.add_argument('-l', '--logfile', required=True)
    args = parser.parse_args()

    packet_fmt = ">III8s"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((args.host, args.port))

            # Send the HELLO
            hello_pkt = struct.pack(packet_fmt, 17, 1, 5, b"HELLO")
            s.sendall(hello_pkt)

            # Receive the Reply
            data = s.recv(20)
            V, _, _, _ = struct.unpack(packet_fmt, data)

            if V == 17:
                log_client(args.logfile, "VERSION ACCEPTED")
                # Send Comman Type 1 = LIGHTON
                cmd_pkt = struct.pack(packet_fmt, 17, 1, 7, b"LIGHTON")
                s.sendall(cmd_pkt)

                # Receive SUCCESS
                final_data = s.recv(20)
                _, _, _, res_raw = struct.unpack(packet_fmt, final_data)
                log_client(args.logfile, f"Server Reply: {res_raw.decode().strip('\x00')}")
            else:
                log_client(args.logfile, "VERSION MISMATCH")

            log_client(args.logfile, "Gracefully shutting down.")

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    run_client()