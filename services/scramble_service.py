import random


class ScrambleService:
    moves = ["U", "D", "F", "B", "R", "L"]
    directions = ["", "'", "2"]
    scramble_length = random.randint(15, 20)

    @staticmethod
    def generate_empty_scramble():
        scramble = [0] * ScrambleService.scramble_length

        for i in range(len(scramble)):
            scramble[i] = [0] * 2

        return scramble

    @staticmethod
    def replace_scramble(empty_scramble):
        for i in range(len(empty_scramble)):
            empty_scramble[i][0] = random.choice(ScrambleService.moves)
            empty_scramble[i][1] = random.choice(ScrambleService.directions)

        return empty_scramble

    @staticmethod
    def validate_scramble(scramble):
        for i in range(1, len(scramble)):
            while scramble[i][0] == scramble[i-1][0]:
                scramble[i][0] = random.choice(ScrambleService.moves)

        for i in range(2, len(scramble)):
            while scramble[i][0] == scramble[i-2][0] or scramble[i][0] == scramble[i-1][0]:
                scramble[i][0] = random.choice(ScrambleService.moves)

        return scramble

    @staticmethod
    def generate_scramble():
        scramble = (
            ScrambleService.validate_scramble(
                ScrambleService.replace_scramble(
                    ScrambleService.generate_empty_scramble()
                )
            )
        )

        scramble_string = ""

        for i in range(len(scramble)):
            scramble_string += f"{scramble[i][0]}{scramble[i][1]} "

        return scramble_string
