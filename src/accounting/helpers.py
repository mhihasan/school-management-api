import random
import string


def generate_gl_code(digit=10):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(digit)
    )
