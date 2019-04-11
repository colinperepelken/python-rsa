import random
import math

# Encrypt an integer m.
def encrypt(m):
    return (m ** public_key.e) % public_key.n

# Decrypt an integer c.
def decrypt(c):
    return (c ** private_key.d) % private_key.n

# Public key class.
class public_key:
    def __init__(self, n, e):
        self.n = n
        self.e = e              

# Private key class.
class private_key:
    def __init__(self, n, d):
        self.n = n
        self.d = d

# Generates public and private keys.
def generate_keys():
    
    # Generate list of primes.
    primes = [i for i in range(2, 100) if is_prime(i)]
    
    # Choose two distinct prime numbers p and q.
    p = random.choice(primes)
    primes.remove(p)
    q = random.choice(primes)
    
    # Compute n.
    # n is used as the modulus for both the public and private keys.
    # Its length is the key length.
    n = p * q
    
    # Compute Carmichael totient function value of n.
    totient = lcm(p - 1, q - 1)
    
    # Choose an integer e s.t. 1 < e < totient and gcd(e, totient) = 1.
    # i.e. e and totient are coprime.
    e = 2
    while math.gcd(e, totient) != 1 and e < totient:
        e += 1
    
    # Calculate d using modulo inverse function.
    d = modinv(e, totient)
    
    return private_key(n, d), public_key(n, e)
    

# gcm function is defined in math.
# Create a lcm function using this gcm function.
def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

# Modulo inverse function.
# Returns d ≡ e^-1 (mod m)
def modinv(a, m):
    for d in range(1, m):
        if (d * a) % m == 1:
            break
    else:
        raise ValueError('{} has no inverse mod {}'.format(a, m))
    return d

# Returns True if n is prime.
def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))

# Encrypt an entire message.
def encrypt_message(plaintext_message):
    encoded_message = list(plaintext_message.encode('utf8'))
    cipher_message = [encrypt(m) for m in encoded_message]
    return cipher_message

# Decrypt an entire message.
def decrypt_message(ciphertext_message):
    plaintext_message = ''.join(chr(decrypt(c)) for c in ciphertext_message)
    return plaintext_message

print("Generating keys...")
private_key, public_key = generate_keys()

message = "Hello, World!!"
ciphertext = encrypt_message(message)
plaintext = decrypt_message(ciphertext)
print(plaintext)
    


    