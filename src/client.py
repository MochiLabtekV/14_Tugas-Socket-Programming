import socket
import threading
from tkinter import *
from tkinter import scrolledtext
from utilities import validate_input
from reglog import register_client, login_client

client = None
server_address = None
username = None

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
    password = 111
    while True:
        passClient = int(input("Insert chatroom password: "))
        if (passClient == password):
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
        except:
            break

def send_message():
    global client, username
    message = entry_message.get()
    if message and client:
        formatted_message = f"{username}: {message}"
        chat_log.insert(END, f"You: {message}\n")
        client.sendto(formatted_message.encode('utf-8'), server_address)  # UDP send
        entry_message.delete(0, END)
        receive_ack()  # Wait for TCP ACK

def receive_ack():
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((server_address[0], server_address[1] + 1))  # Connect to TCP server
    ack = tcp_client.recv(1024).decode('utf-8')
    tcp_client.close()
    # ACK diterima, tapi tidak ditampilkan di client

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

    threading.Thread(target=receive_message, daemon=True).start()
    window.mainloop()

def setup_client():
    global client, server_address
    IpAddress = input("Insert Server IP Address: ") 
    portServer = int(input("Insert Server Port Number: "))
    clientPort = int(input("Insert Client Port Number: "))  # Input port untuk client

    # Create UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind socket ke port yang diinginkan oleh client
    client.bind(('', clientPort))  # Bind ke clientPort yang diinput

    # Set the server address using user input
    server_address = (IpAddress, portServer)
    
    command_prompt()

# Run the setup and start command prompt
setup_client()
