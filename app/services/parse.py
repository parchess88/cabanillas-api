from datetime import datetime, time

def parse_time(hora_str: str) -> time | None:
    """
    Convierte un string de hora a datetime.time.
    Retorna None si la cadena está vacía o inválida.
    Acepta formatos: '21:00', '9:30', '09:30'
    """
    if not hora_str:
        return None
    try:
        # Intentamos convertir el string a time
        return datetime.strptime(hora_str, "%H:%M").time()
    except ValueError:
        # Si el formato no es válido, retornamos None
        return None