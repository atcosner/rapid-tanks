def to_human_readable(unit: str) -> str:
    # Convert the pint units to a more human-readable format
    # i.e. degF -> °F
    if unit.startswith('deg'):
        return unit.replace('deg', '°').upper()
    else:
        return unit


def sanitize_unit(unit: str) -> str:
    # Allow units that are good for the GUI to be sanitized for pint
    sanitizations = {
        'psia': 'psi',  # Absolute PSI
        'psig': 'psi',  # Gauge PSI
    }
    return sanitizations.get(unit, unit)
