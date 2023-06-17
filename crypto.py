
import math
import sys
import string
import random

def getMaxBitsDataSize(key):
    modulus_len = len(str(bin(key[1])))
    size = math.floor(math.log2(modulus_len))
    # print("getMaxBitsDataSize size: " + str(size))
    return size
    # return len(str(key[1])) - 3

def asciiToText(msg):
    length, size = len(msg), 3
    symbols = [ msg[i:i+size] for i in range(0, length, size)]
    return ''.join(chr(int(s[0].strip('0') + s[1:])) for s in symbols).rstrip('\0')

def encrypt(msg, publicKey):
    # hex = toHex(msg)
    # for c in msg:
    #     print(str(ord(c)).zfill(3)) 
    m = int(''.join(str(ord(c)).zfill(3) for c in msg))
    # m = int(''.join(str(ord(c, 'x')) for c in msg))
    # m = 3
    print('message to ascii', m)
    value = pow(m, publicKey[0], publicKey[1])
    print('ENCRYPTED VALUE', value)
    print('BIT LENGTH OF ENCRYPTED VALUE', int.bit_length(value))
    return value

def decrypt(cipher, privateKey):
    decryptedVal = str(pow(cipher, privateKey.d, privateKey[1]))
    if (len(decryptedVal) % 3 != 0):
        decryptedVal = '0' + decryptedVal
    print('DECRYPTED VALUE', decryptedVal)
    return decryptedVal



# in encryptLargeFile gets passed the entire bytemass. Every byte is converted to ASCII values
# so 'abc' gets translated into '097098099' 
def msgToAsciiValue(msg):
    return ''.join(str(ord(c)).zfill(3) for c in msg)

# in encryptLargeFile gets passed the entire bytemass and some wierd int.
# devides the ASCII-converted message and converts them into blocks of length "size"
def splitToBlocks(asciiMsg, size):
    length = len(asciiMsg)
    blocks = [ asciiMsg[i:i+size].ljust(size, '0') for i in range(0, length, size)] # why ljust()?
    # since the size of the block can differ from 3, which is the size of one "charactre" output by msgtoAsciiValue
    # we need to pad it with non-invasive characters. Say we got 097 as the first char from msgToAscii, but size==2.
    # our first block would be "09"
    return blocks

def encryptBlock(block, publicKey): # each block consists of ASCII values.
    val = pow(block, publicKey[0], publicKey[1])
    return val

def encryptBlockMessage(blocks, publicKey):
    return ''.join(str(encryptBlock(int(block), publicKey)) + '\n' for block in blocks).rstrip('\n')


def encryptLargeFileECB(msg, publicKey): # msg here is in utf8 characters
    bits = getMaxBitsDataSize(publicKey) # ??? - gets the size of one block
    asciiMsg = msgToAsciiValue(msg) # convert the bytemass to ASCII values (not chars, but their corresponding codes)
    blocks = splitToBlocks(asciiMsg, bits) # each block is rather sort, like 2-3 chars

    encryptedMsg = encryptBlockMessage(blocks, publicKey)
    return encryptedMsg


def decryptBlock(block, privateKey):
    bits = getMaxBitsDataSize(privateKey)
    decryptedVal = str(pow(block, privateKey[0], privateKey[1]))
    return decryptedVal.zfill(bits)

def decryptBlockMessage(blocks, privateKey):
    decrypted, blocksAmount = '', len(blocks)
    print('\r0%', end='')
    for i, block in enumerate(blocks):
        decrypted = decrypted + str(decryptBlock(int(block), privateKey))
        progress = str(math.floor((i/blocksAmount)*100))
        print('\r' + progress + '%', end='')
    print('\r100%', end='')
    return decrypted
    # return ''.join(str(decryptBlock(int(block), privateKey)) for block in blocks)
"""
def decryptLargeFile(msg, privateKey):
    length = len(msg)
    blocks = msg.split('\n')
    decryptedMsg = decryptBlockMessage(blocks, privateKey)
    text =  asciiToText(decryptedMsg)
    return text
"""

def decryptLargeFileECB(msg, privateKey):
    blocks = msg.split(b'\n')  # Podział na bloki za pomocą bytes
    decryptedMsg = decryptBlockMessage(blocks, privateKey)
    text = asciiToText(decryptedMsg)
    return text


    
"""
def TMP_encrypt(message, public_key):
    e, n = public_key
    encrypted_message = ""
    for char in message:
        encrypted_char = pow(ord(char), e, n) # Szyfrowanie za pomocą potęgi modulo
        encrypted_message += chr(encrypted_char)
    return encrypted_message
"""

"""
# Funkcja do szyfrowania wiadomości
def TMP_encrypt(byte, public_key):
    e, n = public_key
    encrypted_byte = pow(byte, e, n)
    return encrypted_byte

def decrypt(encrypted_byte, private_key):
    d, n = private_key
    decrypted_byte = pow(encrypted_byte, d, n)
    return decrypted_byte




# Funkcja do deszyfrowania wiadomości
def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted_message = ""
    for char in encrypted_message:
        decrypted_char = chr(pow(ord(char), d, n))  # Deszyfrowanie za pomocą potęgi modulo
        decrypted_message += decrypted_char
    return decrypted_message
"""




"""
# Generowanie kluczy
public_key, private_key = generate_keys(20)

# Wiadomość do zaszyfrowania
message = "Hello, world!"

# Szyfrowanie wiadomości
encrypted_message = encrypt(message, public_key)
print("Zaszyfrowana wiadomość:", encrypted_message)

# Sprawdzanie ilości bajtów w message
message_bytes = message.encode()
print("Liczba bajtów w message:", len(message_bytes))

# Sprawdzanie ilości bajtów w encrypted_message
encrypted_message_bytes = encrypted_message.encode()
print("Liczba bajtów w encrypted_message:", len(encrypted_message_bytes))


# Deszyfrowanie wiadomości
decrypted_message = decrypt(encrypted_message, private_key)
print("Odszyfrowana wiadomość:", decrypted_message)
"""
