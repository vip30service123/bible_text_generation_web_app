from typing import List


from .constant import *


def process_string_to_list(input):
    i = 0
    out = []
    # Two pointer run to detect special chars
    for j in range(len(input)):
        if input[j] not in SPECIAL_CHA:
            if input[i] in SPECIAL_CHA:
                if input[i:j] != " ":
                    out.append(input[i:j])
                i = j
        else:
            if input[i:j] != " ":
                out.append(input[i:j])
            i = j

    out.append(input[i:])

    return out


def encode_input(str_ls: List[str]) -> List[int]:
    output = []
    for string in str_ls:
        if string in ENCODER:
            output.append(ENCODER[string])
        else:
            output.append(ENCODER["**"])
    return output


def decode_input(num_ls: List[int]) -> List[str]:
    return [DECODER[i] for i in num_ls]
