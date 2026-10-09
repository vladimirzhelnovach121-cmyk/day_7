"""Расчёт просрочки по учебным правилам SLA."""
LIMITS = {"high": 30, "normal": 120, "low": 480}

def is_overdue(elapsed_minutes, priority="normal"):
    if elapsed_minutes < 0:
        raise ValueError("Время не может быть отрицательным")
    if priority not in LIMITS:
        raise ValueError("Неизвестный приоритет")
    return elapsed_minutes >= LIMITS[priority]
