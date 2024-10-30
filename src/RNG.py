import time

#password generator

def get_seed():
    """Menghasilkan seed berdasarkan waktu saat ini."""
    return int(time.time())

# Fungsi untuk Linear Congruential Method
def linear_congruential_method_int(seed, a, c, m, n, min_val, max_val):
    """
    Menghasilkan urutan bilangan bulat acak semu dalam rentang tertentu
    menggunakan Metode Kongruensial Linier (LCM).
    
    Parameter
        seed (int): Nilai benih awal.
        a (int): Pengali.
        c (int): Kenaikan.
        m (int): Modulus.
        n (int): Jumlah angka acak yang akan dihasilkan.
        min_val (int): Nilai minimum dari rentang.
        max_val (int): Nilai maksimum dari rentang.
        
    Pengembalian:
        daftar Daftar bilangan bulat acak semu dalam rentang yang ditentukan.
    """

    random_numbers = []
    x = seed
    
    for _ in range(n):
        x = (a * x + c) % m
        random_numbers.append(min_val + (x % (max_val - min_val + 1)))
    
    return random_numbers

# Fungsi untuk menghasilkan nilai integer random
def RNG(min_val, max_val): 
    # Mendapatkan seed secara acak
    seed = get_seed()   

    a = 1103515245
    c = 12345
    m = 2**31
    n = 10
    random_sequence = linear_congruential_method_int(seed, a, c, m, n, min_val, max_val)

    # Mengambil satu nilai acak dari array yang dihasilkan
    # Menggunakan algoritma LCM untuk memilih indeks acak dari array
    random_index = linear_congruential_method_int(seed, a, c, m, 1, 0, n-1)[0]
    random_value = random_sequence[random_index]
    return random_value