from utilities import search_index,printDict,isallnumber,validate_input
from typing import Dict, List, Tuple, Union, Optional

DictOfArr = Dict[str, List[Union[str, int]]]
DictOfDict = Dict[str, Dict[str, Union[str, int]]]

def login_client(id, username:str,
               sudah_login: bool, 
               client_data: DictOfArr) -> Tuple[bool,str,bool,int]:
    username = username if username!="" else ""
    if sudah_login:
        print("Failed to login")
        print(f"You have logged in with the username {username}, please log out before logging in.") 
    else:
        username = input("Insert username: ")
        password = input("Insert password: ")
        print()
        if username in client_data['username']:
            index = search_index(client_data, "username", username)
            if client_data["password"][index]==password:
                print(f"Welcome to the chatroom, Client {username}!")
                print()
                sudah_login = True
                index = search_index(client_data, "username", username) #Search username index
                id = client_data["id"][index]
                
            else:
                print("Wrong password!")
                print()
        else:
            print("Username not registered.")
            print()
    return (id, username, sudah_login)

def logout_client(sudah_login:bool) -> bool:
    if sudah_login:
        sudah_login = False
        print("You have logged out.")
        return sudah_login
    else:
        print("Failed to logout")
        print("You have not yet logged in, please login before logging out.")