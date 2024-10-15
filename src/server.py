#Tugas UDP Socket Programming
#II2120 - Jaringan Komputer
#18223052 & 18223106

import socket
import threading
from tkinter import *
from tkinter import scrolledtext

#Initialize socket type = socket.SOCK_DGRAM
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 55555)) #Max port number: 65535