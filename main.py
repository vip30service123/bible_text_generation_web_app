from flask import Flask, render_template, request
import yaml


from bible_text_generation_web_app.src.generate import TextGenerationFactory




with open('configuration.yaml', 'r') as f:
    configs = yaml.safe_load(f)


text_generation = TextGenerationFactory(**configs)


app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def generate_text(name="John"):

    generated_text = ''

    if request.method == 'POST':
        input_text = request.form['input']
        generated_text = text_generation.generate(input_text).replace('\n', '</br>')
    

    return render_template('home.html', name=name, generated_text=generated_text)





