from app.db.repositories.news.insert.insert import NewsDBInsertRepository
from app.db.repositories.news.delete.delete import NewsDBDeleteRepository
from app.db.repositories.news.update.update import NewsDBUpdateRepository
from app.db.repositories.news.select.select import NewsDBSelectRepository

class NewsDBRepository(
    NewsDBInsertRepository,
    NewsDBSelectRepository,
    NewsDBUpdateRepository,
    NewsDBDeleteRepository,
    ):
    pass
