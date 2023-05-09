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

def read_PLTE(file_png, out_file, length):
    print("Block type: PLTE")
    if length % 3 != 0:
        raise ValueError("faulty PLTE chunk")

    print("PLTE block length: " + str(length) )

    plte_writefile = "palette.txt"
    with open(plte_writefile, 'w') as file:
        for i in range(length // 3):
            buffer = file_png.read(3)
            r, g, b = struct.unpack('!BBB', buffer)
            file.write("{} {} {}\n".format(r, g, b)) # writes palette in human-readable format
            out_file.write(buffer)

    print("entries: " + str(i+1))
    print("written to: {}".format(plte_writefile))
    #print(20*'-')

    # zapisz palete do oddzelnego pliku - za duze zeby wyswietlac
    

def read_IDAT(file_png, out_file, length):
    print("Block type: IDAT")
    # data = int.from_bytes(file_png.read(length), byteorder='big')
    buffer = file_png.read(length)
    out_file.write(buffer)
    print("IDAT - continue")
    # print(20*"-")

def read_IEND(file_png, out_file):
    print("Block type: IEND")