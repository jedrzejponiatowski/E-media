import critical
import ancillary
import transform

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def main():

    # Chunks to anonimize
    anon_chunks = [b'dSIG', b'eXIf', b'iTXt', b'tEXt', b'tIME', b'zTXt']
    # Open png in byte read mode (also the output file)
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
                    if block_type in anon_chunks:
                        ancillary.anon(file_png, out_file, length, block_type.decode("utf-8"))
                    else: continue

            # Odczytaj sumę kontrolną bloku
            crc = file_png.read(4)
            out_file.write(crc)
            print("Suma kontrolna {}".format(crc.hex()))
            print(20*"-")
    
    img_gray = cv.imread('large.png', cv.IMREAD_GRAYSCALE)
    img = cv.imread("large.png", cv.IMREAD_UNCHANGED)

    dft = cv.dft(np.float32(img_gray),flags = cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 20*np.log(cv.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

    cv.imshow("image", img)

    plt.subplot(111),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.show()
    
    cv.waitKey(0)
    

if __name__ == "__main__":
    main()
