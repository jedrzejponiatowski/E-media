import critical
import ancillary
import display
#import transform
import getopt, sys
from os.path import exists


def main():
    # shortopts: a - anonymize, i - input file, o - output file, s - show image and spectrum
    # h - display histogram (if exists), f - test fourier
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ai:o:shf")
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit()

    input_filename = ''
    output_filename = ''
    anonymize = False
    show = False
    show_hist = False
    fourier = False
    for option, argument in opts:
        if option == "-a":
            anonymize = True

        elif option == "-i":
            if argument == '':
                print("Input file not specified")
                sys.exit()
            input_filename = argument

        elif option == "-o":
            if argument == '':
                print("Output file not specified")
                sys.exit()
            output_filename = argument

        elif option == "-s":
            show = True
        elif option == "-h":
            show_hist = True
        elif option == "-f":
            fourier = True
        else:
            print("Unrecognised option: {}".format(option))
            sys.exit()


    # Chunks to anonimize
    anon_chunks = [b'dSIG', b'eXIf', b'iTXt', b'tEXt', b'tIME', b'zTXt']
    chunks_read = [] # written as binary strings (eg. b'dSIG')
    palette = [] # format: [(1, 2, 3), (4, 5, 6)]
    histogram = []
    width = 0
    height = 0
    color_type = 0

    # Open png in byte read mode (also the output file)
    try:
        with open(input_filename, 'rb') as file_png, open(output_filename, 'wb') as out_file:
        
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

                # a previously anonymized block will not be read because it was first read in the if clause
                # and the elif clause will then not be checked, since this is how if-elif works
                if block_type in anon_chunks and anonymize:
                    ancillary.anon(file_png, out_file, length, block_type.decode("utf-8"))

                elif (not anonymize) or (anonymize and block_type not in anon_chunks):
                    match block_type:
                        case b'IHDR':
                            width, height, color_type = critical.read_IHDR(file_png, out_file)
                        case b'PLTE':
                            critical.read_PLTE(file_png, out_file, length, palette)
                        case b'IDAT':
                            # instead of this if-else, add IDAT to the list of anonymisable chunks
                            # and update the anon functione
                            # if anonymize:
                            #     critical.read_anon_IDAT(file_png, out_file, length)
                            # else:
                            critical.read_IDAT(file_png, out_file, length)
                        case b'IEND':
                            critical.read_IEND(file_png, out_file)
                            iend_read = True
                        case b'tIME':
                            ancillary.read_tIME(file_png, out_file)
                        case b'gAMA':
                            ancillary.read_gAMA(file_png, out_file)
                        case b'hIST':
                            if b'PLTE' not in chunks_read:
                                print("Error: hIST chunk cannot exist without a PLTE chunk")
                                sys.exit()
                            elif length / 2 != len(palette):
                                print("Invalid number of hIST chunk entries")
                                sys.exit()
                            ancillary.read_hIST1(file_png, out_file, length, histogram)
                        case b'tEXt':
                            ancillary.read_tEXt(file_png, out_file, length)
                        case b'zTXt':
                            ancillary.read_zTXt(file_png, out_file, length)
                        case b'iTXt':
                            ancillary.read_iTXt(file_png, out_file, length)
                        case b'tRNS':
                            if b'PLTE' not in chunks_read:
                                print("Error: hIST chunk cannot exist without a PLTE chunk")
                                sys.exit()
                            ancillary.read_tRNS(file_png, out_file, length, color_type)
                        case _:
                            ancillary.ignore(file_png, out_file, length, block_type.decode("utf-8"))

                # add the recently read chunk to the list
                chunks_read.append(block_type)
                # Odczytaj sumę kontrolną bloku
                crc = file_png.read(4)
                out_file.write(crc)
                print("Control sum: {}".format(crc.hex()))
                print(20*"-")

    except FileNotFoundError as err:
        print("File does not exist: {}".format(err.filename))
    
    if show:
        display.display_image(input_filename)
    if show_hist and (b'hIST' in chunks_read):
        display.display_histogram(palette, histogram)
    if fourier:
        display.test_fourier(input_filename)

def usage():
    print(10*"-" + "USAGE" + 10*"-")
    print("python main.py -i input_file -o output_file [-s -a]")
    print(10*"-" + "USAGE" + 10*"-")
if __name__ == "__main__":
    main()