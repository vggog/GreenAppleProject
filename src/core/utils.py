def delete_none_value_from_dict(original_dict: dict) -> dict:
    """
    Функция для удаления значений = None из словаря.

    :param original_dict: словарь из которого надо удалить None-значения.
    :return: результирующий словарь без None-значений.
    """
    res_dict = {}
    for key, value in original_dict.items():
        if res_dict[key] is None:
            continue
        res_dict[key] = value

    return res_dict
