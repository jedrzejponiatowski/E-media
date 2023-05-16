import struct
import zlib
from io import BufferedReader, BufferedWriter


def anon(file_png: BufferedReader, out_file: BufferedWriter, length: int, chunk_type: str):
    print("Block type: {}".format(chunk_type))

    
    match chunk_type:
        # in order to read an anonymized tEXt chunk, the anonymization must perserve
        # its null separator byte - if we just cleared the whole chunk, the parser would not know how to read
        # it since it would be missing the null separator chunk. There are multiple chunks that require a null
        # terminator byte to work, so beware

        case 'tEXt':
            data = file_png.read(length)            
            null_byte_pos = data.index(b'\x00')
            out_file.write(null_byte_pos*"#".encode("utf-8"))
            out_file.write(b'\x00')
            out_file.write( (length-(null_byte_pos+1))*"#".encode("utf-8") )
        case _:
            file_png.read(length) # pretty much just moves the cursor to the end of chunk contetn
            out_file.write(length*'#'.encode("utf-8"))
        
    print("ANONYMIZED")


def ignore(file_png: BufferedReader, out_file: BufferedWriter, length: int, block_type: str):
    print("Block type: {}".format(block_type))
    print("IGNORING")
    buffer = file_png.read(length)
    out_file.write(buffer)


def read_tIME(file_png: BufferedReader, out_file: BufferedWriter):
    print("Block type: tIME")
    buffer = file_png.read(7)
    out_file.write(buffer)
    year, month, day, hour, minute, second = struct.unpack('!HBBBBB', buffer)
    print("Last modified: {}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second))
    

def read_gAMA(file_png: BufferedReader, out_file: BufferedWriter):
    print("Block type: gAMA")
    buffer = file_png.read(4)
    out_file.write(buffer)
    gamma = struct.unpack('!I', buffer)[0]
    print("Gamma value: {}".format(gamma/100000.0))


def read_hIST1(file_png: BufferedReader, out_file: BufferedWriter, length: int, histogram_list: list[int]):
    print("Block type: hIST")
    if length % 2 != 0:
        raise ValueError("faulty hIST chunk")

    print("hIST block length: " + str(length))

    hist_writefile = "histogram"
    with open(hist_writefile, 'w') as file:
        for i in range(length // 2):
            buffer = file_png.read(2)
            count = struct.unpack('!H', buffer)[0]
            histogram_list.append(count)
            out_file.write(buffer)
            file.write("{}\n".format(count)) # writes histogram count in human-readable format

    print("Histogram entries: " + str(i+1))
    print("written to: {}".format(hist_writefile))


def read_hIST2(file_png: BufferedReader, out_file: BufferedWriter, length: int):
    print("Block type: hIST")
    data = file_png.read(length)
    out_file.write(data)

    # num_entries = length // 2
    num_entries = len(data) // 2  # Each entry is a 2-byte unsigned integer
    entries = []
    for i in range(num_entries):
        entry = int.from_bytes(data[2*i:2*(i+1)], byteorder='big')
        entries.append(entry)

    print("Histogram entries:", entries)


def read_tEXt(file_png: BufferedReader, out_file: BufferedWriter, length: int):
    print("Block type: tEXt")
    data = file_png.read(length)
    out_file.write(data)
    
    null_byte_pos = data.index(b'\x00')
    key = data[:null_byte_pos].decode('ascii')
    value = data[null_byte_pos + 1:].decode('ascii')
    print(key + ": " + value)


def read_zTXt(file_png: BufferedReader, out_file: BufferedWriter, length: int):
    print("Block type: zTXt")
    data = file_png.read(length)
    out_file.write(data)
    
    null_byte_pos = data.index(b'\x00')
    key = data[:null_byte_pos].decode('ascii')
    compression_method = data[null_byte_pos + 1]
    compressed_data = data[null_byte_pos + 2:]

    if compression_method == 0:
        # Decompress using zlib library
        import zlib
        uncompressed_data = zlib.decompress(compressed_data)
        value = uncompressed_data.decode('latin-1')
    else:
        value = compressed_data.decode('latin-1')
    
    print(key + ": " + value)


def read_iTXt(file_png: BufferedReader, out_file: BufferedWriter, length: int):
    print("Block type: iTXt")
    data = file_png.read(length)
    out_file.write(data)

    # Parse keyword
    null_byte_pos = data.index(b'\x00')
    key = data[:null_byte_pos].decode('ascii')
    data = data[null_byte_pos + 1:]

    # Parse compression flag and method
    compression_flag = data[0]
    compression_method = data[1]
    data = data[2:]

    # Parse language tag
    null_byte_pos = data.index(b'\x00')
    language_tag = data[:null_byte_pos].decode('ascii')
    data = data[null_byte_pos + 1:]

    # Parse translated keyword
    null_byte_pos = data.index(b'\x00')
    translated_key = data[:null_byte_pos].decode('utf-8')
    data = data[null_byte_pos + 1:]

    # Parse text
    text = ""
    if compression_flag == 0:
        text = data.decode('utf-8')
    elif compression_flag == 1:
        # Decompress using zlib
        compressed_data = data
        decompressed_data = zlib.decompress(compressed_data)
        text = decompressed_data.decode('utf-8')

    print("Keyword: " + key)
    print("Compression flag: " + str(compression_flag))
    print("Compression method: " + str(compression_method))
    print("Language tag: " + language_tag)
    print("Translated keyword: " + translated_key)
    print("Text: " + text)


def read_tRNS(file_png: BufferedReader, out_file: BufferedWriter, length: int, color_type: int):
    print("Block type: tRNS")
    buffer = []
    match color_type:
        case 0: # grayscale
            buffer = file_png.read(2)
            out_file.write(buffer)
            print("Transparent value (grayscale): {}".format(int.from_bytes(buffer, byteorder="big")))
        case 2: # truecolor
            buffer = file_png.read(6)
            out_file.write(buffer)
            # each color value is contained in 2 bytes, 'H' in the format string represents short int
            # which is written in 2 bytes 
            r, g, b = struct.unpack("!HHH", buffer)
            print("Transparent value (truecolor): r{} g{} b{}".format(r, g, b))
        case 3: # index-color
            trans_map_name = "tRNSmap"
            with open("palette.txt", "r") as palette, open(trans_map_name, "w") as trns_map:
                for i in range(length):
                    alpha = file_png.read(1)
                    out_file.write(alpha)
                    plte_value = palette.readline()
                    trns_map.write("{} {}".format(int.from_bytes(alpha, byteorder="big"), plte_value))
            print("Index-color color type, transparency map printed to {}".format(trans_map_name))
            print("Data format: alpha red green blue")
        case 4, 6: # greyscale with alpha, truecolour with alpha
            print("Transparency is already included in this color type.")



#you cannot replace bytes in-file. you need to create a temp file fo that
#1. copy all bytes from the beginning up to this point into the temp file
#2. write length zeros to temp - the number of 0's is equal to the length of chunk data
#3. copy the rest of the original file into temp
#4. remove original file and rename temp (???)
#5. move file cursor as if the programm read all ancil-chunk's data
# OR
#1. read chunk data into memory
#2. read entire file into memory
#3. replace the chunk's data in the entire file with 0's
#4. save this new file
# OR
#1. save positions and lengths of ancil chunks as you read through the file
#2. once IEND is read, open the original file....

#or maybe read the entire file into memory at the beginning