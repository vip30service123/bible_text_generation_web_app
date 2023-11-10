import torch


from bible_text_generation_web_app.src.model import GPT
from bible_text_generation_web_app.src.process_data import *



class Generation:
    

    def __init__(
        self,
        vocab_sz, 
        window_sz, 
        dim, 
        n_layers, 
        device, 
        head_dim, 
        n_heads, 
        dropout,
        model_path, 
        *args,
        **kwargs
        ):
        
        self.model = GPT(vocab_sz, window_sz, dim, n_layers, device, head_dim, n_heads, dropout)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))




    def generate(self, text):
        text = process_string_to_list("I am not ")
        encoded_input = encode_input(text)
        encoded_input_tensor = torch.Tensor([encoded_input]).type(torch.int64)

        out = self.model.generate(encoded_input_tensor)

        return ' '.join(decode_input(out.tolist()[0]))



