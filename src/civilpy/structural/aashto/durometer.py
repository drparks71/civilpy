durometer_strain_factors = {
    "50": {
        "12": .1697,
        "9": .1413,
        "6": .1166,
        "5": .0858,
        "4": .0627,
        "3": .0414
    },
    "60": {
        "12": .1967,
        "9": .1701,
        "6": .1446,
        "5": .1053,
        "4": .0730,
        "3": .0464
    }
}

def find_closest_key(user_input, durometer_values, category):
    # Convert keys to numbers and compute the closest match
    values = map(float, durometer_values[category].keys())
    closest_key = min(values, key=lambda x: abs(x - float(user_input)))
    return str(int(closest_key))

# This got done because AASHTO lists strain as the independent variable, which
# seems wrong. So x and y in the formulas got twisted around during this
# This function results in the inverse of the y = Ax^1.3 formula
def get_strain_from_stress(stress, durometer, shape_factor):
    shape_factor = find_closest_key(shape_factor, durometer_strain_factors, str(durometer))
    return (stress / durometer_strain_factors[str(durometer)][shape_factor]) ** (1 / 1.3)