from typing import List
import random

def generate_random_id(ids: List, startswith: str, digit_number: int) -> str:
    new_id = startswith + str(random.randint(0, 99999)).zfill(digit_number)
    if new_id in ids:
        return generate_random_id(ids=ids, startswith=startswith, digit_number=digit_number)
    return new_id
