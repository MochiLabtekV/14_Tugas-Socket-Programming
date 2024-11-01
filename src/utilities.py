def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

def isallnumber(string):
    angka = ['0','1','2','3','4','5','6','7','8','9']
    for i in string:
        if i not in angka:
            return False
    return True

def validate_input(user_input):
    # Check if input is not all digits
    if isallnumber(user_input):
        return False

    # Check for allowed characters (alphanumeric, _, -)
    allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    
    for char in user_input:
        if char not in allowed_characters:
            return False

    return True