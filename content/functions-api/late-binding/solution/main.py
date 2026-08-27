def make_multipliers(multipliers):
    return [lambda value, factor=factor: value * factor for factor in multipliers]
