import struct

def read_IHDR(file_png):
    print("Block Type: IHDR")
    print("Width: " + str(int.from_bytes(file_png.read(4), byteorder='big')))
    print("Height: " + str(int.from_bytes(file_png.read(4), byteorder='big')))
    print("Bit depth: " + str(int.from_bytes(file_png.read(1), byteorder='big')))
    print("Color type: " + str(int.from_bytes(file_png.read(1), byteorder='big')))
    print("Compression method: " + str(int.from_bytes(file_png.read(1), byteorder='big')))
    print("Filter method: " + str(int.from_bytes(file_png.read(1), byteorder='big')))
    print("Interlace method: " + str(int.from_bytes(file_png.read(1), byteorder='big')))
    print(20*"-")

def read_PLTE(file_png, length):
    print("Block type: PLTE")
    if length % 3 != 0:
        raise ValueError("faulty PLTE chunk")

    print("PLTE block length: " + str(length) )

    plte_writefile = "palette"
    with open("palette", 'w') as file:
        for i in range(length // 3):
            r, g, b = struct.unpack('!BBB', file_png.read(3))
            file.write("{} {} {}\n".format(r, g, b))
    print("entries: " + str(i+1))
    print("entries written to: {}".format(plte_writefile))
    print(20*'-')

    # zapisz palete do oddzelnego pliku - za duze zeby wyswietlac
    

def read_IDAT(file_png, length):
    print("Block type: IDAT")
    data = int.from_bytes(file_png.read(length), byteorder='big')
    print("IDAT - continue")
    print(20*"-")

def read_IEND(file_png):
    print("IEND")