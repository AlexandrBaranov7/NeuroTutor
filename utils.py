import re    
import datetime

def is_valid_datetime(date_time_str):
    pattern = r'^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})$'
    match = re.match(pattern, date_time_str)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))

        # Проверка корректности даты
        try:
            import datetime
            dt = datetime.datetime(year, month, day, hour, minute)
            return dt
        except ValueError:
            return False
    else:
        return False


def get_current_min():
    now = datetime.datetime.now()
    current_min = now.replace(second=0, microsecond=0)
    return current_min