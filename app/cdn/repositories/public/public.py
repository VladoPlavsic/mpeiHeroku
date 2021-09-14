from typing import List
from app.cdn.types import DefaultFormats
from app.cdn.repositories.base import BaseCDNRepository
from app.cdn.repositories.parsers import get_order_number_from_key, get_format_from_key

from app.models.public import PresentationMediaCreate

class PublicYandexCDNRepository(BaseCDNRepository):
    def format_presentation_content(self, *, folder, type_: DefaultFormats) -> List[PresentationMediaCreate]:
        """Public version of format_presentation_content. This function formats presentation content for it to be inserted into database.
        
        Keyword arguments:
        folder -- s3 key containing given lecture data. (e.g. subscriptions/7-9/physics/mechanics/kinematics/practice/)
        type_  -- data type. Used for figuring out containing folder for given type

        This function returns List of PresentationMediaCreate. 
        In case there are no images found for given path (if type_ = DefaultFolders.IMAGES)
        HTTPException will be raised, and nothing will be added to database.
        """
        shared = self._BaseCDNRepository__share_data(folder=folder, type_=type_)

        formated = []
        for item in shared:
            key = list(item.keys())[0]
            file_format = get_format_from_key(key=key)
         
            order_number = get_order_number_from_key(key=key)
            if order_number:
                formated.append(PresentationMediaCreate(order=order_number, url=item[key], object_key=key))

        if type_ == DefaultFormats.IMAGES and not formated:
            raise HTTPException(status_code=404, detail=f"No images found a path {folder}. Images must be present!")

        return formated