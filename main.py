from flask import Flask, render_template, request
import yaml


from bible_text_generation_web_app.src.generate import Generation
from bible_text_generation_web_app.src.process_data import *
from bible_text_generation_web_app.src.constant import *


with open('configuration.yaml', 'r') as f:
    configs = yaml.safe_load(f)


text_generation = Generation(**configs)


app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def generate_text(name="John"):

    generated_text = ''

    if request.method == 'POST':
        text = request.form['input']
        ge = text_generation.generate(text).replace('\n', '</br>')
        generated_text = ge
    

    return render_template('home.html', name=name, generated_text=generated_text)





