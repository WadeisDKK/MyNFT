import time
import os
from PIL import Image
import numpy as np
from queue import Queue

"""
Author: https://github.com/WadeisDKK
Email: tyyf_wade@163.com
"""

def pictureToPdf(picturepath,writtenPdfPath):
    im = Image.open(picturepath)
    data = np.asarray(im)
    b64data = bytesFrom6bitsArray(data)
    with open(writtenPdfPath,'wb') as f:
        f.write(b64data)

def bytesFrom6bitsArray(data):
    newData = b''

    q = Queue(maxsize=8)

    totalWidth = len(data)
    totalHeight = len(data[0])

    num = 0
    flag = 7
    for depth in range(3):
        print("depth/total: ",depth,"/",3)
        for height in range(totalHeight):
            # print(r"height/total: ",height,"/",totalHeight)
            for width in range(totalWidth):
                item = data[width][height][depth]
                for i in range(6):
                    if (item & (1 << (5 - i))):
                        num += 2**flag
                    flag -= 1
                    if (flag == -1):
                        newData += int.to_bytes(num,1,byteorder="big")
                        flag = 7
                        num = 0

    return newData

def main():

    readFolder = "pictures//"
    writeFolder = "pdf//"

    start = time.time()

    files = os.listdir(readFolder)
    for file in files:
        readpath = readFolder + file
        writepath = writeFolder +  file.split(".")[0] + ".pdf"
        print("Start decoding", file)
        pictureToPdf(readpath,writepath)

        end = time.time()
        print(writepath, "written, takes", end-start, "seconds" , "\n")
        start = end
    
if __name__ == "__main__":
    main()
