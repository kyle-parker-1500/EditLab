import os
from pathlib import Path

from flask import Flask, render_template, request, send_file
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
from PIL import Image

from filters import apply_effect, EFFECT_LIST, get_credits_remaining
from chroma import chroma_key, chroma_key_with_img, reverse_chroma_key

# create instance of Flask
app = Flask(__name__)

bootstrap = Bootstrap5(app)

# filepath to save uploaded images to
dir = Path(__file__).resolve().parent
upload_folder = dir / "uploads"
upload_folder.mkdir(exist_ok=True)

# route decorator binds a function to a URL
@app.route('/')
def home():
    return render_template(
        'index.html',
        effect_list=EFFECT_LIST,
        credits_remaining=get_credits_remaining,
        chroma_key=chroma_key,
        img_chroma=chroma_key_with_img,
        reverse_chroma_key=reverse_chroma_key,
        )

@app.route('/apply-effect', methods=['POST'])
def get_effect():
    # getting data from frontend
    uploaded = request.files['file']
    effect_name = request.form['effect']
    
    # ---- save file to disk ----
    # generate unique filename for secure disk saving things
    filename = secure_filename(uploaded.filename or "input.png")
    uploaded_img_path = upload_folder / filename
    # save on generated path
    uploaded.save(uploaded_img_path) 
    
    # query apply_effect with new filename
    apply_effect(str(uploaded_img_path), effect_name)
    
    # get created image (always named output.png)
    output_path = dir / "output.png"
    
    # debug: print("Path: ", output_path)

    # send all new data back to browser
    return send_file(output_path, mimetype="image/png")

@app.route('/chroma-key', methods=['POST'])
def get_key():
    uploaded = request.files['file']
    color = request.form['color']
    
    # ---- save file to uploaded folder on disk ----
    filename = secure_filename(uploaded.filename or "input.png")
    uploaded_img_path = upload_folder / filename
    # save on path
    uploaded.save(uploaded_img_path)
    
    # convert color hex to rgb
    
    # Source - https://stackoverflow.com/a/29643643
    hex = str(color).lstrip('#')
    converted_color = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

    # call chroma_key to chroma the key :)
    # debug: print("Path of Image: ", uploaded_img_path, "\nand Color: ", converted_color, " of type ", type(converted_color))
    img_obj = chroma_key(str(uploaded_img_path), converted_color)

    # convert pil image to output path
    img_obj.save("/output/chroma_result.png", format="PNG") 
    
    output_path = dir / "output" / "chroma_result.png"
    
    return send_file(output_path, mime_type="image/png")