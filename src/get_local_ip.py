import socket

def get_local_ip():
   hostname = socket.gethostname()
   try:
       local_ip = socket.gethostbyname(hostname)
       return local_ip
   except Exception as e:
       return None

