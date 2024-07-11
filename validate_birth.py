# Comando de validación para aceptar solo números y limitar rango
def validate_numeric_input(value_if_allowed, min_val, max_val):
    if value_if_allowed == "":
        return True
    if value_if_allowed.isdigit():
        value = int(value_if_allowed)
        return min_val <= value <= max_val
    return False

# Comando de validación para year
def validate_year_input(value_if_allowed, length):
    if value_if_allowed == "":
        return True
    if value_if_allowed.isdigit() and len(value_if_allowed) <= length:
        return True
    return False
