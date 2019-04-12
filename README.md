# Python RSA Implementation
A Python implementation of the RSA cryptosystem. Created for my own learning purposes, but useable if you want to!  
Capable of generating extremely simple and breakable (but correct) public and private keys. You can use these keys to encrypt/decrypt any file. Command-line usage is described below.  

## Usage
### Generate keys  
The files 'public_key' and 'private_key' will be created in the current directory. These must remain in the directory you are running the script in.  
```
python rsa.py -g  
```
### Encrypt a file  
Creates the file 'encrypted.\<filetype\>' in the current directory.  
```
python rsa.py -e <filename>  
```
### Decrypt a file  
Creates the file 'decrypted.\<filetype\>' in the current directory.  
```
python rsa.py -d <filename>  
```

### Limitations  
- For speed, and because I don't actually care about security, primes are between 2 and 100. Edit the source code and change this if you want!  
- You will need to send your public_key file to a friend and they will have to place it in their directory for them to encrypt a message for you.  
- Stores encrypted files using base64 encoding of the encrypted bytes. Encrypted files are 10x the size of the plaintext files. Definitely noticeable when encrypting images.  

Created by Colin Bernard for fun (2019).  
