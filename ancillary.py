import struct

def anon(file_png, out_file, length, chunk_type):
    print("Block type: {}".format(chunk_type))
    print("Starting anonymization")
    file_png.read(length) # pretty much just moves the cursor to the end of chunk contetn
    out_file.write(length*'0'.encode("utf-8"))


def read_tIME(file_png, out_file):
    print("Block type: tIME")
    buffer = file_png.read(7)
    out_file.write(buffer)
    year, month, day, hour, minute, second = struct.unpack('!HBBBBB', buffer)
    print("Last modified: {}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second))


def read_gAMA(file_png, out_file):
    print("Block type: gAMA")
    buffer = file_png.read(4)
    out_file.write(buffer)
    gamma = struct.unpack('!I', buffer)[0]
    print("Gamma value: {}".format(gamma/100000.0))


def read_hIST(file_png, out_file, length):
    print("Block type: hIST")
    if length % 2 != 0:
        raise ValueError("faulty hIST chunk")

    print("hIST block length: " + str(length))

    hist_writefile = "histogram"
    with open(hist_writefile, 'w') as file:
        for i in range(length // 2):
            buffer = file_png.read(2)
            out_file.write(buffer)
            count = struct.unpack('!H', buffer)[0]
            file.write("{}\n".format(count)) # writes histogram count in human-readable format

    print("entries: " + str(i+1))
    print("written to: {}".format(hist_writefile))




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