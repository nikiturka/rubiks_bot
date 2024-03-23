import random

moves = ["U", "D", "F", "B", "R", "L"]
directions = ["", "'", "2"]
scramble_length = random.randint(15, 20)


def generate_empty_scramble():
    scramble = [0] * scramble_length

    for i in range(len(scramble)):
        scramble[i] = [0] * 2

    return scramble


def replace_scramble(empty_scramble):
    for i in range(len(empty_scramble)):
        empty_scramble[i][0] = random.choice(moves)
        empty_scramble[i][1] = random.choice(directions)

    return empty_scramble


def validate_scramble(scramble):
    for i in range(1, len(scramble)):
        while scramble[i][0] == scramble[i-1][0]:
            scramble[i][0] = random.choice(moves)

    for i in range(2, len(scramble)):
        while scramble[i][0] == scramble[i-2][0] or scramble[i][0] == scramble[i-1][0]:
            scramble[i][0] = random.choice(moves)

    return scramble


def generate_scramble():
    scramble = validate_scramble(replace_scramble(generate_empty_scramble()))
    scramble_string = ""

    for i in range(len(scramble)):
        scramble_string += f"{scramble[i][0]}{scramble[i][1]} "

    return scramble_string
