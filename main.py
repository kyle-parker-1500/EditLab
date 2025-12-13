from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from filters import apply_effect, EFFECT_LIST, API_KEY

# create instance of Flask
app = Flask(__name__)

bootstrap = Bootstrap5(app)

# route decorator binds a function to a URL
@app.route('/')
def home():
    return render_template(
        'index.html',
        effect_list=EFFECT_LIST
        )

@app.route('/import_image')
def images():
    return render_template('inout.html')
