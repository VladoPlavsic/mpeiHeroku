from fastapi import HTTPException

def parse_youtube_link(link) -> str:
    '''
    Parse youtube link and return only 
    '''
    try:
        link = link.split('?v=')[1]
        link = link.split("&")[0]
    except:
        raise HTTPException(status_code=400, detail="Error trying to parse youtube link. Please refer to documentation to find out how to get and post valid youtube link.")
    return link


def list_to_string(list_) -> str:
    """
    Accepts list object, stringifys it and removes NOTE[]'NOTE symbols
    """
    list_ = str(list_)
    list_ = list_.replace('[','')
    list_ = list_.replace(']','')
    list_ = list_.replace("'",'"')
    return list_


def string_or_null(*args) -> str:
    '''
    Accept any number of STRING args
    Returns formated string where empty string args, or string args = None
    are replaced with null
    '''
    string = ''
    for arg in args:
        if arg == None or arg == '':
            string += 'null, '
        else:
            string += f"'{arg}', "

    return string.strip(', ')
