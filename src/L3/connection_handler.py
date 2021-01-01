import argparse
import collections
import ipaddress
import socket
import sys
import threading
import time
from multiprocessing import Lock
from packet import Packet

class clientcl:
    def __init__(self):
        self.packet_size=20
        self.transmission_delay=0.01

        self.rcv_window=collections.OrderedDict()
        self.window=collections.OrderedDict()
        self.all_pkt=collections.OrderedDict()
        self.window_acks=collections.OrderedDict()
        self.thread_lock=Lock()
        self.listen_nak=True
        self.receive_window_size=0
        self.window_start=0
        self.window_end=0
        self.final_output=''
        self.received_packets=0
        self.sender=tuple()
        self.connections=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.delay=self.transmission_delay+0.05

    def __del__(self):
        print( "Client Recieved the full packet")

    def client(self,inputline,router_addr, router_port, server_addr, server_port):
        contents=bytearray(inputline.encode())
        peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
        no_packets=0
        if(sys.getsizeof(contents)<self.packet_size):
            self.all_pkt[no_packets]=contents
            no_packets=+1
        else:
            for i in range(0,sys.getsizeof(contents),self.packet_size):
                self.all_pkt[no_packets]=contents[i:i + self.packet_size]
                no_packets=no_packets+1
        if(self.handshake(self.connections,router_addr,peer_ip,server_port, router_port,len(self.all_pkt))):
            threading.Thread(target=self.acks, args=(self.connections, 1024)).start()
            self.client_packet_send(self.connections,self.all_pkt,router_addr,router_port,peer_ip,server_port)
            return self.client_receive(self.connections,router_addr,router_port,peer_ip,server_port)
        else:
            print("Handshake unsuccessful")


    def resend_packet(self,conn,router_addr, router_port,peer_ip,server_port):
        while(len(self.window_acks)!=len(self.window)):
            for i in self.window:
                if not self.window_acks.keys().__contains__(i):
                    p = Packet(packet_type=0,
                            seq_num=i,
                            peer_ip_addr=peer_ip,
                            peer_port=server_port,
                            payload=bytes(self.window[i]))
                    print('retransmitting packet:', p.seq_num)
                    self.connections.sendto(p.to_bytes(), (router_addr, router_port))
            time.sleep(self.delay)
        if (len(self.window_acks) == len(self.window)):
            self.window.clear()
            self.window_acks.clear()
            return
    def handshake(self,conn,router_addr,peer_ip,server_port, router_port,len_packets):
            p = Packet(packet_type=1,
                       seq_num=0,
                       peer_ip_addr=peer_ip,
                       peer_port=server_port,
                       payload=''.encode("utf-8"))
            self.connections.sendto(p.to_bytes(), (router_addr, router_port))
            print('Sending "{}" '.format("SYN"))
            time.sleep(self.delay)
            print('Waiting for a response')
            response, sender = self.connections.recvfrom(1024)
            p1 = Packet.from_bytes(response)
            print('Router: ', sender)
            if(p1.packet_type==2):
                print('Recieved SYN+ACK from server')
                p1.packet_type=3
                p1.payload=str(len_packets).encode("utf-8")
                print('Sending ACK for Handshake')
                self.connections.sendto(p1.to_bytes(),sender)
                sendData=True
            return True
            
    def client_packet_send(self,conn,all_packet,router_addr,router_port,peer_ip,server_port):

        if(len(all_packet)>1):
            window_size=int(len(all_packet)/2)
        else:
            window_size = len(all_packet)
        windowcount=0
        while(len(all_packet)!=0):
            while(len(self.window)<window_size and len(all_packet)!=0):
                    j=0
                    windowcount=windowcount+1
                    for i in all_packet:
                        self.window[i]=all_packet[i]
                        j=j+1
                        if len(self.window)==window_size:
                            break
                    for i in self.window.keys():
                        del self.all_pkt[i]
                        p = Packet(packet_type=0,
                                   seq_num=i,
                                   peer_ip_addr=peer_ip,
                                   peer_port=server_port,
                                   payload=bytes(self.window[i]))
                        print('sending packet:', p.seq_num)
                        self.connections.sendto(p.to_bytes(), (router_addr, router_port))
                    time.sleep(self.delay)
                    self.resend_packet(conn,router_addr, router_port,peer_ip,server_port)

        print('data transmission finished')
        self.listen_nak=False
        p.packet_type=5
        self.connections.sendto(p.to_bytes(), (router_addr, router_port))
        return
    def acks(self,conn,port):
        while self.listen_nak:
                response, sender = self.connections.recvfrom(1024)
                p = Packet.from_bytes(response)
                if(p.packet_type==4):
                    p.packet_type=0
                    print('Recieved ack for packet:',p.seq_num)
                    self.window_acks[p.seq_num]=p.payload
        return
    
    

    def client_receive(self,conn,router_addr,router_port,peer_ip,server_port):
        listen = True
        while listen:
            print('waiting for server to to send reply')
            data, sender = self.connections.recvfrom(1024)
            p = Packet.from_bytes(data)
            print("recevied packet type and sequence No.",p.packet_type,p.seq_num)
            if (p.packet_type ==1):
                expected_packets=int(p.payload)
                if (expected_packets > 1):
                    receive_window_size = int(expected_packets / 2)
                else:
                    receive_window_size = expected_packets
                    window_end = receive_window_size
                window_start = 0
                p.packet_type=3
                self.connections.sendto(p.to_bytes(),sender)
            elif(p.packet_type ==0):
                if (len(self.rcv_window) == receive_window_size and p.seq_num >= window_end + 1):
                    str = ''
                    for i in sorted(self.rcv_window.keys()):
                        str = str + self.rcv_window[i].payload.decode("utf-8")
                    self.final_output = self.final_output + str
                    self.rcv_window.clear()
                    window_start = window_end + 1
                    window_end = window_start + receive_window_size

                if (p.seq_num in range(window_start, window_end + 1)):
                    if (not self.rcv_window.__contains__(p.seq_num)):
                        self.rcv_window[p.seq_num] = p
                        self.received_packets += 1
                        p.packet_type = 4
                        print('sending ack for packet:', p.seq_num)
                        self.connections.sendto(p.to_bytes(), sender)
                    else:
                        p.packet_type = 4
                        print('sending ack for packet:', p.seq_num)
                        self.connections.sendto(p.to_bytes(), sender)
                if (self.received_packets == expected_packets ):
                    str = ''
                    for i in sorted(self.rcv_window.keys()):
                        str = str + self.rcv_window[i].payload.decode("utf-8")
                    self.final_output = self.final_output + str
                    p.packet_type=5
                    self.connections.sendto(p.to_bytes(), sender)
                    listen=False
                    return self.final_output
    def bind_port(self,cli_port):
        self.connections.bind(('',cli_port))
    