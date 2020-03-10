from pyzbar.pyzbar import decode
import cv2

def readisbn(filename):
     image = cv2.imread('./uploads/' + filename)
     detectedBarcodes = decode(image)
     for barcode in detectedBarcodes:
          print(barcode.data)
          return(barcode.data)
     # print("barcode not detected!")
     return None