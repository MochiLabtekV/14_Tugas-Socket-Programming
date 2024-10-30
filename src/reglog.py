from utilities import validate_input
import csv

csv_file = 'client_data.csv'

# Helper functions for CSV handling
def read_csv():
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_csv(id, username, password):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id, username, password])

# Register client with unique username
def register_client():
    user_data = read_csv()
    username = input("Insert username: ")
    password = input("Insert password: ")

    if any(user['username'] == username for user in user_data):
        print("Username already taken. Please try again.")
        return False
    else:
        user_id = len(user_data) + 1
        write_csv(user_id, username, password)
        print(f"Registration successful! Welcome, {username}!")
        return True

# Login client with username and password check
def login_client():
    user_data = read_csv()
    username = input("Insert username: ")
    password = input("Insert password: ")

    for user in user_data:
        if user['username'] == username and user['password'] == password:
            print(f"Login successful! Welcome back, {username}!")
            return True
    print("Invalid username or password. Please try again.")
    return False