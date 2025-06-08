import secrets


def generate_random_id(ids: list, startswith: str, digit_number: int) -> str:
    new_id = startswith + str(secrets.randbelow(10**digit_number)).zfill(digit_number)
    while new_id in ids:
        new_id = startswith + str(secrets.randbelow(10**digit_number)).zfill(
            digit_number
        )
    return new_id