import re

l = ['Mike', 'Adam']
txt = "#[Mike] Co tam #[sraka] bq"

def name_validate(message: str, list_of_names: list[str]) -> tuple[bool, str]:
    """
    Search name at the beginning of message
    If found, return True & name, else return False, None
    """
    name_regex = "^\#\[[a-zA-Z]+\]"
    find = re.search(name_regex, message)
    try:
        find = find.group(0)
        if find[2:-1] in list_of_names:
            return True, find[2:-1]
        return False, None
    except AttributeError as err:
        return False, None
    

# print(name_validate("siema", l))