from PIL import Image
from flask import Flask, request, send_file, render_template
from flask_bootstrap import Bootstrap5
import io   

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route("/")
def index():
    return render_template("index.html")   
@app.route("/crop", methods=["POST"])
def crop():
   
    file = request.files.get("filter_img")
    if not file:
        return "No image uploaded", 400
    
    img = Image.open(file.stream)

    
    try:
        left = int(request.form.get("left", 0))
        top = int(request.form.get("top", 0))
        right = int(request.form.get("right", img.width))
        bottom = int(request.form.get("bottom", img.height))
    except ValueError:
        return "Invalid crop coordinates", 400

    
    cropped = img.crop((left, top, right, bottom))

   
    new_w = request.form.get("width")
    new_h = request.form.get("height")
    if new_w and new_h:
        try:
            new_w = int(new_w)
            new_h = int(new_h)
            cropped = cropped.resize((new_w, new_h))
        except ValueError:
       
            pass

    img_io = io.BytesIO()
    cropped.save(img_io, format="PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")
@app.route("/rotate", methods=["POST"])
def rotate_image():
    file = request.files.get("filter_img")
    if not file:
        return "No image uploaded", 400

    img = Image.open(file.stream)
    angle = int(request.form.get("angle", 90))

    rotated = img.rotate(angle, expand=True)

    img_io = io.BytesIO()
    rotated.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


@app.route("/move", methods=["POST"])
def move_image():
    file = request.files.get("filter_img")
    if not file:
        return "No image uploaded", 400

    img = Image.open(file.stream).convert("RGBA")

    offset_x = int(request.form.get("x", 0))
    offset_y = int(request.form.get("y", 0))

    canvas = Image.new("RGBA", img.size, (0, 0, 0, 0))
    canvas.paste(img, (offset_x, offset_y))

    img_io = io.BytesIO()
    canvas.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")









if __name__ == "__main__":
    app.run(debug=True)