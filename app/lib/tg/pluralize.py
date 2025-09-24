def pluralize(
    count: int, 
    forms: dict[str, str]
) -> str:
    if 11 <= count % 100 <= 19:
        form = "many"
    else:
        last_digit = count % 10
        if last_digit == 1:
            form = "one"
        elif 2 <= last_digit <= 4:
            form = "few"
        else:
            form = "many"
    return forms[form].replace("%{count}", str(count))