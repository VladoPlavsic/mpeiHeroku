from databases import Database

class BaseDBRepository:
    def __init__(self, db: Database) -> None:
        self.db = db
