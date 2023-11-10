import torch


from bible_text_generation_web_app.src.GPT_ver_0.model import GPT
from bible_text_generation_web_app.src.GPT_ver_0.process_data import *


class Generation:
    def __init__(self, *args, **kwargs):              
        self.model = GPT()
        self.model.load_state_dict(torch.load('src/GPT_ver_0/GPT.pt', map_location=torch.device('cpu')))


    def generate(self, text):          
        processed_text = process_string_to_list(text)
        encoded_input = encode_input(processed_text)
        encoded_input_tensor = torch.Tensor([encoded_input]).type(torch.int64)

        out = self.model.generate(encoded_input_tensor)

        return ' '.join(decode_input(out.tolist()[0]))



