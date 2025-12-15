import os
from pathlib import Path

from flask import Flask, render_template, request, send_file
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename

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
    
    print("Path: ", output_path)

    # send all new data back to browser
    return send_file(output_path, mimetype="image/png")