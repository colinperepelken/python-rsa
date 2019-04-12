import random
import math
import sys, getopt
import base64

public_key_object = None
private_key_object = None

# Encrypt an integer m.
def encrypt(m):
    global public_key_object
    return (m ** public_key_object.e) % public_key_object.n

# Decrypt an integer c.
def decrypt(c):
    global private_key_object
    return (c ** private_key_object.d) % private_key_object.n

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
    e = random.randrange(1, totient)
    while math.gcd(e, totient) != 1:
        e = random.randrange(1, totient)
    
    # Calculate d using modulo inverse function.
    d = modinv(e, totient)
    
    # Initialize and return the keys.
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

# Encrypt bytes.
def encrypt_bytes(plain_bytes):
    encrypted_bytes = [encrypt(m) for m in plain_bytes]
    return encrypted_bytes

# Decrypt bytes.
def decrypt_bytes(cipher_bytes):
    return [decrypt(c) for c in cipher_bytes]

# Encrypt a file.
def encrypt_file(filename):
    global public_key_object
    
    if public_key_object is None:
        print("Error: Missing public key file.")
        return
    
    try:
        with open(filename, "rb") as f:
            data = f.read()
            cipher_bytes = encrypt_bytes(data)
            with open("encrypted" + filename[filename.index('.'):], "wb") as encrypted_file:
                encrypted_file.write(base64.b64encode(str(cipher_bytes).encode()))
                print("Successfully encrypted file. Created encrypted{}".format(filename[filename.index('.'):]))
    except FileNotFoundError:
        print("The file you are trying to encrypt does not exist.")

def decrypt_file(filename):
    global private_key_object
    
    if private_key_object is None:
        print("Error: Missing private key file.")
        return
    
    try:
        with open(filename, "r") as f:
            data = f.read()
            cipher_bytes = base64.b64decode(data).decode()[1:-1].split(',')
            cipher_bytes = [int(c) for c in cipher_bytes]
            plain_bytes = decrypt_bytes(cipher_bytes)
            with open("decrypted" + filename[filename.index('.'):], "wb") as decrypted_file:
                decrypted_file.write(bytearray(plain_bytes))
                print("Successfully decrypted file. Created decrypted{}".format(filename[filename.index('.'):]))
    except FileNotFoundError:
        print("The file you are trying to decrypt does not exist.")

# Generates keys and creates two files in this directory.
def generate_key_files():
    global public_key_object, private_key_object
    print("Generating keys...")
    private_key_object, public_key_object = generate_keys()
    
    with open("public_key", "wb") as f:
        f.write(base64.b64encode("{},{}".format(public_key_object.n, public_key_object.e).encode()))
        print("Created 'public_key' file in this directory.")
        
    with open("private_key", "wb") as f:
        f.write(base64.b64encode("{},{}".format(private_key_object.n, private_key_object.d).encode()))
        print("Created 'private_key' file in this directory.")

# Load existing public key and private key files.
# Returns public/private key objects.
def load_keys():
    global public_key_object, private_key_object
    
    try:
        with open("public_key", "rb") as f:
            data = f.read()
            key = base64.b64decode(data).decode().split(',')
            public_key_object = public_key(int(key[0]), int(key[1]))
    except FileNotFoundError:
        print("Notice: No public key found.")
    try:
        with open("private_key", "rb") as f:
            data = f.read()
            key = base64.b64decode(data).decode().split(',')
            private_key_object = private_key(int(key[0]), int(key[1]))
    except FileNotFoundError:
        print("Notice: No private key found.")
    
    return public_key_object, private_key_object

# Check command line arguments for instructions.
def main(argv):
    global public_key_object, private_key_object
    try:
        opts, args = getopt.getopt(argv, "ge:d:", ["=ifile"])
    except getopt.GetoptError:
        print('Usage: rsa.py -g | -e <inputfile> | -d <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-e':
            public_key_object, private_key_object = load_keys()
            encrypt_file(arg)
        elif opt == '-d':
            public_key_object, private_key_object = load_keys()
            decrypt_file(arg)
        elif opt == '-g':
            generate_key_files()
    if len(opts) == 0:
        print('Usage: rsa.py -g | -e <inputfile> | -d <inputfile>')

if __name__ == "__main__":
    main(sys.argv[1:])