from datetime import datetime

def compare_dates(date1_str, date2_str, date_format):
    if date1_str == 'Null' or date2_str == 'Null':
        return False
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)
    if date1 > date2:
        return True
    return False


def check_now_dates(date_str, date_format):
    if date_str == 'Null':
        return False
    date_now = datetime.now().date()
    date_now = str(date_now).replace('-', '.')
    date_now = datetime.strptime(date_now, "%Y.%m.%d")
    date = datetime.strptime(date_str, date_format)
    if date_now > date:
        return True
    return False