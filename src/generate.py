'''
Text generation factory
'''
from bible_text_generation_web_app.src.GPT_ver_0 import generate as generate_ver_0
from bible_text_generation_web_app.src.GPT_ver_1 import generate as generate_ver_1


class TextGenerationFactory:
    def __init__(self, model_name: str):
        if model_name == 'GPT_ver_0':
            self.text_generation = generate_ver_0.Generation()
        elif model_name == 'GPT_ver_1':
            self.text_generation = generate_ver_1.Generation()
        else:
            raise Exception(f"Model {model_name} is not available.")


    def generate(self, text: str) -> str:
        return self.text_generation.generate(text)