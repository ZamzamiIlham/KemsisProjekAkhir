from flask import Flask, render_template, request
from PIL import Image
from io import BytesIO
from Stegan import Encode, Decode
import math
import random

app = Flask(__name__)

letter = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",",",".","!","?"," "]
number = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

def cipher(num,e):
    X = []
    for i in range(len(num)):
        X.append((int(num[i])**e)%n)
    return X

def decipher(num,d):
    Y = []
    for i in range(len(num)):
        Y.append((int(num[i])**d)%n)
    return Y

def gcd(a, b):
    while b != 0:
        (a, b) = (b, a % b)
    return a

def phi(n):
    amount = 0
    for k in range(1, n + 1):
        if math.gcd(n, k) == 1:
            amount += 1
    return amount

def Encrypt(img, plaintext):
    plaintext = plaintext.lower()
    numC = []
    for i in range(len(plaintext)):
        for j in range(len(letter)):
            if plaintext[i] == letter[j]:
                numC.append(number[j])
    X = cipher(numC, e)
    encoded_img = Encode(img, plaintext, X)
    return encoded_img

def Decrypt(img):
    hidden_text = Decode(img)
    deciphered_text = decipher(hidden_text, d)
    numD = []
    for i in range(len(deciphered_text)):
        for j in range(len(number)):
            if deciphered_text[i] == int(number[j]):
                numD.append(letter[j])
    decrypted_text = "".join(numD)
    return decrypted_text

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No file selected')

        original_image = Image.open(file)
        plaintext = request.form['plaintext']
        if 'encrypt' in request.form:
            encoded_img = Encrypt(original_image, plaintext)
            if encoded_img:
                encoded_img.save('enc_image.png')
                return render_template('index.html', message='Encryption successful', image_path='enc_image.png')
        elif 'decrypt' in request.form:
            decrypted_text = Decrypt(original_image)
            return render_template('index.html', message='Decryption successful', decrypted_text=decrypted_text)
        
    return render_template('index.html')

if __name__ == '__main__':
    n = 2537
    e = 13
    d = 937
    app.run(debug=True)