import socket
import threading
from tkinter import *
from tkinter import scrolledtext

# Set up server
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', 55555))

clients = set()

def update_client_list():
    list_clients.delete(0, END)
    for client in clients:
        list_clients.insert(END, f"Client = IP : {client[0]} port :{client[1]}")

# Server function to receive and forward messages
def start_server():
    while True:
        message, client_address = server.recvfrom(1024)
        if client_address not in clients:
            clients.add(client_address)
            notify_clients(client_address, "Berhasil terhubung")
            window.after(100, update_client_list)
        forward_message(message, client_address)

# Notify all clients when a new client connects
def notify_clients(client_address, message):
    connect_message = f"Client {client_address[1]} {message}"
    for client in clients:
        server.sendto(connect_message.encode('utf-8'), client)
    window.after(100, lambda: chat_log.insert(END, f"Server: {connect_message}\n"))

# Forward message to other clients
def forward_message(message, sender_address):
    for client in clients:
        if client != sender_address:
            server.sendto(message, client)
    window.after(100, lambda: chat_log.insert(END, f"Client {sender_address} : {message.decode('utf-8')}\n"))

# Function to initialize the GUI
def initialize_gui():
    global window, chat_log, list_clients

    window = Tk()
    window.title("Server")

    main_frame = Frame(window)
    main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    Label(main_frame, text="Chat Log:").grid(row=0, column=0, padx=(0, 10), sticky="w")
    chat_log = scrolledtext.ScrolledText(main_frame, width=60, height=20)
    chat_log.grid(row=1, column=0, padx=(0, 10))
    Label(main_frame, text="List of Connected Clients:").grid(row=0, column=1, sticky="w")
    list_clients = Listbox(main_frame, width=30, height=20)
    list_clients.grid(row=1, column=1)
    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()
    window.mainloop()

initialize_gui()