
from PIL import Image
import random
import tkinter as tk
import cv2
def encrypt(plain_text, shift):
    cipher_text = ""
    for char in plain_text:
        # Convert the character to its ASCII code
        ascii_code = ord(char)
        
        # Shift the ASCII code by the given shift amount
        shifted_ascii_code = ascii_code + shift
        
        # Convert the shifted ASCII code back to a character
        cipher_char = chr(shifted_ascii_code)
        
        # Add the cipher character to the cipher text
        cipher_text += cipher_char
    
    return cipher_text
def decrypt(cipher_text, shift):
    plain_text = ""
    for char in cipher_text:
        # Convert the character to its ASCII code
        ascii_code = ord(char)
        
        # Shift the ASCII code back by the given shift amount
        shifted_ascii_code = ascii_code - shift
        
        # Convert the shifted ASCII code back to a character
        plain_char = chr(shifted_ascii_code)
        
        # Add the plain character to the plain text
        plain_text += plain_char
    
    return plain_text
# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
 
        # list of binary codes
        # of given data
        newd = []
 
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd
 
# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
 
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
 
    for i in range(lendata):
 
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
 
        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1
 
        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
 
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
 
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
 
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
 
    for pixel in modPix(newimg.getdata(), data):
 
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
# Encode data into image
def encode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
 
    random_number = random.randint(1000, 9999)
    random_string = str(random_number)
    print("otp is : " + random_string)
    data=random_string
    #encryption
    data=encrypt(data,6)
    if (len(data) == 0):
        raise ValueError('Data is empty')
 
    newimg = image.copy()
    encode_enc(newimg, data)
 
    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
     
# Decode the data in the image
def decode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
 
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string of binary data
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):

            return data
 
# Main Function
def main():
    
    print("hiding encrypted otp in image")
    encode()
    print("warning: Do not click to share otp ")
    #function for changing otp content
    # # define a function to handle mouse click events
  
def handle_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at ({x}, {y})")

# load the image
image = cv2.imread("2.png")

# create a window to display the image
cv2.namedWindow("Image")

# set the mouse callback function for the window
cv2.setMouseCallback("Image", handle_click)

# display the image and wait for a key press
cv2.imshow("Image", image)
cv2.waitKey(0)

# cleanup
cv2.destroyAllWindows()

    
  
print("the otp for netfilx is :  " + decrypt(decode(),6))
 
# Driver Code
if __name__ == '__main__' :
 
    # Calling main function
    main()