# pypng required
import png
'''
https://pypng.readthedocs.io/en/latest/ca.html 
'''

'''This method is obsolette as PNGTweak and exiftool do a better job at it
but i spend like an hour figuring this out, so im reluctant to remove it'''

# NEED to pass file as a file object - filepath does not work
file = open("PNG-Gradient.png", 'rb')
original = png.Reader(file=file)
og_w, og_h, rows, info = original.read()

with open("added_chunks.png", 'wb') as fout:
    # **info makes the new image "inherit" the metadata (gamma, transparency, bitdepth) of the original image
    # it does that by passing function args as a dict. You can later "overwrite" inherited properties 
    w = png.Writer(width=og_w, height=og_h, **info, gamma=0.5, ) # adds gamma chunk
    w.write(fout, rows)


# r=png.Reader(file=urllib.request.urlopen('http://www.schaik.com/pngsuite/basn0g02.png'))
# r.read()

file.close()