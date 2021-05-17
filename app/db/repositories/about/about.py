from app.db.repositories.about.insert.insert import AboutDBInsertRepository
from app.db.repositories.about.select.select import AboutDBSelectRepository
from app.db.repositories.about.update.update import AboutDBUpdateRepository
from app.db.repositories.about.delete.delete import AboutDBDeleteRepository

class AboutDBRepository(
    AboutDBInsertRepository,
    AboutDBSelectRepository,
    AboutDBUpdateRepository,
    AboutDBDeleteRepository,
    ):
    pass
