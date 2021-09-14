"""This module defines some of default types allowed and default naming configurations"""

from typing import Any
from enum import Enum

class DefaultFolders(Enum):
    """Enum class defining default folders for specific type of content."""
    IMAGES = 'img/'
    AUDIO = 'mp3/'

class Formats:
    def __init__(self, value:Any):
        self.value = value

class DefaultFormats(Enum):
    """Enum class defining suported formats for specific type of content.
    
    NOTE We are using Formats helping class to get around enum aliases.
    If we were not to use it this way, IMAGES and QUIZ would be the same, and we 
    could not differ them.
    """
    IMAGES = Formats(['jpg', 'png'])
    AUDIO = Formats(['vaw', 'mp3'])
    VIDEO = Formats(['mp4'])
    BOOK = Formats(['pdf', 'doc', 'docx'])
    QUIZ = Formats(['jpg', 'png'])
    GAME = Formats(['html'])

    @property
    def formats(self):
        return self.value.value

class ObjectTypes(Enum):
    STRUCTURE = 'structure'
    MATERIAL = 'matreial'
    PARTS = 'parts'
    TEAM = 'team'
    NEWS = 'news'
    