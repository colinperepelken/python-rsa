import random
import math

def encrypt(m):
    return (m ** public_key.e) % public_key.n
    
def decrypt(c):
    return (c ** private_key.d) % private_key.n

class public_key:
    def __init__(self, n, e):
        self.n = n
        self.e = e              
        
class private_key:
    def __init__(self, n, d):
        self.n = n
        self.d = d

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

def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


print("Generating keys...")
private_key, public_key = generate_keys()

message = 50
ciphertext = encrypt(message)
print("Encrypted plaintext {} as ciphertext {}.".format(message, ciphertext))
plaintext = decrypt(ciphertext)
print("Decrypted ciphertext as {}".format(plaintext))

    