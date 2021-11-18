from fastapi import Depends
from app.db.repositories.users.users import UsersDBRepository
from app.api.dependencies.database import get_db_repository
from app.api.dependencies.email import send_message

import logging
logger = logging.getLogger(__name__)

def handle_deactivated_profiles(one_month_warning, one_week_warning, deletion_profiles):

    # logger.warn("-------------------")
    # logger.warn(one_month_warning)
    # logger.warn(one_week_warning)
    # logger.warn(deletion_profiles)
    # logger.warn("-------------------")

    for profile in one_month_warning:
        send_message(subject="Warning! Profile will be deleted!", message_text="This is one month warning. Your profile on our platform will be deleted in one month! If you want to prevent this check profile reactivation", to=profile.email)

    for profile in one_week_warning:
        send_message(subject="Warning! Profile will be deleted!", message_text="This is one week warning. Your profile on our platform will be deleted in one week! If you want to prevent this check profile reactivation", to=profile.email)
    
    for profile in deletion_profiles:
        send_message(subject="Profile deleted!", message_text="Your profile has been deleted. You can no longer access it!", to=profile.email)
