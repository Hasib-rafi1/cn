import argparse
import collections
import socket
import sys
import ipaddress
import threading
import time
from multiprocessing import Lock
from packet import Packet
class server:
    def __init__(self):
        self.clientport=int()
        # self.RseqNo = 0
        self.rcv_data = 0
        self.transmission_delay=0.01
        self.receive_all_pkt=collections.OrderedDict()
        self.receive_window=collections.OrderedDict()
        self.send_window=collections.OrderedDict()
        self.send_all_pkt=collections.OrderedDict()
        self.window_acks=collections.OrderedDict()
        self.send_window_size=0
        self.data_rcv=False
        self.recv_data=False
        #self.final=set()
        self.window_size=0
        self.recieved_packets=0
        self.window_start=0
        self.window_end=0
        self.syn_received=False
        self.final=''
        self.delay=self.transmission_delay+0.05
        self.listen_syc_ackk=True
        self.listen=True
        self.connections=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.router_add='localhost'
        self.server_add='localhost'
        self.router_port=int(0)
        self.server_port=int(0)
        self.thread_lock=Lock()
        self.sender=tuple()
        self.client_port= 0
        self.packet_temp = []
    def __del__(self):
        print( "Job Finished")
    def bind_port(self,port):
        try:
            self.connections.bind(('', port))
        except socket.error as msg:
            print("")
    #listen from client
    def run_server(self,port,pack = None):
            self.listen=True
            print('Echo server is listening at', port)
            self.connections.bind(('', port))
            while self.listen:
                p = None
                if pack != None:
                    p , self.sender = pack
                    pack = None
                else:
                    data, self.sender = self.connections.recvfrom(1024)
                    p = Packet.from_bytes(data)

                if self.client_port == 0 :
                    self.client_port = p.peer_port

                if self.client_port == p.peer_port:
                    server_port=p.peer_port
                    if(p.packet_type==0 and self.data_rcv==True):
                        p.packet_type=4
                        self.connections.sendto(p.to_bytes(), self.sender)
                    elif(p.packet_type==5):
                        self.listen=False
                    if(self.recv_data==True and p.packet_type==0):
                        self.handle_data(self.connections, p, self.sender)
                    else:
                        self.handle_client(self.connections, p, self.sender)
                else:
                    self.packet_temp.append((p, self.sender))
                    print(self.packet_temp)
            self.client_port = 0
            return self.final
    def get_final(self):
        return(self.final)
    def SYNack(self,conn):
        while self.listen_syc_ackk:
            response, self.sender = conn.recvfrom(1024)
            p = Packet.from_bytes(response)
            self.thread_lock.acquire()
            if (p.packet_type == 3):
                self.syn_received = True
                self.listen_syc_ackk=False
                print('SYN ack received from client')
                self.thread_lock.release()
                return
            self.thread_lock.release()
    def handle_data(self,conn, p,sender):
            if(p.seq_num==6):
                print("")
            if (len(self.receive_window)==self.window_size and p.seq_num>=self.window_end+1):
                str=''
                print(sorted(self.receive_window))
                for i in sorted(self.receive_window.keys()):
                    str=str+self.receive_window[i].payload.decode("utf-8")
                self.final=self.final+str
                self.receive_window.clear()
                self.window_start=self.window_end+1
                self.window_end=self.window_start+self.window_size

            if(p.seq_num in range(self.window_start,self.window_end+1)):
                if(not self.receive_window.__contains__(p.seq_num)):
                    self.receive_window[p.seq_num]=p
                    self.recieved_packets+=1
                    p.packet_type=4
                    print('Sending ack for packet:',p.seq_num)
                    conn.sendto(p.to_bytes(), sender)
                else:
                    p.packet_type = 4
                    print('Sending ack for packet:', p.seq_num)
                    conn.sendto(p.to_bytes(), sender)
            if (self.recieved_packets == self.rcv_data):
                str = ''
                for i in sorted(self.receive_window.keys()):
                    str = str + self.receive_window[i].payload.decode("utf-8")
                self.final = self.final + str
                print('Complete string received', self.final)
                self.data_rcv=True
                return False
            return True
    
    def acks(self,conn,port):
        listenack=True
        while listenack:
                response, sender = conn.recvfrom(1024)
                p = Packet.from_bytes(response)
                self.thread_lock.acquire()
                if(p.packet_type==5):
                    listenack=False
                if(p.packet_type==4):
                    p.packet_type=0
                    print('Recieved ack for packet:',p.seq_num)
                    self.window_acks[p.seq_num]=p.payload
                self.thread_lock.release()

    def resend_packet(self,conn,router_addr, router_port,peer_ip,server_port):
        while(len(self.window_acks)!=len(self.send_window)):
            for i in self.send_window:
                if not self.window_acks.keys().__contains__(i):
                    p = Packet(packet_type=0,
                            seq_num=i,
                            peer_ip_addr=peer_ip,
                            peer_port=self.clientport,
                            payload=bytes(self.send_window[i]))
                    print('Retransmitting packet:', p.seq_num)
                    conn.sendto(p.to_bytes(),self.sender)
            time.sleep(self.delay)
        if(len(self.window_acks)==len(self.send_window)):
            self.send_window.clear()
            self.window_acks.clear()
            return
    def resend_SYN(self,conn,p):
        while(not self.syn_received):
            if(not self.listen_syc_ackk):
                return
            print('Resending SYN')
            self.connections.sendto(p.to_bytes(), self.sender)
            time.sleep(self.delay)
        return

    def server_send(self,connections,peer_ip):
        threading.Thread(target=self.acks, args=(connections, 1024)).start()
        if (len(self.send_all_pkt) > 1):
            send_window_size = int(len(self.send_all_pkt) / 2)
        else:
            send_window_size = len(self.send_all_pkt)
        windowcount = 0
        while (len(self.send_all_pkt) != 0):
            while (len(self.send_window) < send_window_size and len(self.send_all_pkt) != 0):
                j = 0
                windowcount = windowcount + 1
                for i in self.send_all_pkt:
                    self.send_window[i] = self.send_all_pkt[i]
                    j = j + 1
                    if len(self.send_window) == send_window_size:
                        break
                for i in self.send_window.keys():
                    del self.send_all_pkt[i]
                    p = Packet(packet_type=0,
                               seq_num=i,
                               peer_ip_addr=peer_ip,
                               peer_port=self.clientport,
                               payload=self.send_window[i])
                    print('Sending packet:', p.seq_num)
                    connections.sendto(p.to_bytes(), self.sender)
                time.sleep(self.delay)
                self.resend_packet(connections,self.router_add, self.router_port, peer_ip, self.server_port)

    def handle_client(self,conn,p, sender):
        try:
            print("Packet type:",p.packet_type)
            print("Packet sequence:", p.seq_num)

            if(p.packet_type==1):
                self.clientport=p.peer_port
                self.first_seqNo=p.seq_num
                print('SYN received')
                p.packet_type=2
                conn.sendto(p.to_bytes(), sender)
                print('SYN+ACK sent')
            if(p.packet_type==3):
                print("ACK received-TCP handshake successful\n")
                self.rcv_data=int(p.payload.decode("utf-8"))
                if(self.rcv_data>1):
                    self.window_size=int(self.rcv_data/2)
                else:
                    self.window_size=self.rcv_data
                self.window_start=0
                self.window_end=self.window_size-1
                self.recv_data=True

        except Exception as e:
            print("Error: ", e)
            
    def server_message(self,message):
        peer_ip = ipaddress.ip_address(socket.gethostbyname(self.server_add))
        contents = bytearray(message.encode())
        no_packets=0
        if (sys.getsizeof(contents) < 1013):
            self.send_all_pkt[no_packets] = contents
            no_packets = +1
        else:
            for i in range(0, sys.getsizeof(contents), 100):
                self.send_all_pkt[no_packets] = contents[i:i + 100]
                no_packets = no_packets + 1
        p = Packet(packet_type=1,
                   seq_num=0,
                   peer_ip_addr=peer_ip,
                   peer_port=self.clientport,
                   payload=str(len(self.send_all_pkt)).encode("utf-8"))
        threading.Thread(target=self.SYNack, args=(self.connections,)).start()
        self.connections.sendto(p.to_bytes(), self.sender)
        print('Send "{}" to client'.format("SYN"))
        time.sleep(self.delay)
        if(self.syn_received==False):
            self.resend_SYN(self.connections,p)
        if(self.syn_received):
            print('Begin transmission of packets to Router: ', self.sender)
            self.server_send(self.connections,peer_ip)
        else:
            print('Unknown response: ', self.sender)
