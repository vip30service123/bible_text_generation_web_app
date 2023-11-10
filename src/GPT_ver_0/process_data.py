from bible_text_generation_web_app.src.GPT_ver_0.constant import *


def process_string_to_list(input):
    return input.strip().split(' ')


def encode_input(ls):
    output = []
    for i in ls:
        if i in ENCODER:
            output.append(ENCODER[i])
        else:
            output.append(ENCODER['**'])
    return output


def decode_input(ls):
    return [DECODER[i] for i in ls]