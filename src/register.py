from utilities import validate_input

def register_client(id, username, sudah_login, client_data):
    id = id if id != 0 else 0
    username = username if username!="" else ""

    if sudah_login:
        print("Failed to register")
        print("You have logged in with the username {username}, please log out before logging in.")
        print()
        return id, username, sudah_login, client_data
    else:
        username = input("Insert username: ")
        password = input("Insert password: ")
        # Check username validity
        if not validate_input(username):
            print("Username can only contain letters, numbers, underscore, and dash.")
            return id, username, sudah_login, client_data
        # Check unique username
        elif username in client_data['username']:
            print(f"Username {username} is not available.")
            return id, username, sudah_login, client_data
        else:
            # Client registration
            client_data["id"].append(str(len(client_data["id"])+1)) 
            client_data["username"].append(username)
            client_data["password"].append(password)

            # Print welcome
            print(f"Welcome to the chatroom {username}!")
            sudah_login = True
            id = len(client_data["id"])

            return id, username, sudah_login, client_data