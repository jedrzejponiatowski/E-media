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

def read_PLTE(file_png, length):
    print("PLTE block length: " + str(length) )
    plte_data = []
    for i in range(length // 3):
        r, g, b = struct.unpack('!BBB', file_png.read(3))
        plte_data.append((r, g, b))
    print("entries: " + str(i+1))

def read_IEND(file_png):
    print("IEND")



# Otwórz plik PNG w trybie binarnym
with open('type_3.png', 'rb') as file_png:
    # Wczytaj pierwsze 8 bajtów nagłówka
    header = file_png.read(8)

    # Sprawdź czy plik ma poprawny nagłówek PNG
    if header[:8] != b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a':
        raise ValueError('To nie jest plik PNG')

    # Dekoduj kolejne bloki nagłówka
    while True:
        # Wczytaj długość bloku
        length = int.from_bytes(file_png.read(4), byteorder='big')

        # Wczytaj typ bloku
        block_type = file_png.read(4)

        # Jeśli to jest blok danych IDAT, to przerwij dekodowanie
        if block_type == b'IDAT':
            data = int.from_bytes(file_png.read(length), byteorder='big')
            #print("IDAT - continue")
            #continue

        # Jeśli to jest blok danych IHDR, to odczytaj dane
        elif block_type == b"IHDR":
            read_IHDR(file_png)
            
        # Jeśli to jest blok PLTE, to odczytaj kolory palety
        elif block_type == b'PLTE':
            read_PLTE(file_png, length)


        else:
            data = int.from_bytes(file_png.read(length), byteorder='big')
            #print(f"Zawartość bloku: {data}")


        
        # Odczytaj sumę kontrolną bloku
        crc = file_png.read(4)
        #print(f"Suma kontrolna: {crc.hex()}")
