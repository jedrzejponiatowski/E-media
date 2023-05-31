import random
import math

# Funkcja do generowania liczby pierwszej o podanej liczbie bitów
def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num

# Funkcja do sprawdzania, czy liczba jest pierwsza
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# Funkcja do obliczania odwrotności modularnej liczby a modulo m
def mod_inverse(e, phi):
    """
    Wyznacza liczbę d spełniającą równanie d * e ≡ 1 (mod φ(n))
    """
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        # Obliczanie ilorazu i reszty dzielenia φ(n) przez e
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        # Obliczanie wartości x i y dla rozszerzonego algorytmu Euklidesa
        x = x2 - temp1 * x1
        y = d - temp1 * y1

        # Aktualizacja wartości zmiennych pomocniczych
        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi


# Funkcja do generowania kluczy
def generate_keys(key_size):
    p = generate_prime(key_size // 2)
    q = generate_prime(key_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Często używana wartość dla e
    d = mod_inverse(e, phi)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key