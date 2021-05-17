from app.db.repositories.public.insert.insert import PublicDBInsertRepository
from app.db.repositories.public.select.select import PublicDBSelectRepository
from app.db.repositories.public.delete.delete import PublicDBDeleteRepository
from app.db.repositories.public.update.update import PublicDBUpdateRepository

class PublicDBRepository(
    PublicDBInsertRepository,
    PublicDBSelectRepository,
    PublicDBDeleteRepository,
    PublicDBUpdateRepository):
    pass