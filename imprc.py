from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

import cv2
import pytesseract
import sys

# TODO: 
# switch prints to log

def find_isbn(text):
     for line in text.splitlines():
          if len(line) >= 13:
               isbn_str = ''
               for char in line:
                    if(str.isdigit(char)):
                         isbn_str += char
                         if len(isbn_str) == 13:
                              print('ocr find isbn: ',isbn_str)
                              return isbn_str
     return None

def readisbn(filename, useArgv=False):
     if useArgv is True:
          # run from cli
          if len(sys.argv) > 2 or len(sys.argv) == 1:
               print('need argument')
               sys.exit(1)
          img_path = sys.argv[1]

          ocr_output = readisbn_ocr(img_path, uploads=False)
          if ocr_output is not None: 
               return ocr_output
               
          print('ocr cant detect isbn trying barcode')
          return readisbn_barcode(img_path, uploads=False)
     else:
          # run from flask
          ocr_output = readisbn_ocr(filename)
          if ocr_output is not None: 
               return ocr_output
               
          # fallback
          print('ocr cant detect isbn trying barcode')
          return readisbn_barcode(filename)

def readisbn_barcode(filename, uploads=True):
     if uploads:
          image = cv2.imread('./uploads/' + filename)
     else:
          image = cv2.imread(filename)

     barcodes = decode(image)
     for barcode in barcodes:
          print('pyzbar find isbn', barcode.data)
          return(barcode.data.decode("utf-8"))
     print("barcode not detected!")
     return None

def readisbn_ocr(filename, uploads=True):
     if uploads:
          image = cv2.imread('./uploads/' + filename)
     else:
          image = cv2.imread(filename,  cv2.COLOR_BGR2RGB)

     img_width = image.shape[0]
     img_height = image.shape[1]

     barcodes = decode(image, symbols=[ZBarSymbol.EAN13])
     # barcodes = decode(image)
     for barcode in barcodes:
          print('barcode')
          (x, y, w, h) = barcode.rect
     # help(barcode)

     if len(barcodes) == 0: 
          print('cant find barcode any barcode, searching all page')
          # scan all page
          ocr_output = pytesseract.image_to_string(image)
          print(ocr_output)
          find_isbn(ocr_output)
          return None

     x_org = x
     y_org = y
     x -= (w//2)
     y -= (h//2)
     w += (w//2)
     h += (h//2)

     # find isbn line and tinker with it
     try:
          isbn_roi = image[y:y_org+h, x:x_org+w]
     except:
          print('exception')

     ocr_output = pytesseract.image_to_string(isbn_roi)
     print('ocr output')
     print(ocr_output)
     return find_isbn(ocr_output)

#out = readisbn('',useArgv=True)
#print('readisbn out: ', out)

# cv2.namedWindow('img', cv2.WINDOW_NORMAL)
# cv2.imshow('img', isbn_roi)
# cv2.resizeWindow('img', 600, 600)
# cv2.waitKey(0)

# image = cv2.imread('./testimg/ocr/IMG_20200410_141351.jpg')
# Beyaz Geceler, 9786053321392, image better, trailing number
# image = cv2.imread('./testimg/ocr/IMG_20200410_141734.jpg')
# cant read properly
# image = cv2.imread('./testimg/ocr/IMG_20200410_144619.jpg') 
# The ultimate guide for vocabulary, 9786058962620, img better

# image = cv2.imread('./testimg/milzen.jpg') # success
# image = cv2.imread('./testimg/isbn_1.png') # success

# Strategy
# find barcode, scale around, search isbn
# if cant detect isbn look for all image
     # improve ocr accuracy
# if cant detect isbn use barcode data
# compare ocr output with barcode

# TODO improve OCR accuracy
# scale characters to 30px