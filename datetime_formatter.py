from datetime import datetime

def format_date(date_str, date_format, wrap_in_link):
    if date_str and date_str != "missing value":
        date_obj = datetime.fromisoformat(date_str)
        formatted_date = date_obj.strftime(date_format.replace('YYYY', '%Y').replace('MM', '%m').replace('DD', '%d'))
        
        if wrap_in_link:
            formatted_date = f"[[{formatted_date}]]"
    else:
        formatted_date = ""
    return formatted_date

def format_time(date_str, time_format):
    if date_str and date_str != "missing value":
        date_obj = datetime.fromisoformat(date_str)
        return date_obj.strftime(time_format.replace('HH', '%H').replace('mm', '%M').replace('SS', '%S'))
    return ""

def format_datetime(date_str, date_format, time_format, separator, wrap_in_link):
    date_part = format_date(date_str, date_format, wrap_in_link)
    time_part = format_time(date_str, time_format)
    if date_part and time_part:
        return f"{date_part}{separator}{time_part}"
    return date_part

def format_date_for_filename(date_obj, date_format):
    return date_obj.strftime(date_format.replace('YYYY', '%Y').replace('MM', '%m').replace('DD', '%d'))