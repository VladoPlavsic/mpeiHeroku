from enum import Enum

class QueryReturnType(Enum):
    """Different query execution types.

    To find out more consulte the documentation @:
        https://www.encode.io/databases/database_queries/
    """
    EXECUTE_ONE   = 0
    EXECUTE_MANY  = 1
    FETCH_ONE     = 2
    FETCH_MANY    = 3
    FETCH_ONE_VAL = 4

class ContentType(Enum):
    """This enum class holds names of db tables based on type of content."""
    PRACTICE = 'practice'
    THEORY = 'theory'
    VIDEO = 'video'
    BOOK = 'book'
    GAME = 'game'
    QUIZ = 'quiz'
    IMAGE = 'image'
    AUDIO = 'audio'
    INTRO = "intro_video" # New
