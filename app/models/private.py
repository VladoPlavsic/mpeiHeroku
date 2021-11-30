from typing import List, Optional
from datetime import datetime
from app.models.core import DBCoreModel

# ###
# Presentation models
# ### 

class PresentationModelCore(DBCoreModel):
    name_ru: str
    description: str

class PresentationCreateModelCheck(DBCoreModel):
    fk: int

class PresentationCreateModel(PresentationModelCore):
    fk: int
    object_key: str

class PresentationMediaCore(DBCoreModel):
    order: int
    url: str
    object_key: str

class PresentationMediaInDB(PresentationMediaCore):
    pass

class PresentationMediaCreate(PresentationMediaCore):
    fk: int

class PresentationMasterInDB(PresentationModelCore):
    id: int

class PresentationInDB(PresentationMasterInDB):
    images: List[PresentationMediaInDB]
    audio: List[PresentationMediaInDB]

# ###
# Book models
# ###

class BookModelCore(DBCoreModel):
    name_ru: str
    description: str

class BookPostModelCheck(DBCoreModel):
    fk: int

class BookPostModel(BookModelCore):
    fk: int
    object_key: str

class BookCreateModel(BookPostModel):
    url: str

class BookInDB(BookModelCore):
    id: int
    url: str
    object_key: str

# ###
# Video models
# ###

class VideoModelCore(DBCoreModel):
    name_ru: str
    description: str

class VideoPostModelYT(VideoModelCore):
    fk: int
    url: str

class VideoPostModelCDNCheck(DBCoreModel):
    fk: int

class VideoPostModelCDN(VideoModelCore):
    fk: int
    object_key: str

class VideoCreateModel(VideoModelCore):
    fk: int
    url: str
    object_key: Optional[str]

class VideoInDB(VideoModelCore):
    id: int
    url: str
    object_key: Optional[str]

# ###
# Game models
# ###

class GameModelCore(DBCoreModel):
    name_ru: str
    description: str
    object_key: str

class GamePostModelCheck(DBCoreModel):
    fk: int

class GamePostModel(GameModelCore):
    fk: int

class GameCreateModel(GameModelCore):
    fk: int
    url: str

class GameInDB(GameModelCore):
    id: int
    url: str

# ###
# Quiz models
# ###
class AnswerCoreModel(DBCoreModel):
    answer: str
    is_true: Optional[bool]    

class AnswersInDB(AnswerCoreModel):
    question_id: int
    answer_id: int

class QuizModelCore(DBCoreModel):
    lecture_id: int
    order_number: int
    question: Optional[str]
    object_key: Optional[str]
    answers: List[AnswerCoreModel]
    
class QuizPostModelCheck(DBCoreModel):
    fk: int
    order_number: int

class QuizPostModel(QuizModelCore):
    pass

class QuizCreateModel(QuizModelCore):
    image_url: Optional[str]

class QuestionInDB(DBCoreModel):
    id: int
    fk: int
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
    lecture_id: int

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
    lecture_id: int

# ###
# Structure models
# ###

# grades
class GradeCoreModel(DBCoreModel):
    name_en: str
    name_ru: str
    object_key: str
    order_number: int

class GradePostModelCheck(DBCoreModel):
    name_en: str

class GradePostModel(GradeCoreModel):
    pass

class GradeCreateModel(GradeCoreModel):
    background: str

class GradeInDB(GradeCoreModel):
    id: int
    background: str

# grade response
class GradeResponse(DBCoreModel):
    grades: List[GradeInDB]

# subjects
class SubjectGetModel(DBCoreModel):
    grade_name_en: str

class SubjectCoreModel(DBCoreModel):
    fk: int
    name_en: str
    name_ru: str
    object_key: str
    order_number: int

class SubejctPostModelCheck(DBCoreModel):
    fk: int
    name_en: str

class SubejctPostModel(SubjectCoreModel):
    pass

class SubjectCreateModel(SubjectCoreModel):
    background: str

class SubjectInDB(SubjectCoreModel):
    id: int
    background: str

# subject response
class SubjectResponse(DBCoreModel):
    fk: int
    path: str
    subjects: List[SubjectInDB]

# branches
class BranchGetModel(DBCoreModel):
    grade_name_en: str
    subject_name_en: str

