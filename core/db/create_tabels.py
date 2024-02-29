from core.db.tables import USER, PRODUCT, CATEGORY
from core.db.connection import Session

all_tables = [USER, PRODUCT, CATEGORY]
db_session = Session()


def create_tables(all_tables=all_tables):
    for table in all_tables:
         db_session.execute(table)
