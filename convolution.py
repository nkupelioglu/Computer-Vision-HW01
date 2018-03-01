from PIL import Image
import numpy as np
import math
import timeit


def main():
    imagePath = "./try4.jpeg"
    imageObject = Image.open(imagePath)
    kernel1 = generatekernel(1)
    kernel2 = generatekernel(2)

    imgarray = PIL2np(imageObject)

    sigma05 = convolution(imgarray, kernel1)
    sigma1 = convolution(sigma05, kernel1)

    sigma2 = convolution(imgarray, kernel2)
    sigma1arr = sigma1.tolist()
    sigma2arr = sigma2.tolist()
    for i in range(50, 60):
        for j in range(50, 60):
            print str(round(sigma1arr[i][j])) + " ",
        print "\n"
    print "\n"
    for i in range(50, 60):
        for j in range(50, 60):
            print str(round(sigma2arr[i][j])) + " ",
        print "\n"

    newimage = np2PIL(sigma2)
    newimage2 = np2PIL(sigma1)
    newimage.show(title="Sigma = 1")
    newimage2.show(title="Sigma = 2")


def generatekernel(sigma=1):
    array = np.zeros((2 * sigma + 1, 2 * sigma + 1))
    for i in range(0, 2 * sigma + 1):
        for j in range(0, 2 * sigma + 1):
            array[i, j] = (1 / (2 * math.pi * math.pow(sigma, 2))) * math.pow(math.e, -(
            math.pow(i - sigma, 2) + math.pow(j - sigma, 2)) / (2 * math.pow(sigma, 2)))
    return array


def PIL2np(img):
    imgarray = np.array(img.convert("L"))
    return imgarray


def np2PIL(imgarray):
    img = Image.fromarray(np.uint8(imgarray))
    return img


def convolution(imgarray, kernel):
    print "Convolving"
    start = timeit.default_timer()
    (nrow, ncol) = imgarray.shape
    (kernelrow, kernelcol) = kernel.shape
    out_array = np.zeros(shape=imgarray.shape)
    sum = 0
    sumkernel = 0
    indexcol = (kernelcol - 1) / 2
    indexrow = (kernelrow - 1) / 2
    for i in range(0, kernelrow):
        for j in range(0, kernelcol):
            sumkernel += kernel[i, j]
    # print indexcol
    # print indexrow
    # print sumkernel
    for i in range(indexrow, nrow - indexrow):
        for j in range(indexcol, ncol - indexcol):
            sum = 0
            for l in range(-indexrow, indexrow + 1):
                for m in range(-indexcol, indexcol + 1):
                    sum += imgarray[i - l, j - m] * kernel[l + indexcol, m + indexrow]
            out_array[i, j] = sum
    for i in range(0, nrow - 1):
        for j in range(0, ncol - 1):
            out_array[i, j] = out_array[i, j] / sumkernel
    stop = timeit.default_timer()
    print stop - start
    return out_array


if __name__ == '__main__':
    main()
