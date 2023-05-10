import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

def display_image(input_filename):
    img_gray = cv.imread(input_filename, cv.IMREAD_GRAYSCALE)
    img = cv.imread(input_filename, cv.IMREAD_UNCHANGED)

    dft = cv.dft(np.float32(img_gray),flags = cv.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 20*np.log(cv.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

    cv.imshow("image", img)

    plt.subplot(111),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.show()
    
    cv.waitKey(0)