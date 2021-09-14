from typing import List, Tuple

from app.models.private import StructureAllModel
from app.models.private import MaterialAllModel
from app.models.private import AudioImagesAllModel
from app.models.about import TeamMemberInDBModel
from app.models.news import NewsImagesAllModel

import logging

logger = logging.getLogger(__name__)

def get_order_number_from_key(key) -> int:
    """Accept any key and try to parse number from file name it's pointing to.
    
    If there is exception, raise warn and return None.
    """
    number_string = key.split('/')[-1].split('.')[0]
    try:
        order_number = int(number_string)
    except:
        logger.warn("---EXCEPTION RAISED TRYING TO PARSE NUMBER FROM KEY---")
        logger.warn(f"Key: {key}")
        logger.warn("---EXCEPTION RAISED TRYING TO PARSE NUMBER FROM KEY---")
        order_number = None

    return order_number


def get_format_from_key(key) -> str:
    """Accept any key and return format of file it's pointing to."""
    try:
        type_ = key.split('/')[-1].split('.')[-1]
    except:
        logger.warn("---EXCEPTION RAISED TRYING TO PARSE TYPE OF FILE FROM KEY---")
        logger.warn(f"Key: {key}")
        logger.warn("---EXCEPTION RAISED TRYING TO PARSE TYPE OF FILE FROM KEY---")

    return type_


def get_folder_by_inner_key(key: str) -> str:
    return key.replace(key.split("/")[-1], "")

