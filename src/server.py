import socket
import threading
from tkinter import *
from tkinter import scrolledtext, messagebox
from utilities import is_valid_ip
import os

# Set up UDP server for receiving messages
ipAddress = input("Enter Server IP: ")
while not is_valid_ip(ipAddress):
    print("Invalid IP address. Please enter a valid IPv4 address.")
    ipAddress = input("Enter Server IP: ")

portServer = int(input("Enter Server port: "))
chatroom_password = input("Enter Chatroom password: ")

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((ipAddress, portServer))

# Set up TCP server for sending ACKs
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((ipAddress, portServer + 1))  # Use different port for TCP
tcp_server.listen(5)

clients = set()
client_usernames = {}

#password_input = RNG(100, 999)

# Write the password to password.py
#with open("password.py", "w") as f:
#    f.write(f'password = "{password_input}"')

def update_client_list():
    list_clients.delete(0, END)
    for client in clients:
        list_clients.insert(END, f"Client = {client_usernames[client]} : {client[0]}:{client[1]}")  # Displaying username

def start_server():
    while True:
        try:
            message, client_address = udp_server.recvfrom(1024)
            message = message.decode('utf-8')

            # Check if it's an authentication message
            if message.startswith("AUTH |"):
                _, username, password = message.split("|", 2)
                if password.strip() == chatroom_password:  # Check password
                    clients.add(client_address)
                    client_usernames[client_address] = username.strip()
                    udp_server.sendto("AUTH_SUCCESS".encode('utf-8'), client_address)
                    notify_clients(client_address, "has joined the chat")
                else:
                    udp_server.sendto("AUTH_FAILED".encode('utf-8'), client_address)
            else:
                # Handle other types of messages (e.g., chat messages)
                forward_message(message.encode('utf-8'), client_address)

            send_ack(client_address)  # Send ACK after processing the message
        except Exception as e:
            print(f"Error: {e}")  # Debug output for any exceptions


# Handle file transfer
def handle_file_transfer(message, sender_address):
    _, username, filename = message.decode('utf-8').split(':', 2)
    
    try:
        with open(filename, 'wb') as f:
            while True:
                data, addr = udp_server.recvfrom(1024)
                if not data:  # Stop sending if an empty message is received
                    break
                f.write(data)

        window.after(100, lambda: chat_log.insert(END, f"File {filename} received from {username}.\n"))
        
        # Confirmation dialog to open a file
        window.after(100, lambda: confirm_open_file(filename))
        
        # Send the file to all other clients
        with open(filename, 'rb') as f:
            file_data = f.read(1024)
            while file_data:
                for client in clients:
                    if client != sender_address:
                        udp_server.sendto(f"FILE:{username}:{filename}".encode('utf-8'), client)  # Kirim informasi file
                        udp_server.sendto(file_data, client)  # Kirim data file
                file_data = f.read(1024)
    except Exception as e:
        window.after(100, lambda: chat_log.insert(END, f"Error receiving file: {e}\n"))

# Confirm to open the received file
def confirm_open_file(filename):
    if messagebox.askyesno("Open File", f"File {filename} received. Do you want to open it?"):
        try:
            os.startfile(filename)  # Windows only
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

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
            formatted_message = f"{client_usernames[sender_address]}: {message.decode('utf-8').split(':', 1)[1]}" 
            udp_server.sendto(formatted_message.encode('utf-8'), client)
    window.after(100, lambda: chat_log.insert(END, f"{client_usernames[sender_address]}:{message.decode('utf-8').split(':', 1)[1]}\n"))

# Send ACK using TCP
sequence_number = 0

def send_ack(client_address):
    global sequence_number
    try:
        # Accept connection from client
        tcp_client, _ = tcp_server.accept()
        
        # Prepare the ACK message with sequence number
        ack_message = f"ACK-{sequence_number}"
        
        # Send ACK message to the client
        tcp_client.send(ack_message.encode('utf-8'))
        
        # Increment the sequence number for the next ACK
        sequence_number += 1
    except Exception as e:
        print(f"Error sending ACK: {e}")
    finally:
        tcp_client.close()
        
        # Print ACK log with sequence number
        window.after(100, lambda: chat_log.insert(END, f"ACK-{sequence_number - 1} sent to {client_address}\n"))

# Function to initialize the GUI
def initialize_gui():
    global window, chat_log, list_clients
 
    window = Tk()
    window.title("Server")

    main_frame = Frame(window)
    main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    chatroom_label = Label(main_frame, text="MochiLabtekV ʕ•́ᴥ•̀ʔっ♡ ", font=("Arial", 12, "bold"))
    chatroom_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

    password_label = Label(main_frame, text=f"Chatroom Password: {chatroom_password}", font=("Arial", 10, "bold"))
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
