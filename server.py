from flask import Flask, request
import base64
from googletrans import Translator
import main

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

app = Flask(__name__)
translator = Translator()

def to_english(text):
    return translator.translate(text, dest="en").text

@app.route("/", methods=["POST"])
def get_data():
    image = request.form["image"].encode("utf-8")
    IMAGE = "image"
    with open("image.png", "wb") as fh:
        fh.write(base64.decodebytes(image))
    
    stringed_image = to_english(pytesseract.image_to_string("image.png"))
    print(stringed_image)
    return stringed_image

@app.route("/summary", methods=["POST"])
def get_summary():
    sents = request.form["count"]
    string = request.form["content"]

    res = main.main(string, int(sents))

    return res

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
