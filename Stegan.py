from PIL import Image
def Encode(img, msg, lst):
    global L
    L = []
    length=len(msg)
    if length > 255:
        print("Textmelebihi 255 karakter")
        return False
    if img.mode != 'RGB':
        print("Gunakan foto berformat RGB")
        return False
   
    encoded_img = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                c = lst[index - 1]
                asc = c // 255
                L += [c % 255]
            else:
                asc = r
            encoded_img.putpixel((col, row), (asc, g, b))
            index += 1
    return encoded_img


# Decode function of Steganography

def Decode(img):
    global L
    width, height = img.size
    msg = ""
    lst = []
    index = 0
    length = 0
    for row in range(height):
        for col in range(width):
            try:
                r, g, b = img.getpixel((col, row))
            except ValueError:
                r, g, b, a = img.getpixel((col, row))
            if row == 0 and col == 0:
                length = r
            elif index <= length:
                lst += [r * 255 + L[index - 1]]
            index += 1
    return lst
