import struct
import zlib
from io import BufferedWriter, BufferedReader
from crypto import *
from cryptoCBC import *
import base64
from keys import *


def read_IHDR(file_png: BufferedReader, out_file: BufferedWriter):
    buffer = []
    width = 0
    height = 0
    color_type = 0

    print("Block type: IHDR")

    buffer = file_png.read(4)
    out_file.write(buffer)
    width = int.from_bytes(buffer, byteorder='big')
    print("Width: " + str(width))

    buffer = file_png.read(4)
    out_file.write(buffer)
    height = int.from_bytes(buffer, byteorder='big')
    print("Height: " + str(height))

    buffer = file_png.read(1)
    out_file.write(buffer)
    print("Bit depth: " + str(int.from_bytes(buffer, byteorder='big')))

    buffer = file_png.read(1)
    out_file.write(buffer)
    color_type = int.from_bytes(buffer, byteorder='big')
    print("Color type: " + str(color_type))

    buffer = file_png.read(1)
    out_file.write(buffer)
    print("Compression method: " + str(int.from_bytes(buffer, byteorder='big')))

    buffer = file_png.read(1)
    out_file.write(buffer)
    print("Filter method: " + str(int.from_bytes(buffer, byteorder='big')))

    buffer = file_png.read(1)
    out_file.write(buffer)
    print("Interlace method: " + str(int.from_bytes(buffer, byteorder='big')))

    return width, height, color_type

