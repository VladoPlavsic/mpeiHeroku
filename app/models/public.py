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
    key: str

class VideoCreateModel(VideoCoreModel):
    url: str

class VideoInDB(VideoCoreModel):
    url: str

# game
class GameCoreModel(MaterialCoreModel):
    url: str

class GamePostModel(GameCoreModel):
    pass

class GameCreateModel(GameCoreModel):
    pass

class GameInDB(GameCoreModel):
    pass

# book
class BookCoreModel(MaterialCoreModel):
    key: str

class BookPostModel(BookCoreModel):
    pass

class BookCreateModel(BookCoreModel):
    url: str

class BookInDB(BookCoreModel):
    url: str

# presentation
class PresentationCoreModel(MaterialCoreModel):
    key: str

class PresentationPostModel(PresentationCoreModel):
    pass

class PresentationCreateModel(PresentationCoreModel):
    pass

class PresentationMediaCoreModel(DBCoreModel):
    order: int
    url: str
    key: str

class PresentationMediaCreate(PresentationMediaCoreModel):
    pass

class PresentationMediaInDB(PresentationMediaCoreModel):
    pass

class PresentationInDB(PresentationCoreModel):
    images: List[PresentationMediaInDB]
    audio: List[PresentationMediaInDB]


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
class UpdateVideoModel(DBCoreModel):
    name_ru: Optional[str]
    url: Optional[str]
    description: Optional[str]

class UpdateGameModel(DBCoreModel):
    name_ru: Optional[str]
    url: Optional[str]
    description: Optional[str]

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
    key: str

class AudioImagesAllModel(DBCoreModel):
    order: int
    key: str
