from typing import Dict, List, Optional


from .constant import *


def process_string_to_list(input: str) -> List[str]:
    return input.strip().split(' ')


def encode_input(str_ls: List[str]) -> List[int]:
    output = []
    for string in str_ls:
        if string in ENCODER:
            output.append(ENCODER[string])
        else:
            output.append(ENCODER['**'])
    return output


def decode_input(num_ls: List[int]) -> List[str]:
    return [DECODER[i] for i in num_ls]