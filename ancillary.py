

# def anonymize(file_png, length):
#     entire_file = file_png.read();
#     # cut_file = entire_file[file_png.tell() : file_png.tell()+length]
#     cut_file = entire_file[0 : file_png.tell()] + entire_file[file_png.tell()+length]
#     with open("out.png", 'wb') as fout:
#         fout.write(entire_file)

# Literally just cuts out the chunk content. REMEMBER to truncate() the file later.

# THIS IS AN INCORRECT APPROACH: setting chunk contents will be easier
def anon(file_png, length):
    current_pos = file_png.tell()

    # read up to the possition of the chunk
    slice1 = file_png.read(file_png.tell())

    # read data from the end of the chunk until EOF
    file_png.seek(length, 2)
    slice2 = file_png.read()

    #combine
    anonymous = slice1 + slice2

    with open("out.png", 'wb') as fout:
        fout.write(anonymous)
