from flask import Flask, render_template, request
import yaml


from src.generate import Generation
from src.process_data import *
from src.constant import *


with open('configuration.yaml', 'r') as f:
    configs = yaml.safe_load(f)


text_generation = Generation(**configs)


app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def generate_text(name="John"):

    generated_text = ''

    if request.method == 'POST':
        text = request.form['input']
        generated_text = text_generation.generate(text)
    

    return render_template('home.html', name=name, generated_text=generated_text)
