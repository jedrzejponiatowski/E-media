import critical
import ancillary

def main():

    # Chunks to anonimize
    anon_chunks = [b'dSIG', b'eXIf', b'iTXt', b'tEXt', b'tIME', b'zTXt']
    # Otwórz plik PNG w trybie binarnym
    with open('moded.png', 'rb') as file_png, open('out.png', 'wb') as out_file:
        
        # Wczytaj pierwsze 8 bajtów nagłówka
        header = file_png.read(8)
        # Sprawdź czy plik ma poprawny nagłówek PNG
        if header[:8] != b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a':
            raise ValueError('To nie jest plik PNG')
        out_file.write(header)

        # Dekoduj kolejne bloki nagłówka
        iend_read = False
        while not iend_read:
            # Wczytaj długość bloku
            length_bytes = file_png.read(4)
            length = int.from_bytes(length_bytes, byteorder='big') # decode length from bytes
            out_file.write(length_bytes)
            # Wczytaj typ bloku
            block_type = file_png.read(4)
            out_file.write(block_type)

            match block_type:
                case b'IHDR':
                    critical.read_IHDR(file_png, out_file)
                case b'PLTE':
                    critical.read_PLTE(file_png, out_file, length)
                case b'IDAT':
                    critical.read_IDAT(file_png, out_file, length)
                case b'IEND':
                    critical.read_IEND(file_png, out_file)
                    iend_read = True
                case _:
                    print(block_type.decode("utf-8"))
                    if block_type in anon_chunks:
                        ancillary.anon(file_png, out_file, length, block_type.decode("utf-8"))
                    else: continue

            # Odczytaj sumę kontrolną bloku
            crc = file_png.read(4)
            out_file.write(crc)
            print("Suma kontrolna {}".format(crc.hex()))
            print(20*"-")



if __name__ == "__main__":
    main()
