from app.db.repositories.users.select.select import UsersDBSelectRepository
from app.db.repositories.users.insert.insert import UsersDBInsertRepository
from app.db.repositories.users.subscriptions.subscriptions import UsersDBSubscriptionsRepository
from app.db.repositories.users.password.password import UsersDBPasswordRepository


class UsersDBRepository(
    UsersDBSelectRepository,
    UsersDBInsertRepository,
    UsersDBSubscriptionsRepository,
    UsersDBPasswordRepository,
    ):
    pass
