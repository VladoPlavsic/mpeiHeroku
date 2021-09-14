from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK

from app.db.repositories.private.private import PrivateDBRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.auth import get_user_from_token, is_superuser, is_verified

# ###
# response models
# ###
# structure
from app.models.private import GradeResponse
from app.models.private import SubjectResponse
from app.models.private import BranchResponse
from app.models.private import LectureResponse
# material
from app.models.private import MaterialResponse
# offers
from app.models.private import AvailableGradeSubscriptionOffers
from app.models.private import AvailableSubjectSubscriptionOffers
# plans
from app.models.private import AvailableGradeSubscriptionPlans
from app.models.private import AvailableSubjectSubscriptionPlans

from app.models.user import UserInDB

router = APIRouter()

# ###
# GRADES
# ###
@router.get("/grade/subscription/plans", response_model=List[AvailableGradeSubscriptionPlans], name="privete:get-grade-subscription-offers", status_code=HTTP_200_OK)
async def get_grade_subscription_plans(
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> List[AvailableGradeSubscriptionPlans]:

    return await db_repo.select_all_grade_subscription_plans()

@router.get("/grade/subscription/offers", response_model=List[AvailableGradeSubscriptionOffers], name="privete:get-grade-subscription-offers", status_code=HTTP_200_OK)
async def get_grade_subscription_offers(
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> List[AvailableGradeSubscriptionOffers]:

    return await db_repo.select_all_grade_subscription_offers()

@router.get("/grade/available", response_model=GradeResponse, name="private:get-grades-offer", status_code=HTTP_200_OK)
async def get_grade_offers(
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> GradeResponse:

    response = await db_repo.select_grades()
    return GradeResponse(grades=response)

@router.get("/grade", response_model=GradeResponse, name="private:get-grades", status_code=HTTP_200_OK)
async def get_private_grades(
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    user: UserInDB = Depends(get_user_from_token),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> GradeResponse:
    """We decide what content to provide based on JWT.
    
    If JWT contains user who has not confirmed their email  -- Raise 401
    If JWT contains superuser                               -- Grant access to all content
    If JWT contains any other use but superuser             -- Grant access based on user available grades
    """
    if is_superuser:
        response = await db_repo.select_grades()
    else:
        available_grades = await db_repo.select_user_available_grades(user_id=user.id)
        identifications  = [grade.grade_id for grade in available_grades]
        if identifications:
            response = await db_repo.select_grades(identifications=identifications)
        else:
            response = []

    return GradeResponse(grades=response)


# ###
# SUBJECTS
# ###
@router.get("/subject/subscription/plans", response_model=List[AvailableSubjectSubscriptionPlans], name="privete:get-subject-subscription-plans", status_code=HTTP_200_OK)
async def get_grade_subscription_plans(
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> List[AvailableSubjectSubscriptionPlans]:

    return await db_repo.select_all_subject_subscription_plans()

@router.get("/subject/subscription/offers", response_model=List[AvailableSubjectSubscriptionOffers], name="privete:get-subject-subscription-offers", status_code=HTTP_200_OK)
async def get_subject_subscription_offers(
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> List[AvailableSubjectSubscriptionOffers]:

    return await db_repo.select_all_subject_subscription_offers()

@router.get("/subject/available", response_model=SubjectResponse, name="private:get-subjects-offer", status_code=HTTP_200_OK)
async def get_subject_offer(
    grade_name_en: str,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> SubjectResponse:

    grade = await db_repo.get_grade_by_name(grade_name=grade_name_en)
    response = await db_repo.select_subjects(fk=grade.id)

    return SubjectResponse(subjects=response, fk=grade.id, path=grade.name_ru)

@router.get("/subject", response_model=SubjectResponse, name="private:get-subjects", status_code=HTTP_200_OK)
async def get_private_subjects(
    grade_name_en: str,
    user: UserInDB = Depends(get_user_from_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> SubjectResponse:
    """We decide what content to provide based on JWT.
    
    If JWT contains user who has not confirmed their email  -- Raise 401
    If JWT contains superuser                               -- Grant access to all content
    If JWT contains any other use but superuser             -- Grant access based on user available subjects
                                                            or grades if specific subject is not available
    """
    grade = await db_repo.get_grade_by_name(grade_name=grade_name_en)

    if is_superuser:
        response = await db_repo.select_subjects(fk=grade.id)
    else:
        available_grades = await db_repo.select_user_available_grades(user_id=user.id)
        identifications = [grade.grade_id for grade in available_grades]
        if grade.id in identifications:
            available_subjects = await db_repo.select_user_available_subjects(user_id=user.id)
            identifications = [subject.subject_id for subject in available_subjects]
            if identifications:
                response = await db_repo.select_subjects(fk=grade.id, identifications=identifications)
            else:
                response = []
        else:
            raise HTTPException(status_code=402, detail="Ooops! Looks like you don't have access to this content. Check our offers to gain access!")

    return SubjectResponse(subjects=response, fk=grade.id, path=grade.name_ru)


# ###
# BRANCHES
# ###
@router.get("/branch/available", response_model=BranchResponse, name="private:get-branches", status_code=HTTP_200_OK)
async def get_private_branches(
    grade_name_en: str,
    subject_name_en: str,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> BranchResponse:

    (subject, path) = await db_repo.get_subject_by_name(grade_name=grade_name_en, subject_name=subject_name_en)
    response = await db_repo.select_branches(fk=subject.id)

    return BranchResponse(branches=response, fk=subject.id, path=path + '/' + subject.name_ru)

@router.get("/branch", response_model=BranchResponse, name="private:get-branches", status_code=HTTP_200_OK)
async def get_private_branches(
    grade_name_en: str,
    subject_name_en: str,
    user = Depends(get_user_from_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> BranchResponse:

    """We decide what content to provide based on JWT.
    
    If JWT contains user who has not confirmed their email  -- Raise 401
    If JWT contains superuser                               -- Grant access to all content
    If JWT contains any other use but superuser             -- Grant access based on user available subjects
                                                            or grades if specific subject is not available
    """
    if is_superuser:
        (subject, path) = await db_repo.get_subject_by_name(grade_name=grade_name_en, subject_name=subject_name_en)
        response = await db_repo.select_branches(fk=subject.id)
    else:
        if await db_repo.check_if_content_available(user_id=user.id ,grade_name=grade_name_en, subject_name=subject_name_en):
            (subject, path) = await db_repo.get_subject_by_name(grade_name=grade_name_en, subject_name=subject_name_en)
            response = await db_repo.select_branches(fk=subject.id)
        else:
            raise HTTPException(status_code=402, detail="Ooops! Looks like you don't have access to this content. Check our offers to gain access!")

    return BranchResponse(branches=response, fk=subject.id, path=path + '/' + subject.name_ru)


# ###
# LECTURES
# ###
@router.get("/lecture/available", response_model=LectureResponse, name="private:get-lectures", status_code=HTTP_200_OK)
async def get_private_lectures(
    grade_name_en: str,
    subject_name_en: str,
    branch_name_en: str,
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    ) -> LectureResponse:

    (branch, path) = await db_repo.get_branch_by_name(grade_name=grade_name_en, subject_name=subject_name_en, branch_name=branch_name_en)
    response = await db_repo.select_lectures(fk=branch.id)
    return LectureResponse(lectures=response, fk=branch.id, path=path + '/' + branch.name_ru)


@router.get("/lecture", response_model=LectureResponse, name="private:get-lectures", status_code=HTTP_200_OK)
async def get_private_lectures(
    grade_name_en: str,
    subject_name_en: str,
    branch_name_en: str,
    user = Depends(get_user_from_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> LectureResponse:
    """We decide what content to provide based on JWT.
    
    If JWT contains user who has not confirmed their email  -- Raise 401
    If JWT contains superuser                               -- Grant access to all content
    If JWT contains any other use but superuser             -- Grant access based on user available subjects
                                                            or grades if specific subject is not available
    """
    if is_superuser:
        (branch, path) = await db_repo.get_branch_by_name(grade_name=grade_name_en, subject_name=subject_name_en, branch_name=branch_name_en)
        response = await db_repo.select_material(fk=branch.id)
    else:
        if await db_repo.check_if_content_available(user_id=user.id ,grade_name=grade_name_en, subject_name=subject_name):
            (branch, path) = await db_repo.get_branch_by_name(grade_name=grade_name_en, subject_name=subject_name_en, branch_name=branch_name_en)
            response = await db_repo.select_material(fk=branch.id)
        else:
            raise HTTPException(status_code=402, detail="Ooops! Looks like you don't have access to this content. Check our offers to gain access!")
   

    return LectureResponse(lectures=response, fk=branch.id, path=path + '/' + branch.name_ru)


@router.get("/material", response_model=MaterialResponse, name="private:get-material", status_code=HTTP_200_OK)
async def get_private_material(
    grade_name_en: str,
    subject_name_en: str,
    branch_name_en: str,
    lecture_name_en: str,
    user = Depends(get_user_from_token),
    db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    is_superuser = Depends(is_superuser),
    is_verified = Depends(is_verified),
    ) -> MaterialResponse:
    """We decide what content to provide based on JWT.
    
    If JWT contains user who has not confirmed their email  -- Raise 401
    If JWT contains superuser                               -- Grant access to all content
    If JWT contains any other use but superuser             -- Grant access based on user available subjects
                                                            or grades if specific subject is not available
    """
    if is_superuser:
        (lecture, path) = await db_repo.get_lecture_by_name(grade_name=grade_name_en, subject_name=subject_name_en, branch_name=branch_name_en, lecture_name=lecture_name_en)
        response = await db_repo.select_material(fk=lecture.id)
    else:
        if await db_repo.check_if_content_available(user_id=user.id ,grade_name=grade_name_en, subject_name=subject_name):
            (lecture, path) = await db_repo.get_lecture_by_name(grade_name=grade_name_en, subject_name=subject_name_en, branch_name=branch_name_en, lecture_name=lecture_name_en)
            response = await db_repo.select_material(fk=lecture.id)
        else:
            raise HTTPException(status_code=402, detail="Ooops! Looks like you don't have access to this content. Check our offers to gain access!")
  
    return MaterialResponse(material=response, path=path, fk=lecture.id)
