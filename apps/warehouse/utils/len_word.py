def LenWord(str_in: str, col: int, replace='0') -> str:
    """change word to need count chars

    Args:
        str_in (str): string
        col (int): count chars in result world
        replace (str, optional): to what_replace, need 1 char str. Defaults to '0'.

    Returns:
        str: result word with add or remove chars
    """
    if len(str_in) < col:
        add = col - len(str_in)
        str_in = replace*add + str_in
    elif len(str_in) > col:
        rem = len(str_in) - col
        str_in = str_in[rem:]
    return str_in
