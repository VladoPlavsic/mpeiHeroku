from typing import List, Dict, Optional

from app.models.core import BaseModel

class NewsCoreModel(BaseModel):
    date: str
    title: str
    short_desc: str
    content: str
    url: str
    cloud_key: str

class NewsImagesCore(BaseModel):
    order: int
    url: str
    cloud_key: str

class NewsImagesInDB(NewsImagesCore):
    pass

class NewsImagesCreate(NewsImagesCore):
    pass

class NewsPostModel(NewsCoreModel):
    folder: str

class NewsCreateModel(NewsCoreModel):
    preview_image_url: str
    images: List[NewsImagesCreate]

class NewsPreviewInDBModel(NewsCoreModel):
    id: int
    preview_image_url: str

class NewsInDBModel(NewsCoreModel):
    id: int
    preview_image_url: str
    images: List[NewsImagesInDB]

class NewsResponseModel(BaseModel):
    count: int 
    news: List[NewsPreviewInDBModel]

class NewsUpdateModel(BaseModel):
    id: int
    date: Optional[str]
    title: Optional[str]
    short_desc: Optional[str]
    content: Optional[str]
    url: Optional[str]
    cloud_key: Optional[str]
    preview_image_url: Optional[str]

class NewsImagesAllModel(BaseModel):
    cloud_key: str

class NewsAllModel(BaseModel):
    cloud_key: str