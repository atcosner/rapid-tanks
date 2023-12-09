def to_human_readable(unit: str) -> str:
    # Convert the pint units to a more human-readable format
    # i.e. degF -> °F
    if unit.startswith('deg'):
        return unit.replace('deg', '°').upper()
    else:
        return unit