class BranchCoreModel(DBCoreModel):
    fk: int
    name_en: str
    name_ru: str
    object_key: str
    order_number: int

class BranchPostModelCheck(DBCoreModel):
    fk: int
    name_en: str

class BranchPostModel(BranchCoreModel):
    pass

class BranchCreateModel(BranchCoreModel):
    background: str

class BranchInDB(BranchCoreModel):
    id: int
    background: str

# branch response
class BranchResponse(DBCoreModel):
    fk: int
    path: str
    branches: List[BranchInDB]

# lectures
class LectureGetModel(DBCoreModel):
    grade_name_en: str
    subject_name_en: str
    branch_name_en: str

class LectureCoreModel(DBCoreModel):
    fk: int
    name_en: str
    name_ru: str
    description: str
    object_key: str
    order_number: int

class LecturePostModelCheck(DBCoreModel):
    fk: int
    name_en: str

class LecturePostModel(LectureCoreModel):
    pass

class LectureCreateModel(LectureCoreModel):
    background: str

class LectureInDB(LectureCoreModel):
    id: int
    background: str

# lecture response
class LectureResponse(DBCoreModel):
    fk: int
    path: str
    lectures: List[LectureInDB]

# material response
class MaterialResponseModel(DBCoreModel):
    video: Optional[VideoInDB]
    game: Optional[GameInDB]
    book: Optional[BookInDB]
    quiz: Optional[QuizInDB]
    practice: Optional[PresentationInDB]
    theory: Optional[PresentationInDB]

class MaterialBulk(DBCoreModel):
    # video
    video_url: str
    video_name_ru: str
    video_description: str
    video_key: Optional[str]
    # game
    game_url: str
    game_name_ru: str
    game_description: str
    # theory
    theory_name_ru: str
    theory_description: str
    theory_key: str
    # practice
    practice_name_ru: str
    practice_description: str
    practice_key: str
    # book
    book_url: str
    book_name_ru: str
    book_key: str
    book_description: str

class MaterialResponse(DBCoreModel):
    fk: int
    path: str
    material: MaterialResponseModel

# ###
# select all
# ###
class StructureAllModel(DBCoreModel):
    id: int
    object_key: str

class MaterialAllModel(DBCoreModel):
    id: int
    object_key: str

class AudioImagesAllModel(DBCoreModel):
    order: int
    object_key: str


# Update models
class UpdateBaseModel(DBCoreModel):
    id: int
    name_ru: Optional[str]

class UpdateVideoModel(UpdateBaseModel):
    description: Optional[str]
    url: Optional[str]

class UpdateGameModel(UpdateBaseModel):
    description: Optional[str]
    url: Optional[str]

class UpdateLectureModel(UpdateBaseModel):
    description: Optional[str]
    object_key: Optional[str]
    order_number: Optional[int]

class UpdateStructureModel(UpdateBaseModel):
    object_key: Optional[str]
    order_number: Optional[int]

class UpdateBookModel(UpdateBaseModel):
    description: Optional[str]

class UpdatePresentationModel(UpdateBaseModel):
    description: Optional[str]


# ###
# Subscriptions
# ###
class SubscriptionsBase(DBCoreModel):
    name: str
    price: float
    month_count: int

class OfferDetails(DBCoreModel):
    id: int
    product_fk: int
    subscription_fk: int

class CreateGradeSubscriptionPlan(SubscriptionsBase):
    pass

class CreateSubjectSubscriptionPlan(SubscriptionsBase):
    pass

class AvailableGradeSubscriptionPlans(SubscriptionsBase):
    id: int

class AvailableSubjectSubscriptionPlans(SubscriptionsBase):
    id: int

class AvailableGradeSubscriptionOffers(SubscriptionsBase):
    id: int
    plan_id: int
    grade_id: int
    name_en: str
    name_ru: str

class AvailableSubjectSubscriptionOffers(SubscriptionsBase):
    id: int
    plan_id: int
    subject_id: int
    grade_id: int
    name_en: str
    name_ru: str


class PaymentRequestDetails(DBCoreModel):
    user_fk: int
    offer_fk: int
    payment_id: str
    level: bool
    confirmation_token: str
