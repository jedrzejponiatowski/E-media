import cv2 as cv
from matplotlib import pyplot as plt
import matplotlib.image as mpimg 
import numpy as np
import math, cmath

def display_image(input_filename):
    img_gray = cv.imread(input_filename, cv.IMREAD_GRAYSCALE)
    img = mpimg.imread(input_filename)

    dft1 = cv.dft(np.float32(img_gray), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift1 = np.fft.fftshift(dft1)
    magnitude_spectrum1 = 20 * np.log(cv.magnitude(dft_shift1[:, :, 0] + 1e-10, dft_shift1[:, :, 1] + 1e-10))
    phase_spectrum1 = cv.phase(dft_shift1[:, :, 0], dft_shift1[:, :, 1])
    
    plt.subplot(221), plt.imshow(img)
    plt.title('Original image'), plt.xticks([]), plt.yticks([])

    plt.subplot(222), plt.imshow(img_gray, cmap="gray")
    plt.title('Grayscale image'), plt.xticks([]), plt.yticks([])

    plt.subplot(223), plt.imshow(magnitude_spectrum1, cmap='gray')
    plt.title('Magnitude spectrum (log scale)'), plt.xticks([]), plt.yticks([])

    plt.subplot(224), plt.imshow(phase_spectrum1, cmap="gray")
    plt.title('Phase spectrum'), plt.xticks([]), plt.yticks([])

    plt.show()
    cv.waitKey(0)

def test_fourier(input_filename):
    # display grayscale image, its rotation, and spectrum of both of these.
    img_gray = cv.imread(input_filename, cv.IMREAD_GRAYSCALE)
    rotated_img_gray = cv.rotate(img_gray, cv.ROTATE_90_CLOCKWISE)

    plt.figure("DFT test 1: Image, its rotation, and their spectrums")

    plt.subplot(221), plt.imshow(img_gray, cmap="gray"), plt.xticks([]), plt.yticks([])
    plt.subplot(222), plt.imshow(rotated_img_gray, cmap="gray"), plt.xticks([]), plt.yticks([])

    dft1 = cv.dft(np.float32(img_gray), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift1 = np.fft.fftshift(dft1)
    magnitude_spectrum1 = 20 * np.log(cv.magnitude(dft_shift1[:, :, 0] + 1e-10, dft_shift1[:, :, 1] + 1e-10))

    dft2 = cv.dft(np.float32(rotated_img_gray), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_shift2 = np.fft.fftshift(dft2)
    magnitude_spectrum2 = 20 * np.log(cv.magnitude(dft_shift2[:, :, 0] + 1e-10, dft_shift2[:, :, 1] + 1e-10))

    plt.subplot(223), plt.imshow(magnitude_spectrum1, cmap="gray"), plt.xticks([]), plt.yticks([])
    plt.subplot(224), plt.imshow(magnitude_spectrum2, cmap="gray"), plt.xticks([]), plt.yticks([])

    # display transforms of steps
    gray_vert = cv.imread("zdj\step_vert_paint.png", cv.IMREAD_GRAYSCALE)
    gray_hori = cv.rotate(gray_vert, cv.ROTATE_90_CLOCKWISE)

    plt.figure("DFT test 2: Spectrums of steps")

    plt.subplot(221), plt.imshow(gray_hori, cmap="gray"), plt.xticks([]), plt.yticks([])
    plt.subplot(222), plt.imshow(gray_vert, cmap="gray"), plt.xticks([]), plt.yticks([])

    dft_hori = cv.dft(np.float32(gray_hori), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_hori_shift = np.fft.fftshift(dft_hori)
    magnitude_spectrum_hori = 20 * np.log(cv.magnitude(dft_hori_shift[:, :, 0] + 1e-10, dft_hori_shift[:, :, 1] + 1e-10))

    dft_vert = cv.dft(np.float32(gray_vert), flags=cv.DFT_COMPLEX_OUTPUT)
    dft_vert_shift = np.fft.fftshift(dft_vert)
    magnitude_spectrum_vert = 20 * np.log(cv.magnitude(dft_vert_shift[:, :, 0] + 1e-10, dft_vert_shift[:, :, 1] + 1e-10))

    plt.subplot(223), plt.imshow(magnitude_spectrum_hori, cmap="gray"), plt.xticks([]), plt.yticks([])
    plt.subplot(224), plt.imshow(magnitude_spectrum_vert, cmap="gray"), plt.xticks([]), plt.yticks([])

    plt.show()
    cv.waitKey(0)


def display_histogram(palette: list[int], histogram: list[int]):
    # convert palette to grayscale
    Y = []
    for rgb in palette:
        Y.append(math.floor(0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]))
    plt.bar(Y, height=histogram)
    plt.title("Image histogram")
    plt.show()