'''
Text generation factory
'''
from bible_text_generation_web_app.src.GPT_ver_0.generate import Generation


class TextGenerationFactory:
    def __init__(self, model_name):
        if model_name == 'GPT_ver_0':
            self.text_generation = Generation()
        else:
            raise Exception(f"Model {model_name} is not available.")


    def generate(self, text):
        return self.text_generation.generate(text)