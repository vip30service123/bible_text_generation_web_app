from flask import Flask, render_template, request
import yaml


from src.generate import Generation
from src.process_data import *


with open('configuration.yaml', 'r') as f:
    configs = yaml.safe_load(f)


text_generation = Generation(**configs)


# app = Flask(__name__)

# @app.route("/", methods = ['POST', 'GET'])
# def generate_text(name="John"):

#     generated_text = ''

#     if request.method == 'POST':
#         generated_text = request.form['input']
    

#     return render_template('home.html', name=name, generated_text=generated_text)



print(process_string_to_list("I am not "))