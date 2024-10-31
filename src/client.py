import socket
import threading
from tkinter import *
from tkinter import scrolledtext, filedialog, messagebox
from utilities import validate_input
from reglog import register_client, login_client
import re
import os

client = None
server_address = None
username = None

def validate_ip(ip):
    # Regex untuk memvalidasi alamat IP
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(pattern, ip):
        # Memastikan setiap oktet antara 0 dan 255
        octets = ip.split(".")
        return all(0 <= int(octet) <= 255 for octet in octets)
    return False

def command_prompt():
    global client, username  
    print("Welcome! Please choose an option:")
    print("1. Register")
    print("2. Login")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        username = register_client()  
        if username:
            validate_password()  
    elif choice == "2":
        username = login_client()  
        if username:
            validate_password()  
    else:
        print("Invalid choice. Please enter 1 or 2.")

def validate_password():
    import password
    expected_password = password.password  # Simpan password di sini
    while True:
        passClient = input("Insert chatroom password: ")
        if passClient == expected_password:
            initialize_gui()
            break
        else:
            print("Wrong password!")

def receive_message():
    global client
    while True:
        try:
            message = client.recv(1024).decode('utf-8')  # TCP recv
            chat_log.insert(END, f"{message}\n")
            if message.startswith("FILE:"):
                handle_received_file(message)
        except:
            break

def send_message():
    global client, username
    message = entry_message.get()
    if message and client:
        formatted_message = f"{username}:{message}"
        chat_log.insert(END, f"You: {message}\n")
        client.sendto(formatted_message.encode('utf-8'), server_address)  # UDP send
        entry_message.delete(0, END)
        receive_ack()  # Wait for TCP ACK

def send_file(filepath):
    global client, username
    if filepath:
        filename = os.path.basename(filepath)
        chat_log.insert(END, f"You are sending file: {filename}\n")
        
        # Send file information to the server
        client.sendto(f"FILE:{username}:{filename}".encode('utf-8'), server_address)

        # Send binary file data to the server
        with open(filepath, 'rb') as file:
            data = file.read(1024)
            while data:
                client.sendto(data, server_address)  # Send file data to the server
                data = file.read(1024)

        # Send a signal that the file has been fully sent
        client.sendto(b'', server_address)  # Send an empty message as a signal that file sending is complete
        chat_log.insert(END, f"File {filename} sent successfully!\n")
        receive_ack()  # Wait for ACK from the server after sending the file

def attach_file():
    filepath = filedialog.askopenfilename()  # Dialog to choose a file
    if filepath:
        send_file(filepath)  # Send the selected file to the server

def handle_received_file(message):
    # Parse the message to get the sender's username and file name
    _, sender_username, filename = message.split(':', 2)  # Split the message to get sender information and file name
    # Save the received file
    with open(filename, 'wb') as f:
        while True:
            data = client.recv(1024)  # Receiving file data from the server
            if not data:
                break
            f.write(data)
    
    # Update the chat log that the file has been received
    chat_log.insert(END, f"File {filename} received from {sender_username}.\n")
    
    # Display a message box to open a file
    confirm_open_file(filename)

def confirm_open_file(filename):
    if messagebox.askyesno("Open File", f"File {filename} received. Do you want to open it?"):
        if os.path.isfile(filename):
            try:
                os.startfile(filename)  # Opening file (Windows)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
        else:
            messagebox.showerror("Error", f"File {filename} does not exist.")

def receive_ack():
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((server_address[0], server_address[1] + 1))  # Connect to TCP server
    ack = tcp_client.recv(1024).decode('utf-8')
    tcp_client.close()
    # ACK received, but not displayed on the client

def initialize_gui():
    global window, chat_log, entry_message

    window = Tk()
    window.title("Client")

    chat_label = Label(window, text="MochiLabtekV ʕ•́ᴥ•̀ʔっ♡ ", font=("Arial", 10, "bold"))
    chat_label.grid(column=0, row=0, padx=10, pady=(10, 5))

    chat_log = scrolledtext.ScrolledText(window, width=70, height=10)
    chat_log.grid(column=0, row=1, padx=10, pady=10)

    entry_message = Entry(window, width=60)
    entry_message.grid(column=0, row=2, padx=10, pady=10)

    send_button = Button(window, text="Send", command=send_message)
    send_button.grid(column=0, row=3, padx=10, pady=10)

    attach_file_button = Button(window, text="Attach File", command=attach_file)
    attach_file_button.grid(column=0, row=4, padx=10, pady=10)

    entry_message.bind("<Return>", lambda event: send_message())

    threading.Thread(target=receive_message, daemon=True).start()
    window.mainloop()

def setup_client():
    global client, server_address
    while True:
        IpAddress = input("Insert Server IP Address: ")
        if validate_ip(IpAddress):
            break
        else:
            print("Invalid IP address. Please enter a valid IP.")

    portServer = int(input("Insert Server Port Number: "))
    clientPort = int(input("Insert Client Port Number: "))  

    # Create UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(('', clientPort))  # Bind to the input clientPort

    # Set the server address using user input
    server_address = (IpAddress, portServer)
    
    command_prompt()

# Run the setup and start command prompt
setup_client()
