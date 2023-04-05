import critical
import ancillary

def main():
    # Otwórz plik PNG w trybie binarnym
    with open('added_chunks.png', 'rb') as file_png:
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

            match block_type:
                case b'IHDR':
                    critical.read_IHDR(file_png)
                case b'PLTE':
                    critical.read_PLTE(file_png, length)
                case b'IDAT':
                    critical.read_IDAT(file_png, length)
                case b'IEND':
                    critical.read_IEND(file_png)
                    break
                case _:
                    print("dupa")
                    print("Block type: {}".format(block_type))
                    ancillary.anon(file_png, length) #anonymise the chunk
                    break
                    # data = int.from_bytes(file_png.read(length), byteorder='big')

            # Odczytaj sumę kontrolną bloku
            crc = file_png.read(4)
            #print(f"Suma kontrolna: {crc.hex()}")


            # Jeśli to jest blok danych IDAT, to przerwij dekodowanie
            # if block_type == b'IDAT':
            #     critical.read_IDAT(file_png, length)
            # Jeśli to jest blok danych IHDR, to odczytaj dane
            # elif block_type == b"IHDR":
            #     critical.read_IHDR(file_png)
            # Jeśli to jest blok PLTE, to odczytaj kolory palety
            # elif block_type == b'PLTE':
            #     critical.read_PLTE(file_png, length)
            # else: # przypadek, w ktorym typ bloku jest inny niż wyżejwymienione
                # data = int.from_bytes(file_png.read(length), byteorder='big')
                #print(f"Zawartość bloku: {data}")




            
            



    


if __name__ == "__main__":
    main()
