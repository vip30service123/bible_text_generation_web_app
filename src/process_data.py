from src.constant import *


def process_string_to_list(input):
    i = 0
    out = []
    # Two pointer run to detect special chars
    for j in range(len(input)):
        if input[j] not in SPECIAL_CHA:
            if input[i] in SPECIAL_CHA:
                if input[i:j] != ' ':
                    out.append(input[i:j])
                i = j
        else:
            if input[i:j] != ' ':
                out.append(input[i:j])
            i = j

    return out


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