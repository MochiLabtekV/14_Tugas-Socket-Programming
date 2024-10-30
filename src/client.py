import socket
import threading
from tkinter import *
from tkinter import scrolledtext
import csv
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
    
    if choice == '1':
        if register_client():
            initialize_gui()
    elif choice == '2':
        if login_client():
            initialize_gui()
    else:
        print("Invalid choice. Please enter 1 or 2.")

def receive_message():
    global client
    while True:
        message, _ = client.recvfrom(1024)
        window.after(100,chat_log.insert(END, f"Client {client.getsockname()} : {message.decode('utf-8')} \n"))

def send_message():
    global client, username
    message = entry_message.get()
    if message and client:
        formatted_message = f"{username}: {message}"
        chat_log.insert(END, f"You: {message}\n")
        client.sendto(message.encode('utf-8'), server_address)
        entry_message.delete(0, END)

def initialize_gui():
    global window, chat_log, entry_message

    window = Tk()
    window.title("Client")

    chat_log = scrolledtext.ScrolledText(window, width=70, height=10)
    chat_log.grid(column=0, row=0, padx=10, pady=10)

    entry_message = Entry(window, width=60)
    entry_message.grid(column=0, row=1, padx=10, pady=10)

    send_button = Button(window, text="Send", command=send_message)
    send_button.grid(column=0, row=2, padx=10, pady=10)

    threading.Thread(target=receive_message, daemon=True).start()
    window.mainloop()

def setup_client():
    global client, server_address
    IpAddress = input("Masukkan IP Address Server: ") 
    portServer = int(input("Masukkan Port Number Server: "))
    clientPort = int(input("Masukkan Port Number Client: "))

    # Create UDP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the client to the specified client port
    client.bind(('', clientPort))

    # Set the server address using user input
    server_address = (IpAddress, portServer)
    
    command_prompt()

# Run the setup and start command prompt
setup_client()