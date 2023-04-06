

def anon(file_png, out_file, length, chunk_type):
    print("Block type: {}".format(chunk_type))
    print("Starting anonymization")
    file_png.read(length) # pretty much just moves the cursor to the end of chunk contetn
    out_file.write(length*'0'.encode("utf-8"))

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