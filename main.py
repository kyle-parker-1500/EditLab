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

# filepaths for uploaded images & chroma uploaded images
dir = Path(__file__).resolve().parent
upload_folder = dir / "uploads"
output_dir = dir / "output"

# making dirs if not already exist
upload_folder.mkdir(exist_ok=True)
output_dir.mkdir(exist_ok=True)

# route decorator binds a function to a URL
@app.route('/')
def home():
    return render_template(
        'index.html',
        effect_list=EFFECT_LIST,
        credits_remaining=get_credits_remaining,
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
def chroma_route():
    # get data from flask
    file1 = request.files.get('file')
    color = request.form.get('color')
    mode = request.form.get('mode')
    
    if file1 is None:
        return "Missing required file", 400  
    
    file2 = request.files.get('second_file')
    
    # save file1
    filename1 = secure_filename(file1.filename or "input.png")
    file1_path = upload_folder / filename1
    file1.save(file1_path)
    
    # save file2 if it exists
    file2_path = None
    if file2 is not None:
        filename2 = secure_filename(file2.filename or "input.png")
        file2_path = upload_folder / filename2
        file2.save(file2_path)

    # if color not selected
    if not color:
        return "Missing 'color' value.", 400     
    
    # convert color hex to rgb
    # Source - https://stackoverflow.com/a/29643643
    hex = str(color).lstrip('#')
    converted_color = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

    if mode == "replace_img_chroma":
        if file2_path is None:
            return "Second file required for replace_img_chroma", 400
        img_obj = chroma_key_with_img(str(file1_path), str(file2_path), converted_color)
    elif mode == "reverse":
        img_obj = reverse_chroma_key(str(file1_path), converted_color)
    else:
        img_obj = chroma_key(str(file1_path), converted_color)
    
    # save resulting image and return data to frontend
    output_path = output_dir / "chroma_result.png"
    img_obj.save(output_path, format="PNG") 
    
    return send_file(output_path, mimetype="image/png")