import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

def display_image(input_filename):
    img_gray = cv.imread(input_filename, cv.IMREAD_GRAYSCALE)
    img = cv.imread(input_filename, cv.IMREAD_UNCHANGED)
    rotated_img = cv.rotate(img_gray, cv.ROTATE_90_CLOCKWISE)
    rotated_img_color = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)

    cv.imshow("Original Image", cv.resize(img, (400, 300)))
    cv.imshow("Original Image (Gray)", cv.resize(img_gray, (400, 300)))
    cv.imshow("Rotated Image (Gray)", cv.resize(rotated_img, (400, 300)))

    dft1 = cv.dft(np.float32(img_gray), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift1 = np.fft.fftshift(dft1)
    magnitude_spectrum1 = 20 * np.log(cv.magnitude(dft_shift1[:, :, 0] + 1e-10, dft_shift1[:, :, 1] + 1e-10))

    plt.subplot(121), plt.imshow(magnitude_spectrum1, cmap='gray')
    plt.title('Magnitude Spectrum 1'), plt.xticks([]), plt.yticks([])


    dft2 = cv.dft(np.float32(rotated_img), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift2 = np.fft.fftshift(dft2)
    magnitude_spectrum2 = 20 * np.log(cv.magnitude(dft_shift2[:, :, 0] + 1e-10, dft_shift2[:, :, 1] + 1e-10))

    plt.subplot(122), plt.imshow(magnitude_spectrum2, cmap='gray')
    plt.title('Magnitude Spectrum 2'), plt.xticks([]), plt.yticks([])

    plt.show()
    
    cv.waitKey(0)