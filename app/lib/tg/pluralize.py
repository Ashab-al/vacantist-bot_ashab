MANY, ONE, FEW = 'many', 'one', 'few'
TEEN_START, TEEN_END = 11, 19
LOW_END_FEW, HIGH_END_FEW = 2, 4
SINGULAR = 1

def pluralize(
    count: int, 
    forms: dict[str, str]
) -> str:
    """
    Возвращает корректную форму слова в зависимости от числа (русская система склонения).

    Параметры:
        count (int): число, определяющее форму слова.
        forms (dict[str, str]): словарь с тремя формами слова:
            - 'one': форма для 1 (например, "1 яблоко")
            - 'few': форма для 2–4 (например, "2 яблока")
            - 'many': форма для всех остальных случаев (например, "5 яблок")

    Возвращает:
        str: строка с числом и корректной формой слова, 
             где "%{count}" заменяется на значение count.
    """
    last_two, last_digit = count % 100, count % 10
    form = (
        MANY if TEEN_START <= last_two <= TEEN_END else
        ONE if last_digit == SINGULAR else
        FEW if LOW_END_FEW <= last_digit <= HIGH_END_FEW else
        MANY
    )
    return forms[form].replace("%{count}", str(count))
