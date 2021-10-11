import time
import asyncio

from fastapi import Depends, BackgroundTasks

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository
from app.db.repositories.public.public import PublicDBRepository
from app.db.repositories.about.about import AboutDBRepository
from app.db.repositories.news.news import NewsDBRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

from app.cdn.types import ObjectTypes
from app.db.repositories.types import ContentType

import logging

logger = logging.getLogger(__name__)

async def update_sharing_links_function(
    background_tasks: BackgroundTasks,
    public_db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    private_db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    about_db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    news_db_repo: NewsDBRepository = Depends(get_db_repository(NewsDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    ) -> None:

    # private content update
    async def update():
        grades = await private_db_repo.select_all_grades()
        if grades:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=grades)
            await private_db_repo.update_grade_links(grades=updated)

        subjects = await private_db_repo.select_all_subjects()
        if subjects:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=subjects)
            await private_db_repo.update_subject_links(subjects=updated)

        branches = await private_db_repo.select_all_branches()
        if branches:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=branches)
            await private_db_repo.update_branch_links(branches=updated)

        lectures = await private_db_repo.select_all_lectures()
        if lectures:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=lectures)
            await private_db_repo.update_lecture_links(lectures=updated)

        private_books = await private_db_repo.select_all_books()
        if private_books:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=private_books)
            await private_db_repo.update_book_links(book=updated)

        private_video = await private_db_repo.select_all_video()
        if private_video:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=private_video)
            await private_db_repo.update_video_links(video=updated)

        private_game = await private_db_repo.select_all_game()
        if private_game:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=private_game)
            await private_db_repo.update_game_links(game=updated)

        private_quiz = await private_db_repo.select_all_quiz()
        if private_quiz:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=private_quiz)
            await private_db_repo.update_quiz_links(quiz=updated)

        private_theory_images = await private_db_repo.select_all_presentation_parts(presentation=ContentType.THEORY, media_type=ContentType.IMAGE)
        if private_theory_images:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=private_theory_images)
            await private_db_repo.update_presentation_part_links(prats=updated, presentation=ContentType.THEORY, media_type=ContentType.IMAGE)

        private_theory_audio = await private_db_repo.select_all_presentation_parts(presentation=ContentType.THEORY, media_type=ContentType.AUDIO)
        if private_theory_audio:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=private_theory_audio)
            await private_db_repo.update_presentation_part_links(prats=updated, presentation=ContentType.THEORY, media_type=ContentType.AUDIO)

        private_practice_images = await private_db_repo.select_all_presentation_parts(presentation=ContentType.PRACTICE, media_type=ContentType.IMAGE)
        if private_practice_images:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=private_practice_images)
            await private_db_repo.update_presentation_part_links(prats=updated, presentation=ContentType.PRACTICE, media_type=ContentType.IMAGE)

        private_practice_audio = await private_db_repo.select_all_presentation_parts(presentation=ContentType.PRACTICE, media_type=ContentType.AUDIO)
        if private_practice_audio:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=private_practice_audio)
            await private_db_repo.update_presentation_part_links(prats=updated, presentation=ContentType.PRACTICE, media_type=ContentType.AUDIO)

        # public content update
        public_books = await public_db_repo.select_all_books()
        if public_books:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_books)
            await public_db_repo.update_book_links(book=updated)

        """
        NEW
        """

        public_video = await public_db_repo.select_all_video()
        if public_video:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_video)
            await public_db_repo.update_video_links(video=updated)

        public_intro_video = await public_db_repo.select_all_intro_video()
        if public_intro_video:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_intro_video)
            await public_db_repo.update_intro_video_links(video=updated)

        public_game = await public_db_repo.select_all_game()
        if public_game:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_game)
            await public_db_repo.update_game_links(game=updated)

        public_quiz = await public_db_repo.select_all_quiz()
        if public_quiz:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_quiz)
            await public_db_repo.update_quiz_links(quiz=updated)
        
        """
        END NEW
        """

        public_theory_images = await public_db_repo.select_all_presentation_parts(presentation=ContentType.THEORY, media_type=ContentType.IMAGE)
        if public_theory_images:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_theory_images)
            await public_db_repo.update_presentation_part_links(prats=updated, presentation=ContentType.THEORY, media_type=ContentType.IMAGE)

        public_theory_audio = await public_db_repo.select_all_presentation_parts(presentation=ContentType.THEORY, media_type=ContentType.AUDIO)
        if public_theory_audio:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_theory_audio)
            await public_db_repo.update_presentation_part_links(prats=updated, presentation=ContentType.THEORY, media_type=ContentType.AUDIO)
    
        public_practice_images = await public_db_repo.select_all_presentation_parts(presentation=ContentType.PRACTICE, media_type=ContentType.IMAGE)
        if public_practice_images:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_practice_images)
            await public_db_repo.update_presentation_part_links(prats=updated, presentation=ContentType.PRACTICE, media_type=ContentType.IMAGE)

        public_practice_audio = await public_db_repo.select_all_presentation_parts(presentation=ContentType.PRACTICE, media_type=ContentType.AUDIO)
        if public_practice_audio:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_practice_audio)
            await public_db_repo.update_presentation_part_links(prats=updated, presentation=ContentType.PRACTICE, media_type=ContentType.AUDIO)

        # about content update
        team_members = await about_db_repo.select_all_team_members()
        if team_members:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=team_members)
            await about_db_repo.update_team_member_photos(photos=updated)

        # news content update
        news = await news_db_repo.select_all_news()
        if news:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=news)
            await news_db_repo.update_news_links(news=updated)

        news_images = await news_db_repo.select_all_news_images()
        if news_images:
            updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=news_images)
            await news_db_repo.update_images_links(images=updated)

    background_tasks.add_task(update)
    #await update()