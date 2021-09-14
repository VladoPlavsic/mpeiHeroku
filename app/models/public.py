from typing import List, Optional
from app.models.core import DBCoreModel

# ###
# Material models
# ###

class MaterialCoreModel(DBCoreModel):
    name_ru: str
    description: str

# video
class VideoCoreModel(MaterialCoreModel):
    pass

class VideoPostModelYT(VideoCoreModel):
    url: str

class VideoPostModelCDN(VideoCoreModel):
    object_key: str

class VideoCreateModel(VideoCoreModel):
    url: str
    object_key: Optional[str]

class VideoInDB(VideoCoreModel):
    url: str
    object_key: Optional[str]

# game
class GameCoreModel(MaterialCoreModel):
    object_key: str

class GamePostModel(GameCoreModel):
    pass

class GameCreateModel(GameCoreModel):
    url: str

class GameInDB(GameCoreModel):
    url: str

# book
class BookCoreModel(MaterialCoreModel):
    object_key: str

class BookPostModel(BookCoreModel):
    pass

class BookCreateModel(BookCoreModel):
    url: str

class BookInDB(BookCoreModel):
    url: str

# presentation
class PresentationCoreModel(MaterialCoreModel):
    object_key: str

class PresentationPostModel(PresentationCoreModel):
    pass

class PresentationCreateModel(PresentationCoreModel):
    pass

class PresentationMediaCoreModel(DBCoreModel):
    order: int
    url: str
    object_key: str

class PresentationMediaCreate(PresentationMediaCoreModel):
    pass

class PresentationMediaInDB(PresentationMediaCoreModel):
    pass

class PresentationInDB(PresentationCoreModel):
    images: List[PresentationMediaInDB]
    audio: List[PresentationMediaInDB]

class AnswerCoreModel(DBCoreModel):
    answer: str
    is_true: Optional[bool]

class AnswersInDB(AnswerCoreModel):
    question_id: int
    answer_id: int

class QuizModelCore(DBCoreModel):
    order_number: int
    question: Optional[str]
    object_key: Optional[str]
    answers: List[AnswerCoreModel]

class QuizPostModel(QuizModelCore):
    pass

class QuizCreateModel(QuizModelCore):
    image_url: Optional[str]

class QuestionInDB(DBCoreModel):
    id: int
    order_number: int
    question: Optional[str]
    object_key: Optional[str]
    image_url: Optional[str]

class QuizQuestionInDB(QuestionInDB):
    answers: List[AnswersInDB]

class QuizInDB(DBCoreModel):
    questions: List[QuizQuestionInDB]

class QuizQuestionAnswerPair(DBCoreModel):
    question: int
    answer: int

class QuizGetResultsModel(DBCoreModel):
    results: List[QuizQuestionAnswerPair]

class QuizQuestionAnswerCorrectPair(DBCoreModel):
    question_id: int
    answer_id: int
    question_number: int
    answer: str
    correct: bool
    correct_answer: str
    correct_answer_id: int

class QuizResults(DBCoreModel):
    results: List[QuizQuestionAnswerCorrectPair]


# AboutUs, FAQ, instruction
class AboutUsCoreModel(DBCoreModel):
    order: int
    title: str
    description: str
    svg: str

class AboutUsCreateModel(AboutUsCoreModel):
    pass

class AboutUsPostModel(AboutUsCoreModel):
    pass

class AboutUsInDB(AboutUsCoreModel):
    pass



class FAQCoreModel(DBCoreModel):
    question: str
    answer: str

class FAQCreateModel(FAQCoreModel):
    pass

class FAQPostModel(FAQCoreModel):
    pass

class FAQInDB(FAQCoreModel):
    id: int



class InstructionCoreModel(DBCoreModel):
    order: int
    title: str
    description: str

class InstructionCreateModel(InstructionCoreModel):
    pass

class InstructionPostModel(InstructionCoreModel):
    pass

class InstructionInDB(InstructionCoreModel):
    pass

# material response
class MaterialResponseModel(DBCoreModel):
    video: Optional[VideoInDB]
    game: Optional[GameInDB]
    book: Optional[BookInDB]
    quiz: Optional[QuizInDB]
    practice: Optional[PresentationInDB]
    theory: Optional[PresentationInDB]

class MaterialResponse(DBCoreModel):
    material: MaterialResponseModel


class AboutUsAllResponse(DBCoreModel):
    about_us: List[AboutUsInDB]

class FaqAllResponse(DBCoreModel):
    faq: List[FAQInDB]

class InstructionAllResponse(DBCoreModel):
    instructions: List[InstructionInDB]


# update models
class UpdateCoreModel(DBCoreModel):
    name_ru: Optional[str]
    description: Optional[str]

class UpdateVideoModel(UpdateCoreModel):
    pass

class UpdateGameModel(UpdateCoreModel):
    pass

class UpdateBookModel(UpdateCoreModel):
    pass

class UpdatePresentationModel(UpdateCoreModel):
    pass

class PresentationMasterInDB(PresentationCoreModel):
    pass

class UpdateAboutUsModel(DBCoreModel):
    order: int
    title: Optional[str]
    description: Optional[str]
    svg: Optional[str]

class UpdateFAQModel(DBCoreModel):
    id: int
    question: Optional[str]
    answer: Optional[str]

class UpdateInstructionModel(DBCoreModel):
    order: int
    title: Optional[str]
    description: Optional[str]
    
# select all models
class MaterialAllModel(DBCoreModel):
    object_key: str

class AudioImagesAllModel(DBCoreModel):
    order: int
    object_key: str
