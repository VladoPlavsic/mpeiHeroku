from app.db.repositories.users.select.select import UsersDBSelectRepository
from app.db.repositories.users.insert.insert import UserDBInsertRepository
from app.db.repositories.users.subscriptions.subscriptions import UserDBSubscriptionsRepository

class UsersDBRepository(
    UsersDBSelectRepository,
    UserDBInsertRepository,
    UserDBSubscriptionsRepository,
    ):
    pass

