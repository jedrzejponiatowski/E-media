import struct

def read_IHDR(file_png, out_file):
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

    #print(20*"-")

def read_PLTE(file_png, out_file, length: int, palette_list: list[int]):
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
    

def read_IDAT(file_png, out_file, length):
    print("Block type: IDAT")
    # data = int.from_bytes(file_png.read(length), byteorder='big')
    buffer = file_png.read(length)
    out_file.write(buffer)
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
def read_anon_IDAT(file_png, out_file, length):
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


def read_IEND(file_png, out_file):
    print("Block type: IEND")