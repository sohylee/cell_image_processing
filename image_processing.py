import cv2
import numpy as np
import csv
from matplotlib import pyplot as plt

def calculatePixels(_str):
    # calculate activated (red) pixels
    img = cv2.imread(_str)
    ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    gray = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
    num_activated = cv2.countNonZero(gray)

    # calculate cell pixels
    img = cv2.imread(_str)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite("gray_" + _str, gray)
    high_thresh, thresh_im = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    num_cells = cv2.countNonZero(thresh_im)

    # save image for debugging purposes
    cv2.imwrite("converted_" + _str, thresh_im)

    # return pixel numbers
    return (num_activated, num_cells)

with open('taylor_lab_data.csv', 'w') as csvfile:
    fieldnames = ['file_name', 'num_activated_pixels', 'num_cell_pixels', 'ratio', 'correctedCell_per_pixel']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i in range (0,50):
        _str = ''
        if i < 10:
            _str += "IMAGE_00" + str(i) + ".tif"
        else:
            _str += "IMAGE_0" + str(i) + ".tif"

        (num_activated, num_cells) = calculatePixels(_str)
        ratio = float(num_activated)/num_cells*100
        correctedCell_per_pixel = ratio / 57.83 * 100
        writer.writerow({'file_name': _str, 'num_activated_pixels': num_activated, 'num_cell_pixels': num_cells, 'ratio': ratio,
        'correctedCell_per_pixel': correctedCell_per_pixel})

'''
# visualization
titles = ['Original Image','BINARY','GRAY']
images = [img, thresh1, gray]
for i in xrange(3):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
'''
