import torch


from .model import GPT
from .process_data import *


class Generation:
    def __init__(self, *args, **kwargs):
        self.model = GPT()
        self.model.load_state_dict(
            torch.load(
                "bible_app/src/GPT_ver_1/GPT_1.pt", map_location=torch.device("cpu")
            )
        )

    def generate(self, text: str) -> str:
        processed_text = process_string_to_list(text)
        encoded_input = encode_input(processed_text)
        encoded_input_tensor = torch.Tensor([encoded_input]).type(torch.int64)

        out = self.model.generate(encoded_input_tensor)

        return " ".join([text.strip()] + decode_input(out["generate"].tolist()[0]))
