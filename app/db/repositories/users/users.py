from app.db.repositories.users.select.select import UsersDBSelectRepository
from app.db.repositories.users.insert.insert import UserDBInsertRepository

class UsersDBRepository(
    UsersDBSelectRepository,
    UserDBInsertRepository,):
    pass

