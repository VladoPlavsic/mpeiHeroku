from app.db.repositories.private.insert.insert import PrivateDBInsertRepository
from app.db.repositories.private.select.select import PrivateDBSelectRepository
from app.db.repositories.private.delete.delete import PrivateDBDeleteRepository
from app.db.repositories.private.update.update import PrivateDBUpdateRepository

class PrivateDBRepository(
    PrivateDBInsertRepository, 
    PrivateDBSelectRepository, 
    PrivateDBDeleteRepository,
    PrivateDBUpdateRepository):
    pass