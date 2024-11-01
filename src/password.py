from RNG import RNG

def set_password ():
    global room_password
    room_password = RNG(100, 999)

password = None