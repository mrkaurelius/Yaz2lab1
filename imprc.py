from pyzbar.pyzbar import decode
import cv2

def readisbn(filename):
     image = cv2.imread('./uploads/' + filename)
     detectedBarcodes = decode(image)
     for barcode in detectedBarcodes:
          print(barcode.data)
          return(barcode.data.decode("utf-8"))
     # print("barcode not detected!")
     return None

def readisbn_test(filename):
     image = cv2.imread('./testimg/' + filename)
     detectedBarcodes = decode(image)
     for barcode in detectedBarcodes:
          print(barcode.data)
          return(barcode.data.decode("utf-8"))
     # print("barcode not detected!")
     return None