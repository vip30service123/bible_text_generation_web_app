import os

from flask import Flask, render_template, request
import yaml


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    from .src.generate import TextGenerationFactory

    with open("bible_app/configuration.yaml", "r") as f:
        configs = yaml.safe_load(f)

    text_generation = TextGenerationFactory(**configs)

    app = Flask(__name__)

    @app.route("/", methods=["POST", "GET"])
    def generate_text(name="John"):
        generated_text = ""

        if request.method == "POST":
            input_text = request.form["input"]
            generated_text = text_generation.generate(input_text).replace("\n", "</br>")

        return render_template("home.html", name=name, generated_text=generated_text)

    return app