def read_PLTE(file_png: BufferedReader, out_file: BufferedWriter, length: int, palette_list: list[int]):
    print("Block type: PLTE")
    if length % 3 != 0:
        raise ValueError("faulty PLTE chunk")

    print("PLTE block length: " + str(length) )

    plte_writefile = "palette"
    with open(plte_writefile, 'w') as file:
        for i in range(length // 3):
            buffer = file_png.read(3)
            r, g, b = struct.unpack('!BBB', buffer)
            palette_list.append( (r, g, b) )
            file.write("{} {} {}\n".format(r, g, b)) # writes palette in human-readable format
            out_file.write(buffer)

    print("entries: " + str(i+1))
    print("written to: {}".format(plte_writefile))
    

def read_IDAT(file_png: BufferedReader, out_file: BufferedWriter, length: int, de_comp: bool):
    print("Block type: IDAT")
    
    # bytes object is immutable.
    first_byte = file_png.read(1)
    the_rest = file_png.read(length-1)
    data = first_byte + the_rest # i know how this looks, but bytes objects are immutable, so i gotta make do for now
    if de_comp:
        # new_content = bytes()
        if first_byte == b'\x78': # the file is zlib-compressed
            print("Decompressing...")
            data = zlib.decompress(data) # only keep this in the if-elif

        else: # the file is not zlib-compressed
            print("Compressing...")
            data = zlib.compress(data) # default compression level = 6
            
        out_file.write(len(data).to_bytes(4, byteorder="big"))
    else:
        out_file.write(length.to_bytes(4, byteorder="big"))
        
    out_file.write(b'IDAT')
    out_file.write(data)
    print("IDAT - continue")

def read_IDAT_encrypt(file_png: BufferedReader, out_file: BufferedWriter, length: int, public_key: tuple, mode: str):
    print("Block type: IDAT (encrypt)")
    buffer = file_png.read(length) # read byte-mass into buffer
    image64 = ''
    encrypted = ''
    # takes in binary, converts to utf8 bytes, and then decodes to utf8 chars.
    image64 = base64.b64encode(buffer).decode() 
    match mode:
        case 'ecb':
            encrypted = encryptLargeFileECB(image64, public_key) # later, utf8_chars -> utf8_values
        case 'cbc':
            encrypted = encryptLargeFileCBC(image64, public_key)
        case _:
            raise ValueError("This encoding mode does not exist: {mode}")  
        
    # print(length)
    # print(len(buffer))
    # print(len(encrypted))
    # print(type(buffer))
    # print(type(encrypted))

    encrypted_bytes = encrypted.encode()
    # print(type(encrypted_bytes))
    # print(len(encrypted_bytes))
    encrypt_len = len(encrypted_bytes)
    
    out_file.write(encrypt_len.to_bytes(4, byteorder='big'))
    out_file.write(b'IDAT')
    out_file.write(encrypted_bytes)
    print("IDAT - continue")


def read_IDAT_decrypt(file_png: BufferedReader, out_file: BufferedWriter, length: int, private_key: tuple, mode: str):
    print("Block type: IDAT (decrypt)")

    buffer = file_png.read(length)
    print("new size:: " + str(length))
    decryptedVal = ''

    match mode:
        case 'ecb':
            decryptedVal = decryptLargeFileECB(buffer, private_key)
        case 'cbc':
            decryptedVal = decryptLargeFileCBC(buffer, private_key)
            
    decryptedBytes = base64.b64decode(decryptedVal)

    decrypt_len = len(decryptedBytes)
    out_file.write(decrypt_len.to_bytes(4, byteorder='big'))
    out_file.write(b'IDAT')
    out_file.write(decryptedBytes)

    print("IDAT - continue")




# when anonymization is True, glue together consecutive IDAT chunks
# problem - gluing IDAT chunks increases chunk size.
# To properly glue together multiple IDATs we need to update teh chunk length as we go.
# In the current implementation the length of the first IDAT chunk
# is read and written to the outfile before this function executes. In other words, the only way
# to edit the chunk length, which is constantly increasing if we are adding IDATs together
# is to substitute the previously written value with the true one. 
# Do this: scan the infile to add up all IDAT lengths, seek() to the position before the scan, plop
# down the total IDAT length, read IDAT data.
# CURRENTLY DOES NOT WORK - messed up tracking read bytes
# It does not work because you need to play with compresion/decompression first. Thats kinda how IDAT works
def read_anon_IDAT(file_png: BufferedReader, out_file: BufferedWriter, length: int):
    print("Block type: IDAT")
    print("anon is true - IDAT concatenation")
    total_lengh = length # sum of all IDAT lengths
    total_bytes_read = 8 # allows for backtracking. This is the sum of length_bytes and chunk_type bytes (4+4=8)

    # scan the file to find out the total length of all IDATs. this preferably has to be done
    # before we write IDAT data to the outfile
    buffer = file_png.read(length) # read the first IDAT portion into memory
    total_bytes_read += length
    while True:
        crc = file_png.read(4)
        length_next = file_png.read(4)
        chunk_type_next = file_png.read(4)
        total_bytes_read += 12 # a set number, just read 4+4+4 bytes
        if chunk_type_next == b'IDAT':
            length_next_number = int.from_bytes(length_next, byteorder="big") # because raw length is read in bytes
            total_lengh += length_next_number
            file_png.read(length_next_number) # dont save IDAT because we are just summing up lenght bytes
            total_bytes_read += length_next_number
        else:
            file_png.seek( -total_bytes_read, 1 ) # backrack the exact ammout of bytes read, starting from the current location
            break

    # since we already written the length of the chunk and its type before we even started this command
    # we first need to update the chunk length to match teh total length of all consecutive IDATs.
    # length + type will always have the total length of 8 bytes
    # just moving the cursor with seek() may NOT work since there will be data after the cursor.
    # We are just moving it, we are not removing any data in the process
    out_file.seek(-8, 1)
    out_file.write(str(total_lengh).encode("utf-8"))
    out_file.write('IDAT'.encode("utf-8"))
    out_file.write(buffer)

    # this is the actual reading of IDAT data. 
    while True:
        crc = file_png.read(4)
        length_next = file_png.read(4)
        chunk_type_next = file_png.read(4)

        if chunk_type_next != b'IDAT': # if the next chunk is not IDAT, unread all data needed for the next chunk read and the crc
            file_png.seek( -(len(chunk_type_next)+len(length_next)+len(crc)), 1 )
            return
        else:
            #discard crc, read lenght_next bytes
            buffer = file_png.read(int.from_bytes(length_next, byteorder="big"))
            out_file.write(buffer)


def read_IEND(file_png: BufferedReader, out_file: BufferedWriter):
    print("Block type: IEND")