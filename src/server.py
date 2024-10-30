import socket
import threading
from tkinter import *
from tkinter import scrolledtext
from RNG import RNG
import password

# Set up UDP server for receiving messages
ipAddress = input("Enter server IP: ")
portServer = int(input("Enter server port: "))

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((ipAddress, portServer))

# Set up TCP server for sending ACKs
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((ipAddress, portServer + 1))  # Use different port for TCP
tcp_server.listen(5)

clients = set()
client_usernames = {} 

password_input = RNG(100,999)

# Write the password to password.py
with open("password.py", "w") as f:
    f.write(f'password = "{password_input}"')

def update_client_list():
    list_clients.delete(0, END)
    for client in clients:
        list_clients.insert(END, f"Client = {client_usernames[client]} : {client[0]}:{client[1]}")  # Menampilkan username

# Server function to receive and forward messages
def start_server():
    while True:
        message, client_address = udp_server.recvfrom(1024)
        if client_address not in clients:
            clients.add(client_address)
            username = message.decode('utf-8').split(":")[0]  
            client_usernames[client_address] = username  
            notify_clients(client_address, "has joined the chat")
            window.after(100, update_client_list)
        else:
            forward_message(message, client_address)
        send_ack(client_address)

# Notify all clients when a new client connects
def notify_clients(client_address, message):
    connect_message = f"{client_usernames[client_address]} {message}"
    for client in clients:
        udp_server.sendto(connect_message.encode('utf-8'), client)
    window.after(100, lambda: chat_log.insert(END, f"Server: {connect_message}\n"))

# Forward message to other clients
def forward_message(message, sender_address):
    for client in clients:
        if client != sender_address:
            formatted_message = f"{client_usernames[sender_address]}: {message.decode('utf-8').split(':', 1)[1]}"  # Hanya tampilkan isi pesan
            udp_server.sendto(formatted_message.encode('utf-8'), client)
    window.after(100, lambda: chat_log.insert(END, f"{client_usernames[sender_address]}:{message.decode('utf-8').split(':', 1)[1]}\n"))

# Send ACK using TCP
def send_ack(client_address):
    tcp_client, _ = tcp_server.accept()  # Wait for TCP connection from client
    ack_message = "ACK"
    tcp_client.send(ack_message.encode('utf-8'))  # Send ACK to client
    tcp_client.close()
    window.after(100, lambda: chat_log.insert(END, f"ACK sent to {client_address}\n"))

# Function to initialize the GUI
def initialize_gui():
    global window, chat_log, list_clients, password

    window = Tk()
    window.title("Server")

    main_frame = Frame(window)
    main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    chatroom_label = Label(main_frame, text="MochiLabtekV ʕ•́ᴥ•̀ʔっ♡ ", font=("Arial", 12, "bold"))
    chatroom_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

    password_label = Label(main_frame, text=f"Chatroom Password: {password_input}", font=("Arial", 10, "bold"))
    password_label.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="w")

    Label(main_frame, text="Chat Log:").grid(row=2, column=0, padx=(0, 10), sticky="w")
    chat_log = scrolledtext.ScrolledText(main_frame, width=60, height=20)
    chat_log.grid(row=3, column=0, padx=(0, 10))

    Label(main_frame, text="List of Connected Clients:").grid(row=2, column=1, sticky="w")
    list_clients = Listbox(main_frame, width=30, height=20)
    list_clients.grid(row=3, column=1)

    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()
    window.mainloop()

initialize_gui()
